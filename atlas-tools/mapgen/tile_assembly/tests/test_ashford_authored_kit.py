"""Acceptance tests for the human-gated authored Ashford assembly candidates."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

from PIL import Image

MAPGEN = Path(__file__).resolve().parents[2]
CONTRACT = MAPGEN / "compiler/contract"
KIT = Path(__file__).resolve().parents[1] / "kits/ashford/authored"
sys.path.insert(0, str(CONTRACT))

from tile_assembly_validation import validate_tile_assembly_semantics  # noqa: E402
from validate_contract import validate  # noqa: E402


class AuthoredAshfordKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index = json.loads((KIT / "index.json").read_text())
        cls.schema = json.loads((CONTRACT / "schemas/tile_assembly.schema.json").read_text())

    def test_human_selection_is_partial_and_fail_closed(self) -> None:
        self.assertEqual(9, len(self.index["assemblies"]))
        self.assertEqual("adapter_authored_candidate", self.index["authorship"])
        self.assertFalse(self.index["reference_extracted"])
        self.assertEqual("partial_human_approval", self.index["approval_state"])
        self.assertFalse(self.index["enabled"])
        for entry in self.index["assemblies"]:
            self.assertFalse(entry["reference_extracted"])

        enabled = {entry["tile_assembly_id"] for entry in self.index["assemblies"] if entry["enabled"]}
        self.assertEqual(enabled, {
            "TASM-ASHFORD-ELARA-HOUSE-AUTHORED",
            "TASM-ASHFORD-SHOP-AUTHORED",
            "TASM-ASHFORD-INN-AUTHORED",
            "TASM-ASHFORD-ELDER-HOUSE-AUTHORED",
            "TASM-ASHFORD-WARM-VENT-AUTHORED",
        })

    def test_fidelity_review_records_human_decisions(self) -> None:
        states = {entry["tile_assembly_id"]: entry["fidelity_review_state"] for entry in self.index["assemblies"]}
        self.assertEqual(states["TASM-ASHFORD-WARM-VENT-AUTHORED"], "human_approved")
        self.assertEqual(sum(value in {"human_approved", "human_approved_with_revision"} for value in states.values()), 5)
        self.assertEqual(sum(value == "human_rejected" for value in states.values()), 3)
        self.assertEqual(states["TASM-ASHFORD-BRIDGE-AUTHORED"], "human_corrected_bridge_reference")
        for entry in self.index["assemblies"]:
            expected = entry["fidelity_review_state"] in {"human_approved", "human_approved_with_revision"}
            self.assertEqual(entry["downstream_generation_allowed"], expected)

    def test_contracts_hashes_and_previews_are_complete(self) -> None:
        source = KIT / self.index["source_fixture"]
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(source_hash, self.index["source_fixture_sha256"])
        for entry in self.index["assemblies"]:
            with self.subTest(assembly=entry["tile_assembly_id"]):
                instance = json.loads((KIT / entry["file"]).read_text())
                self.assertEqual([], validate(instance, self.schema))
                self.assertEqual([], validate_tile_assembly_semantics(instance))
                self.assertEqual(source_hash, instance["source"]["hashes"]["map"]["expected_sha256"])
                for preview in instance["preview_refs"]:
                    self.assertGreater((KIT / preview).stat().st_size, 0)

    def test_buildings_are_low_broad_and_have_complete_doors(self) -> None:
        buildings = [entry for entry in self.index["assemblies"] if any(role in entry["tile_assembly_id"] for role in ("ELARA-HOUSE", "SHOP-AUTHORED", "INN-AUTHORED", "ELDER-HOUSE"))]
        self.assertEqual(4, len(buildings))
        for entry in buildings:
            instance = json.loads((KIT / entry["file"]).read_text())
            self.assertGreater(instance["dimensions"]["width"], instance["dimensions"]["height"])
            self.assertEqual(1, len(instance["event_overlays"]))
            self.assertEqual("!Door1", instance["event_overlays"][0]["character_name"])
            self.assertEqual("south", instance["connectors"][0]["facing"])

    def test_landmark_and_proxy_signatures_are_nonempty_and_explicitly_limited(self) -> None:
        limited = 0
        for entry in self.index["assemblies"]:
            instance = json.loads((KIT / entry["file"]).read_text())
            visible = [layer["tile_id"] for cell in instance["layered_cells"] for layer in cell["layers"] if layer["tile_id"]]
            self.assertTrue(visible)
            if entry["asset_vocabulary_limitation"]:
                limited += 1
                self.assertTrue(
                    "no verified" in entry["asset_vocabulary_limitation"]
                    or "Human-corrected classification" in entry["asset_vocabulary_limitation"]
                )
        self.assertEqual(5, limited)

    def test_hash_drift_is_rejected(self) -> None:
        entry = self.index["assemblies"][0]
        instance = json.loads((KIT / entry["file"]).read_text())
        instance["source"]["hashes"]["source"]["observed_sha256"] = "0" * 64
        self.assertIn("source hash mismatch", validate_tile_assembly_semantics(instance))

    def test_authored_proxy_signatures_are_exact_and_complete(self) -> None:
        expected = {
            "tasm-ashford-well-roofed-authored.json": [[5, 6, 7], [88, 0, 89], [0, 139, 0]],
            "tasm-ashford-warm-vent-authored.json": [[0, 128, 0], [140, 140, 140]],
            "tasm-ashford-humming-panel-authored.json": [[117, 118], [82, 84]],
            "tasm-ashford-patched-metal-fence-authored.json": [[188, 84, 189, 86, 190]],
        }
        for filename, signature in expected.items():
            with self.subTest(assembly=filename):
                instance = json.loads((KIT / filename).read_text())
                observed = [[0 for _ in range(instance["dimensions"]["width"])] for _ in range(instance["dimensions"]["height"])]
                for cell in instance["layered_cells"]:
                    observed[cell["y"]][cell["x"]] = next(
                        layer["tile_id"] for layer in cell["layers"] if layer["layer"] == 3
                    )
                self.assertEqual(signature, observed)

    def test_custom_extension_records_complete_human_approval(self) -> None:
        extension = KIT.parent / "custom_extension"
        manifest = json.loads((extension / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("human_approved", manifest["approval_state"])
        self.assertTrue(manifest["enabled"])
        self.assertEqual(4, len(manifest["assets"]))
        enabled = {asset["asset_id"] for asset in manifest["assets"] if asset["enabled"]}
        self.assertEqual({asset["asset_id"] for asset in manifest["assets"]}, enabled)
        self.assertTrue(all(asset["enabled"] == asset["downstream_generation_allowed"] for asset in manifest["assets"]))
        sizes = {asset["asset_id"]: asset["tile_size"] for asset in manifest["assets"]}
        self.assertEqual({"width": 2, "height": 2}, sizes["ASH-CUSTOM-WELL-ROOFED-01"])
        self.assertEqual({"width": 2, "height": 2}, sizes["ASH-CUSTOM-DRAINAGE-01"])
        self.assertEqual({"width": 1, "height": 2}, sizes["ASH-CUSTOM-PANEL-01"])
        self.assertEqual({"width": 6, "height": 2}, sizes["ASH-CUSTOM-FENCE-01"])
        with Image.open(extension / manifest["tileset_image"]) as tileset:
            self.assertEqual((768, 768), tileset.size)
            self.assertEqual("RGBA", tileset.mode)
            self.assertEqual(0, tileset.getpixel((767, 767))[3])


if __name__ == "__main__":
    unittest.main()
