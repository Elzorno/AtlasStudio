#!/usr/bin/env python3
"""Render a disposable schema-first artwork candidate with approved overlays."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAPGEN = ROOT.parent
sys.path.insert(0, str(MAPGEN))

from compiler.style_study.wo0060.render_map import TW, TH, add_tile  # noqa: E402


def load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def render(example_dir: Path) -> Path:
    candidate = load(example_dir / "MapArtworkCandidate.json")
    profile_path = ROOT / "profiles" / "ashford_artwork_profile.json"
    profile = load(profile_path)
    game = ROOT.parents[3] / "TheLastSwordProtocol-Game"
    tilesets = load(game / "data" / "Tilesets.json")
    tileset = tilesets[candidate["tilesetId"]]
    images = {}
    for index, name in enumerate(tileset["tilesetNames"]):
        image_path = game / "img" / "tilesets" / f"{name}.png"
        if name and image_path.is_file():
            images[index] = Image.open(image_path).convert("RGBA")

    width, height = candidate["width"], candidate["height"]
    size = width * height
    canvas = Image.new("RGBA", (width * TW, height * TH), (0, 0, 0, 255))
    for y in range(height):
        for x in range(width):
            for z in range(4):
                tile_id = candidate["data"][z * size + y * width + x]
                add_tile(canvas, images, tile_id, x * TW, y * TH)

    for placement in candidate["_atlas"]["approved_assembly_placements"]:
        overlay_key = placement.get("preview_overlay")
        if not overlay_key:
            continue
        overlay = profile["preview_overlays"][overlay_key]
        source = Image.open((profile_path.parent / overlay["image"]).resolve()).convert("RGBA")
        crop = source.crop(tuple(overlay["source_box"]))
        canvas.alpha_composite(crop, (placement["x"] * TW, placement["y"] * TH))

    output = example_dir / "final_artwork_candidate.png"
    canvas.save(output)
    return output


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "output" / "example_map_outputs" / "EX-RURAL-VILLAGE-001"
    print(render(target))
