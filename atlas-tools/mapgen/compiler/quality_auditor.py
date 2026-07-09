"""Quality checks for Atlas terrain models and RPG Maker overworld maps."""

from __future__ import annotations

import json
from collections import Counter, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from models import TerrainModel, WorldSpec
from spec_parser import REQUIRED_LOCATIONS


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "evidence": self.evidence,
        }


@dataclass
class AuditResult:
    target: str
    passed: bool
    findings: list[Finding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "passed": self.passed,
            "findings": [finding.to_dict() for finding in self.findings],
        }


class QualityAuditor:
    """Audits terrain intent before any RPG Maker tile painter runs."""

    def audit_terrain_model(
        self,
        model: TerrainModel,
        spec: WorldSpec | None = None,
    ) -> AuditResult:
        findings: list[Finding] = []
        required_locations = set(spec.canonical_locations) if spec else REQUIRED_LOCATIONS

        missing = sorted(required_locations.difference(model.locations))
        if missing:
            findings.append(
                Finding(
                    code="required_locations_missing",
                    severity="error",
                    message="Required canonical locations are missing from the terrain model.",
                    evidence={"missing": missing},
                )
            )

        max_coastline_run = self._max_straight_coastline_run(model)
        if max_coastline_run > 18:
            findings.append(
                Finding(
                    code="straight_coastline",
                    severity="error",
                    message="Coastline contains an overly long straight segment.",
                    evidence={"max_run": max_coastline_run, "threshold": 18},
                )
            )

        max_road_run = self._max_straight_road_run(model)
        if max_road_run > 14:
            findings.append(
                Finding(
                    code="straight_road",
                    severity="error",
                    message="Road network contains an overly long straight segment.",
                    evidence={"max_run": max_road_run, "threshold": 14},
                )
            )

        for biome in ("forest", "mountain", "marsh"):
            rectangular = self._rectangular_components(model, biome)
            if rectangular:
                findings.append(
                    Finding(
                        code=f"rectangular_{biome}",
                        severity="error",
                        message=f"{biome} contains a large rectangular-looking block.",
                        evidence=rectangular[0],
                    )
                )

        uninterrupted = self._largest_component(model, "plains")
        if uninterrupted and uninterrupted["size"] > model.width * model.height * 0.32:
            findings.append(
                Finding(
                    code="large_uninterrupted_plains",
                    severity="warning",
                    message="Plains dominate the model without enough biome interruption.",
                    evidence=uninterrupted,
                )
            )

        floating = self._floating_landmarks(model)
        if floating:
            findings.append(
                Finding(
                    code="floating_landmarks",
                    severity="error",
                    message="Some landmarks are not integrated with nearby roads or terrain variety.",
                    evidence={"locations": floating},
                )
            )

        unreachable = self._unreachable_locations(model)
        if unreachable:
            findings.append(
                Finding(
                    code="unreachable_locations",
                    severity="error",
                    message="Required locations are unreachable from Ashford through walkable terrain.",
                    evidence={"locations": unreachable},
                )
            )

        passed = not any(finding.severity == "error" for finding in findings)
        return AuditResult(target=f"terrain:{model.region_id}", passed=passed, findings=findings)

    def audit_rpgmaker_map(self, path: Path) -> AuditResult:
        payload = json.loads(path.read_text(encoding="utf-8"))
        findings: list[Finding] = []
        width = int(payload["width"])
        height = int(payload["height"])
        tiles = payload.get("data", [])
        note = str(payload.get("note", ""))
        events = [event for event in payload.get("events", []) if event]

        if width < 64 or height < 48:
            findings.append(
                Finding(
                    code="overworld_too_small",
                    severity="error",
                    message="Production overworld candidate is below the compiler foundation's minimum review size.",
                    evidence={"width": width, "height": height, "minimum": "64x48"},
                )
            )

        if "atlas-map-compiler" not in note and "TerrainModel" not in note:
            findings.append(
                Finding(
                    code="missing_intermediate_model_provenance",
                    severity="error",
                    message="RPG Maker map does not cite an intermediate terrain model.",
                    evidence={"note": note[:240]},
                )
            )

        if "WO-0024 Home Island overworld foundation" in note:
            findings.append(
                Finding(
                    code="known_negative_example",
                    severity="error",
                    message="Map027 foundation is explicitly retained as a negative example for WO-0025.",
                    evidence={"note": note[:240]},
                )
            )

        layer_size = width * height
        layer_count = len(tiles) // max(1, layer_size)
        layer_variety = []
        for layer in range(layer_count):
            layer_tiles = tiles[layer * layer_size : (layer + 1) * layer_size]
            layer_variety.append(len(set(layer_tiles)))
        if layer_variety and max(layer_variety[:2] or layer_variety) < 10:
            findings.append(
                Finding(
                    code="low_tile_variety",
                    severity="warning",
                    message="Early visual layers have very low tile variety for an overworld candidate.",
                    evidence={"layer_variety": layer_variety[:3]},
                )
            )

        required_event_fragments = (
            "Ashford",
            "Rustshore",
            "Fogfen",
            "Glassfield",
            "Skyreach",
            "Hidden Cave",
            "Sealed Node",
        )
        event_names = " | ".join(event.get("name", "") for event in events)
        missing_events = [
            fragment for fragment in required_event_fragments
            if fragment not in event_names
        ]
        if missing_events:
            findings.append(
                Finding(
                    code="missing_location_events",
                    severity="error",
                    message="RPG Maker map is missing canonical location transfer/stub events.",
                    evidence={"missing": missing_events},
                )
            )

        passed = not any(finding.severity == "error" for finding in findings)
        return AuditResult(target=str(path), passed=passed, findings=findings)

    def _max_straight_coastline_run(self, model: TerrainModel) -> int:
        max_run = 0
        for y in range(model.height):
            run = 0
            for x in range(model.width):
                if self._is_coast(model, x, y):
                    run += 1
                    max_run = max(max_run, run)
                else:
                    run = 0
        for x in range(model.width):
            run = 0
            for y in range(model.height):
                if self._is_coast(model, x, y):
                    run += 1
                    max_run = max(max_run, run)
                else:
                    run = 0
        return max_run

    def _is_coast(self, model: TerrainModel, x: int, y: int) -> bool:
        cell = model.cell(x, y)
        if not cell.land:
            return False
        return any(not neighbor.land for neighbor in model.neighbors4(x, y))

    def _max_straight_road_run(self, model: TerrainModel) -> int:
        max_run = 0
        for y in range(model.height):
            run = 0
            for x in range(model.width):
                if model.cell(x, y).road:
                    run += 1
                    max_run = max(max_run, run)
                else:
                    run = 0
        for x in range(model.width):
            run = 0
            for y in range(model.height):
                if model.cell(x, y).road:
                    run += 1
                    max_run = max(max_run, run)
                else:
                    run = 0
        return max_run

    def _rectangular_components(self, model: TerrainModel, biome: str) -> list[dict[str, Any]]:
        result = []
        for component in self._components(model, lambda cell: cell.biome == biome):
            if component["size"] < 36:
                continue
            fill = component["size"] / max(1, component["bbox_area"])
            aspect = max(component["width"], component["height"]) / max(1, min(component["width"], component["height"]))
            if fill > 0.88 and aspect < 4.0:
                result.append({**component, "fill_ratio": round(fill, 3), "aspect": round(aspect, 3)})
        return result

    def _largest_component(self, model: TerrainModel, biome: str) -> dict[str, Any] | None:
        components = self._components(model, lambda cell: cell.biome == biome)
        return max(components, key=lambda item: item["size"], default=None)

    def _components(self, model: TerrainModel, predicate) -> list[dict[str, Any]]:
        seen: set[tuple[int, int]] = set()
        components = []
        for cell in model.cells:
            start = (cell.x, cell.y)
            if start in seen or not predicate(cell):
                continue
            queue = deque([start])
            seen.add(start)
            xs = []
            ys = []
            while queue:
                x, y = queue.popleft()
                xs.append(x)
                ys.append(y)
                for neighbor in model.neighbors4(x, y):
                    point = (neighbor.x, neighbor.y)
                    if point not in seen and predicate(neighbor):
                        seen.add(point)
                        queue.append(point)
            width = max(xs) - min(xs) + 1
            height = max(ys) - min(ys) + 1
            components.append(
                {
                    "size": len(xs),
                    "bbox": [min(xs), min(ys), max(xs), max(ys)],
                    "width": width,
                    "height": height,
                    "bbox_area": width * height,
                }
            )
        return components

    def _floating_landmarks(self, model: TerrainModel) -> list[str]:
        result = []
        for key, location in model.locations.items():
            x = int(location["x"])
            y = int(location["y"])
            nearby_biomes = Counter()
            road_nearby = False
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    nx = x + dx
                    ny = y + dy
                    if not model.in_bounds(nx, ny):
                        continue
                    cell = model.cell(nx, ny)
                    nearby_biomes[cell.biome] += 1
                    road_nearby = road_nearby or cell.road
            if key not in {"hidden_cave", "sealed_node"} and not road_nearby:
                result.append(key)
            elif len(nearby_biomes) < 2:
                result.append(key)
        return result

    def _unreachable_locations(self, model: TerrainModel) -> list[str]:
        if "ashford" not in model.locations:
            return sorted(model.locations)
        start = model.locations["ashford"]
        start_point = (int(start["x"]), int(start["y"]))
        seen = {start_point}
        queue = deque([start_point])
        while queue:
            x, y = queue.popleft()
            for neighbor in model.neighbors4(x, y):
                point = (neighbor.x, neighbor.y)
                if point in seen or not neighbor.walkable:
                    continue
                seen.add(point)
                queue.append(point)
        unreachable = []
        for key, location in model.locations.items():
            point = (int(location["x"]), int(location["y"]))
            if point not in seen:
                unreachable.append(key)
        return unreachable
