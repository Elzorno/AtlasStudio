"""Deterministic semantic layout assembler for WO-0058.

The assembler resolves gameplay-graph zones and reusable modules into an
engine-neutral MapPlan. It never paints tiles or emits RPG Maker data.
"""

from __future__ import annotations

import copy
import math
import random
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable

from map_plan import MapPlan
from seed_streams import SeedStreams


class PortType(str, Enum):
    EXTERIOR_DOOR = "exterior_door"
    INTERIOR_DOOR = "interior_door"
    SERVICE_POINT = "service_point"
    STAIRS_UP = "stairs_up"
    STAIRS_DOWN = "stairs_down"
    ROAD_CONNECTION = "road_connection"
    WATERFRONT_CONNECTION = "waterfront_connection"
    DUNGEON_CONNECTOR = "dungeon_connector"
    TRANSFER_ANCHOR = "transfer_anchor"
    EVENT_ANCHOR = "event_anchor"
    DOOR_TRANSFER = "door_transfer"
    OPEN_FLOOR = "open_floor"
    CHOKEPOINT_CORRIDOR = "chokepoint_corridor"


class Orientation(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    ANY = "any"


OPPOSITE = {
    Orientation.NORTH: Orientation.SOUTH,
    Orientation.SOUTH: Orientation.NORTH,
    Orientation.EAST: Orientation.WEST,
    Orientation.WEST: Orientation.EAST,
    Orientation.ANY: Orientation.ANY,
}


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)


class AssemblyError(ValueError):
    def __init__(self, diagnostic: Diagnostic):
        super().__init__(f"{diagnostic.code}: {diagnostic.message}")
        self.diagnostic = diagnostic


@dataclass(frozen=True)
class AssemblyBudget:
    max_attempts: int
    max_depth: int

    def __post_init__(self) -> None:
        if self.max_attempts < 1 or self.max_depth < 1:
            raise ValueError("assembly budgets must be positive")


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    def overlaps(self, other: "Rect") -> bool:
        return not (
            self.right <= other.x
            or other.right <= self.x
            or self.bottom <= other.y
            or other.bottom <= self.y
        )

    def in_bounds(self, width: int, height: int) -> bool:
        return self.x >= 0 and self.y >= 0 and self.right <= width and self.bottom <= height

    def to_area(self) -> dict[str, Any]:
        return {"shape": "rect", "x": self.x, "y": self.y, "w": self.width, "h": self.height}


@dataclass(frozen=True)
class Port:
    port_id: str
    port_type: str
    orientation: Orientation


@dataclass(frozen=True)
class ConnectorDefinition:
    connector_type: str
    compatible_port_types: frozenset[str]
    width: int = 1
    traversal: str = "bidirectional"
    allow_rotation: bool = True

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ConnectorDefinition":
        return cls(
            connector_type=str(payload["connector_type"]),
            compatible_port_types=frozenset(str(item) for item in payload["compatible_port_types"]),
            width=int(payload["width"]),
            traversal=str(payload["traversal"]),
            allow_rotation=bool(payload.get("allow_rotation", False)),
        )

    def accepts(self, first: Port, second: Port) -> bool:
        types_ok = first.port_type in self.compatible_port_types and second.port_type in self.compatible_port_types
        orientations_ok = (
            first.orientation is Orientation.ANY
            or second.orientation is Orientation.ANY
            or OPPOSITE[first.orientation] is second.orientation
        )
        return types_ok and orientations_ok


@dataclass(frozen=True)
class AssemblyResult:
    map_plan: MapPlan
    variant_id: str
    rotation: int
    reflected: bool
    attempts: int
    diagnostics: tuple[Diagnostic, ...] = ()


