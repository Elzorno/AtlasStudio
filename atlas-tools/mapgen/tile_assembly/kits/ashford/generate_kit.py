#!/usr/bin/env python3
"""Generate the WO-0070 Ashford reference kit from accepted Map017 regions.

The source map and database are read-only. Outputs are adapter-owned evidence:
contract instances plus isolated and two-placement fixture previews.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from tile_assembly import (
    extract_tile_assembly,
    render_assembly,
    render_composition,
    to_contract_tile_assembly,
)


ROOT = Path(__file__).resolve().parents[5]
GAME = ROOT.parent / "TheLastSwordProtocol-Game"
MAP = GAME / "data/Map017.json"
TILESETS = GAME / "data/Tilesets.json"
TILESET_IMAGES = GAME / "img/tilesets"
CHARACTER_IMAGES = GAME / "img/characters"
OUT = Path(__file__).resolve().parent
PREVIEWS = OUT / "previews"
CONTACT_SHEET_REL = "previews/ashford-kit-contact-sheet.png"


DEFINITIONS: list[dict[str, Any]] = [
    {"id": "TASM-ASHFORD-TREE-BROADLEAF-01", "name": "Complete broadleaf tree", "rect": (8, 3, 2, 2), "anchors": [("origin", "placement", 0, 1)]},
    {"id": "TASM-ASHFORD-COTTAGE-LOW-A", "name": "Low cottage A with complete door", "rect": (1, 18, 3, 5), "events": [17], "anchors": [("door", "entry", 1, 4)], "connectors": [("front-path", "footpath", 1, 4, "south", 1)]},
    {"id": "TASM-ASHFORD-COTTAGE-LOW-B", "name": "Low cottage B with complete door", "rect": (5, 18, 3, 5), "events": [18], "anchors": [("door", "entry", 1, 4)], "connectors": [("front-path", "footpath", 1, 4, "south", 1)]},
    {"id": "TASM-ASHFORD-HOUSE-COMPACT-01", "name": "Compact timber house with complete door", "rect": (19, 11, 3, 4), "events": [13], "anchors": [("door", "entry", 1, 3)], "connectors": [("front-path", "footpath", 1, 3, "south", 1)]},
    {"id": "TASM-ASHFORD-SHOP-TAVERN-FRONTAGE", "name": "Broad paired-service frontage", "rect": (6, 4, 7, 5), "events": [14, 15], "anchors": [("shop-door", "entry", 1, 4), ("service-door", "entry", 4, 4)], "connectors": [("shop-path", "footpath", 1, 4, "south", 1), ("service-path", "footpath", 4, 4, "south", 1)]},
    {"id": "TASM-ASHFORD-INN-BROAD-01", "name": "Broad Inn exterior and frontage", "rect": (22, 17, 7, 7), "events": [12], "anchors": [("door", "entry", 1, 5), ("sign", "role_marker", 1, 4)], "connectors": [("front-path", "footpath", 1, 6, "south", 1)]},
    {"id": "TASM-ASHFORD-FARM-FENCE-CLUSTER", "name": "Farm plot and fence cluster", "rect": (2, 10, 7, 7), "anchors": [("cluster-origin", "placement", 0, 0)]},
    {"id": "TASM-ASHFORD-WELL-OPEN-CONTEXT", "name": "Open well and plaza context", "rect": (9, 21, 3, 3), "anchors": [("well", "landmark", 1, 1)]},
    {"id": "TASM-ASHFORD-BRIDGE-BANKS-REFERENCE", "name": "Bridge and banks composition reference", "rect": (12, 17, 3, 4), "anchors": [("bridge", "crossing", 1, 2)], "connectors": [("north-bank", "path", 1, 0, "north", 1), ("south-bank", "path", 1, 3, "south", 1)]},
    {"id": "TASM-ASHFORD-SHOP-PROP-CLUSTER", "name": "Shop frontage functional prop cluster", "rect": (5, 7, 8, 3), "events": [14, 15], "anchors": [("shop-door", "entry", 2, 1), ("service-door", "entry", 5, 1)], "connectors": [("shop-path", "footpath", 2, 2, "south", 1), ("service-path", "footpath", 5, 2, "south", 1)]},
    {"id": "TASM-ASHFORD-INN-PROP-CLUSTER", "name": "Inn hospitality frontage cluster", "rect": (21, 20, 8, 4), "events": [12], "anchors": [("door", "entry", 2, 2), ("sign", "role_marker", 2, 1)], "connectors": [("front-path", "footpath", 2, 3, "south", 1)]},
    {"id": "TASM-ASHFORD-WINDOW-01", "name": "Complete exterior window component", "rect": (2, 21, 1, 1), "anchors": [("origin", "wall_attachment", 0, 0)]},
    {"id": "TASM-ASHFORD-SIGN-SHOP-01", "name": "Complete Shop sign component", "rect": (7, 7, 1, 1), "anchors": [("origin", "wall_attachment", 0, 0)]},
]

CLASSIFICATION: dict[str, tuple[str, str]] = {
    "TASM-ASHFORD-TREE-BROADLEAF-01": ("verified_reusable", "Complete object-specific 2x2 tree signature verified."),
    "TASM-ASHFORD-WINDOW-01": ("verified_reusable", "Complete atomic window component verified."),
    "TASM-ASHFORD-SIGN-SHOP-01": ("verified_reusable", "Complete atomic Shop sign component verified."),
    "TASM-ASHFORD-COTTAGE-LOW-A": ("study_only", "Reference proportion and complete-door study; not the selected Ashford material family."),
    "TASM-ASHFORD-COTTAGE-LOW-B": ("study_only", "Reference variation study; not the selected Ashford material family."),
    "TASM-ASHFORD-HOUSE-COMPACT-01": ("study_only", "Compact-house and door study; role and material mapping remain unapproved."),
    "TASM-ASHFORD-FARM-FENCE-CLUSTER": ("study_only", "Functional context study; not an Ashford patched-metal fence assembly."),
    "TASM-ASHFORD-WELL-OPEN-CONTEXT": ("study_only", "Open-well plaza context only; Ashford requires a roofed well."),
    "TASM-ASHFORD-BRIDGE-BANKS-REFERENCE": ("study_only", "Natural bridge composition only; cannot establish maintenance drainage."),
    "TASM-ASHFORD-SHOP-PROP-CLUSTER": ("study_only", "Functional frontage cluster study; not a complete Shop building."),
    "TASM-ASHFORD-INN-PROP-CLUSTER": ("study_only", "Hospitality frontage cluster study; not a complete Inn building."),
    "TASM-ASHFORD-SHOP-TAVERN-FRONTAGE": ("blocked_for_ashford", "Cropped paired frontage with tree overlap and an unsupported extra service."),
    "TASM-ASHFORD-INN-BROAD-01": ("blocked_for_ashford", "Cropped mixed composition, seven rows high, and mismatched to approved Ashford silhouette/material direction."),
}


def records(items: list[tuple[Any, ...]], *, connector: bool = False) -> list[dict[str, Any]]:
    result = []
    for item in items:
        if connector:
            key, kind, x, y, facing, width = item
            result.append({"connector_id": key, "type": kind, "position": {"x": x, "y": y}, "orientation": facing, "width": width})
        else:
            key, role, x, y = item
            result.append({"anchor_id": key, "role": role, "position": {"x": x, "y": y}})
    return result


def collision_mask(x: int, y: int, width: int, height: int) -> list[list[bool]]:
    map_data = json.loads(MAP.read_text(encoding="utf-8"))
    tilesets = json.loads(TILESETS.read_text(encoding="utf-8"))
    flags = tilesets[map_data["tilesetId"]]["flags"]
    mw, mh, data = map_data["width"], map_data["height"], map_data["data"]
    mask: list[list[bool]] = []
    for local_y in range(height):
        row = []
        for local_x in range(width):
            blocked = False
            for layer in range(4):
                tile_id = data[(layer * mh + y + local_y) * mw + x + local_x] or 0
                if tile_id and tile_id < len(flags):
                    flag = flags[tile_id]
                    if not (flag & 0x10) and (flag & 0x0F) == 0x0F:
                        blocked = True
            row.append(blocked)
        mask.append(row)
    return mask


def main() -> int:
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    index: list[dict[str, Any]] = []
    for definition in DEFINITIONS:
        x, y, width, height = definition["rect"]
        stem = definition["id"].lower()
        isolated_rel = f"previews/{stem}-isolated.png"
        fixture_rel = f"previews/{stem}-fixture.png"
        extracted = extract_tile_assembly(
            MAP,
            TILESETS,
            assembly_id=definition["id"],
            x=x,
            y=y,
            width=width,
            height=height,
            layers=(0, 1, 2, 3),
            collision_mask=collision_mask(x, y, width, height),
            connectors=records(definition.get("connectors", []), connector=True),
            anchors=records(definition["anchors"]),
            source_event_ids=definition.get("events", []),
            tileset_image_dir=TILESET_IMAGES,
            character_image_dir=CHARACTER_IMAGES,
        )
        render_assembly(extracted, OUT / isolated_rel, character_image_dir=CHARACTER_IMAGES)
        render_composition(
            [{"assembly": extracted, "x": 0, "y": 1}, {"assembly": extracted, "x": width + 2, "y": 1}],
            OUT / fixture_rel,
            width=width * 2 + 2,
            height=height + 2,
            character_image_dir=CHARACTER_IMAGES,
        )
        contract = to_contract_tile_assembly(
            extracted,
            name=definition["name"],
            preview_refs=[isolated_rel, fixture_rel, CONTACT_SHEET_REL],
            owner_repo="AtlasStudio",
            adapter_ref="rpg_maker_mz@0.1",
            serialization_owner="rpgmakerLSP",
        )
        contract["source"]["map_ref"] = "TheLastSwordProtocol-Game/data/Map017.json"
        contract["source"]["tileset_ref"] = "TheLastSwordProtocol-Game/data/Tilesets.json#tilesetId=2"
        output = OUT / f"{stem}.json"
        output.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
        review_state, review_reason = CLASSIFICATION[definition["id"]]
        index.append({"tile_assembly_id": definition["id"], "file": output.name, "source_region": {"x": x, "y": y, "width": width, "height": height}, "preview_refs": [isolated_rel, fixture_rel, CONTACT_SHEET_REL], "review_state": review_state, "downstream_generation_allowed": review_state == "verified_reusable", "review_reason": review_reason})
    thumbs: list[tuple[str, Image.Image]] = []
    for definition in DEFINITIONS:
        path = PREVIEWS / f"{definition['id'].lower()}-isolated.png"
        image = Image.open(path).convert("RGBA")
        image.thumbnail((288, 192))
        thumbs.append((definition["id"], image.copy()))
    columns, cell_w, cell_h = 3, 320, 240
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), (245, 242, 232, 255))
    draw = ImageDraw.Draw(sheet)
    for index_value, (label, image) in enumerate(thumbs):
        column, row = index_value % columns, index_value // columns
        ox, oy = column * cell_w, row * cell_h
        sheet.alpha_composite(image, (ox + (cell_w - image.width) // 2, oy + 28))
        draw.text((ox + 8, oy + 8), label, fill=(35, 35, 35, 255))
    sheet.save(OUT / CONTACT_SHEET_REL)
    (OUT / "index.json").write_text(json.dumps({"schema_version": "0.1", "kit_id": "TASM-KIT-ASHFORD-001", "source": "TheLastSwordProtocol-Game/data/Map017.json", "assemblies": index}, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
