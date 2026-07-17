"""Projection from extraction records to the adapter-owned TileAssembly contract."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def _canonical_region_bytes(extracted: Mapping[str, Any]) -> bytes:
    """Return the stable byte representation pinned by ``source`` hash.

    Only the extracted rectangular tile payload and its source coordinates are
    included. Adapter metadata, previews, and reusable placement semantics do
    not change the identity of the source region.
    """

    region = extracted["source"]["region"]
    payload = {
        "dimensions": extracted["dimensions"],
        "source_origin": {"x": region["x"], "y": region["y"]},
        "layers": extracted["layers"],
        "event_overlays": extracted.get("event_overlays", []),
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def extracted_region_sha256(extracted: Mapping[str, Any]) -> str:
    """Hash the canonical extracted-region bytes used by the contract."""

    return hashlib.sha256(_canonical_region_bytes(extracted)).hexdigest()


def to_contract_tile_assembly(
    extracted: Mapping[str, Any],
    *,
    version: str = "0.1",
    name: str | None = None,
    preview_refs: Sequence[str],
    owner_repo: str,
    adapter_ref: str = "rpg_maker_mz@0.1",
    serialization_owner: str | None = None,
    variations: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Convert a rectangular extraction record into TileAssembly contract 0.1.

    Hash policy is deliberately explicit:

    * ``source`` hashes canonical bytes for only the extracted region;
    * ``map`` hashes the exact full RPG Maker map file bytes;
    * ``tileset`` hashes the canonical selected tileset entry, not the full
      ``Tilesets.json`` file (whose exact full-file hash remains in the
      extraction record for drift diagnostics);
    * ``tileset_images`` contains each non-empty image hash recorded during
      extraction.
    """

    if not preview_refs:
        raise ValueError("TileAssembly contract requires at least one preview reference")
    if not extracted.get("anchors"):
        raise ValueError("TileAssembly contract requires at least one anchor")
    if not extracted.get("source", {}).get("tileset_image_sha256"):
        raise ValueError("TileAssembly contract requires at least one tileset image hash")

    dimensions = extracted["dimensions"]
    width, height = dimensions["width"], dimensions["height"]
    source = extracted["source"]
    origin_x, origin_y = source["region"]["x"], source["region"]["y"]

    cells: list[dict[str, Any]] = []
    for y in range(height):
        for x in range(width):
            layers: list[dict[str, Any]] = []
            for layer in extracted["layers"]:
                source_layer = layer["source_layer"]
                layers.append(
                    {
                        "layer": source_layer,
                        "tile_id": layer["cells"][y][x],
                        "source_coordinate": {
                            "map_x": origin_x + x,
                            "map_y": origin_y + y,
                            "layer": source_layer,
                        },
                    }
                )
            cells.append({"x": x, "y": y, "layers": layers})

    anchors = []
    for anchor in extracted.get("anchors", []):
        position = anchor.get("position", {})
        anchors.append(
            {
                "anchor_id": anchor["anchor_id"],
                "role": anchor.get("role", "placement"),
                "x": position["x"],
                "y": position["y"],
            }
        )
    connectors = []
    for connector in extracted.get("connectors", []):
        position = connector.get("position", {})
        connectors.append(
            {
                "connector_id": connector["connector_id"],
                "type": connector.get("type", "attachment"),
                "x": position["x"],
                "y": position["y"],
                "facing": connector["orientation"],
                "width": connector.get("width", 1),
            }
        )

    region_hash = extracted_region_sha256(extracted)
    map_hash = source["map_sha256"]
    selected_tileset_hash = source["tileset_entry_sha256"]
    image_hashes = [
        {
            "asset_name": f"{asset_name}.png",
            "expected_sha256": digest,
            "observed_sha256": digest,
        }
        for asset_name, digest in sorted(source.get("tileset_image_sha256", {}).items())
    ]

    contract: dict[str, Any] = {
        "schema_version": "0.1",
        "tile_assembly_id": extracted["assembly_id"],
        "version": version,
        "dimensions": dict(dimensions),
        "layered_cells": cells,
        "anchors": anchors,
        "collision_mask": extracted["collision_mask"],
        "connectors": connectors,
        "variations": list(variations)
        if variations is not None
        else [{"variation_id": "base", "weight": 1, "operations": []}],
        "source": {
            "owner_repo": owner_repo,
            "map_ref": source["map_path"],
            "tileset_ref": f"{source['tilesets_path']}#tilesetId={source['tileset_id']}",
            "hashes": {
                "source": {"expected_sha256": region_hash, "observed_sha256": region_hash},
                "map": {"expected_sha256": map_hash, "observed_sha256": map_hash},
                "tileset": {
                    "expected_sha256": selected_tileset_hash,
                    "observed_sha256": selected_tileset_hash,
                },
                "tileset_images": image_hashes,
            },
        },
        "preview_refs": list(preview_refs),
        "event_overlays": [
            {
                "x": overlay["local_coordinate"]["x"],
                "y": overlay["local_coordinate"]["y"],
                "source_event_id": overlay["source_event_id"],
                "source_coordinate": dict(overlay["source_coordinate"]),
                "character_name": overlay["image"]["characterName"],
                "character_index": overlay["image"]["characterIndex"],
                "direction": overlay["image"]["direction"],
                "pattern": overlay["image"]["pattern"],
                "priority_type": overlay["priorityType"],
                "through": overlay["through"],
            }
            for overlay in extracted.get("event_overlays", [])
        ],
        "adapter_ownership": {
            "owner_repo": owner_repo,
            "adapter_ref": adapter_ref,
            "serialization_owner": serialization_owner or owner_repo,
        },
    }
    if name is not None:
        contract["name"] = name
    return contract