def standard_connector_registry() -> dict[str, ConnectorDefinition]:
    """Connector registry covering the vocabulary required by WO-0058."""

    pairs = {
        "exterior_door": {PortType.EXTERIOR_DOOR.value, PortType.DOOR_TRANSFER.value, PortType.TRANSFER_ANCHOR.value},
        "interior_door": {PortType.INTERIOR_DOOR.value, PortType.DOOR_TRANSFER.value},
        "service_point": {PortType.SERVICE_POINT.value, PortType.OPEN_FLOOR.value, PortType.EVENT_ANCHOR.value},
        "stairs": {PortType.STAIRS_UP.value, PortType.STAIRS_DOWN.value},
        "road_connection": {PortType.ROAD_CONNECTION.value, PortType.EXTERIOR_DOOR.value},
        "waterfront_connection": {PortType.WATERFRONT_CONNECTION.value, PortType.ROAD_CONNECTION.value},
        "dungeon_connector": {PortType.DUNGEON_CONNECTOR.value, PortType.DOOR_TRANSFER.value},
        "transfer_anchor": {PortType.TRANSFER_ANCHOR.value, PortType.DOOR_TRANSFER.value},
        "event_anchor": {PortType.EVENT_ANCHOR.value, PortType.OPEN_FLOOR.value},
        "door_transfer": {PortType.DOOR_TRANSFER.value, PortType.INTERIOR_DOOR.value, PortType.EXTERIOR_DOOR.value},
        "open_floor": {PortType.OPEN_FLOOR.value},
        "chokepoint_corridor": {PortType.OPEN_FLOOR.value, PortType.DOOR_TRANSFER.value},
    }
    return {
        connector_type: ConnectorDefinition(connector_type, frozenset(port_types), width=2 if connector_type in {"open_floor", "chokepoint_corridor"} else 1)
        for connector_type, port_types in pairs.items()
    }


