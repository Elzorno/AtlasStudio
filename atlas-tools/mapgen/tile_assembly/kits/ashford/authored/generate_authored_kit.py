#!/usr/bin/env python3
"""Generate human-gated Ashford assemblies from an authored MZ fixture.

This is deliberately not reference extraction. Map017 supplies verified tile
component vocabulary (compact facade, door event, well, bridge, fence context),
but every combination produced here is a new adapter-owned authored candidate.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
MAPGEN = HERE.parents[3]
sys.path.insert(0, str(MAPGEN))

from tile_assembly import (  # noqa: E402
    extract_tile_assembly,
    render_assembly,
    render_composition,
    to_contract_tile_assembly,
)

ROOT = HERE.parents[6]
GAME = ROOT / "TheLastSwordProtocol-Game"
MAP017 = GAME / "data/Map017.json"
TILESETS = GAME / "data/Tilesets.json"
TILESET_IMAGES = GAME / "img/tilesets"
CHARACTER_IMAGES = GAME / "img/characters"
SOURCE = HERE / "source/MapAshfordAuthored.json"
PREVIEWS = HERE / "previews"
CONTACT_SHEET = "previews/ashford-authored-contact-sheet.png"

MAP_WIDTH = 72
MAP_HEIGHT = 20
LAYER_COUNT = 6

DEFINITIONS: list[dict[str, Any]] = [
    {"id": "TASM-ASHFORD-ELARA-HOUSE-AUTHORED", "name": "Low broad Elara House", "origin": (1, 1), "size": (6, 5), "kind": "building", "door_x": 2, "door_y": 3, "wall_rows": 1, "role": "home"},
    {"id": "TASM-ASHFORD-SHOP-AUTHORED", "name": "Two-wall-row Ashford Shop", "origin": (9, 1), "size": (7, 6), "kind": "building", "door_x": 3, "door_y": 4, "wall_rows": 2, "role": "shop"},
    {"id": "TASM-ASHFORD-INN-AUTHORED", "name": "Two-wall-row broad Ashford Inn", "origin": (18, 1), "size": (9, 6), "kind": "building", "door_x": 4, "door_y": 4, "wall_rows": 2, "role": "inn"},
    {"id": "TASM-ASHFORD-ELDER-HOUSE-AUTHORED", "name": "Low broad Elder House", "origin": (29, 1), "size": (7, 5), "kind": "building", "door_x": 3, "door_y": 3, "wall_rows": 1, "role": "elder"},
    {"id": "TASM-ASHFORD-WELL-ROOFED-AUTHORED", "name": "Roofed stone well candidate", "origin": (38, 1), "size": (3, 3), "kind": "roofed_well"},
    {"id": "TASM-ASHFORD-BRIDGE-AUTHORED", "name": "Natural bridge reference", "origin": (43, 1), "size": (3, 4), "kind": "bridge"},
    {"id": "TASM-ASHFORD-WARM-VENT-AUTHORED", "name": "Warm vent visual proxy", "origin": (48, 1), "size": (3, 2), "kind": "warm_vent"},
    {"id": "TASM-ASHFORD-HUMMING-PANEL-AUTHORED", "name": "Humming panel visual proxy", "origin": (53, 1), "size": (2, 2), "kind": "humming_panel"},
    {"id": "TASM-ASHFORD-PATCHED-METAL-FENCE-AUTHORED", "name": "Patched-metal fence visual proxy", "origin": (57, 1), "size": (5, 1), "kind": "patched_fence"},
]

LIMITATIONS = {
    "TASM-ASHFORD-WELL-ROOFED-AUTHORED": "Outside has no verified roofed-well object; candidate combines verified roof/facade and open-well components.",
    "TASM-ASHFORD-BRIDGE-AUTHORED": "Human-corrected classification: this is a natural bridge reference and provides no maintenance-drainage evidence.",
    "TASM-ASHFORD-WARM-VENT-AUTHORED": "Outside has no verified warm-vent graphic; this is an abstract prop proxy and must not establish canon appearance.",
    "TASM-ASHFORD-HUMMING-PANEL-AUTHORED": "Outside has no verified powered-panel graphic; this is an abstract facade-detail proxy.",
    "TASM-ASHFORD-PATCHED-METAL-FENCE-AUTHORED": "Outside has no verified patched-metal fence set; this uses general-purpose boundary fragments as a silhouette proxy.",
}

FIDELITY_REVIEW = {
    "TASM-ASHFORD-WARM-VENT-AUTHORED": ("human_approved", "Approved by Chris 2026-07-15; grounded closed vent and stone context fit the ordinary agricultural-utility direction."),
    "TASM-ASHFORD-ELARA-HOUSE-AUTHORED": ("human_approved", "Building direction approved by Chris 2026-07-15 with compact one-wall-row treatment retained."),
    "TASM-ASHFORD-SHOP-AUTHORED": ("human_approved_with_revision", "Building direction approved by Chris 2026-07-15; requested two wall rows applied."),
    "TASM-ASHFORD-INN-AUTHORED": ("human_approved_with_revision", "Building direction approved by Chris 2026-07-15; requested two wall rows applied."),
    "TASM-ASHFORD-ELDER-HOUSE-AUTHORED": ("human_approved", "Building direction approved by Chris 2026-07-15 with compact one-wall-row treatment retained."),
    "TASM-ASHFORD-HUMMING-PANEL-AUTHORED": ("human_rejected", "Chris found the panel visually incorrect."),
    "TASM-ASHFORD-PATCHED-METAL-FENCE-AUTHORED": ("human_rejected", "Chris found the fence visually incorrect."),
    "TASM-ASHFORD-WELL-ROOFED-AUTHORED": ("human_rejected", "Chris did not approve the detached awning/tent-like well proxy."),
    "TASM-ASHFORD-BRIDGE-AUTHORED": ("human_corrected_bridge_reference", "Chris identified this correctly as a bridge, not drainage; it cannot satisfy the drainage requirement."),
}


def read_tile(source: dict[str, Any], x: int, y: int, layer: int) -> int:
    return int(source["data"][(layer * source["height"] + y) * source["width"] + x] or 0)


def write_tile(data: list[int], x: int, y: int, layer: int, tile_id: int) -> None:
    data[(layer * MAP_HEIGHT + y) * MAP_WIDTH + x] = tile_id


def copy_cell(source: dict[str, Any], data: list[int], sx: int, sy: int, dx: int, dy: int) -> None:
    for layer in range(4):
        write_tile(data, dx, dy, layer, read_tile(source, sx, sy, layer))


def broaden_compact_building(source: dict[str, Any], data: list[int], ox: int, oy: int, width: int, wall_rows: int) -> None:
    """Author a broad 4-row facade from verified Map017 house edge shapes.

    The wall/roof autotiles move to layer 1 over neutral grass so their
    transparent quarters cannot render as black voids in isolation.
    Unrelated source signs, tree overlaps, and neighboring context are omitted.
    """
    for local_y in range(4):
        for local_x in range(width):
            source_x = 19 if local_x == 0 else 21 if local_x == width - 1 else 20
            building_tile = read_tile(source, source_x, 11 + local_y, 0)
            write_tile(data, ox + local_x, oy + local_y, 1, building_tile)
            if local_y < 3:
                left, middle, right = ((413, 414, 415), (421, 422, 423), (429, 430, 431))[local_y]
                write_tile(data, ox + local_x, oy + local_y, 3, left if local_x == 0 else right if local_x == width - 1 else middle)
    for extra_row in range(1, wall_rows):
        target_y = oy + 3 + extra_row
        for local_x in range(width):
            source_x = 19 if local_x == 0 else 21 if local_x == width - 1 else 20
            write_tile(data, ox + local_x, target_y, 1, read_tile(source, source_x, 14, 0))


def authored_map() -> dict[str, Any]:
    reference = json.loads(MAP017.read_text(encoding="utf-8"))
    data = [0] * (MAP_WIDTH * MAP_HEIGHT * LAYER_COUNT)
    # A neutral Outside grass floor keeps authored objects readable.
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            write_tile(data, x, y, 0, 2816)

    events: list[dict[str, Any] | None] = [None]
    door_image = json.loads(json.dumps(reference["events"][13]["pages"][0]["image"]))
    event_id = 1
    for definition in DEFINITIONS:
        ox, oy = definition["origin"]
        width, height = definition["size"]
        kind = definition["kind"]
        if kind == "building":
            broaden_compact_building(reference, data, ox, oy, width, definition["wall_rows"])
            role = definition["role"]
            # Windows and role markers are deliberate authored differentiation,
            # never copied event logic or new services.
            for wx in (1, width - 2):
                if wx != definition["door_x"]:
                    write_tile(data, ox + wx, oy + definition["door_y"], 3, 97)
            if role == "shop":
                write_tile(data, ox + 1, oy + definition["door_y"], 3, 66)
                for px, tile_id in ((0, 145), (2, 188), (5, 144), (6, 145)):
                    write_tile(data, ox + px, oy + height - 1, 3, tile_id)
            elif role == "inn":
                write_tile(data, ox + 1, oy + definition["door_y"], 3, 70)
                for px, tile_id in ((0, 145), (2, 137), (6, 188), (8, 145)):
                    write_tile(data, ox + px, oy + height - 1, 3, tile_id)
            elif role == "home":
                for px, tile_id in ((0, 160), (4, 164), (5, 161)):
                    write_tile(data, ox + px, oy + 4, 3, tile_id)
            elif role == "elder":
                for px, tile_id in ((1, 137), (5, 160)):
                    write_tile(data, ox + px, oy + 4, 3, tile_id)
            door = {
                "id": event_id,
                "name": f"AUTHORED-DOOR-{definition['id']}",
                "note": "<visual-fixture-only><no-gameplay-transfer>",
                "pages": [{
                    "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A", "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1, "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
                    "directionFix": True,
                    "image": door_image,
                    "list": [{"code": 0, "indent": 0, "parameters": []}],
                    "moveFrequency": 3,
                    "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
                    "moveSpeed": 3,
                    "moveType": 0,
                    "priorityType": 1,
                    "stepAnime": False,
                    "through": False,
                    "trigger": 0,
                    "walkAnime": False,
                }],
                "x": ox + definition["door_x"],
                "y": oy + definition["door_y"],
            }
            events.append(door)
            definition["event_id"] = event_id
            event_id += 1
        elif kind == "roofed_well":
            # Full three-part canopy, posts, and verified well component.
            for lx, ly, tile_id in ((0, 0, 5), (1, 0, 6), (2, 0, 7), (0, 1, 88), (2, 1, 89), (1, 2, 139)):
                write_tile(data, ox + lx, oy + ly, 3, tile_id)
        elif kind == "bridge":
            for ly in range(4):
                for lx in range(width):
                    sx = 12 if lx == 0 else 14 if lx == width - 1 else 13
                    copy_cell(reference, data, sx, 17 + ly, ox + lx, oy + ly)
        elif kind == "warm_vent":
            proxy = [[0, 128, 0], [140, 140, 140]]
            for ly, row in enumerate(proxy):
                for lx, tile_id in enumerate(row):
                    write_tile(data, ox + lx, oy + ly, 3, tile_id)
        elif kind == "humming_panel":
            proxy = [[117, 118], [82, 84]]
            for ly, row in enumerate(proxy):
                for lx, tile_id in enumerate(row):
                    write_tile(data, ox + lx, oy + ly, 3, tile_id)
        elif kind == "patched_fence":
            for lx, tile_id in enumerate([188, 84, 189, 86, 190]):
                write_tile(data, ox + lx, oy, 3, tile_id)

    return {
        "autoplayBgm": False,
        "autoplayBgs": False,
        "battleback1Name": "",
        "battleback2Name": "",
        "bgm": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "bgs": {"name": "", "pan": 0, "pitch": 100, "volume": 90},
        "disableDashing": False,
        "displayName": "NON-PRODUCTION Ashford Authored Assembly Fixture",
        "encounterList": [],
        "encounterStep": 30,
        "height": MAP_HEIGHT,
        "note": "<adapter-authored-fixture><human-approval-required><not-reference-extracted>",
        "parallaxLoopX": False,
        "parallaxLoopY": False,
        "parallaxName": "",
        "parallaxShow": True,
        "parallaxSx": 0,
        "parallaxSy": 0,
        "scrollType": 0,
        "specifyBattleback": False,
        "tilesetId": 2,
        "width": MAP_WIDTH,
        "data": data,
        "events": events,
    }


def anchors(definition: dict[str, Any]) -> list[dict[str, Any]]:
    width, height = definition["size"]
    if definition["kind"] == "building":
        return [{"anchor_id": "door", "role": "entry", "position": {"x": definition["door_x"], "y": definition["door_y"]}}]
    return [{"anchor_id": "origin", "role": "placement", "position": {"x": width // 2, "y": height - 1}}]


def connectors(definition: dict[str, Any]) -> list[dict[str, Any]]:
    width, height = definition["size"]
    if definition["kind"] == "building":
        return [{"connector_id": "front-path", "type": "footpath", "position": {"x": definition["door_x"], "y": height - 1}, "orientation": "south", "width": 1}]
    if definition["kind"] == "bridge":
        return [
            {"connector_id": "north-bank", "type": "path", "position": {"x": width // 2, "y": 0}, "orientation": "north", "width": 1},
            {"connector_id": "south-bank", "type": "path", "position": {"x": width // 2, "y": height - 1}, "orientation": "south", "width": 1},
        ]
    return []


def collision(definition: dict[str, Any]) -> list[list[bool]]:
    width, height = definition["size"]
    mask = [[True for _ in range(width)] for _ in range(height)]
    if definition["kind"] == "building":
        mask[definition["door_y"]][definition["door_x"]] = False
        mask[height - 1] = [False for _ in range(width)]
    elif definition["kind"] == "bridge":
        for y in range(height):
            mask[y][width // 2] = False
    return mask


def main() -> int:
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    for stale in (
        HERE / "tasm-ashford-maintenance-drainage-authored.json",
        PREVIEWS / "tasm-ashford-maintenance-drainage-authored-isolated.png",
        PREVIEWS / "tasm-ashford-maintenance-drainage-authored-fixture.png",
    ):
        stale.unlink(missing_ok=True)
    SOURCE.write_text(json.dumps(authored_map(), separators=(",", ":")) + "\n", encoding="utf-8")
    entries = []
    thumbnails = []
    for definition in DEFINITIONS:
        ox, oy = definition["origin"]
        width, height = definition["size"]
        stem = definition["id"].lower()
        isolated = f"previews/{stem}-isolated.png"
        fixture = f"previews/{stem}-fixture.png"
        extracted = extract_tile_assembly(
            SOURCE,
            TILESETS,
            assembly_id=definition["id"],
            x=ox,
            y=oy,
            width=width,
            height=height,
            collision_mask=collision(definition),
            anchors=anchors(definition),
            connectors=connectors(definition),
            source_event_ids=[definition["event_id"]] if "event_id" in definition else [],
            tileset_image_dir=TILESET_IMAGES,
            character_image_dir=CHARACTER_IMAGES,
        )
        render_assembly(extracted, HERE / isolated)
        render_composition(
            [{"assembly": extracted, "x": 1, "y": 1}, {"assembly": extracted, "x": width + 3, "y": 1}],
            HERE / fixture,
            width=width * 2 + 4,
            height=height + 2,
        )
        contract = to_contract_tile_assembly(
            extracted,
            name=definition["name"],
            preview_refs=[isolated, fixture, CONTACT_SHEET],
            owner_repo="AtlasStudio",
            serialization_owner="AtlasStudio",
        )
        contract["source"]["map_ref"] = "AtlasStudio/atlas-tools/mapgen/tile_assembly/kits/ashford/authored/source/MapAshfordAuthored.json"
        contract["source"]["tileset_ref"] = "TheLastSwordProtocol-Game/data/Tilesets.json#tilesetId=2"
        contract_path = HERE / f"{stem}.json"
        contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
        fidelity_state, fidelity_reason = FIDELITY_REVIEW[definition["id"]]
        approved = fidelity_state in {"human_approved", "human_approved_with_revision"}
        entries.append({
            "tile_assembly_id": definition["id"],
            "file": contract_path.name,
            "authorship": "adapter_authored_candidate",
            "reference_extracted": False,
            "review_state": fidelity_state,
            "enabled": approved,
            "downstream_generation_allowed": approved,
            "fidelity_review_state": fidelity_state,
            "fidelity_review_reason": fidelity_reason,
            "source_region": {"x": ox, "y": oy, "width": width, "height": height},
            "preview_refs": [isolated, fixture, CONTACT_SHEET],
            "asset_vocabulary_limitation": LIMITATIONS.get(definition["id"]),
        })
        image = Image.open(HERE / isolated).convert("RGBA")
        image.thumbnail((320, 192))
        thumbnails.append((definition["id"], image.copy()))

    columns, cell_w, cell_h = 3, 360, 240
    rows = (len(thumbnails) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), (245, 242, 232, 255))
    draw = ImageDraw.Draw(sheet)
    for i, (label, image) in enumerate(thumbnails):
        cx, cy = i % columns, i // columns
        x, y = cx * cell_w, cy * cell_h
        sheet.alpha_composite(image, (x + (cell_w - image.width) // 2, y + 38))
        draw.text((x + 8, y + 8), label, fill=(30, 30, 30, 255))
    sheet.save(HERE / CONTACT_SHEET)

    index = {
        "schema_version": "0.1",
        "kit_id": "TASM-KIT-ASHFORD-AUTHORED-001",
        "source_fixture": "source/MapAshfordAuthored.json",
        "source_fixture_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "tileset_id": 2,
        "tileset_name": "Outside",
        "authorship": "adapter_authored_candidate",
        "reference_extracted": False,
        "approval_state": "partial_human_approval",
        "enabled": False,
        "assemblies": entries,
    }
    (HERE / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
