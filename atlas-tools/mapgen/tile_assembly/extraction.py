"""Read-only extraction of rectangular regions from RPG Maker MZ maps."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rectangular_mask(
    mask: Sequence[Sequence[bool]] | None, width: int, height: int
) -> list[list[bool]]:
    if mask is None:
        return [[False for _ in range(width)] for _ in range(height)]
    return [[bool(value) for value in row] for row in mask]


def extract_tile_assembly(
    map_path: str | Path,
    tilesets_path: str | Path,
    *,
    assembly_id: str,
    x: int,
    y: int,
    width: int,
    height: int,
    layers: Iterable[int] = (0, 1, 2, 3),
    collision_mask: Sequence[Sequence[bool]] | None = None,
    connectors: Sequence[Mapping[str, Any]] = (),
    anchors: Sequence[Mapping[str, Any]] = (),
    tileset_image_dir: str | Path | None = None,
    source_event_ids: Iterable[int] | None = None,
    discover_events: bool = False,
    character_image_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Extract a region without writing to either RPG Maker source file.

    Hashes cover the exact bytes read. The selected tileset entry is also
    hashed canonically so unrelated edits elsewhere in ``Tilesets.json`` can
    be distinguished from changes to the assembly's actual tileset.
    """

    map_path = Path(map_path).resolve()
    tilesets_path = Path(tilesets_path).resolve()
    map_data = json.loads(map_path.read_text(encoding="utf-8"))
    tilesets_data = json.loads(tilesets_path.read_text(encoding="utf-8"))

    map_width = int(map_data["width"])
    map_height = int(map_data["height"])
    if width < 1 or height < 1 or x < 0 or y < 0:
        raise ValueError("extraction rectangle must have positive dimensions and non-negative origin")
    if x + width > map_width or y + height > map_height:
        raise ValueError("extraction rectangle exceeds source map bounds")

    layer_numbers = list(layers)
    available_layers = len(map_data["data"]) // (map_width * map_height)
    if not layer_numbers or len(set(layer_numbers)) != len(layer_numbers):
        raise ValueError("layers must be a non-empty sequence of unique indexes")
    if any(layer < 0 or layer >= available_layers for layer in layer_numbers):
        raise ValueError(f"source map contains {available_layers} layers")

    extracted_layers: list[dict[str, Any]] = []
    for source_layer in layer_numbers:
        cells: list[list[int]] = []
        for local_y in range(height):
            row: list[int] = []
            for local_x in range(width):
                offset = (
                    source_layer * map_width * map_height
                    + (y + local_y) * map_width
                    + x
                    + local_x
                )
                row.append(int(map_data["data"][offset] or 0))
            cells.append(row)
        extracted_layers.append({"source_layer": source_layer, "cells": cells})

    tileset_id = int(map_data["tilesetId"])
    if tileset_id < 0 or tileset_id >= len(tilesets_data) or not tilesets_data[tileset_id]:
        raise ValueError(f"tilesetId {tileset_id} is absent from Tilesets.json")
    tileset = tilesets_data[tileset_id]
    tileset_entry_bytes = json.dumps(
        tileset, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")

    image_hashes: dict[str, str] = {}
    if tileset_image_dir is not None:
        image_dir = Path(tileset_image_dir).resolve()
        for name in tileset.get("tilesetNames", []):
            if not name:
                continue
            image_path = image_dir / f"{name}.png"
            if not image_path.is_file():
                raise FileNotFoundError(image_path)
            image_hashes[name] = _sha256(image_path)

    requested_event_ids = set(source_event_ids or ())
    event_overlays: list[dict[str, Any]] = []
    found_event_ids: set[int] = set()
    for event in map_data.get("events", []):
        if not event:
            continue
        event_id = int(event["id"])
        inside = x <= event["x"] < x + width and y <= event["y"] < y + height
        selected = event_id in requested_event_ids or (discover_events and inside)
        if not selected:
            continue
        if not inside:
            raise ValueError(f"selected source event {event_id} is outside extraction region")
        pages = event.get("pages", [])
        if not pages:
            raise ValueError(f"selected source event {event_id} has no page 0")
        page = pages[0]
        image = page.get("image", {})
        character_name = image.get("characterName", "")
        if not character_name:
            if event_id in requested_event_ids:
                raise ValueError(f"selected source event {event_id} has no page-0 character graphic")
            continue
        found_event_ids.add(event_id)
        event_overlays.append(
            {
                "source_event_id": event_id,
                "local_coordinate": {"x": event["x"] - x, "y": event["y"] - y},
                "source_coordinate": {"map_x": event["x"], "map_y": event["y"]},
                "image": {
                    "characterName": character_name,
                    "characterIndex": int(image.get("characterIndex", 0)),
                    "direction": int(image.get("direction", 2)),
                    "pattern": int(image.get("pattern", 0)),
                },
                "priorityType": int(page.get("priorityType", 1)),
                "through": bool(page.get("through", False)),
            }
        )
    missing_event_ids = requested_event_ids - found_event_ids
    if missing_event_ids:
        raise ValueError(f"selected source events were not found: {sorted(missing_event_ids)}")

    return {
        "schema_version": "0.1",
        "assembly_id": assembly_id,
        "dimensions": {"width": width, "height": height},
        "layers": extracted_layers,
        "collision_mask": _rectangular_mask(collision_mask, width, height),
        "connectors": [dict(connector) for connector in connectors],
        "anchors": [dict(anchor) for anchor in anchors],
        "event_overlays": event_overlays,
        "source": {
            "adapter": "rpg_maker_mz",
            "map_path": str(map_path),
            "map_sha256": _sha256(map_path),
            "map_dimensions": {"width": map_width, "height": map_height},
            "region": {"x": x, "y": y, "width": width, "height": height},
            "tilesets_path": str(tilesets_path),
            "tilesets_sha256": _sha256(tilesets_path),
            "tileset_id": tileset_id,
            "tileset_entry_sha256": hashlib.sha256(tileset_entry_bytes).hexdigest(),
            "tileset_names": list(tileset.get("tilesetNames", [])),
            "tileset_image_dir": str(Path(tileset_image_dir).resolve()) if tileset_image_dir else None,
            "tileset_image_sha256": image_hashes,
            "character_image_dir": str(Path(character_image_dir).resolve()) if character_image_dir else None,
        },
    }
