"""Cross-field, fail-closed validation for TileAssembly 0.1."""

from __future__ import annotations

from typing import Any


def validate_tile_assembly_semantics(instance: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    dimensions = instance.get("dimensions", {})
    width, height = dimensions.get("width"), dimensions.get("height")
    if not isinstance(width, int) or not isinstance(height, int) or width < 1 or height < 1:
        return ["dimensions must provide positive integer width and height"]

    cells = instance.get("layered_cells", [])
    coordinates: list[tuple[int, int]] = []
    for cell in cells:
        xy = (cell.get("x"), cell.get("y"))
        if not all(isinstance(v, int) for v in xy) or not (0 <= xy[0] < width and 0 <= xy[1] < height):
            errors.append(f"layered cell coordinate {xy!r} is outside dimensions")
        coordinates.append(xy)
        layers = [layer.get("layer") for layer in cell.get("layers", [])]
        if len(layers) != len(set(layers)):
            errors.append(f"layered cell {xy!r} repeats a layer")
    expected = {(x, y) for y in range(height) for x in range(width)}
    observed = set(coordinates)
    if observed != expected or len(coordinates) != width * height:
        errors.append("layered_cells must contain exactly one complete cell for every assembly coordinate")

    mask = instance.get("collision_mask", [])
    if len(mask) != height or any(not isinstance(row, list) or len(row) != width for row in mask):
        errors.append("collision_mask must be exactly dimensions.height rows by dimensions.width columns")

    for group in ("anchors", "connectors"):
        for item in instance.get(group, []):
            xy = (item.get("x"), item.get("y"))
            if not all(isinstance(v, int) for v in xy) or not (0 <= xy[0] < width and 0 <= xy[1] < height):
                errors.append(f"{group} coordinate {xy!r} is outside dimensions")

    cells_by_local_coordinate = {
        (cell.get("x"), cell.get("y")): {
            (layer.get("source_coordinate", {}).get("map_x"), layer.get("source_coordinate", {}).get("map_y"))
            for layer in cell.get("layers", [])
            if isinstance(layer, dict)
        }
        for cell in cells
        if isinstance(cell, dict)
    }
    for overlay in instance.get("event_overlays", []):
        xy = (overlay.get("x"), overlay.get("y"))
        if not all(isinstance(v, int) for v in xy) or not (0 <= xy[0] < width and 0 <= xy[1] < height):
            errors.append(f"event_overlays coordinate {xy!r} is outside dimensions")
        source_coordinate = overlay.get("source_coordinate", {})
        source_xy = (source_coordinate.get("map_x"), source_coordinate.get("map_y"))
        if source_xy not in cells_by_local_coordinate.get(xy, set()):
            errors.append(f"event overlay at {xy!r} source coordinate {source_xy!r} does not match its layered cell provenance")
        if not isinstance(overlay.get("character_name"), str) or not overlay["character_name"].strip():
            errors.append("event overlay character_name must be nonblank")

    hashes = instance.get("source", {}).get("hashes", {})
    for component in ("source", "map", "tileset"):
        record = hashes.get(component)
        if not isinstance(record, dict):
            errors.append(f"missing required {component} hash record")
        elif record.get("expected_sha256") != record.get("observed_sha256"):
            errors.append(f"{component} hash mismatch")
    image_hashes = hashes.get("tileset_images")
    if not isinstance(image_hashes, list) or not image_hashes:
        errors.append("tileset_images hash records must be nonempty")
    else:
        names = [record.get("asset_name") for record in image_hashes if isinstance(record, dict)]
        if len(names) != len(image_hashes) or any(not isinstance(name, str) or not name for name in names):
            errors.append("every tileset image hash record must have a nonempty asset_name")
        elif len(names) != len(set(names)):
            errors.append("tileset image asset_name values must be unique")
        for record in image_hashes:
            if isinstance(record, dict) and record.get("expected_sha256") != record.get("observed_sha256"):
                errors.append(f"tileset image hash mismatch: {record.get('asset_name', '<unnamed>')}")
    return errors
