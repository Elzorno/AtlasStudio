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

    def audit_generated_candidate(
        self,
        *,
        plan: dict[str, Any],
        map_json: dict[str, Any],
        manifest: dict[str, Any],
        diagnostics: dict[str, Any],
        palette: dict[str, Any],
    ) -> dict[str, Any]:
        """WO-0062 hard gates plus advisory classic-JRPG evidence.

        Hard failures cannot be offset by the advisory score. Human review is
        intentionally read from the manifest and never inferred from scores.
        """
        hard: list[Finding] = []
        width, height = int(map_json.get("width", 0)), int(map_json.get("height", 0))
        data = map_json.get("data", [])
        events = [event for event in map_json.get("events", []) if event]
        route = diagnostics.get("route_audit", {})
        if route.get("result") != "pass":
            hard.append(Finding("reachability_failed", "error", "Required route audit did not pass.", route))
        if route.get("interaction_ring_failures"):
            hard.append(Finding("interaction_ring_failed", "error", "One or more interaction rings are unreachable.", route))
        interior_capacity = max(0, (width - 2) * (height - 2))
        if int(route.get("reachable_cells", 0)) < max(1, interior_capacity // 2):
            hard.append(Finding("isolated_pockets", "error", "Reachable interior is below the minimum connected fraction.", {"reachable": route.get("reachable_cells"), "interior_capacity": interior_capacity}))
        zone_ids = {item.get("terrain_id", "").removeprefix("ZONE-") for item in plan.get("terrain", [])}
        bad_edges = [edge.get("area_id") for edge in plan.get("traversable_areas", []) if edge.get("from_zone") not in zone_ids or edge.get("to_zone") not in zone_ids]
        if bad_edges:
            hard.append(Finding("connector_alignment_failed", "error", "Connectors reference missing zones.", {"edges": bad_edges}))
        zone_areas = {item.get("terrain_id", "").removeprefix("ZONE-"): item.get("area", {}) for item in plan.get("terrain", [])}
        clearance_failures = []
        for obstacle in plan.get("obstacles", []):
            parent, area = zone_areas.get(obstacle.get("parent_zone")), obstacle.get("area", {})
            if not parent or not all((area.get("x", 0) >= parent.get("x", 0), area.get("y", 0) >= parent.get("y", 0), area.get("x", 0) + area.get("w", 0) <= parent.get("x", 0) + parent.get("w", 0), area.get("y", 0) + area.get("h", 0) <= parent.get("y", 0) + parent.get("h", 0))):
                clearance_failures.append(obstacle.get("obstacle_id"))
        if clearance_failures:
            hard.append(Finding("clearance_failed", "error", "Obstacle footprint escapes its parent zone.", {"obstacles": clearance_failures}))
        transfer_ids = {item.get("transfer_id") for item in plan.get("transfer_points", [])}
        event_names = {event.get("name") for event in events}
        if not transfer_ids.issubset(event_names) or manifest.get("round_trip_contract") not in {"verified", "fixture_unbound_safe"}:
            hard.append(Finding("transfer_round_trip_failed", "error", "Transfer identities or round-trip contract are incomplete.", {"expected": sorted(transfer_ids), "round_trip_contract": manifest.get("round_trip_contract")}))
        anchor_ids = {item.get("local_anchor_id") for item in plan.get("event_anchors", [])}
        if not anchor_ids.issubset(event_names):
            hard.append(Finding("event_anchor_failed", "error", "Required event anchor identity is absent.", {"missing": sorted(anchor_ids - event_names)}))
        if width < 1 or height < 1 or len(data) != width * height * 6 or int(map_json.get("tilesetId", 0)) != int(palette.get("tileset_id", -1)):
            hard.append(Finding("rpgmaker_shape_failed", "error", "Dimensions, six-layer data, or tileset reference are invalid.", {"width": width, "height": height, "data_length": len(data), "tileset_id": map_json.get("tilesetId")}))
        palette_kinds = {(binding["source_index"]["addressing"], binding["source_index"]["index"]) for binding in palette.get("bindings", [])}
        unknown_tiles = []
        for tile in set(data[: width * height * 4]):
            if not tile:
                continue
            address = ("autotile_kind", (tile - 2048) // 48) if tile >= 2048 else ("normal_tile", tile - (1536 if 1536 <= tile < 2048 else 256 if tile >= 256 else 0))
            if address not in palette_kinds:
                unknown_tiles.append(tile)
        if unknown_tiles:
            hard.append(Finding("tile_family_failed", "error", "Candidate uses tiles outside the verified palette.", {"tile_ids": sorted(unknown_tiles)}))
        required_manifest = {"schema_version", "status", "map_plan", "palette", "style_pack", "candidate_map", "render", "promotion", "ownership_state", "provenance", "round_trip_contract", "human_review"}
        missing_manifest = sorted(required_manifest - set(manifest))
        provenance_required = {"map_plan_sha256", "palette_sha256", "style_pack_sha256", "candidate_map_sha256", "render_sha256", "tilesets_sha256"}
        missing_provenance = sorted(provenance_required - set(manifest.get("provenance", {})))
        if missing_manifest or missing_provenance or manifest.get("promotion") != "not_applied":
            hard.append(Finding("manifest_incomplete", "error", "Candidate manifest is incomplete or promotion separation is absent.", {"missing_fields": missing_manifest, "missing_provenance": missing_provenance, "promotion": manifest.get("promotion")}))

        landmark = any(item.get("dominant") for item in plan.get("landmark_slots", []))
        optional_branch = any(not edge.get("required", False) for edge in plan.get("traversable_areas", []))
        occupied = sum(int(item.get("area", {}).get("w", 0)) * int(item.get("area", {}).get("h", 0)) for item in plan.get("obstacles", []))
        density = occupied / max(1, interior_capacity)
        advisory_checks = {
            # WO-0065: broadened to also recognize exterior-palette role names
            # (ground/building/dressing/threshold), which WO-0063's own
            # Outside palette uses instead of the interior vocabulary
            # (floor/wall/edge_dressing) this check originally hardcoded --
            # that mismatch was undercounting genuinely varied exterior
            # palettes. See WO-0064 finding F3 and WO-0065's report.
            "immediate_place_identity": len({binding.get("role") for binding in palette.get("bindings", []) if binding.get("role") in {"floor", "wall", "landmark", "edge_dressing", "ground", "building", "dressing", "threshold"}}) >= 3,
            "dominant_landmark": landmark,
            "route_legibility": route.get("result") == "pass" and not route.get("interaction_ring_failures"),
            "compact_meaningful_travel": width <= 30 and height <= 24 and bool(plan.get("traversable_areas")),
            "curiosity_hook": landmark or optional_branch,
            "compression_release": bool(plan.get("obstacles")) and int(route.get("reachable_cells", 0)) >= max(1, interior_capacity // 2),
            "selective_density": 0.01 <= density <= 0.35,
        }
        score = round(100 * sum(advisory_checks.values()) / len(advisory_checks), 1)
        return {
            "target": map_json.get("displayName", "generated candidate"),
            "hard_passed": not hard,
            "hard_findings": [item.to_dict() for item in hard],
            "advisory": {"score": score, "checks": advisory_checks, "evidence": {"obstacle_density": round(density, 4)}},
            "human_review": manifest.get("human_review", {"status": "pending", "decision": None}),
            "promotion": manifest.get("promotion", "not_applied"),
        }

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
