import json, sys
from PIL import Image

GAME = "/Users/christopherzornes/Documents/GitHub/TheLastSwordProtocol-Game"
TW = TH = 48

FLOOR_AUTOTILE_TABLE = [
    [[2,4],[1,4],[2,3],[1,3]],[[2,0],[1,4],[2,3],[1,3]],[[2,4],[3,0],[2,3],[1,3]],[[2,0],[3,0],[2,3],[1,3]],
    [[2,4],[1,4],[2,3],[3,1]],[[2,0],[1,4],[2,3],[3,1]],[[2,4],[3,0],[2,3],[3,1]],[[2,0],[3,0],[2,3],[3,1]],
    [[2,4],[1,4],[2,1],[1,3]],[[2,0],[1,4],[2,1],[1,3]],[[2,4],[3,0],[2,1],[1,3]],[[2,0],[3,0],[2,1],[1,3]],
    [[2,4],[1,4],[2,1],[3,1]],[[2,0],[1,4],[2,1],[3,1]],[[2,4],[3,0],[2,1],[3,1]],[[2,0],[3,0],[2,1],[3,1]],
    [[0,4],[1,4],[0,3],[1,3]],[[0,4],[3,0],[0,3],[1,3]],[[0,4],[1,4],[0,3],[3,1]],[[0,4],[3,0],[0,3],[3,1]],
    [[2,2],[1,2],[2,3],[1,3]],[[2,2],[1,2],[2,3],[3,1]],[[2,2],[1,2],[2,1],[1,3]],[[2,2],[1,2],[2,1],[3,1]],
    [[2,4],[3,4],[2,3],[3,3]],[[2,4],[3,4],[2,1],[3,3]],[[2,0],[3,4],[2,3],[3,3]],[[2,0],[3,4],[2,1],[3,3]],
    [[2,4],[1,4],[2,5],[1,5]],[[2,0],[1,4],[2,5],[1,5]],[[2,4],[3,0],[2,5],[1,5]],[[2,0],[3,0],[2,5],[1,5]],
    [[0,4],[3,4],[0,3],[3,3]],[[2,2],[1,2],[2,5],[1,5]],[[0,2],[1,2],[0,3],[1,3]],[[0,2],[1,2],[0,3],[3,1]],
    [[2,2],[3,2],[2,3],[3,3]],[[2,2],[3,2],[2,1],[3,3]],[[2,4],[3,4],[2,5],[3,5]],[[2,0],[3,4],[2,5],[3,5]],
    [[0,4],[1,4],[0,5],[1,5]],[[0,4],[3,0],[0,5],[1,5]],[[0,2],[3,2],[0,3],[3,3]],[[0,2],[1,2],[0,5],[1,5]],
    [[0,4],[3,4],[0,5],[3,5]],[[2,2],[3,2],[2,5],[3,5]],[[0,2],[3,2],[0,5],[3,5]],[[0,0],[1,0],[0,1],[1,1]]
]
WATERFALL_AUTOTILE_TABLE = [
    [[2,0],[1,0],[2,1],[1,1]],[[0,0],[1,0],[0,1],[1,1]],[[2,0],[3,0],[2,1],[3,1]],[[0,0],[3,0],[0,1],[3,1]]
]
WALL_AUTOTILE_TABLE = [
    [[2,2],[1,2],[2,1],[1,1]],[[0,2],[1,2],[0,1],[1,1]],[[2,0],[1,0],[2,1],[1,1]],[[0,0],[1,0],[0,1],[1,1]],
    [[2,2],[3,2],[2,1],[3,1]],[[0,2],[3,2],[0,1],[3,1]],[[2,0],[3,0],[2,1],[3,1]],[[0,0],[3,0],[0,1],[3,1]],
    [[2,2],[1,2],[2,3],[1,3]],[[0,2],[1,2],[0,3],[1,3]],[[2,0],[1,0],[2,3],[1,3]],[[0,0],[1,0],[0,3],[1,3]],
    [[2,2],[3,2],[2,3],[3,3]],[[0,2],[3,2],[0,3],[3,3]],[[2,0],[3,0],[2,3],[3,3]],[[0,0],[3,0],[0,3],[3,3]]
]

TILE_ID_B = 0
TILE_ID_A5 = 1536
TILE_ID_A1 = 2048
TILE_ID_A2 = 2816
TILE_ID_A3 = 4352
TILE_ID_A4 = 5888
TILE_ID_MAX = 8192

def is_autotile(t): return t >= TILE_ID_A1
def get_kind(t): return (t - TILE_ID_A1) // 48
def get_shape(t): return (t - TILE_ID_A1) % 48
def is_A1(t): return TILE_ID_A1 <= t < TILE_ID_A2
def is_A2(t): return TILE_ID_A2 <= t < TILE_ID_A3
def is_A3(t): return TILE_ID_A3 <= t < TILE_ID_A4
def is_A4(t): return TILE_ID_A4 <= t < TILE_ID_MAX
def is_higher_tile(t, flags): return bool(flags[t] & 0x10) if t < len(flags) else False
def is_A5(t): return TILE_ID_A5 <= t < TILE_ID_A1
def is_visible(t): return t > 0

