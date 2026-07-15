import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map as R

GAME = "/Users/christopherzornes/Documents/GitHub/TheLastSwordProtocol-Game"
TW = TH = 48


def contact_sheet_autotile(png_path, out_path, set_number, kinds_range, label, is_a3=False, is_a4=False):
    img = Image.open(png_path).convert("RGBA")
    imgs = {set_number: img}
    cols = 8
    rows = (len(kinds_range) + cols - 1) // cols
    cell = TW + 20
    sheet = Image.new("RGBA", (cols * cell, rows * cell + 30), (30, 30, 30, 255))
    d = ImageDraw.Draw(sheet)
    d.text((4, 4), f"{label} ({png_path.split('/')[-1]})", fill=(255, 255, 255, 255))
    for i, kind in enumerate(kinds_range):
        cx = (i % cols) * cell
        cy = 30 + (i // cols) * cell
        tile_id = R.TILE_ID_A1 + kind * 48 + 0
        R.add_autotile(sheet, imgs, tile_id, cx, cy)
        d.rectangle([cx, cy, cx + TW - 1, cy + TH - 1], outline=(255, 0, 255, 255))
        d.text((cx, cy + TH + 1), str(kind), fill=(255, 255, 0, 255))
    sheet.save(out_path)
    print("saved", out_path)


def contact_sheet_normal(png_path, out_path, label, max_tiles=256, set_number=5, id_base=0):
    img = Image.open(png_path).convert("RGBA")
    imgs = {set_number: img}
    cols = 16
    rows = (max_tiles + cols - 1) // cols
    cell = TW + 14
    sheet = Image.new("RGBA", (cols * cell, rows * cell + 30), (30, 30, 30, 255))
    d = ImageDraw.Draw(sheet)
    d.text((4, 4), f"{label} ({png_path.split('/')[-1]})", fill=(255, 255, 255, 255))
    for i in range(max_tiles):
        tid = id_base + i
        cx = (i % cols) * cell
        cy = 30 + (i // cols) * cell
        R.add_normal_tile(sheet, imgs, tid, cx, cy)
        d.rectangle([cx, cy, cx + TW - 1, cy + TH - 1], outline=(80, 80, 80, 255))
        d.text((cx, cy + TH + 1), str(i), fill=(200, 200, 0, 255))
    sheet.save(out_path)
    print("saved", out_path)
