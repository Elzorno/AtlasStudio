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


if __name__ == "__main__":
    unittest.main()
