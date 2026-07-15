from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


COMPILER_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(COMPILER_DIR))

from models import TerrainCell, TerrainModel  # noqa: E402
from planner import TerrainPlanner  # noqa: E402
from quality_auditor import QualityAuditor  # noqa: E402
from spec_parser import REQUIRED_LOCATIONS, load_world_spec  # noqa: E402
from tile_painter import TilePainterUnavailable, describe_painter_plan, paint_tiles  # noqa: E402


SPEC_PATH = COMPILER_DIR / "specs" / "home_island.world.json"
MAP027_PATH = REPO_ROOT.parent / "TheLastSwordProtocol-Game" / "data" / "Map027.json"
MAP027_NEGATIVE_AUDIT = COMPILER_DIR / "audits" / "map027_negative_audit.json"


class CompilerTests(unittest.TestCase):
    def test_home_island_spec_contains_required_locations(self) -> None:
        spec = load_world_spec(SPEC_PATH)
        self.assertEqual(REQUIRED_LOCATIONS, set(spec.canonical_locations))
        self.assertIn(["glassfield", "sealed_node"], spec.required_routes)

    def test_planner_produces_auditable_terrain_model(self) -> None:
        spec = load_world_spec(SPEC_PATH)
        model = TerrainPlanner().build(spec)
        result = QualityAuditor().audit_terrain_model(model, spec)

        self.assertTrue(result.passed, [finding.to_dict() for finding in result.findings])
        self.assertEqual("atlas-map-compiler", model.generator)
        self.assertEqual({"width": spec.width, "height": spec.height}, model.to_dict()["size"])
        self.assertEqual(REQUIRED_LOCATIONS, set(model.locations))

    def test_auditor_rejects_current_map027_without_compiler_provenance(self) -> None:
        if not MAP027_PATH.exists():
            self.skipTest("TheLastSwordProtocol-Game Map027 is not available")

        result = QualityAuditor().audit_rpgmaker_map(MAP027_PATH)
        codes = {finding.code for finding in result.findings}

        self.assertFalse(result.passed)
        self.assertIn("missing_intermediate_model_provenance", codes)

    def test_preserved_map027_negative_audit_records_known_example(self) -> None:
        payload = json.loads(MAP027_NEGATIVE_AUDIT.read_text(encoding="utf-8"))
        codes = {finding["code"] for finding in payload["findings"]}

        self.assertFalse(payload["passed"])
        self.assertIn("known_negative_example", codes)

    def test_auditor_rejects_rectangular_forest_blocks(self) -> None:
        width = 12
        height = 12
        cells = []
        for y in range(height):
            for x in range(width):
                biome = "forest" if 2 <= x <= 8 and 2 <= y <= 8 else "plains"
                cells.append(TerrainCell(x=x, y=y, land=True, elevation=0.2, biome=biome))
        model = TerrainModel(
            schema_version="0.1.0",
            region_id="TEST",
            map_name="Rectangular Forest",
            width=width,
            height=height,
            cells=cells,
            locations={"ashford": {"x": 0, "y": 0}},
        )

        result = QualityAuditor().audit_terrain_model(model)
        codes = {finding.code for finding in result.findings}

        self.assertFalse(result.passed)
        self.assertIn("rectangular_forest", codes)

    def test_tile_painter_is_explicitly_deferred(self) -> None:
        spec = load_world_spec(SPEC_PATH)
        model = TerrainPlanner().build(spec)
        plan = describe_painter_plan(model)

        self.assertEqual("deferred", plan.status)
        with self.assertRaises(TilePainterUnavailable):
            paint_tiles(model)

    def test_generated_prototype_file_round_trips(self) -> None:
        prototype = COMPILER_DIR / "prototypes" / "home_island_terrain.json"
        if not prototype.exists():
            self.skipTest("Generated prototype has not been written")

        model = TerrainModel.from_dict(json.loads(prototype.read_text(encoding="utf-8")))
        self.assertEqual("REG-HOM-001", model.region_id)
        self.assertEqual(REQUIRED_LOCATIONS, set(model.locations))


if __name__ == "__main__":
    unittest.main()
