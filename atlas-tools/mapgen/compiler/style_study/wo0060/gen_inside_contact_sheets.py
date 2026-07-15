import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contact_sheet import contact_sheet_autotile, contact_sheet_normal

GAME = "/Users/christopherzornes/Documents/GitHub/TheLastSwordProtocol-Game"
T = f"{GAME}/img/tilesets"
O = str(Path(__file__).resolve().parent / "contact_sheets")

contact_sheet_autotile(f"{T}/Inside_A1.png", f"{O}/inside_a1_kinds.png", 0, range(0, 16), "Inside_A1 kinds")
contact_sheet_autotile(f"{T}/Inside_A2.png", f"{O}/inside_a2_kinds.png", 1, range(16, 48), "Inside_A2 kinds")
contact_sheet_autotile(f"{T}/Inside_A4.png", f"{O}/inside_a4_kinds.png", 3, range(80, 128), "Inside_A4 kinds", is_a4=True)
contact_sheet_normal(f"{T}/Inside_A5.png", f"{O}/inside_a5_tiles.png", "Inside_A5 normal tiles", max_tiles=128, set_number=4, id_base=1536)
contact_sheet_normal(f"{T}/Inside_B.png", f"{O}/inside_b_tiles.png", "Inside_B normal tiles", max_tiles=256, set_number=5, id_base=0)
contact_sheet_normal(f"{T}/Inside_C.png", f"{O}/inside_c_tiles.png", "Inside_C normal tiles", max_tiles=256, set_number=6, id_base=256)
