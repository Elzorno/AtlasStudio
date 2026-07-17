"""WO-0071: MapVision + TileAssembly compiler integration tests.

Runs the real, human-approved MV-HOM-ASH-001 MapVision, AVCP-HOM-ASH-001
constraint profile, and the real Ashford TileAssembly catalog (reference kit
+ authored kit + custom tileset extension) through SemanticAssembler against
the disposable Ashford compiler-example fixtures. Nothing here writes to
TheLastSwordProtocol-Game -- every MapPlan produced carries the
ARCH-EXTERIOR-SETTLEMENT-COMPACT example's fixture map_intent_id, never a
production atlas_screen_id, and outputs stay in-memory or under
prototypes/wo0071/.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

COMPILER_DIR = Path(__file__).resolve().parents[1]
EXAMPLES = COMPILER_DIR / "contract" / "examples" / "ashford"
SHARED = COMPILER_DIR / "contract" / "examples" / "shared"
WORKSPACE = COMPILER_DIR.parents[3]
ATLAS_MAP_GENERATION_DIR = (
    WORKSPACE / "TheLastSwordProtocol-Atlas" / "atlas" / "docs" / "09_Technical" / "Map_Generation"
)
KIT_DIR = COMPILER_DIR.parent / "tile_assembly" / "kits" / "ashford"
sys.path.insert(0, str(COMPILER_DIR))

from assembler import AssemblyBudget, AssemblyError, SemanticAssembler  # noqa: E402
from map_vision_resolution import MapVisionResolutionError  # noqa: E402
from seed_streams import SeedStreams, derive_root_seed  # noqa: E402
from tile_assembly_catalog import (  # noqa: E402
    load_custom_extension_manifest,
    load_tile_assembly_kit_index,
    merge_catalogs,
)


def load_example(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def load_modules() -> dict[str, dict]:
    result = {}
    for path in sorted(SHARED.glob("module_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        result[payload["module_id"]] = payload
    return result


def load_catalog() -> dict:
    return merge_catalogs(
        load_tile_assembly_kit_index(KIT_DIR / "index.json"),
        load_tile_assembly_kit_index(KIT_DIR / "authored" / "index.json"),
        load_custom_extension_manifest(KIT_DIR / "custom_extension" / "manifest.json"),
    )


def load_map_vision() -> dict:
    return json.loads(
        (ATLAS_MAP_GENERATION_DIR / "Instances" / "MV-HOM-ASH-001.json").read_text(encoding="utf-8")
    )


def load_constraint_profile() -> dict:
    return json.loads(
        (ATLAS_MAP_GENERATION_DIR / "Academy" / "ASHFORD-VISUAL-CONSTRAINT-PROFILE-001.json").read_text(
            encoding="utf-8"
        )
    )


MAP_INTENT = load_example("map_intent.json")
GAMEPLAY_GRAPH = load_example("gameplay_graph.json")
ARCHETYPE = load_example("building_archetype.json")
LAYOUT_FAMILY = load_example("layout_family.json")
MODULES = load_modules()
CATALOG = load_catalog()
MAP_VISION = load_map_vision()
CONSTRAINT_PROFILE = load_constraint_profile()


def assemble(seed: int, *, required_beats=("exit_transfer",), map_vision=None, constraint_profile=None, catalog=None):
    return SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
        map_intent=MAP_INTENT,
        gameplay_graph=GAMEPLAY_GRAPH,
        archetype=ARCHETYPE,
        layout_family=LAYOUT_FAMILY,
        modules=MODULES,
        streams=SeedStreams(seed),
        manifest_id=f"GEN-WO0071-TEST-{seed}",
        required_beats=required_beats,
        assembly_catalog=CATALOG if catalog is None else catalog,
        map_vision=MAP_VISION if map_vision is None else map_vision,
        visual_constraint_profile=CONSTRAINT_PROFILE if constraint_profile is None else constraint_profile,
    )


class DeterminismTests(unittest.TestCase):
    def test_same_seed_reproduces_byte_identical_map_plan(self) -> None:
        seed = derive_root_seed(("determinism-check", "WO-0071"))
        first = assemble(seed).map_plan.to_json()
        second = assemble(seed).map_plan.to_json()
        self.assertEqual(first, second)

    def test_same_seed_reproduces_identical_bindings(self) -> None:
        seed = derive_root_seed(("bindings-determinism", "WO-0071"))
        first = assemble(seed).tile_assembly_bindings
        second = assemble(seed).tile_assembly_bindings
        self.assertEqual(first, second)
        self.assertTrue(first, "expected at least one resolved binding")


class CompositionVarietyTests(unittest.TestCase):
    def test_required_beats_change_zone_and_module_composition_not_only_color(self) -> None:
        seed = derive_root_seed(("composition-check", "WO-0071"))
        core = assemble(seed, required_beats=("exit_transfer",)).map_plan.to_dict()
        dressed = assemble(
            seed, required_beats=("exit_transfer", "cultivation_dressing", "forest_dressing")
        ).map_plan.to_dict()

        core_roles = {zone["terrain_type"] for zone in core["terrain"]}
        dressed_roles = {zone["terrain_type"] for zone in dressed["terrain"]}
        self.assertNotEqual(core_roles, dressed_roles)
        self.assertTrue({"cultivation_edge", "forest_edge"}.issubset(dressed_roles))
        self.assertFalse({"cultivation_edge", "forest_edge"} & core_roles)

        core_obstacle_tags = {o["name"] for o in core["obstacles"]}
        dressed_obstacle_tags = {o["name"] for o in dressed["obstacles"]}
        self.assertNotEqual(core_obstacle_tags, dressed_obstacle_tags)
        self.assertIn("patched_metal_fence", dressed_obstacle_tags)
        self.assertIn("broadleaf_tree", dressed_obstacle_tags)
        self.assertNotIn("patched_metal_fence", core_obstacle_tags)

        # The four canonical buildings and their bound assemblies are stable
        # across both compositions -- only the optional dressing differs.
        core_bindings = {b["semantic_tag"]: b["tile_assembly_id"] for b in assemble(seed).tile_assembly_bindings}
        dressed_bindings = {
            b["semantic_tag"]: b["tile_assembly_id"]
            for b in assemble(seed, required_beats=("exit_transfer", "cultivation_dressing", "forest_dressing")).tile_assembly_bindings
        }
        for tag in ("elara_house", "ashford_shop", "ashford_inn", "ashford_elder_house", "central_well"):
            self.assertEqual(core_bindings[tag], dressed_bindings[tag])
        self.assertIn("patched_metal_fence", dressed_bindings)
        self.assertNotIn("patched_metal_fence", core_bindings)


class FailClosedTests(unittest.TestCase):
    def test_unapproved_map_vision_fails_closed(self) -> None:
        broken = copy.deepcopy(MAP_VISION)
        broken["status"] = "pending_human_approval"
        seed = derive_root_seed(("unapproved-vision", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            assemble(seed, map_vision=broken)
        self.assertEqual("unresolved_canon", caught.exception.code)

    def test_unresolved_conflicts_fail_closed(self) -> None:
        broken = copy.deepcopy(MAP_VISION)
        broken["approval"]["unresolved_conflicts"] = ["some open canon question"]
        seed = derive_root_seed(("unresolved-conflicts", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            assemble(seed, map_vision=broken)
        self.assertEqual("unresolved_canon", caught.exception.code)

    def test_constraint_profile_targeting_wrong_map_vision_version_fails_closed(self) -> None:
        broken = copy.deepcopy(CONSTRAINT_PROFILE)
        broken["target_map_vision"] = "MV-HOM-ASH-001@99.0"
        seed = derive_root_seed(("wrong-target-version", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            assemble(seed, constraint_profile=broken)
        self.assertEqual("incomplete_visual_constraints", caught.exception.code)

    def test_unapproved_constraint_profile_fails_closed(self) -> None:
        broken = copy.deepcopy(CONSTRAINT_PROFILE)
        broken["status"] = "draft"
        seed = derive_root_seed(("unapproved-profile", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            assemble(seed, constraint_profile=broken)
        self.assertEqual("incomplete_visual_constraints", caught.exception.code)

    def test_missing_assembly_fails_closed_for_village_cottage(self) -> None:
        # Both reference-kit cottage records remain study_only/blocked today
        # (see REFERENCE-FIDELITY-REVIEW.md) -- forcing a required cottage
        # module must fail closed rather than silently place a blocked tile.
        archetype = copy.deepcopy(ARCHETYPE)
        graph = copy.deepcopy(GAMEPLAY_GRAPH)
        graph["zones"].append(
            {
                "zone_id": "cottage_row",
                "role": "cottage_row",
                "required": True,
                "min_area": 20,
                "clearance": {"min_adjacent_walkable": 1},
                "ports": [],
                "beats": [],
            }
        )
        graph["edges"].append(
            {"from_zone": "elder_frontage", "to_zone": "cottage_row", "connector_type": "road_connection", "required": True}
        )
        graph["reachability"]["must_reach"].append("cottage_row")
        archetype["modules_required"].append(
            {"zone_role": "cottage_row", "module_ref": "MOD-VILLAGE-COTTAGE", "min_count": 1, "max_count": 1}
        )
        module_defs = dict(MODULES)
        module_defs["MOD-VILLAGE-COTTAGE"] = {
            "schema_version": "0.1",
            "module_id": "MOD-VILLAGE-COTTAGE",
            "version": "1.0",
            "semantic_tag": "village_cottage",
            "footprint": {"width": 3, "height": 5},
            "ports": [],
            "blocks_movement": True,
        }
        seed = derive_root_seed(("missing-cottage", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
                map_intent=MAP_INTENT,
                gameplay_graph=graph,
                archetype=archetype,
                layout_family=LAYOUT_FAMILY,
                modules=module_defs,
                streams=SeedStreams(seed),
                manifest_id="GEN-WO0071-TEST-MISSING-COTTAGE",
                required_beats=("exit_transfer",),
                assembly_catalog=CATALOG,
                map_vision=MAP_VISION,
                visual_constraint_profile=CONSTRAINT_PROFILE,
            )
        self.assertEqual("missing_assembly", caught.exception.code)
        self.assertEqual("village_cottage", caught.exception.context["semantic_tag"])

    def test_incompatible_dimensions_fail_closed(self) -> None:
        # Inflate the bound Inn assembly's declared size past its placed
        # module footprint (9x6) so it can no longer fit -- this is the
        # dimension-mismatch case WO-0071 requires failing closed on.
        oversized_catalog = copy.deepcopy(CATALOG)
        record = oversized_catalog["TASM-ASHFORD-INN-AUTHORED"]
        oversized_catalog["TASM-ASHFORD-INN-AUTHORED"] = record.__class__(
            assembly_id=record.assembly_id,
            width=50,
            height=50,
            enabled=record.enabled,
            review_state=record.review_state,
            adapter_ref=record.adapter_ref,
            source_kit=record.source_kit,
        )
        seed = derive_root_seed(("oversized-inn", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            assemble(seed, catalog=oversized_catalog)
        self.assertEqual("incompatible_dimensions", caught.exception.code)
        self.assertEqual("ashford_inn", caught.exception.context["semantic_tag"])

    def test_unsupported_adapter_capability_fails_closed(self) -> None:
        seed = derive_root_seed(("unsupported-adapter", "WO-0071"))
        with self.assertRaises(MapVisionResolutionError) as caught:
            SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
                map_intent=MAP_INTENT,
                gameplay_graph=GAMEPLAY_GRAPH,
                archetype=ARCHETYPE,
                layout_family=LAYOUT_FAMILY,
                modules=MODULES,
                streams=SeedStreams(seed),
                manifest_id="GEN-WO0071-TEST-ADAPTER",
                required_beats=("exit_transfer",),
                assembly_catalog=CATALOG,
                map_vision=MAP_VISION,
                visual_constraint_profile=CONSTRAINT_PROFILE,
                adapter_ref="godot@0.1",
            )
        self.assertEqual("unsupported_adapter_capability", caught.exception.code)


class NoProductionWriteTests(unittest.TestCase):
    def test_map_plan_never_targets_a_production_atlas_screen(self) -> None:
        seed = derive_root_seed(("no-production-write", "WO-0071"))
        plan = assemble(seed).map_plan.to_dict()
        self.assertIsNone(plan["atlas_screen_id"])
        self.assertEqual("MI-ASHFORD-EXAMPLE-001", MAP_INTENT["map_intent_id"])
        self.assertNotEqual("MI-HOM-ASH-001", MAP_INTENT["map_intent_id"])


if __name__ == "__main__":
    unittest.main()
