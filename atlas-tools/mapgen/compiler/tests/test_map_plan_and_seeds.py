from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


COMPILER_DIR = Path(__file__).resolve().parents[1]
WORKSPACE = COMPILER_DIR.parents[3]
ATLAS_ROOT = WORKSPACE / "TheLastSwordProtocol-Atlas"
sys.path.insert(0, str(COMPILER_DIR))

from generation_manifest import GenerationManifest, ManifestValidationError  # noqa: E402
from legacy_adapters import apply_adventure_flow, blueprint_to_map_plan, landmass_to_map_plan  # noqa: E402
from map_plan import MapPlan, MapPlanValidationError  # noqa: E402
from seed_streams import SeedStreams, derive_root_seed  # noqa: E402


BLUEPRINT = ATLAS_ROOT / "atlas-tools/mapgen/prototype/SCR-HOM-ASH-003.blueprint.json"
LANDMASS = ATLAS_ROOT / "atlas-tools/mapgen/compiler/out/home_island_landmass_plan.json"
ADVENTURE = ATLAS_ROOT / "atlas-tools/mapgen/compiler/out/home_island_adventure_flow.json"


def build_manifest(**overrides) -> GenerationManifest:
    args = {
        "manifest_id": "GEN-WO0057-TEST-001",
        "map_intent_id": "MI-SHOP-EXAMPLE-001",
        "generator_id": "atlas-reusable-map-compiler",
        "generator_version": "0.1.0",
        "archetype_id": "ARCH-INTERIOR-SHOP",
        "archetype_version": "1.0",
        "layout_family_id": "LAY-INTERIOR-SHOP-BILATERAL",
        "layout_family_version": "1.0",
        "variant_id": "single_aisle",
        "style_pack_id": "STY-ASHFORD-COZY-INTERIOR",
        "style_pack_version": "1.0",
        "salt": "wo-0057-test",
        "generated_at": "2026-07-13",
    }
    args.update(overrides)
    return GenerationManifest.create(**args)


class SeedTests(unittest.TestCase):
    def test_contract_example_seed_is_exact(self) -> None:
        inputs = [
            "MI-SHOP-EXAMPLE-001",
            "ARCH-INTERIOR-SHOP@1.0",
            "LAY-INTERIOR-SHOP-BILATERAL@1.0",
            "single_aisle",
            "STY-ASHFORD-COZY-INTERIOR@1.0",
            "example-salt-shop-001",
        ]
        self.assertEqual(17801666076276065200, derive_root_seed(inputs))

    def test_repeated_manifest_is_byte_identical(self) -> None:
        self.assertEqual(build_manifest().to_json(), build_manifest().to_json())

    def test_named_streams_are_isolated(self) -> None:
        streams = build_manifest().streams
        before = {
            "terrain": streams.seed("terrain"),
            "roads": streams.seed("structures", "roads"),
            "rooms": streams.seed("structures", "rooms"),
            "transfers": streams.seed("structures", "transfers"),
            "event_anchors": streams.seed("structures", "event_anchors"),
        }
        decoration_a = streams.seed("decoration", "variant-a")
        decoration_b = streams.seed("decoration", "variant-b")
        after = {
            "terrain": streams.seed("terrain"),
            "roads": streams.seed("structures", "roads"),
            "rooms": streams.seed("structures", "rooms"),
            "transfers": streams.seed("structures", "transfers"),
            "event_anchors": streams.seed("structures", "event_anchors"),
        }
        self.assertNotEqual(decoration_a, decoration_b)
        self.assertEqual(before, after)

    def test_structure_scopes_are_independent(self) -> None:
        streams = SeedStreams(build_manifest().root_seed)
        self.assertNotEqual(streams.structure("inn-1"), streams.structure("shop-1"))


class ManifestTests(unittest.TestCase):
    def test_versions_are_pinned(self) -> None:
        payload = build_manifest(adapter_id="rpgmaker-mz", adapter_version="0.1.0").to_dict()
        self.assertEqual("0.1.0", payload["generator_ref"]["version"])
        self.assertEqual("0.1.0", payload["adapter_ref"]["version"])
        self.assertEqual("1.0", payload["archetype_ref"]["version"])
        self.assertEqual("1.0", payload["layout_family_ref"]["version"])
        self.assertEqual("1.0", payload["style_pack_ref"]["version"])

    def test_seed_tampering_fails(self) -> None:
        payload = build_manifest().to_dict()
        payload["seed"]["value"] += 1
        with self.assertRaises(ManifestValidationError):
            GenerationManifest.from_dict(payload)

    def test_unknown_versions_fail(self) -> None:
        payload = build_manifest().to_dict()
        payload["contract_version"] = "99"
        with self.assertRaises(ManifestValidationError):
            GenerationManifest.from_dict(payload)

    def test_partial_adapter_ref_fails(self) -> None:
        with self.assertRaises(ManifestValidationError):
            build_manifest(adapter_id="rpgmaker-mz")


class MapPlanTests(unittest.TestCase):
    def test_existing_blueprint_round_trips_canonically(self) -> None:
        payload = json.loads(BLUEPRINT.read_text(encoding="utf-8"))
        plan_a = blueprint_to_map_plan(payload, "GEN-WO0057-TEST-001")
        plan_b = MapPlan.from_dict(json.loads(plan_a.to_json()))
        self.assertEqual(plan_a.to_json(), plan_b.to_json())
        self.assertEqual("GEN-WO0057-TEST-001", plan_b.generation_manifest_ref)

    def test_landmass_and_adventure_flow_adapters(self) -> None:
        landmass = json.loads(LANDMASS.read_text(encoding="utf-8"))
        adventure = json.loads(ADVENTURE.read_text(encoding="utf-8"))
        plan = landmass_to_map_plan(landmass, "GEN-WO0057-HOM-001")
        enriched = apply_adventure_flow(plan, adventure)
        self.assertEqual(96, enriched.to_dict()["dimensions"]["width"])
        self.assertEqual(len(adventure["travel_corridors"]), len(enriched.to_dict()["traversable_areas"]))
        self.assertEqual(landmass["anchor_zones"].keys(), {
            icon["landmark_id"] for icon in enriched.to_dict()["landmark_icons"]
        })

    def test_unknown_map_plan_version_fails(self) -> None:
        payload = json.loads(BLUEPRINT.read_text(encoding="utf-8"))
        payload["schema_version"] = "99"
        with self.assertRaises(MapPlanValidationError):
            MapPlan.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
