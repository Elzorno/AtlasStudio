#!/usr/bin/env python3
"""Build the human-gated Ashford custom B-sheet and review contact sheet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source/ashford-custom-extension-alpha-v1.png"
TILESET = HERE / "Ashford_Custom_B.png"
PREVIEW = HERE / "previews/ashford-custom-extension-review-v1.png"
SCALE_PREVIEW = HERE / "previews/ashford-custom-extension-scale-context-v2.png"
TILE = 48

ASSETS = [
    {"id": "ASH-CUSTOM-WELL-ROOFED-01", "name": "Roofed civic well", "crop": (135, 125, 505, 510), "cell": (0, 0), "size": (2, 2), "visible_size": (88, 88), "review_state": "human_approved"},
    {"id": "ASH-CUSTOM-DRAINAGE-01", "name": "Maintenance drainage outlet", "crop": (735, 120, 1065, 520), "cell": (2, 0), "size": (2, 2), "visible_size": (72, 88), "review_state": "human_approved"},
    {"id": "ASH-CUSTOM-PANEL-01", "name": "Humming utility panel", "crop": (195, 775, 435, 1045), "cell": (4, 0), "size": (1, 2), "visible_size": (44, 52), "review_state": "human_approved"},
    {"id": "ASH-CUSTOM-FENCE-01", "name": "Patched metal fence", "crop": (625, 780, 1175, 1045), "cell": (0, 4), "size": (6, 2), "visible_size": (268, 68), "review_state": "human_approved"},
]


def fit(image: Image.Image, box: tuple[int, int, int, int], size: tuple[int, int], visible_size: tuple[int, int]) -> Image.Image:
    cropped = image.crop(box)
    target = (size[0] * TILE, size[1] * TILE)
    cropped = cropped.resize(visible_size, Image.Resampling.NEAREST)
    result = Image.new("RGBA", target, (0, 0, 0, 0))
    result.alpha_composite(cropped, ((target[0] - cropped.width) // 2, target[1] - cropped.height))
    return result


def main() -> int:
    source = Image.open(SOURCE).convert("RGBA")
    sheet = Image.new("RGBA", (16 * TILE, 16 * TILE), (0, 0, 0, 0))
    rendered = []
    for asset in ASSETS:
        image = fit(source, asset["crop"], asset["size"], asset["visible_size"])
        x, y = asset["cell"]
        sheet.alpha_composite(image, (x * TILE, y * TILE))
        rendered.append((asset, image))
    sheet.save(TILESET)

    review = Image.new("RGBA", (960, 600), (245, 242, 232, 255))
    draw = ImageDraw.Draw(review)
    positions = ((20, 55), (500, 55), (80, 350), (470, 350))
    for (asset, image), (x, y) in zip(rendered, positions):
        draw.text((x, y - 28), f'{asset["id"]} - {asset["name"]}', fill=(30, 30, 30, 255))
        grass = Image.new("RGBA", image.size, (111, 173, 67, 255))
        grass.alpha_composite(image)
        review.alpha_composite(grass, (x, y))
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    review.save(PREVIEW)

    # A tile-grid scene makes scale review explicit rather than presenting each
    # object in a differently sized display cell.
    context = Image.new("RGBA", (20 * TILE, 12 * TILE), (111, 173, 67, 255))
    grid = ImageDraw.Draw(context)
    for x in range(21):
        grid.line((x * TILE, 0, x * TILE, context.height), fill=(80, 130, 55, 90))
    for y in range(13):
        grid.line((0, y * TILE, context.width, y * TILE), fill=(80, 130, 55, 90))
    authored = HERE.parent / "authored/previews"
    context.alpha_composite(Image.open(authored / "tasm-ashford-elara-house-authored-isolated.png").convert("RGBA"), (TILE, TILE))
    context.alpha_composite(Image.open(authored / "tasm-ashford-warm-vent-authored-isolated.png").convert("RGBA"), (TILE, 7 * TILE))
    placements = {0: (8, 1), 1: (12, 1), 2: (16, 2), 3: (8, 7)}
    for i, (_, image) in enumerate(rendered):
        x, y = placements[i]
        context.alpha_composite(image, (x * TILE, y * TILE))
    actor_sheet = Image.open(HERE.parents[6] / "TheLastSwordProtocol-Game/img/characters/Actor1.png").convert("RGBA")
    actor = actor_sheet.crop((48, 0, 96, 48))
    context.alpha_composite(actor, (6 * TILE, 7 * TILE))
    grid.text((TILE + 4, 6), "approved Elara House", fill=(25, 25, 25, 255))
    grid.text((TILE + 4, 7 * TILE - 18), "approved vent", fill=(25, 25, 25, 255))
    grid.text((6 * TILE, 7 * TILE - 18), "1-tile actor", fill=(25, 25, 25, 255))
    grid.text((8 * TILE, 6), "2x2 well", fill=(25, 25, 25, 255))
    grid.text((12 * TILE, 6), "2x2 drainage", fill=(25, 25, 25, 255))
    grid.text((16 * TILE, 2 * TILE - 18), "1x2 panel", fill=(25, 25, 25, 255))
    grid.text((8 * TILE, 7 * TILE - 18), "6x2 modular fence", fill=(25, 25, 25, 255))
    context.save(SCALE_PREVIEW)

    manifest = {
        "schema_version": "0.1",
        "extension_id": "ASHFORD-CUSTOM-TILESET-EXTENSION-001",
        "approval_state": "human_approved",
        "enabled": True,
        "tile_size": TILE,
        "tileset_slot": "B",
        "tileset_image": TILESET.name,
        "tileset_image_sha256": hashlib.sha256(TILESET.read_bytes()).hexdigest(),
        "source": {
            "type": "ai_generated_adapter_asset",
            "generator": "OpenAI built-in image generation",
            "source_image": str(SOURCE.relative_to(HERE)),
            "source_image_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "reference_role": "approved Ashford authored contact sheet supplied style and scale only",
        },
        "assets": [
            {
                "asset_id": asset["id"],
                "name": asset["name"],
                "tile_origin": {"x": asset["cell"][0], "y": asset["cell"][1]},
                "tile_size": {"width": asset["size"][0], "height": asset["size"][1]},
                "visible_pixel_size": {"width": asset["visible_size"][0], "height": asset["visible_size"][1]},
                "review_state": asset["review_state"],
                "enabled": asset["review_state"] == "human_approved",
                "downstream_generation_allowed": asset["review_state"] == "human_approved",
            }
            for asset in ASSETS
        ],
        "preview_refs": [str(PREVIEW.relative_to(HERE)), str(SCALE_PREVIEW.relative_to(HERE))],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