def load_tileset_images(tileset_names):
    imgs = {}
    for i, name in enumerate(tileset_names):
        if not name:
            continue
        path = f"{GAME}/img/tilesets/{name}.png"
        try:
            imgs[i] = Image.open(path).convert("RGBA")
        except FileNotFoundError:
            pass
    return imgs

def add_normal_tile(canvas, imgs, tile_id, dx, dy):
    if is_A5(tile_id):
        set_number = 4
    else:
        set_number = 5 + (tile_id // 256)
    sx = (((tile_id // 128) % 2) * 8 + (tile_id % 8)) * TW
    sy = ((tile_id % 256) // 8 % 16) * TH
    img = imgs.get(set_number)
    if img is None:
        return
    tile = img.crop((sx, sy, sx + TW, sy + TH))
    canvas.alpha_composite(tile, (dx, dy))

def add_autotile(canvas, imgs, tile_id, dx, dy, anim_frame=0):
    kind = get_kind(tile_id)
    shape = get_shape(tile_id)
    tx = kind % 8
    ty = kind // 8
    set_number = 0
    bx = by = 0
    table = FLOOR_AUTOTILE_TABLE
    if is_A1(tile_id):
        water_idx = [0,1,2,1][anim_frame % 4]
        set_number = 0
        if kind == 0:
            bx = water_idx * 2; by = 0
        elif kind == 1:
            bx = water_idx * 2; by = 3
        elif kind == 2:
            bx = 6; by = 0
        elif kind == 3:
            bx = 6; by = 3
        else:
            bx = (tx // 4) * 8
            by = ty * 6 + (tx // 2 % 2) * 3
            if kind % 2 == 0:
                bx += water_idx * 2
            else:
                bx += 6
                table = WATERFALL_AUTOTILE_TABLE
                by += anim_frame % 3
    elif is_A2(tile_id):
        set_number = 1
        bx = tx * 2
        by = (ty - 2) * 3
    elif is_A3(tile_id):
        set_number = 2
        bx = tx * 2
        by = (ty - 6) * 2
        table = WALL_AUTOTILE_TABLE
    elif is_A4(tile_id):
        set_number = 3
        bx = tx * 2
        by = int((ty - 10) * 2.5 + (0.5 if ty % 2 == 1 else 0))
        if ty % 2 == 1:
            table = WALL_AUTOTILE_TABLE
    else:
        return

    img = imgs.get(set_number)
    if img is None:
        return
    w1 = TW // 2
    h1 = TH // 2
    entry = table[shape]
    for i in range(4):
        qsx, qsy = entry[i]
        sx1 = (bx * 2 + qsx) * w1
        sy1 = (by * 2 + qsy) * h1
        dx1 = dx + (i % 2) * w1
        dy1 = dy + (i // 2) * h1
        tile = img.crop((sx1, sy1, sx1 + w1, sy1 + h1))
        canvas.alpha_composite(tile, (dx1, dy1))

def add_tile(canvas, imgs, tile_id, dx, dy):
    if not is_visible(tile_id):
        return
    if is_autotile(tile_id):
        add_autotile(canvas, imgs, tile_id, dx, dy)
    else:
        add_normal_tile(canvas, imgs, tile_id, dx, dy)

def render_map(map_path, tilesets_path, out_path):
    with open(map_path, encoding="utf-8") as handle:
        m = json.load(handle)
    with open(tilesets_path, encoding="utf-8") as handle:
        tsdata = json.load(handle)
    tileset = tsdata[m["tilesetId"]]
    imgs = load_tileset_images(tileset["tilesetNames"])
    w, h = m["width"], m["height"]
    data = m["data"]
    def rd(x, y, z):
        if 0 <= x < w and 0 <= y < h:
            return data[(z * h + y) * w + x] or 0
        return 0
    canvas = Image.new("RGBA", (w * TW, h * TH), (0, 0, 0, 255))
    for y in range(h):
        for x in range(w):
            dx, dy = x * TW, y * TH
            t0 = rd(x, y, 0)
            t1 = rd(x, y, 1)
            t2 = rd(x, y, 2)
            t3 = rd(x, y, 3)
            add_tile(canvas, imgs, t0, dx, dy)
            add_tile(canvas, imgs, t1, dx, dy)
            add_tile(canvas, imgs, t2, dx, dy)
            add_tile(canvas, imgs, t3, dx, dy)
    # event markers
    for ev in m.get("events", []):
        if not ev:
            continue
        if ev.get("name", "").startswith("ADAPTER-COLLISION-"):
            continue
        ex, ey = ev["x"], ev["y"]
        from PIL import ImageDraw
        d = ImageDraw.Draw(canvas)
        d.rectangle([ex*TW, ey*TH, ex*TW+TW-1, ey*TH+TH-1], outline=(255,0,255,255), width=2)
    canvas.save(out_path)
    print(f"saved {out_path} ({w}x{h} tiles, {w*TW}x{h*TH}px)")

if __name__ == "__main__":
    map_name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{map_name}-render.png"
    render_map(f"{GAME}/data/{map_name}.json", f"{GAME}/data/Tilesets.json", out)