class SemanticAssembler:
    def __init__(self, *, budget: AssemblyBudget, connector_registry: dict[str, ConnectorDefinition] | None = None):
        self.budget = budget
        self.connectors = connector_registry or standard_connector_registry()
        self._attempts = 0

    def assemble(
        self,
        *,
        map_intent: dict[str, Any],
        gameplay_graph: dict[str, Any],
        archetype: dict[str, Any],
        layout_family: dict[str, Any],
        modules: dict[str, dict[str, Any]],
        streams: SeedStreams,
        manifest_id: str,
        required_beats: Iterable[str] = (),
    ) -> AssemblyResult:
        self._validate_references(gameplay_graph, archetype, layout_family)
        variant = self._choose_variant(layout_family, streams.seed("structures", "layout_variant"))
        zones = self._selected_zones(gameplay_graph, set(required_beats), variant["variant_id"])
        self._apply_module_size_requirements(zones, archetype, modules)
        edges = self._selected_edges(gameplay_graph, {zone["zone_id"] for zone in zones})
        self._validate_graph(zones, edges, gameplay_graph)
        width, height = self._choose_dimensions(archetype, layout_family, streams.seed("structures", "dimensions"))
        placements = self._place_zones(zones, edges, gameplay_graph["reachability"]["entry_zone"], width, height, streams)
        module_placements = self._place_modules(archetype, modules, zones, placements)
        self._validate_reachability(gameplay_graph, zones, edges)
        rotation = self._choose_rotation(layout_family, streams.seed("structures", "rotation"))
        reflected = bool(layout_family.get("allow_reflection", False) and streams.seed("structures", "reflection") % 2)
        placements, module_placements, width, height = self._transform(
            placements, module_placements, width, height, rotation, reflected
        )
        plan = self._build_map_plan(
            map_intent,
            gameplay_graph,
            archetype,
            layout_family,
            variant["variant_id"],
            placements,
            module_placements,
            edges,
            width,
            height,
            manifest_id,
            streams.root_seed,
            rotation,
            reflected,
        )
        return AssemblyResult(plan, variant["variant_id"], rotation, reflected, self._attempts)

    def _validate_references(self, graph: dict[str, Any], archetype: dict[str, Any], family: dict[str, Any]) -> None:
        if archetype["gameplay_graph_ref"] != graph["graph_id"]:
            raise AssemblyError(Diagnostic("graph_reference_mismatch", "archetype references a different gameplay graph"))
        if family["applies_to_archetype"] != archetype["archetype_id"]:
            raise AssemblyError(Diagnostic("archetype_reference_mismatch", "layout family applies to a different archetype"))

    def _choose_variant(self, family: dict[str, Any], seed: int) -> dict[str, Any]:
        variants = family["variants"]
        total = sum(float(variant["weight"]) for variant in variants)
        if total <= 0:
            raise AssemblyError(Diagnostic("invalid_variant_weights", "layout family has no positive variant weight"))
        target = random.Random(seed).random() * total
        cumulative = 0.0
        for variant in variants:
            cumulative += float(variant["weight"])
            if target < cumulative:
                return variant
        return variants[-1]

    def _selected_zones(self, graph: dict[str, Any], required_beats: set[str], variant_id: str) -> list[dict[str, Any]]:
        selected = []
        for zone in graph["zones"]:
            include = bool(zone["required"] or required_beats.intersection(zone.get("beats", [])))
            if not include and "loop" in variant_id and zone["role"] == "browse_loop":
                include = True
            if include:
                selected.append(copy.deepcopy(zone))
        return selected

    def _selected_edges(self, graph: dict[str, Any], selected: set[str]) -> list[dict[str, Any]]:
        return [copy.deepcopy(edge) for edge in graph["edges"] if edge["from_zone"] in selected and edge["to_zone"] in selected]

    def _validate_graph(self, zones: list[dict[str, Any]], edges: list[dict[str, Any]], graph: dict[str, Any]) -> None:
        zone_ids = {zone["zone_id"] for zone in zones}
        entry = graph["reachability"]["entry_zone"]
        missing = [zone for zone in graph["reachability"]["must_reach"] if zone not in zone_ids]
        if entry not in zone_ids or missing:
            raise AssemblyError(Diagnostic("missing_required_zone", "required gameplay zones were not selected", {"entry": entry, "missing": missing}))
        for edge in edges:
            if edge["connector_type"] not in self.connectors:
                raise AssemblyError(Diagnostic("unknown_connector_type", "edge uses an unregistered connector", {"edge": edge}))

    def _choose_dimensions(self, archetype: dict[str, Any], family: dict[str, Any], seed: int) -> tuple[int, int]:
        constraints = archetype.get("size_constraints", {})
        family_range = family.get("size_range", {})
        min_width = max(int(constraints.get("min_width", 8)), int(family_range.get("min_width", 1)))
        min_height = max(int(constraints.get("min_height", 6)), int(family_range.get("min_height", 1)))
        max_width = min(int(constraints.get("max_width", min_width + 6)), int(family_range.get("max_width", 10**9)))
        max_height = min(int(constraints.get("max_height", min_height + 6)), int(family_range.get("max_height", 10**9)))
        if min_width > max_width or min_height > max_height:
            raise AssemblyError(Diagnostic(
                "incompatible_size_ranges",
                "layout-family size range does not overlap its archetype bounds",
                {"archetype_bounds": constraints, "layout_family_range": family_range},
            ))
        # Use the full archetype envelope during structural assembly. Variation is
        # supplied by the selected family, placement stream, rotation and reflection;
        # a later tile-resolution pass may compact the validated structure.
        return max_width, max_height

    @staticmethod
    def _apply_module_size_requirements(
        zones: list[dict[str, Any]],
        archetype: dict[str, Any],
        modules: dict[str, dict[str, Any]],
    ) -> None:
        by_role = {zone["role"]: zone for zone in zones}
        for requirement in archetype.get("modules_required", []):
            count = int(requirement["min_count"])
            if count < 1 or requirement["zone_role"] not in by_role:
                continue
            module = modules.get(requirement["module_ref"])
            if module is None:
                continue  # _place_modules emits the actionable missing-definition diagnostic.
            footprint = module["footprint"]
            zone = by_role[requirement["zone_role"]]
            zone["_min_width"] = max(int(zone.get("_min_width", 1)), int(footprint["width"]) * count)
            zone["_min_height"] = max(int(zone.get("_min_height", 1)), int(footprint["height"]))

    @staticmethod
    def _zone_size(zone: dict[str, Any]) -> tuple[int, int]:
        area = int(zone.get("min_area", 1))
        width = max(1, math.ceil(math.sqrt(area)))
        height = max(1, math.ceil(area / width))
        return max(width, int(zone.get("_min_width", 1))), max(height, int(zone.get("_min_height", 1)))

    def _place_zones(
        self,
        zones: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        entry_zone: str,
        width: int,
        height: int,
        streams: SeedStreams,
    ) -> dict[str, Rect]:
        by_id = {zone["zone_id"]: zone for zone in zones}
        adjacency: dict[str, list[str]] = {zone_id: [] for zone_id in by_id}
        for edge in edges:
            adjacency[edge["from_zone"]].append(edge["to_zone"])
            adjacency[edge["to_zone"]].append(edge["from_zone"])
        entry_width, entry_height = self._zone_size(by_id[entry_zone])
        start = Rect(max(0, (width - entry_width) // 2), height - entry_height, entry_width, entry_height)
        order: list[tuple[str, str]] = []
        seen = {entry_zone}
        queue = deque([entry_zone])
        while queue:
            parent = queue.popleft()
            for child in sorted(adjacency[parent]):
                if child not in seen:
                    seen.add(child)
                    order.append((parent, child))
                    queue.append(child)
        if seen != set(by_id):
            raise AssemblyError(Diagnostic("disconnected_selected_graph", "selected zones do not form one connected graph", {"unreached": sorted(set(by_id) - seen)}))
        self._attempts = 0
        placements = {entry_zone: start}
        rng = random.Random(streams.seed("structures", "zone_placement"))
        result = self._search_placements(order, 0, placements, by_id, width, height, rng)
        if result is None:
            raise AssemblyError(Diagnostic(
                "placement_budget_exhausted",
                "no valid zone placement was found inside the configured bounds",
                {"attempts": self._attempts, "max_attempts": self.budget.max_attempts, "max_depth": self.budget.max_depth, "dimensions": [width, height]},
            ))
        return result

    def _search_placements(
        self,
        order: list[tuple[str, str]],
        depth: int,
        placements: dict[str, Rect],
        zones: dict[str, dict[str, Any]],
        width: int,
        height: int,
        rng: random.Random,
    ) -> dict[str, Rect] | None:
        if depth >= len(order):
            return dict(placements)
        if depth >= self.budget.max_depth or self._attempts >= self.budget.max_attempts:
            return None
        parent_id, child_id = order[depth]
        parent = placements[parent_id]
        child_width, child_height = self._zone_size(zones[child_id])
        candidates = [
            Rect(parent.x + (parent.width - child_width) // 2, parent.y - child_height, child_width, child_height),
            Rect(parent.right, parent.y + (parent.height - child_height) // 2, child_width, child_height),
            Rect(parent.x + (parent.width - child_width) // 2, parent.bottom, child_width, child_height),
            Rect(parent.x - child_width, parent.y + (parent.height - child_height) // 2, child_width, child_height),
        ]
        rng.shuffle(candidates)
        for candidate in candidates:
            self._attempts += 1
            if self._attempts > self.budget.max_attempts:
                return None
            if not candidate.in_bounds(width, height) or any(candidate.overlaps(existing) for existing in placements.values()):
                continue
            placements[child_id] = candidate
            result = self._search_placements(order, depth + 1, placements, zones, width, height, rng)
            if result is not None:
                return result
            del placements[child_id]
        return None

    def _place_modules(
        self,
        archetype: dict[str, Any],
        modules: dict[str, dict[str, Any]],
        zones: list[dict[str, Any]],
        placements: dict[str, Rect],
    ) -> list[dict[str, Any]]:
        zone_by_role = {zone["role"]: zone for zone in zones}
        result = []
        for requirement in archetype.get("modules_required", []):
            count = int(requirement["min_count"])
            if count == 0:
                continue
            role = requirement["zone_role"]
            module_ref = requirement["module_ref"]
            if role not in zone_by_role:
                raise AssemblyError(Diagnostic("module_parent_zone_missing", "required module has no selected parent zone", {"module_ref": module_ref, "zone_role": role}))
            if module_ref not in modules:
                raise AssemblyError(Diagnostic("module_definition_missing", "required module definition was not supplied", {"module_ref": module_ref}))
            zone = zone_by_role[role]
            rect = placements[zone["zone_id"]]
            module = modules[module_ref]
            footprint = module["footprint"]
            module_width, module_height = int(footprint["width"]), int(footprint["height"])
            clearance = int(module.get("clearance", {}).get("min_adjacent_walkable", 0))
            if module_width > rect.width or module_height > rect.height or clearance > (2 * module_width + 2 * module_height):
                raise AssemblyError(Diagnostic("module_clearance_unsatisfied", "module footprint or clearance does not fit its parent zone", {"module_ref": module_ref, "zone_id": zone["zone_id"], "zone": rect.to_area(), "footprint": footprint, "clearance": clearance}))
            for index in range(count):
                module_rect = Rect(rect.x + index * module_width, rect.y, module_width, module_height)
                if not module_rect.in_bounds(rect.right, rect.bottom):
                    raise AssemblyError(Diagnostic("module_clearance_unsatisfied", "module instances do not fit without overlap", {"module_ref": module_ref, "zone_id": zone["zone_id"], "instance": index + 1}))
                result.append({
                    "module_id": f"{module_ref.lower()}-{index + 1}",
                    "module_ref": module_ref,
                    "zone_id": zone["zone_id"],
                    "semantic_tag": module["semantic_tag"],
                    "rect": module_rect,
                    "blocks_movement": bool(module["blocks_movement"]),
                    "clearance": clearance,
                })
        return result

    @staticmethod
    def _validate_reachability(graph: dict[str, Any], zones: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
        selected = {zone["zone_id"] for zone in zones}
        adjacency = {zone_id: set() for zone_id in selected}
        for edge in edges:
            adjacency[edge["from_zone"]].add(edge["to_zone"])
            adjacency[edge["to_zone"]].add(edge["from_zone"])
        entry = graph["reachability"]["entry_zone"]
        reached = {entry}
        queue = deque([entry])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current] - reached:
                reached.add(neighbor)
                queue.append(neighbor)
        missing = set(graph["reachability"]["must_reach"]) - reached
        if missing:
            raise AssemblyError(Diagnostic("required_route_unreachable", "required gameplay zones are unreachable", {"entry": entry, "missing": sorted(missing)}))

    @staticmethod
    def _choose_rotation(family: dict[str, Any], seed: int) -> int:
        return [0, 90, 180, 270][seed % 4] if family.get("allow_rotation", False) else 0

    @staticmethod
    def _transform_rect(rect: Rect, width: int, height: int, rotation: int, reflected: bool) -> tuple[Rect, int, int]:
        value = rect
        current_width, current_height = width, height
        if reflected:
            value = Rect(current_width - value.right, value.y, value.width, value.height)
        for _ in range((rotation % 360) // 90):
            value = Rect(current_height - value.bottom, value.x, value.height, value.width)
            current_width, current_height = current_height, current_width
        return value, current_width, current_height

    def _transform(
        self,
        placements: dict[str, Rect],
        modules: list[dict[str, Any]],
        width: int,
        height: int,
        rotation: int,
        reflected: bool,
    ) -> tuple[dict[str, Rect], list[dict[str, Any]], int, int]:
        transformed = {}
        final_width, final_height = width, height
        for zone_id, rect in placements.items():
            transformed[zone_id], final_width, final_height = self._transform_rect(rect, width, height, rotation, reflected)
        transformed_modules = []
        for module in modules:
            item = dict(module)
            item["rect"], _, _ = self._transform_rect(module["rect"], width, height, rotation, reflected)
            transformed_modules.append(item)
        return transformed, transformed_modules, final_width, final_height

    def _build_map_plan(
        self,
        intent: dict[str, Any],
        graph: dict[str, Any],
        archetype: dict[str, Any],
        family: dict[str, Any],
        variant_id: str,
        zones: dict[str, Rect],
        modules: list[dict[str, Any]],
        edges: list[dict[str, Any]],
        width: int,
        height: int,
        manifest_id: str,
        root_seed: int,
        rotation: int,
        reflected: bool,
    ) -> MapPlan:
        graph_zones = {zone["zone_id"]: zone for zone in graph["zones"]}
        terrain = [
            {
                "terrain_id": f"ZONE-{zone_id}",
                "terrain_type": graph_zones[zone_id]["role"],
                "area": rect.to_area(),
                "movement": "walkable",
            }
            for zone_id, rect in sorted(zones.items())
        ]
        obstacles = [
            {
                "obstacle_id": module["module_id"],
                "name": module["semantic_tag"],
                "area": module["rect"].to_area(),
                "blocking": module["blocks_movement"],
                "module_ref": module["module_ref"],
                "parent_zone": module["zone_id"],
                "clearance": module["clearance"],
            }
            for module in modules
        ]
        transfer_points = []
        event_anchors = []
        for zone_id, rect in zones.items():
            beats = graph_zones[zone_id].get("beats", [])
            point = {"shape": "point", "x": rect.x + rect.width // 2, "y": rect.y + rect.height // 2}
            for beat in beats:
                if "transfer" in beat:
                    transfer_points.append({"transfer_id": f"GEN-{beat}-{zone_id}", "anchor": point, "placement_intent": beat})
                elif "service" in beat or "event" in beat or "treasure" in beat:
                    event_anchors.append({"local_anchor_id": f"GEN-{beat}-{zone_id}", "anchor": point, "trigger_intent": beat})
        return MapPlan.from_dict({
            "schema_version": "0.1",
            "blueprint_id": f"BP-GEN-{intent['map_intent_id']}",
            "atlas_screen_id": intent.get("atlas_screen_id"),
            "title": f"{intent['title']} - generated structural candidate",
            "source_documents": list(intent["source_documents"]),
            "map_intent": {
                "purpose": intent["purpose"],
                "layout_mode": "procedural",
                "generation_seed": root_seed,
                "critical_path_role": intent.get("critical_path_role", "unspecified"),
                "archetype_ref": f"{archetype['archetype_id']}@{archetype['version']}",
                "layout_family_ref": f"{family['layout_family_id']}@{family['version']}",
                "variant_id": variant_id,
                "rotation": rotation,
                "reflected": reflected,
            },
            "dimensions": {"width": width, "height": height, "unit": "tile", "coordinate_system": "atlas_tile", "origin": "top_left"},
            "terrain": terrain,
            "traversable_areas": [
                {"area_id": f"EDGE-{index + 1}", "from_zone": edge["from_zone"], "to_zone": edge["to_zone"], "connector_type": edge["connector_type"], "required": edge["required"]}
                for index, edge in enumerate(edges)
            ],
            "obstacles": obstacles,
            "transfer_points": transfer_points,
            "event_anchors": event_anchors,
            "validation": {
                "entry_zone": graph["reachability"]["entry_zone"],
                "must_reach": list(graph["reachability"]["must_reach"]),
                "assembly_attempts": self._attempts,
                "assembly_budget": {"max_attempts": self.budget.max_attempts, "max_depth": self.budget.max_depth},
            },
            "landmark_slots": self._resolve_landmark_slots(archetype, graph_zones, zones),
            "generation_manifest_ref": manifest_id,
        })

    @staticmethod
    def _resolve_landmark_slots(
        archetype: dict[str, Any],
        graph_zones: dict[str, dict[str, Any]],
        placements: dict[str, Rect],
    ) -> list[dict[str, Any]]:
        zone_by_role = {zone["role"]: zone_id for zone_id, zone in graph_zones.items() if zone_id in placements}
        resolved = []
        for slot in archetype.get("landmark_slots", []):
            zone_id = zone_by_role.get(slot["zone_role"])
            if zone_id is None:
                if slot.get("required", False):
                    raise AssemblyError(Diagnostic(
                        "required_landmark_zone_missing",
                        "a required landmark slot has no selected parent zone",
                        {"zone_role": slot["zone_role"], "landmark_tag": slot["landmark_tag"]},
                    ))
                continue
            rect = placements[zone_id]
            resolved.append({
                "landmark_tag": slot["landmark_tag"],
                "zone_role": slot["zone_role"],
                "zone_id": zone_id,
                "required": bool(slot.get("required", False)),
                "dominant": bool(slot.get("dominant", False)),
                "anchor": {"shape": "point", "x": rect.x + rect.width // 2, "y": rect.y + rect.height // 2},
            })
        return resolved
