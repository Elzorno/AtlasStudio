"""Deterministic terrain planner for Atlas overworlds."""

from __future__ import annotations

import heapq
import math
from collections.abc import Iterable

from models import TerrainCell, TerrainModel, WorldSpec


LOCATION_TARGETS = {
    "ashford": (0.34, 0.68),
    "rustshore": (0.36, 0.86),
    "fogfen": (0.78, 0.56),
    "glassfield": (0.52, 0.50),
    "skyreach": (0.52, 0.18),
    "hidden_cave": (0.61, 0.20),
    "sealed_node": (0.52, 0.54),
}


class TerrainPlanner:
    """Builds an intermediate terrain model from a high-level world spec."""

    def build(self, spec: WorldSpec) -> TerrainModel:
        cells = self._initial_cells(spec)
        self._apply_hydrology(spec, cells)
        self._apply_biomes(spec, cells)
        locations = self._place_landmarks(spec, cells)
        routes = self._build_routes(spec, cells, locations)
        self._apply_routes(cells, spec.width, routes)
        return TerrainModel(
            schema_version="0.1.0",
            region_id=spec.region_id,
            map_name=spec.map_name,
            width=spec.width,
            height=spec.height,
            cells=cells,
            locations=locations,
            routes=routes,
        )

    def _initial_cells(self, spec: WorldSpec) -> list[TerrainCell]:
        cells: list[TerrainCell] = []
        width = spec.width
        height = spec.height
        for y in range(height):
            for x in range(width):
                nx = (x / (width - 1) - 0.50) / 0.46
                ny = (y / (height - 1) - 0.53) / 0.43
                angle = math.atan2(ny, nx)
                radius = math.sqrt(nx * nx + ny * ny)
                boundary = (
                    0.92
                    + 0.07 * math.sin(3 * angle + 0.35)
                    + 0.05 * math.sin(5 * angle - 0.90)
                    + 0.035 * math.sin(9 * angle + 1.10)
                )
                land = radius <= boundary
                coast_factor = max(0.0, 1.0 - radius / max(boundary, 0.1))
                north = 1.0 - y / max(1, height - 1)
                elevation = 0.12 + 0.38 * coast_factor + 0.18 * north
                elevation += 0.34 * self._gaussian(x, y, 0.52 * width, 0.18 * height, 0.16 * width)
                elevation += 0.18 * self._gaussian(x, y, 0.48 * width, 0.46 * height, 0.20 * width)
                elevation += 0.08 * math.sin((x + y * 1.7) * 0.17)
                elevation = min(1.0, max(0.0, elevation))
                if not land:
                    elevation = 0.0
                cells.append(
                    TerrainCell(
                        x=x,
                        y=y,
                        land=land,
                        elevation=elevation,
                        biome="plains" if land else "deep_water",
                        water=not land,
                        walkable=land,
                    )
                )
        return cells

    def _apply_hydrology(self, spec: WorldSpec, cells: list[TerrainCell]) -> None:
        width = spec.width
        river_paths = [
            self._meander_path(spec, (0.52, 0.20), (0.36, 0.86), wobble=0.08),
            self._meander_path(spec, (0.55, 0.35), (0.82, 0.58), wobble=0.06),
        ]
        for path in river_paths:
            for x, y in path:
                for nx, ny in self._disk(x, y, 1):
                    if 0 <= nx < spec.width and 0 <= ny < spec.height:
                        cell = cells[ny * width + nx]
                        if cell.land and cell.elevation < 0.72:
                            cell.biome = "river"
                            cell.water = True
                            cell.walkable = False
                            cell.elevation = min(cell.elevation, 0.18)

    def _apply_biomes(self, spec: WorldSpec, cells: list[TerrainCell]) -> None:
        width = spec.width
        height = spec.height
        for cell in cells:
            if not cell.land or cell.biome == "river":
                continue
            x_ratio = cell.x / max(1, width - 1)
            y_ratio = cell.y / max(1, height - 1)
            if self._near_water(spec, cells, cell.x, cell.y) and cell.elevation < 0.18:
                cell.biome = "beach"
                cell.walkable = True
            elif cell.elevation > 0.76 and self._noise(cell.x, cell.y) > -0.28:
                cell.biome = "mountain"
                cell.walkable = False
            elif cell.elevation > 0.62:
                cell.biome = "hill"
                cell.walkable = True
            elif x_ratio > 0.67 and 0.43 < y_ratio < 0.70 and cell.elevation < 0.38:
                cell.biome = "marsh"
                cell.walkable = True
            elif (
                0.18 < x_ratio < 0.48
                and 0.32 < y_ratio < 0.66
                and self._noise(cell.x, cell.y) > 0.15
            ):
                cell.biome = "forest"
                cell.walkable = True
            elif 0.42 < x_ratio < 0.62 and 0.42 < y_ratio < 0.58:
                cell.biome = "ruins_field"
                cell.walkable = True
            else:
                cell.biome = "plains"
                cell.walkable = True

    def _place_landmarks(
        self,
        spec: WorldSpec,
        cells: list[TerrainCell],
    ) -> dict[str, dict[str, object]]:
        locations: dict[str, dict[str, object]] = {}
        width = spec.width
        for key, location in spec.canonical_locations.items():
            tx, ty = LOCATION_TARGETS.get(key, (0.5, 0.5))
            x, y = self._nearest_land(spec, cells, round(tx * (spec.width - 1)), round(ty * (spec.height - 1)))
            cell = cells[y * width + x]
            cell.feature = key
            if key == "ashford":
                cell.biome = "settlement"
            elif key == "rustshore":
                cell.biome = "port"
            elif key == "fogfen":
                cell.biome = "marsh"
            elif key == "glassfield":
                cell.biome = "ruins_field"
            elif key == "skyreach":
                cell.biome = "hill"
            elif key == "hidden_cave":
                cell.biome = "cave"
            elif key == "sealed_node":
                cell.biome = "old_world_node"
            cell.walkable = True
            cell.water = False
            locations[key] = {
                "label": location.label,
                "x": x,
                "y": y,
                "placement": location.placement,
                "gate": location.gate,
            }
        return locations

    def _build_routes(
        self,
        spec: WorldSpec,
        cells: list[TerrainCell],
        locations: dict[str, dict[str, object]],
    ) -> list[list[tuple[int, int]]]:
        routes: list[list[tuple[int, int]]] = []
        for route in spec.required_routes:
            for start_key, end_key in zip(route, route[1:]):
                start = locations[start_key]
                end = locations[end_key]
                path = self._weighted_path(
                    spec,
                    cells,
                    (int(start["x"]), int(start["y"])),
                    (int(end["x"]), int(end["y"])),
                )
                if path:
                    routes.append(path)
        return routes

    def _apply_routes(
        self,
        cells: list[TerrainCell],
        width: int,
        routes: list[list[tuple[int, int]]],
    ) -> None:
        for route in routes:
            for x, y in route:
                cell = cells[y * width + x]
                if cell.land:
                    if cell.biome == "river":
                        cell.feature = "bridge"
                    elif cell.biome == "mountain":
                        cell.biome = "hill"
                        cell.feature = "mountain_pass"
                    cell.road = True
                    cell.walkable = True
        self._break_long_straight_roads(cells, width, max_run=12)

    def _weighted_path(
        self,
        spec: WorldSpec,
        cells: list[TerrainCell],
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        width = spec.width
        frontier: list[tuple[float, tuple[int, int]]] = [(0, start)]
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        cost_so_far: dict[tuple[int, int], float] = {start: 0.0}
        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break
            for nx, ny in self._neighbors4(spec, *current):
                cell = cells[ny * width + nx]
                if not cell.land:
                    continue
                step_cost = 1.0
                if cell.biome in {"hill", "forest", "marsh"}:
                    step_cost += 0.7
                if cell.biome == "river":
                    step_cost += 2.0
                if cell.biome == "mountain":
                    step_cost += 7.0
                if cell.biome == "beach":
                    step_cost += 0.3
                turn_bias = 0.12 * abs(math.sin((nx * 0.31) + (ny * 0.17)))
                new_cost = cost_so_far[current] + step_cost + turn_bias
                neighbor = (nx, ny)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self._distance(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current
        if goal not in came_from:
            return []
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def _break_long_straight_roads(
        self,
        cells: list[TerrainCell],
        width: int,
        max_run: int,
    ) -> None:
        height = len(cells) // width
        for _ in range(6):
            changed = False
            changed = self._bend_horizontal_roads(cells, width, height, max_run) or changed
            changed = self._bend_vertical_roads(cells, width, height, max_run) or changed
            if not changed:
                return

    def _bend_horizontal_roads(
        self,
        cells: list[TerrainCell],
        width: int,
        height: int,
        max_run: int,
    ) -> bool:
        for y in range(height):
            run_start: int | None = None
            for x in range(width + 1):
                is_road = x < width and cells[y * width + x].road
                if is_road and run_start is None:
                    run_start = x
                elif (not is_road or x == width) and run_start is not None:
                    run_end = x - 1
                    if run_end - run_start + 1 > max_run:
                        mid = run_start + max_run // 2
                        if self._insert_horizontal_bend(cells, width, height, mid, y):
                            return True
                    run_start = None
        return False

    def _bend_vertical_roads(
        self,
        cells: list[TerrainCell],
        width: int,
        height: int,
        max_run: int,
    ) -> bool:
        for x in range(width):
            run_start: int | None = None
            for y in range(height + 1):
                is_road = y < height and cells[y * width + x].road
                if is_road and run_start is None:
                    run_start = y
                elif (not is_road or y == height) and run_start is not None:
                    run_end = y - 1
                    if run_end - run_start + 1 > max_run:
                        mid = run_start + max_run // 2
                        if self._insert_vertical_bend(cells, width, height, x, mid):
                            return True
                    run_start = None
        return False

    def _insert_horizontal_bend(
        self,
        cells: list[TerrainCell],
        width: int,
        height: int,
        x: int,
        y: int,
    ) -> bool:
        for direction in (1, -1):
            points = ((x - 1, y + direction), (x, y + direction), (x + 1, y + direction))
            if self._can_bend(cells, width, height, points):
                cells[y * width + x].road = False
                for px, py in points:
                    self._mark_bent_road(cells[py * width + px])
                return True
        return False

    def _insert_vertical_bend(
        self,
        cells: list[TerrainCell],
        width: int,
        height: int,
        x: int,
        y: int,
    ) -> bool:
        for direction in (1, -1):
            points = ((x + direction, y - 1), (x + direction, y), (x + direction, y + 1))
            if self._can_bend(cells, width, height, points):
                cells[y * width + x].road = False
                for px, py in points:
                    self._mark_bent_road(cells[py * width + px])
                return True
        return False

    def _can_bend(
        self,
        cells: list[TerrainCell],
        width: int,
        height: int,
        points: Iterable[tuple[int, int]],
    ) -> bool:
        for x, y in points:
            if not (0 <= x < width and 0 <= y < height):
                return False
            if not cells[y * width + x].land:
                return False
        return True

    def _mark_bent_road(self, cell: TerrainCell) -> None:
        if cell.biome == "river":
            cell.feature = "bridge"
        elif cell.biome == "mountain":
            cell.biome = "hill"
            cell.feature = "mountain_pass"
        cell.road = True
        cell.walkable = True

    def _meander_path(
        self,
        spec: WorldSpec,
        start_ratio: tuple[float, float],
        end_ratio: tuple[float, float],
        wobble: float,
    ) -> list[tuple[int, int]]:
        points: list[tuple[int, int]] = []
        steps = max(spec.width, spec.height)
        for i in range(steps + 1):
            t = i / steps
            x = start_ratio[0] * (1 - t) + end_ratio[0] * t
            y = start_ratio[1] * (1 - t) + end_ratio[1] * t
            x += wobble * math.sin(t * math.tau * 2.1)
            y += wobble * 0.4 * math.sin(t * math.tau * 3.2 + 0.8)
            points.append((round(x * (spec.width - 1)), round(y * (spec.height - 1))))
        return self._dedupe(points)

    def _nearest_land(
        self,
        spec: WorldSpec,
        cells: list[TerrainCell],
        x: int,
        y: int,
    ) -> tuple[int, int]:
        best = (x, y)
        best_score = float("inf")
        for cell in cells:
            if not cell.land or cell.biome == "river":
                continue
            score = (cell.x - x) ** 2 + (cell.y - y) ** 2
            if score < best_score:
                best_score = score
                best = (cell.x, cell.y)
        return best

    def _near_water(
        self,
        spec: WorldSpec,
        cells: list[TerrainCell],
        x: int,
        y: int,
    ) -> bool:
        width = spec.width
        for nx, ny in self._disk(x, y, 2):
            if 0 <= nx < spec.width and 0 <= ny < spec.height:
                cell = cells[ny * width + nx]
                if not cell.land:
                    return True
        return False

    def _neighbors4(self, spec: WorldSpec, x: int, y: int) -> Iterable[tuple[int, int]]:
        for nx, ny in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)):
            if 0 <= nx < spec.width and 0 <= ny < spec.height:
                yield nx, ny

    def _disk(self, x: int, y: int, radius: int) -> Iterable[tuple[int, int]]:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    yield x + dx, y + dy

    def _distance(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def _gaussian(self, x: float, y: float, cx: float, cy: float, spread: float) -> float:
        return math.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / max(1.0, 2 * spread * spread)))

    def _noise(self, x: int, y: int) -> float:
        return (
            math.sin(x * 0.31 + y * 0.17)
            + 0.6 * math.sin(x * 0.13 - y * 0.29 + 1.7)
            + 0.3 * math.sin(x * 0.61 + y * 0.41)
        ) / 1.9

    def _dedupe(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        previous: tuple[int, int] | None = None
        for point in points:
            if point != previous:
                result.append(point)
                previous = point
        return result
