"""Data models for the Atlas Map Compiler.

The compiler works on terrain intent first. RPG Maker tile IDs are a later
output target, not the design representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class LocationSpec:
    key: str
    label: str
    placement: str
    required: bool = True
    gate: str | None = None

    @classmethod
    def from_dict(cls, key: str, payload: dict[str, Any]) -> "LocationSpec":
        return cls(
            key=key,
            label=str(payload.get("label", key)),
            placement=str(payload["placement"]),
            required=bool(payload.get("required", True)),
            gate=payload.get("gate"),
        )

    def to_dict(self) -> dict[str, Any]:
        result = {
            "label": self.label,
            "placement": self.placement,
            "required": self.required,
        }
        if self.gate:
            result["gate"] = self.gate
        return result


@dataclass(frozen=True)
class WorldSpec:
    region_id: str
    map_name: str
    width: int
    height: int
    shape: dict[str, Any]
    canonical_locations: dict[str, LocationSpec]
    required_routes: list[list[str]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WorldSpec":
        size = payload["size"]
        locations = {
            key: LocationSpec.from_dict(key, value)
            for key, value in payload["canonical_locations"].items()
        }
        return cls(
            region_id=str(payload["region_id"]),
            map_name=str(payload["map_name"]),
            width=int(size["width"]),
            height=int(size["height"]),
            shape=dict(payload.get("shape", {})),
            canonical_locations=locations,
            required_routes=[list(route) for route in payload.get("required_routes", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "region_id": self.region_id,
            "map_name": self.map_name,
            "size": {"width": self.width, "height": self.height},
            "shape": self.shape,
            "canonical_locations": {
                key: location.to_dict()
                for key, location in self.canonical_locations.items()
            },
            "required_routes": self.required_routes,
        }


@dataclass
class TerrainCell:
    x: int
    y: int
    land: bool
    elevation: float
    biome: str
    temperature: str = "temperate"
    feature: str | None = None
    walkable: bool = True
    road: bool = False
    water: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "x": self.x,
            "y": self.y,
            "land": self.land,
            "elevation": round(self.elevation, 3),
            "biome": self.biome,
            "temperature": self.temperature,
            "feature": self.feature,
            "walkable": self.walkable,
        }
        if self.road:
            payload["road"] = True
        if self.water:
            payload["water"] = True
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TerrainCell":
        return cls(
            x=int(payload["x"]),
            y=int(payload["y"]),
            land=bool(payload["land"]),
            elevation=float(payload["elevation"]),
            biome=str(payload["biome"]),
            temperature=str(payload.get("temperature", "temperate")),
            feature=payload.get("feature"),
            walkable=bool(payload.get("walkable", True)),
            road=bool(payload.get("road", False)),
            water=bool(payload.get("water", False)),
        )


@dataclass
class TerrainModel:
    schema_version: str
    region_id: str
    map_name: str
    width: int
    height: int
    cells: list[TerrainCell]
    locations: dict[str, dict[str, Any]]
    routes: list[list[tuple[int, int]]] = field(default_factory=list)
    generator: str = "atlas-map-compiler"

    def index(self, x: int, y: int) -> int:
        return y * self.width + x

    def cell(self, x: int, y: int) -> TerrainCell:
        return self.cells[self.index(x, y)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors4(self, x: int, y: int) -> list[TerrainCell]:
        result = []
        for nx, ny in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)):
            if self.in_bounds(nx, ny):
                result.append(self.cell(nx, ny))
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generator": self.generator,
            "region_id": self.region_id,
            "map_name": self.map_name,
            "size": {"width": self.width, "height": self.height},
            "locations": self.locations,
            "routes": [
                [{"x": x, "y": y} for x, y in route]
                for route in self.routes
            ],
            "cells": [cell.to_dict() for cell in self.cells],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TerrainModel":
        size = payload["size"]
        return cls(
            schema_version=str(payload["schema_version"]),
            generator=str(payload.get("generator", "atlas-map-compiler")),
            region_id=str(payload["region_id"]),
            map_name=str(payload["map_name"]),
            width=int(size["width"]),
            height=int(size["height"]),
            locations=dict(payload.get("locations", {})),
            routes=[
                [(int(point["x"]), int(point["y"])) for point in route]
                for route in payload.get("routes", [])
            ],
            cells=[TerrainCell.from_dict(cell) for cell in payload["cells"]],
        )
