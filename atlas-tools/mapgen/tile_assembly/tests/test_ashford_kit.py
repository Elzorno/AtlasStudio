"""Acceptance tests for the reference-derived WO-0070 Ashford kit."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


MAPGEN = Path(__file__).resolve().parents[2]
CONTRACT = MAPGEN / "compiler/contract"
KIT = Path(__file__).resolve().parents[1] / "kits/ashford"
sys.path.insert(0, str(CONTRACT))

from tile_assembly_validation import validate_tile_assembly_semantics  # noqa: E402
from validate_contract import validate  # noqa: E402


class AshfordKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads((CONTRACT / "schemas/tile_assembly.schema.json").read_text())
        cls.index = json.loads((KIT / "index.json").read_text())

    def test_every_kit_assembly_and_preview_is_valid(self) -> None:
        self.assertGreaterEqual(len(self.index["assemblies"]), 13)
        for entry in self.index["assemblies"]:
            with self.subTest(assembly=entry["tile_assembly_id"]):
                instance = json.loads((KIT / entry["file"]).read_text())
                self.assertEqual(validate(instance, self.schema), [])
                self.assertEqual(validate_tile_assembly_semantics(instance), [])
                for preview in instance["preview_refs"]:
                    path = KIT / preview
                    self.assertTrue(path.is_file())
                    self.assertGreater(path.stat().st_size, 0)

    def test_complete_tree_signature_contains_canopy_and_base(self) -> None:
        instance = json.loads((KIT / "tasm-ashford-tree-broadleaf-01.json").read_text())
        layer_three = {
            (cell["x"], cell["y"]): next(layer["tile_id"] for layer in cell["layers"] if layer["layer"] == 3)
            for cell in instance["layered_cells"]
        }
        self.assertEqual(layer_three, {(0, 0): 176, (1, 0): 177, (0, 1): 184, (1, 1): 185})

    def test_only_fidelity_verified_records_allow_downstream_generation(self) -> None:
        reusable = {
            "TASM-ASHFORD-TREE-BROADLEAF-01",
            "TASM-ASHFORD-WINDOW-01",
            "TASM-ASHFORD-SIGN-SHOP-01",
        }
        observed = {
            entry["tile_assembly_id"]
            for entry in self.index["assemblies"]
            if entry["downstream_generation_allowed"]
        }
        self.assertEqual(observed, reusable)
        for entry in self.index["assemblies"]:
            self.assertIn(entry["review_state"], {"verified_reusable", "study_only", "blocked_for_ashford"})
            self.assertEqual(entry["downstream_generation_allowed"], entry["review_state"] == "verified_reusable")
            self.assertTrue(entry["review_reason"].strip())

    def test_atomic_component_signatures_are_exact(self) -> None:
        expected = {
            "tasm-ashford-window-01.json": 97,
            "tasm-ashford-sign-shop-01.json": 66,
        }
        for name, tile_id in expected.items():
            with self.subTest(assembly=name):
                instance = json.loads((KIT / name).read_text())
                self.assertEqual(instance["dimensions"], {"width": 1, "height": 1})
                visible = [
                    layer["tile_id"]
                    for layer in instance["layered_cells"][0]["layers"]
                    if layer["tile_id"]
                ]
                self.assertEqual(visible[-1], tile_id)

    def test_buildings_include_complete_door_overlays(self) -> None:
        names = [
            "tasm-ashford-cottage-low-a.json",
            "tasm-ashford-cottage-low-b.json",
            "tasm-ashford-house-compact-01.json",
            "tasm-ashford-shop-tavern-frontage.json",
            "tasm-ashford-inn-broad-01.json",
        ]
        for name in names:
            with self.subTest(assembly=name):
                instance = json.loads((KIT / name).read_text())
                overlays = instance.get("event_overlays", [])
                self.assertGreaterEqual(len(overlays), 1)
                self.assertTrue(all(overlay["character_name"] == "!Door1" for overlay in overlays))


if __name__ == "__main__":
    unittest.main()
