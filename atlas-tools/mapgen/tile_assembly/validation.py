"""Structural and provenance validation for adapter-owned TileAssemblies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class TileAssemblyValidationError(ValueError):
    """Raised when a TileAssembly cannot be safely consumed."""


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _point(record: Mapping[str, Any], label: str, width: int, height: int) -> None:
    position = record.get("position")
    if not isinstance(position, Mapping):
        raise TileAssemblyValidationError(f"{label}.position must be an object")
    x, y = position.get("x"), position.get("y")
    if not isinstance(x, int) or isinstance(x, bool) or not isinstance(y, int) or isinstance(y, bool):
        raise TileAssemblyValidationError(f"{label}.position must contain integer x and y")
    if not (0 <= x < width and 0 <= y < height):
        raise TileAssemblyValidationError(f"{label}.position is outside assembly dimensions")


def validate_tile_assembly(
    assembly: Mapping[str, Any], *, check_source_hashes: bool = True
) -> None:
    """Validate dimensions, layers, collision, connectors, and hash drift."""

    dimensions = assembly.get("dimensions")
    if not isinstance(dimensions, Mapping):
        raise TileAssemblyValidationError("dimensions must be an object")
    width, height = dimensions.get("width"), dimensions.get("height")
    if (
        not isinstance(width, int)
        or isinstance(width, bool)
        or not isinstance(height, int)
        or isinstance(height, bool)
        or width < 1
        or height < 1
    ):
        raise TileAssemblyValidationError("dimensions must contain positive integer width and height")

    layers = assembly.get("layers")
    if not isinstance(layers, list) or not layers:
        raise TileAssemblyValidationError("layers must be a non-empty array")
    source_layers: set[int] = set()
    for index, layer in enumerate(layers):
        if not isinstance(layer, Mapping):
            raise TileAssemblyValidationError(f"layers[{index}] must be an object")
        source_layer = layer.get("source_layer")
        if not isinstance(source_layer, int) or isinstance(source_layer, bool) or source_layer < 0:
            raise TileAssemblyValidationError(f"layers[{index}].source_layer must be a non-negative integer")
        if source_layer in source_layers:
            raise TileAssemblyValidationError("source_layer values must be unique")
        source_layers.add(source_layer)
        cells = layer.get("cells")
        if not isinstance(cells, list) or len(cells) != height:
            raise TileAssemblyValidationError(f"layers[{index}].cells height mismatch")
        for row in cells:
            if not isinstance(row, list) or len(row) != width:
                raise TileAssemblyValidationError(f"layers[{index}].cells width mismatch")
            if any(not isinstance(tile, int) or isinstance(tile, bool) or tile < 0 for tile in row):
                raise TileAssemblyValidationError(f"layers[{index}].cells contains an invalid tile ID")

    mask = assembly.get("collision_mask")
    if not isinstance(mask, list) or len(mask) != height:
        raise TileAssemblyValidationError("collision_mask height mismatch")
    if any(
        not isinstance(row, list)
        or len(row) != width
        or any(not isinstance(value, bool) for value in row)
        for row in mask
    ):
        raise TileAssemblyValidationError("collision_mask must be a rectangular boolean grid")

    seen_connectors: set[str] = set()
    for index, connector in enumerate(assembly.get("connectors", [])):
        if not isinstance(connector, Mapping):
            raise TileAssemblyValidationError(f"connectors[{index}] must be an object")
        connector_id = connector.get("connector_id")
        if not isinstance(connector_id, str) or not connector_id:
            raise TileAssemblyValidationError(f"connectors[{index}].connector_id is required")
        if connector_id in seen_connectors:
            raise TileAssemblyValidationError(f"duplicate connector_id {connector_id}")
        seen_connectors.add(connector_id)
        _point(connector, f"connectors[{index}]", width, height)
        orientation = connector.get("orientation")
        if orientation not in {"north", "south", "east", "west", "any"}:
            raise TileAssemblyValidationError(f"connectors[{index}].orientation is invalid")
        x, y = connector["position"]["x"], connector["position"]["y"]
        if orientation == "north" and y != 0 or orientation == "south" and y != height - 1:
            raise TileAssemblyValidationError(f"connector {connector_id} is not on its declared edge")
        if orientation == "west" and x != 0 or orientation == "east" and x != width - 1:
            raise TileAssemblyValidationError(f"connector {connector_id} is not on its declared edge")

    for index, anchor in enumerate(assembly.get("anchors", [])):
        if not isinstance(anchor, Mapping) or not isinstance(anchor.get("anchor_id"), str):
            raise TileAssemblyValidationError(f"anchors[{index}].anchor_id is required")
        _point(anchor, f"anchors[{index}]", width, height)

    for index, overlay in enumerate(assembly.get("event_overlays", [])):
        if not isinstance(overlay, Mapping):
            raise TileAssemblyValidationError(f"event_overlays[{index}] must be an object")
        coordinate = overlay.get("local_coordinate")
        if not isinstance(coordinate, Mapping):
            raise TileAssemblyValidationError(f"event_overlays[{index}].local_coordinate is required")
        x, y = coordinate.get("x"), coordinate.get("y")
        if not isinstance(x, int) or not isinstance(y, int) or not (0 <= x < width and 0 <= y < height):
            raise TileAssemblyValidationError(f"event_overlays[{index}] is outside assembly dimensions")
        image = overlay.get("image")
        if not isinstance(image, Mapping) or not image.get("characterName"):
            raise TileAssemblyValidationError(f"event_overlays[{index}] requires a character graphic")
        if image.get("characterIndex") not in range(8):
            raise TileAssemblyValidationError(f"event_overlays[{index}] characterIndex is invalid")
        if image.get("direction") not in {2, 4, 6, 8} or image.get("pattern") not in range(3):
            raise TileAssemblyValidationError(f"event_overlays[{index}] frame selection is invalid")

    if not check_source_hashes:
        return
    source = assembly.get("source")
    if not isinstance(source, Mapping):
        raise TileAssemblyValidationError("source provenance is required")
    for path_key, hash_key in (
        ("map_path", "map_sha256"),
        ("tilesets_path", "tilesets_sha256"),
    ):
        path = Path(str(source.get(path_key, "")))
        if not path.is_file():
            raise TileAssemblyValidationError(f"source file is missing: {path}")
        if _hash(path) != source.get(hash_key):
            raise TileAssemblyValidationError(f"source hash drift: {path_key}")

    tilesets = json.loads(Path(source["tilesets_path"]).read_text(encoding="utf-8"))
    tileset_id = source.get("tileset_id")
    if not isinstance(tileset_id, int) or tileset_id >= len(tilesets) or not tilesets[tileset_id]:
        raise TileAssemblyValidationError("source tileset no longer exists")
    encoded = json.dumps(
        tilesets[tileset_id], sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    if hashlib.sha256(encoded).hexdigest() != source.get("tileset_entry_sha256"):
        raise TileAssemblyValidationError("source hash drift: tileset entry")

    image_dir_value = source.get("tileset_image_dir")
    for name, expected in source.get("tileset_image_sha256", {}).items():
        if not image_dir_value:
            raise TileAssemblyValidationError("tileset image hashes require tileset_image_dir")
        image_path = Path(image_dir_value) / f"{name}.png"
        if not image_path.is_file() or _hash(image_path) != expected:
            raise TileAssemblyValidationError(f"source hash drift: tileset image {name}")
