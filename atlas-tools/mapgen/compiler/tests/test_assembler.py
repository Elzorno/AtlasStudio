from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


COMPILER_DIR = Path(__file__).resolve().parents[1]
EXAMPLES = COMPILER_DIR / "contract" / "examples"
sys.path.insert(0, str(COMPILER_DIR))

from assembler import (  # noqa: E402
    AssemblyBudget,
    AssemblyError,
    ConnectorDefinition,
    Orientation,
    Port,
    SemanticAssembler,
    standard_connector_registry,
)
from seed_streams import SeedStreams, derive_root_seed  # noqa: E402
from structural_preview import render_ascii, render_svg  # noqa: E402


def load(relative: str) -> dict:
    return json.loads((EXAMPLES / relative).read_text(encoding="utf-8"))


def modules() -> dict[str, dict]:
    result = {}
    for path in sorted((EXAMPLES / "shared").glob("module_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        result[payload["module_id"]] = payload
    return result


def assemble(seed: int = 1, *, beats: tuple[str, ...] = ("exit_transfer",), graph: dict | None = None, module_defs: dict | None = None):
    return SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
        map_intent=load("shop/map_intent.json"),
        gameplay_graph=graph or load("shop/gameplay_graph.json"),
        archetype=load("shop/building_archetype.json"),
        layout_family=load("shop/layout_family.json"),
        modules=module_defs or modules(),
        streams=SeedStreams(seed),
        manifest_id=f"GEN-WO0058-{seed}",
        required_beats=beats,
    )


class ConnectorTests(unittest.TestCase):
    def test_registry_covers_required_connector_vocabulary(self) -> None:
        required = {
            "exterior_door", "interior_door", "service_point", "stairs",
            "road_connection", "waterfront_connection", "dungeon_connector",
            "transfer_anchor", "event_anchor",
        }
        self.assertTrue(required.issubset(standard_connector_registry()))

    def test_every_standard_connector_accepts_an_opposed_compatible_pair(self) -> None:
        for name, connector in standard_connector_registry().items():
            with self.subTest(connector=name):
                port_type = sorted(connector.compatible_port_types)[0]
                self.assertTrue(connector.accepts(
                    Port("first", port_type, Orientation.WEST),
                    Port("second", port_type, Orientation.EAST),
                ))

    def test_valid_opposed_ports_are_accepted(self) -> None:
        connector = ConnectorDefinition("stairs", frozenset({"stairs_up", "stairs_down"}))
        self.assertTrue(connector.accepts(Port("up", "stairs_up", Orientation.NORTH), Port("down", "stairs_down", Orientation.SOUTH)))

    def test_invalid_type_and_orientation_fail_closed(self) -> None:
        connector = standard_connector_registry()["interior_door"]
        self.assertFalse(connector.accepts(Port("a", "road_connection", Orientation.NORTH), Port("b", "interior_door", Orientation.SOUTH)))
        self.assertFalse(connector.accepts(Port("a", "interior_door", Orientation.NORTH), Port("b", "interior_door", Orientation.EAST)))

    def test_unknown_graph_connector_has_actionable_diagnostic(self) -> None:
        graph = load("shop/gameplay_graph.json")
        graph["edges"][0]["connector_type"] = "teleporter_guess"
        with self.assertRaises(AssemblyError) as caught:
            assemble(graph=graph)
        self.assertEqual("unknown_connector_type", caught.exception.diagnostic.code)
        self.assertIn("edge", caught.exception.diagnostic.context)


class AssemblyTests(unittest.TestCase):
    def test_three_seed_fixtures_reproduce_exactly(self) -> None:
        outputs = []
        for label in ("ashford-shop-a", "ashford-shop-b", "ashford-shop-c"):
            seed = derive_root_seed((label, "WO-0058"))
            first = assemble(seed).map_plan.to_json()
            second = assemble(seed).map_plan.to_json()
            self.assertEqual(first, second)
            outputs.append(first)
        self.assertEqual(3, len(set(outputs)))

    def test_required_nodes_and_route_are_preserved(self) -> None:
        payload = assemble(7).map_plan.to_dict()
        roles = {zone["terrain_type"] for zone in payload["terrain"]}
        self.assertTrue({"entry_threshold", "center_aisle", "wall_stock", "focal_feature"}.issubset(roles))
        self.assertEqual({"center_aisle", "wall_stock", "focal_feature"}, set(payload["validation"]["must_reach"]))
        self.assertTrue(payload["transfer_points"])

    def test_blocked_required_route_fails_closed(self) -> None:
        graph = load("shop/gameplay_graph.json")
        graph["edges"] = [edge for edge in graph["edges"] if edge["to_zone"] != "wall_stock"]
        with self.assertRaises(AssemblyError) as caught:
            assemble(graph=graph)
        self.assertEqual("disconnected_selected_graph", caught.exception.diagnostic.code)
        self.assertIn("wall_stock", caught.exception.diagnostic.context["unreached"])

    def test_optional_service_beat_is_preserved_when_requested(self) -> None:
        payload = assemble(8, beats=("exit_transfer", "npc_service_point")).map_plan.to_dict()
        self.assertIn("service_point", {zone["terrain_type"] for zone in payload["terrain"]})
        self.assertTrue(any(anchor["trigger_intent"] == "npc_service_point" for anchor in payload["event_anchors"]))

    def test_rotation_and_reflection_are_recorded_and_in_bounds(self) -> None:
        payload = assemble(9).map_plan.to_dict()
        self.assertIn(payload["map_intent"]["rotation"], (0, 90, 180, 270))
        self.assertIsInstance(payload["map_intent"]["reflected"], bool)
        width, height = payload["dimensions"]["width"], payload["dimensions"]["height"]
        for zone in payload["terrain"]:
            area = zone["area"]
            self.assertLessEqual(area["x"] + area["w"], width)
            self.assertLessEqual(area["y"] + area["h"], height)

    def test_layout_family_size_range_controls_dimensions(self) -> None:
        family = load("shop/layout_family.json")
        payload = assemble(12).map_plan.to_dict()
        expected = (family["size_range"]["max_width"], family["size_range"]["max_height"])
        actual = (payload["dimensions"]["width"], payload["dimensions"]["height"])
        if payload["map_intent"]["rotation"] in (90, 270):
            expected = tuple(reversed(expected))
        self.assertEqual(expected, actual)

    def test_incompatible_family_and_archetype_size_ranges_fail_closed(self) -> None:
        family = load("shop/layout_family.json")
        family["size_range"] = {"min_width": 30, "min_height": 30, "max_width": 40, "max_height": 40}
        with self.assertRaises(AssemblyError) as caught:
            SemanticAssembler(budget=AssemblyBudget(5000, 20)).assemble(
                map_intent=load("shop/map_intent.json"), gameplay_graph=load("shop/gameplay_graph.json"),
                archetype=load("shop/building_archetype.json"), layout_family=family, modules=modules(),
                streams=SeedStreams(12), manifest_id="GEN-SIZE-FAIL", required_beats=("exit_transfer",),
            )
        self.assertEqual("incompatible_size_ranges", caught.exception.diagnostic.code)

    def test_landmark_semantics_are_resolved_into_map_plan(self) -> None:
        landmarks = assemble(13).map_plan.to_dict()["landmark_slots"]
        self.assertEqual(1, len(landmarks))
        self.assertEqual("floor_rug_focal_accent", landmarks[0]["landmark_tag"])
        self.assertEqual("focal_feature", landmarks[0]["zone_role"])
        self.assertTrue(landmarks[0]["required"])
        self.assertTrue(landmarks[0]["dominant"])

    def test_clearance_failure_has_context(self) -> None:
        defs = modules()
        defs["MOD-SHELF-WALL-RUN"] = copy.deepcopy(defs["MOD-SHELF-WALL-RUN"])
        defs["MOD-SHELF-WALL-RUN"]["clearance"]["min_adjacent_walkable"] = 999
        with self.assertRaises(AssemblyError) as caught:
            assemble(module_defs=defs)
        self.assertEqual("module_clearance_unsatisfied", caught.exception.diagnostic.code)
        self.assertEqual("MOD-SHELF-WALL-RUN", caught.exception.diagnostic.context["module_ref"])

    def test_budget_is_mandatory_and_bounded_failure_is_reported(self) -> None:
        with self.assertRaises(ValueError):
            AssemblyBudget(0, 1)
        assembler = SemanticAssembler(budget=AssemblyBudget(1, 1))
        with self.assertRaises(AssemblyError) as caught:
            assembler.assemble(
                map_intent=load("shop/map_intent.json"), gameplay_graph=load("shop/gameplay_graph.json"),
                archetype=load("shop/building_archetype.json"), layout_family=load("shop/layout_family.json"),
                modules=modules(), streams=SeedStreams(4), manifest_id="GEN-BOUND", required_beats=("exit_transfer",),
            )
        self.assertEqual("placement_budget_exhausted", caught.exception.diagnostic.code)
        self.assertEqual(1, caught.exception.diagnostic.context["max_attempts"])

    def test_structural_previews_are_derived_from_plan(self) -> None:
        plan = assemble(11).map_plan
        self.assertIn("entry_threshold", render_ascii(plan))
        self.assertTrue(render_svg(plan).startswith("<svg"))


if __name__ == "__main__":
    unittest.main()
