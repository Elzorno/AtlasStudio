"""TileAssembly preview rendering using the WO-0060 RPG Maker tile primitives."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

from PIL import Image

from compiler.style_study.wo0060.render_map import TW, TH, add_tile

from .validation import validate_tile_assembly


def _load_images(assembly: Mapping[str, Any], image_dir: str | Path | None) -> dict[int, Image.Image]:
    source = assembly["source"]
    root_value = image_dir or source.get("tileset_image_dir")
    if not root_value:
        raise ValueError("tileset image directory is required for rendering")
    root = Path(root_value)
    images: dict[int, Image.Image] = {}
    for index, name in enumerate(source["tileset_names"]):
        if name:
            path = root / f"{name}.png"
            if path.is_file():
                images[index] = Image.open(path).convert("RGBA")
    return images


def _paint(
    canvas: Image.Image,
    assembly: Mapping[str, Any],
    images: Mapping[int, Image.Image],
    offset_x: int,
    offset_y: int,
) -> None:
    for layer in assembly["layers"]:
        for y, row in enumerate(layer["cells"]):
            for x, tile_id in enumerate(row):
                add_tile(canvas, images, tile_id, (offset_x + x) * TW, (offset_y + y) * TH)


def _paint_event_overlays(
    canvas: Image.Image,
    assembly: Mapping[str, Any],
    offset_x: int,
    offset_y: int,
    character_image_dir: str | Path | None,
) -> None:
    overlays = assembly.get("event_overlays", [])
    if not overlays:
        return
    root_value = character_image_dir or assembly["source"].get("character_image_dir")
    if not root_value:
        raise ValueError("event overlays require a character image directory; preview cannot omit them")
    root = Path(root_value)
    direction_row = {2: 0, 4: 1, 6: 2, 8: 3}
    for overlay in overlays:
        image_record = overlay["image"]
        name = image_record["characterName"]
        path = root / f"{name}.png"
        if not path.is_file():
            raise FileNotFoundError(f"event overlay character image is missing: {path}")
        sheet = Image.open(path).convert("RGBA")
        single_character = name.startswith("$") or name.startswith("!$")
        columns, rows = (3, 4) if single_character else (12, 8)
        frame_width, frame_height = sheet.width // columns, sheet.height // rows
        character_index = image_record["characterIndex"]
        block_x = 0 if single_character else (character_index % 4) * 3
        block_y = 0 if single_character else (character_index // 4) * 4
        frame_x = (block_x + image_record["pattern"]) * frame_width
        frame_y = (block_y + direction_row[image_record["direction"]]) * frame_height
        frame = sheet.crop((frame_x, frame_y, frame_x + frame_width, frame_y + frame_height))
        local = overlay["local_coordinate"]
        tile_center_x = (offset_x + local["x"]) * TW + TW // 2
        tile_bottom_y = (offset_y + local["y"] + 1) * TH
        canvas.alpha_composite(frame, (tile_center_x - frame_width // 2, tile_bottom_y - frame_height))


def render_assembly(
    assembly: Mapping[str, Any],
    output_path: str | Path,
    *,
    tileset_image_dir: str | Path | None = None,
    character_image_dir: str | Path | None = None,
    check_source_hashes: bool = True,
) -> Path:
    """Render one assembly against transparency and return the output path."""

    validate_tile_assembly(assembly, check_source_hashes=check_source_hashes)
    width, height = assembly["dimensions"]["width"], assembly["dimensions"]["height"]
    canvas = Image.new("RGBA", (width * TW, height * TH), (0, 0, 0, 0))
    _paint(canvas, assembly, _load_images(assembly, tileset_image_dir), 0, 0)
    _paint_event_overlays(canvas, assembly, 0, 0, character_image_dir)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return output


def render_composition(
    placements: Sequence[Mapping[str, Any]],
    output_path: str | Path,
    *,
    width: int,
    height: int,
    tileset_image_dir: str | Path | None = None,
    character_image_dir: str | Path | None = None,
    check_source_hashes: bool = True,
) -> Path:
    """Render a small fixture made from positioned TileAssemblies."""

    if width < 1 or height < 1:
        raise ValueError("composition dimensions must be positive")
    canvas = Image.new("RGBA", (width * TW, height * TH), (0, 0, 0, 0))
    for index, placement in enumerate(placements):
        assembly = placement.get("assembly")
        if not isinstance(assembly, Mapping):
            raise ValueError(f"placements[{index}].assembly is required")
        validate_tile_assembly(assembly, check_source_hashes=check_source_hashes)
        x, y = placement.get("x"), placement.get("y")
        if not isinstance(x, int) or not isinstance(y, int) or x < 0 or y < 0:
            raise ValueError(f"placements[{index}] requires non-negative integer x and y")
        assembly_width = assembly["dimensions"]["width"]
        assembly_height = assembly["dimensions"]["height"]
        if x + assembly_width > width or y + assembly_height > height:
            raise ValueError(f"placements[{index}] exceeds composition bounds")
        images = _load_images(assembly, tileset_image_dir)
        _paint(canvas, assembly, images, x, y)
        _paint_event_overlays(canvas, assembly, x, y, character_image_dir)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return output
