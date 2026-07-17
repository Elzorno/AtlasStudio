from __future__ import annotations

import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

MAPGEN_ROOT = Path(__file__).resolve().parents[2]
if str(MAPGEN_ROOT) not in sys.path:
    sys.path.insert(0, str(MAPGEN_ROOT))

from tile_assembly import (  # noqa: E402
    TileAssemblyValidationError,
    extract_tile_assembly,
    extracted_region_sha256,
    render_assembly,
    render_composition,
    to_contract_tile_assembly,
    validate_tile_assembly,
)


class TileAssemblyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.map_path = self.root / "Map001.json"
        self.tilesets_path = self.root / "Tilesets.json"
        self.images = self.root / "tilesets"
        self.images.mkdir()
        self.characters = self.root / "characters"
        self.characters.mkdir()

        width, height, layer_count = 3, 2, 6
        data = [0] * (width * height * layer_count)
        for layer in range(4):
            for y in range(height):
                for x in range(width):
                    data[(layer * height + y) * width + x] = layer * 10 + y * width + x + 1
        door_event = {
            "id": 1,
            "x": 2,
            "y": 1,
            "pages": [{
                "image": {
                    "characterName": "!Door1",
                    "characterIndex": 0,
                    "direction": 2,
                    "pattern": 0,
                },
                "priorityType": 1,
                "through": False,
            }],
        }
        self.map_path.write_text(
            json.dumps({"width": width, "height": height, "tilesetId": 1, "data": data, "events": [None, door_event]}),
            encoding="utf-8",
        )
        names = ["", "", "", "", "", "SyntheticB", "", "", ""]
        self.tilesets_path.write_text(
            json.dumps([None, {"id": 1, "tilesetNames": names, "flags": [0] * 8192}]),
            encoding="utf-8",
        )
        image = Image.new("RGBA", (768, 768), (0, 0, 0, 0))
        for y in range(16):
            for x in range(16):
                color = (20 + x * 4, 30 + y * 4, 100, 255)
                tile = Image.new("RGBA", (48, 48), color)
                image.alpha_composite(tile, (x * 48, y * 48))
        image.save(self.images / "SyntheticB.png")
        character = Image.new("RGBA", (576, 384), (0, 0, 0, 0))
        character.alpha_composite(Image.new("RGBA", (48, 48), (240, 20, 40, 255)), (0, 0))
        character.save(self.characters / "!Door1.png")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def extract(self):
        return extract_tile_assembly(
            self.map_path,
            self.tilesets_path,
            assembly_id="TASM-TEST-001",
            x=1,
            y=0,
            width=2,
            height=2,
            collision_mask=[[False, True], [True, False]],
            connectors=[
                {
                    "connector_id": "south-door",
                    "orientation": "south",
                    "position": {"x": 0, "y": 1},
                }
            ],
            anchors=[{"anchor_id": "origin", "position": {"x": 0, "y": 0}}],
            tileset_image_dir=self.images,
        )

    def test_extracts_rectangular_layers_and_provenance_without_mutation(self):
        before_map = self.map_path.read_bytes()
        before_tilesets = self.tilesets_path.read_bytes()

        assembly = self.extract()

        self.assertEqual([[2, 3], [5, 6]], assembly["layers"][0]["cells"])
        self.assertEqual([[12, 13], [15, 16]], assembly["layers"][1]["cells"])
        self.assertEqual({"x": 1, "y": 0, "width": 2, "height": 2}, assembly["source"]["region"])
        self.assertEqual(64, len(assembly["source"]["map_sha256"]))
        self.assertIn("SyntheticB", assembly["source"]["tileset_image_sha256"])
        self.assertEqual(before_map, self.map_path.read_bytes())
        self.assertEqual(before_tilesets, self.tilesets_path.read_bytes())
        validate_tile_assembly(assembly)

    def test_rejects_invalid_dimensions_layers_collision_and_connector(self):
        cases = []
        assembly = self.extract()
        assembly["dimensions"]["width"] = 3
        cases.append(assembly)

        assembly = self.extract()
        assembly["layers"][1]["source_layer"] = assembly["layers"][0]["source_layer"]
        cases.append(assembly)

        assembly = self.extract()
        assembly["collision_mask"][0] = [False]
        cases.append(assembly)

        assembly = self.extract()
        assembly["connectors"][0]["position"] = {"x": 0, "y": 0}
        cases.append(assembly)

        for invalid in cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(TileAssemblyValidationError):
                    validate_tile_assembly(invalid, check_source_hashes=False)

    def test_rejects_source_and_tileset_image_hash_drift(self):
        assembly = self.extract()
        original = self.map_path.read_text(encoding="utf-8")
        self.map_path.write_text(original + " ", encoding="utf-8")
        with self.assertRaisesRegex(TileAssemblyValidationError, "map_path"):
            validate_tile_assembly(assembly)

        self.map_path.write_text(original, encoding="utf-8")
        image_path = self.images / "SyntheticB.png"
        image_path.write_bytes(image_path.read_bytes() + b"drift")
        with self.assertRaisesRegex(TileAssemblyValidationError, "SyntheticB"):
            validate_tile_assembly(assembly)

    def test_renders_isolated_assembly_and_composition_fixture(self):
        assembly = self.extract()
        isolated = render_assembly(assembly, self.root / "isolated.png")
        composition = render_composition(
            [
                {"assembly": assembly, "x": 0, "y": 0},
                {"assembly": assembly, "x": 2, "y": 1},
            ],
            self.root / "composition.png",
            width=4,
            height=3,
        )
        with Image.open(isolated) as image:
            self.assertEqual((96, 96), image.size)
            self.assertGreater(image.getbbox()[2], 0)
        with Image.open(composition) as image:
            self.assertEqual((192, 144), image.size)
            self.assertGreater(image.getbbox()[2], 96)

    def test_rejects_out_of_bounds_extraction_and_composition(self):
        with self.assertRaisesRegex(ValueError, "bounds"):
            extract_tile_assembly(
                self.map_path,
                self.tilesets_path,
                assembly_id="TA-BAD",
                x=2,
                y=0,
                width=2,
                height=1,
            )
        assembly = self.extract()
        with self.assertRaisesRegex(ValueError, "bounds"):
            render_composition(
                [{"assembly": assembly, "x": 1, "y": 1}],
                self.root / "bad.png",
                width=2,
                height=2,
            )

    def test_contract_projection_matches_schema_and_semantics(self):
        from compiler.contract.tile_assembly_validation import validate_tile_assembly_semantics
        from compiler.contract.validate_contract import validate

        extracted = self.extract()
        contract = to_contract_tile_assembly(
            extracted,
            name="Synthetic assembly",
            preview_refs=["previews/TASM-TEST-001.png"],
            owner_repo="test-adapter",
        )
        schema_path = MAPGEN_ROOT / "compiler/contract/schemas/tile_assembly.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        schema_errors = validate(contract, schema)
        self.assertEqual([], schema_errors)
        self.assertEqual([], validate_tile_assembly_semantics(contract))
        self.assertEqual("TASM-TEST-001", contract["tile_assembly_id"])
        self.assertEqual(
            {"map_x": 1, "map_y": 0, "layer": 0},
            contract["layered_cells"][0]["layers"][0]["source_coordinate"],
        )
        self.assertEqual("placement", contract["anchors"][0]["role"])
        self.assertEqual("south", contract["connectors"][0]["facing"])
        self.assertEqual("base", contract["variations"][0]["variation_id"])

        source_hash = contract["source"]["hashes"]["source"]["expected_sha256"]
        self.assertEqual(extracted_region_sha256(extracted), source_hash)
        self.assertNotEqual(extracted["source"]["map_sha256"], source_hash)
        self.assertEqual(
            extracted["source"]["tileset_entry_sha256"],
            contract["source"]["hashes"]["tileset"]["expected_sha256"],
        )
        image_record = contract["source"]["hashes"]["tileset_images"][0]
        self.assertEqual("SyntheticB.png", image_record["asset_name"])
        self.assertEqual(
            hashlib.sha256((self.images / "SyntheticB.png").read_bytes()).hexdigest(),
            image_record["observed_sha256"],
        )

    def test_contract_projection_fails_closed_without_required_evidence(self):
        extracted = self.extract()
        with self.assertRaisesRegex(ValueError, "preview"):
            to_contract_tile_assembly(
                extracted,
                preview_refs=[],
                owner_repo="test-adapter",
            )
        extracted["source"]["tileset_image_sha256"] = {}
        with self.assertRaisesRegex(ValueError, "image hash"):
            to_contract_tile_assembly(
                extracted,
                preview_refs=["preview.png"],
                owner_repo="test-adapter",
            )

    def test_contract_projection_accepts_connectorless_atomic_assembly(self):
        from compiler.contract.tile_assembly_validation import validate_tile_assembly_semantics
        from compiler.contract.validate_contract import validate

        extracted = self.extract()
        extracted["connectors"] = []
        contract = to_contract_tile_assembly(
            extracted,
            name="Atomic complete tree",
            preview_refs=["previews/TASM-TEST-001-tree.png"],
            owner_repo="test-adapter",
        )
        schema_path = MAPGEN_ROOT / "compiler/contract/schemas/tile_assembly.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertEqual([], contract["connectors"])
        self.assertEqual([], validate(contract, schema))
        self.assertEqual([], validate_tile_assembly_semantics(contract))

    def test_extracts_projects_and_renders_selected_event_overlay(self):
        extracted = extract_tile_assembly(
            self.map_path,
            self.tilesets_path,
            assembly_id="TASM-TEST-DOOR",
            x=1,
            y=0,
            width=2,
            height=2,
            collision_mask=[[False, True], [True, False]],
            anchors=[{"anchor_id": "door", "role": "entry", "position": {"x": 1, "y": 1}}],
            source_event_ids=[1],
            tileset_image_dir=self.images,
            character_image_dir=self.characters,
        )
        overlay = extracted["event_overlays"][0]
        self.assertEqual({"x": 1, "y": 1}, overlay["local_coordinate"])
        self.assertEqual({"map_x": 2, "map_y": 1}, overlay["source_coordinate"])
        self.assertEqual("!Door1", overlay["image"]["characterName"])
        self.assertEqual(1, overlay["priorityType"])
        self.assertFalse(overlay["through"])

        contract = to_contract_tile_assembly(
            extracted,
            preview_refs=["previews/TASM-TEST-DOOR.png"],
            owner_repo="test-adapter",
        )
        self.assertEqual("!Door1", contract["event_overlays"][0]["character_name"])
        self.assertEqual(1, contract["event_overlays"][0]["x"])
        from compiler.contract.tile_assembly_validation import validate_tile_assembly_semantics
        from compiler.contract.validate_contract import validate

        schema_path = MAPGEN_ROOT / "compiler/contract/schemas/tile_assembly.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual([], validate(contract, schema))
        self.assertEqual([], validate_tile_assembly_semantics(contract))

        output = render_assembly(extracted, self.root / "door.png")
        with Image.open(output) as preview:
            self.assertEqual((240, 20, 40, 255), preview.getpixel((72, 72)))

    def test_discovers_region_events_and_preview_fails_closed_without_characters(self):
        extracted = extract_tile_assembly(
            self.map_path,
            self.tilesets_path,
            assembly_id="TASM-TEST-DISCOVERY",
            x=1,
            y=0,
            width=2,
            height=2,
            collision_mask=[[False, False], [False, False]],
            anchors=[{"anchor_id": "origin", "position": {"x": 0, "y": 0}}],
            discover_events=True,
            tileset_image_dir=self.images,
        )
        self.assertEqual([1], [overlay["source_event_id"] for overlay in extracted["event_overlays"]])
        with self.assertRaisesRegex(ValueError, "cannot omit"):
            render_assembly(extracted, self.root / "must-not-exist.png")
        self.assertFalse((self.root / "must-not-exist.png").exists())


if __name__ == "__main__":
    unittest.main()
