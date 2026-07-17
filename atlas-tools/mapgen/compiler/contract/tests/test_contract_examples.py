"""Validate every fixture in contract/examples/ against its schema, and confirm
MapPlan is genuinely blueprint-compatible by validating the existing, already
production-used blueprint corpus in TheLastSwordProtocol-Atlas against it."""

from __future__ import annotations

import glob
import json
import sys
import unittest
from pathlib import Path

CONTRACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CONTRACT_ROOT))

from validate_contract import EXAMPLE_MANIFEST, validate  # noqa: E402
from map_vision_validation import validate_map_vision_semantics  # noqa: E402
from tile_assembly_validation import validate_tile_assembly_semantics  # noqa: E402

BLUEPRINT_GLOB = str(
    CONTRACT_ROOT.parents[4]
    / "TheLastSwordProtocol-Atlas"
    / "atlas-tools"
    / "mapgen"
    / "prototype"
    / "*.blueprint.json"
)


class TestContractExamples(unittest.TestCase):
    def test_every_example_validates_against_its_schema(self) -> None:
        for instance_rel, schema_rel in EXAMPLE_MANIFEST.items():
            with self.subTest(instance=instance_rel):
                instance = json.loads((CONTRACT_ROOT / instance_rel).read_text(encoding="utf-8"))
                schema = json.loads((CONTRACT_ROOT / schema_rel).read_text(encoding="utf-8"))
                errors = validate(instance, schema)
                self.assertEqual(errors, [], f"{instance_rel} failed: {errors}")

    def test_archetype_and_layout_family_examples_carry_no_raw_tile_ids(self) -> None:
        forbidden_keys = {"tileId", "tile_id", "tilesetId"}
        no_tile_id_schemas = (
            "schemas/building_archetype.schema.json",
            "schemas/layout_family.schema.json",
            "schemas/style_pack.schema.json",
        )
        rels = [rel for rel, schema_rel in EXAMPLE_MANIFEST.items() if schema_rel in no_tile_id_schemas]
        self.assertGreaterEqual(
            len(rels), 12,
            "expected at least the WO-0059 kit's 3 archetypes + 7 layout families + 2 WO-0060 style packs",
        )
        for rel in rels:
            with self.subTest(instance=rel):
                text = (CONTRACT_ROOT / rel).read_text(encoding="utf-8")
                for key in forbidden_keys:
                    self.assertNotIn(key, text, f"{rel} unexpectedly references '{key}'")

    def test_style_pack_biome_substitution_references_are_consistent(self) -> None:
        style_packs: dict[str, dict] = {}
        for rel, schema_rel in EXAMPLE_MANIFEST.items():
            if schema_rel == "schemas/style_pack.schema.json":
                instance = json.loads((CONTRACT_ROOT / rel).read_text(encoding="utf-8"))
                style_packs[instance["style_pack_id"]] = instance
        self.assertGreaterEqual(len(style_packs), 2, "expected at least the temperate and coastal WO-0060 style packs")

        def all_tags(pack: dict) -> set[str]:
            tags = set(pack.get("visual_tags", []))
            for group in pack.get("vocabulary", {}).values():
                tags.update(group)
            return tags

        for pack_id, pack in style_packs.items():
            for entry in pack.get("biome_substitution", []):
                with self.subTest(pack=pack_id, entry=entry["to_tag"]):
                    self.assertIn(entry["from_style_pack"], style_packs, f"{pack_id}: unknown from_style_pack '{entry['from_style_pack']}'")
                    source_pack = style_packs[entry["from_style_pack"]]
                    self.assertIn(entry["from_tag"], all_tags(source_pack), f"{pack_id}: from_tag '{entry['from_tag']}' not found in {entry['from_style_pack']}'s vocabulary")
                    self.assertIn(entry["to_tag"], all_tags(pack), f"{pack_id}: to_tag '{entry['to_tag']}' not found in its own vocabulary")

    def test_layout_families_and_archetypes_reference_ids_that_exist(self) -> None:
        graph_ids: set[str] = set()
        archetype_ids: set[str] = set()
        layout_family_targets: list[tuple[str, str]] = []
        archetype_graph_refs: list[tuple[str, str]] = []

        for rel, schema_rel in EXAMPLE_MANIFEST.items():
            instance = json.loads((CONTRACT_ROOT / rel).read_text(encoding="utf-8"))
            if schema_rel == "schemas/gameplay_graph.schema.json":
                graph_ids.add(instance["graph_id"])
            elif schema_rel == "schemas/building_archetype.schema.json":
                archetype_ids.add(instance["archetype_id"])
                archetype_graph_refs.append((rel, instance["gameplay_graph_ref"]))
            elif schema_rel == "schemas/layout_family.schema.json":
                layout_family_targets.append((rel, instance["applies_to_archetype"]))

        for rel, graph_ref in archetype_graph_refs:
            with self.subTest(instance=rel):
                self.assertIn(graph_ref, graph_ids, f"{rel} references unknown gameplay_graph_ref '{graph_ref}'")
        for rel, archetype_ref in layout_family_targets:
            with self.subTest(instance=rel):
                self.assertIn(archetype_ref, archetype_ids, f"{rel} references unknown applies_to_archetype '{archetype_ref}'")

    def test_existing_blueprint_corpus_is_map_plan_compatible(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/map_plan.schema.json").read_text(encoding="utf-8"))
        paths = sorted(glob.glob(BLUEPRINT_GLOB))
        self.assertGreater(len(paths), 0, "expected to find the existing blueprint corpus")
        for path in paths:
            with self.subTest(blueprint=path):
                instance = json.loads(Path(path).read_text(encoding="utf-8"))
                errors = validate(instance, schema)
                self.assertEqual(errors, [], f"{path} failed: {errors}")

    def test_map_vision_invalid_examples_fail_closed(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/map_vision.schema.json").read_text(encoding="utf-8"))
        for name in ("invalid_raw_tile_id.json", "invalid_silent_canon.json"):
            with self.subTest(instance=name):
                instance = json.loads((CONTRACT_ROOT / "examples/map_vision" / name).read_text(encoding="utf-8"))
                self.assertTrue(validate(instance, schema), f"{name} must not pass schema validation")

    def test_map_vision_cannot_use_concept_art_as_canon_authority(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/map_vision/invalid_silent_canon.json").read_text(encoding="utf-8"))
        provenance = {entry["source_ref"]: entry for entry in instance["source_provenance"]}
        identity = instance["memorable_identity"]
        canon_sources = [provenance[ref] for ref in identity["source_refs"]]
        self.assertEqual(identity["authority"], "required_canon")
        self.assertTrue(any(source["source_type"] == "concept_art" for source in canon_sources))
        self.assertFalse(all(source["source_type"] == "atlas_canon" for source in canon_sources))
        errors = validate_map_vision_semantics(instance)
        self.assertIn("required_canon statement has no atlas_canon source", errors)
        self.assertIn("concept_art provenance cannot have required_canon authority", errors)

    def test_map_vision_has_no_raw_engine_bindings(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/map_vision/valid_map_vision.json").read_text(encoding="utf-8"))
        forbidden = {"tile_id", "tileId", "tilesetId", "asset_filename", "database_id"}

        def walk(value: object) -> None:
            if isinstance(value, dict):
                self.assertTrue(forbidden.isdisjoint(value), f"MapVision carries engine binding: {forbidden.intersection(value)}")
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(instance)
        self.assertEqual(validate_map_vision_semantics(instance), [])

    def test_map_vision_conflict_forces_human_pending_state(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/map_vision/valid_map_vision.json").read_text(encoding="utf-8"))
        instance["status"] = "approved"
        instance["approval"] = {
            "canon_reconciled": True,
            "unresolved_conflicts": [{
                "conflict_id": "CONFLICT-ROUTE-001",
                "statement_refs": ["ST-GEOGRAPHY-001", "ST-ROAD-001"],
                "question_for_human": "Which route requirement controls?",
            }],
            "approved_by": "Agent",
            "approved_at": "2026-07-15",
        }
        errors = validate_map_vision_semantics(instance)
        self.assertIn("unresolved conflicts require pending_human_approval status", errors)
        self.assertIn("unresolved conflicts require canon_reconciled=false", errors)
        self.assertIn("approved MapVision cannot have unresolved conflicts", errors)

    def test_approved_map_vision_requires_resolved_human_gate(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/map_vision/valid_map_vision.json").read_text(encoding="utf-8"))
        approval = instance["approval"]
        if instance["status"] == "approved":
            self.assertTrue(approval["canon_reconciled"])
            self.assertEqual(approval["unresolved_conflicts"], [])
            self.assertIsNotNone(approval["approved_by"])
            self.assertIsNotNone(approval["approved_at"])
        else:
            self.assertEqual(instance["status"], "pending_human_approval")

    def test_tile_assembly_valid_example_passes_schema_and_semantics(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/tile_assembly.schema.json").read_text(encoding="utf-8"))
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/valid_tile_assembly.json").read_text(encoding="utf-8"))
        self.assertEqual(validate(instance, schema), [])
        self.assertEqual(validate_tile_assembly_semantics(instance), [])

    def test_tile_assembly_accepts_connectorless_atomic_prop(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/tile_assembly.schema.json").read_text(encoding="utf-8"))
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/valid_atomic_prop.json").read_text(encoding="utf-8"))
        self.assertEqual(instance["connectors"], [])
        self.assertGreaterEqual(len(instance["anchors"]), 1)
        self.assertEqual(validate(instance, schema), [])
        self.assertEqual(validate_tile_assembly_semantics(instance), [])

    def test_tile_assembly_event_overlay_is_source_consistent(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/valid_tile_assembly.json").read_text(encoding="utf-8"))
        overlay = instance["event_overlays"][0]
        self.assertEqual(overlay["character_name"], "!Door1")
        self.assertEqual(validate_tile_assembly_semantics(instance), [])

        overlay["source_coordinate"] = {"map_x": 99, "map_y": 99}
        overlay["character_name"] = "   "
        errors = validate_tile_assembly_semantics(instance)
        self.assertTrue(any("does not match its layered cell provenance" in error for error in errors))
        self.assertIn("event overlay character_name must be nonblank", errors)

    def test_tile_assembly_incomplete_fixture_fails_closed(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/tile_assembly.schema.json").read_text(encoding="utf-8"))
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/invalid_incomplete.json").read_text(encoding="utf-8"))
        self.assertTrue(validate(instance, schema), "incomplete hash components must fail schema validation")
        errors = validate_tile_assembly_semantics(instance)
        self.assertIn("layered_cells must contain exactly one complete cell for every assembly coordinate", errors)
        self.assertIn("collision_mask must be exactly dimensions.height rows by dimensions.width columns", errors)

    def test_tile_assembly_hash_drift_fixture_fails_closed(self) -> None:
        schema = json.loads((CONTRACT_ROOT / "schemas/tile_assembly.schema.json").read_text(encoding="utf-8"))
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/invalid_hash_drift.json").read_text(encoding="utf-8"))
        self.assertEqual(validate(instance, schema), [])
        errors = validate_tile_assembly_semantics(instance)
        self.assertIn("source hash mismatch", errors)
        self.assertIn("tileset image hash mismatch: Outside_B.png", errors)

    def test_tile_assembly_rejects_duplicate_tileset_image_names(self) -> None:
        instance = json.loads((CONTRACT_ROOT / "examples/tile_assembly/valid_tile_assembly.json").read_text(encoding="utf-8"))
        instance["source"]["hashes"]["tileset_images"].append(
            dict(instance["source"]["hashes"]["tileset_images"][0])
        )
        self.assertIn("tileset image asset_name values must be unique", validate_tile_assembly_semantics(instance))


if __name__ == "__main__":
    unittest.main()
