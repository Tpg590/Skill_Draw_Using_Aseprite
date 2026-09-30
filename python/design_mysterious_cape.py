import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (22, 10, 30, 130),     # Ground shadow (Alpha 130)
    "#": (18, 12, 24, 255),     # Viền sẫm tối Terraria (#120c18)
    
    # Cape / Cloak - Deep Arcane Purple
    "P1": (166, 92, 216, 255),  # Wave crest bright highlight (#a65cd8)
    "P2": (108, 46, 152, 255),  # Rich royal purple midtone (#6c2e98)
    "P3": (60, 22, 92, 255),    # Wave trough / shadow purple (#3c165c)
    "P4": (34, 12, 54, 255),    # Deep crevice darkest purple (#220c36)

    # Gold Trim & Brooch
    "Y1": (255, 235, 120, 255), # Specular gold highlight (#ffeb78)
    "Y2": (224, 160, 32, 255),  # Warm gold midtone (#e0a020)
    "Y3": (138, 82, 10, 255),   # Shadow bronze gold (#8a520a)

    # Ancient Stone Pedestal & Bust
    "M1": (152, 164, 184, 255), # Stone highlight (#98a4b8)
    "M2": (94, 106, 126, 255),  # Stone midtone (#5e6a7e)
    "M3": (52, 58, 74, 255),    # Stone deep shadow (#343a4a)

    # Void & Arcane Eyes/Runes (OSL Exception)
    "K":  (10, 6, 15, 255),     # Pitch black face void under cowl (#0a060f)
    "E1": (112, 255, 255, 255), # Arcane glow cyan highlight (#70ffff)
    "E2": (38, 160, 196, 255),  # Arcane glow cyan/blue shade (#26a0c4)
}

def create_static_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Ground Shadow S at y=43..46 (firmly grounded at bottom)
    for x in range(4, 23):
        grid[44][x] = "S"
    for x in range(3, 24):
        grid[45][x] = "S"
    for x in range(6, 21):
        grid[46][x] = "S"
    for x in range(8, 19):
        grid[47][x] = "S"

    # 2. Pedestal Plinth Base (y=40..43, width x=5..21)
    # y=43: bottom row outline and shadow
    for x in range(5, 22):
        grid[43][x] = "#"
    grid[43][6] = "M3"
    grid[43][7] = "M3"
    grid[43][19] = "M3"
    grid[43][20] = "M3"

    # y=42: plinth body
    grid[42][5] = "#"
    grid[42][6] = "M1"
    grid[42][7] = "M2"
    for x in range(8, 16):
        grid[42][x] = "M2"
    grid[42][16] = "M3"
    grid[42][17] = "M2" # notch
    grid[42][18] = "M3"
    grid[42][19] = "M3"
    grid[42][20] = "M3"
    grid[42][21] = "#"

    # y=41: plinth top bevel
    grid[41][5] = "#"
    grid[41][6] = "M1"
    grid[41][7] = "M1"
    for x in range(8, 14):
        grid[41][x] = "M1" if x % 3 == 0 else "M2"
    for x in range(14, 19):
        grid[41][x] = "M2" if x % 2 == 0 else "M3"
    grid[41][19] = "M3"
    grid[41][20] = "M3"
    grid[41][21] = "#"

    # y=40: plinth step top
    grid[40][5] = "."
    grid[40][6] = "#"
    for x in range(7, 12):
        grid[40][x] = "M1"
    for x in range(12, 17):
        grid[40][x] = "M2"
    for x in range(17, 20):
        grid[40][x] = "M3"
    grid[40][20] = "#"
    grid[40][21] = "."

    # 3. Pedestal Sub-base step (y=38..39, width x=6..20)
    grid[39][6] = "#"
    grid[39][7] = "M1"
    for x in range(8, 14):
        grid[39][x] = "M2"
    for x in range(14, 20):
        grid[39][x] = "M3"
    grid[39][20] = "#"

    grid[38][6] = "."
    grid[38][7] = "#"
    for x in range(8, 12):
        grid[38][x] = "M1"
    for x in range(12, 16):
        grid[38][x] = "M2"
    for x in range(16, 19):
        grid[38][x] = "M3"
    grid[38][19] = "#"
    grid[38][20] = "."

    # 4. Pillar Shaft (y=29..37, width x=8..18, shaft indent = overhang)
    for y in range(29, 38):
        grid[y][8] = "#"
        grid[y][18] = "#"
        grid[y][9] = "M1"
        for x in range(10, 15):
            grid[y][x] = "M2"
        for x in range(15, 18):
            grid[y][x] = "M3"

    # Shadow under capital on shaft (y=29, 30)
    grid[29][9] = "M2"
    for x in range(10, 18):
        grid[29][x] = "M3"
    grid[30][15] = "M3"
    grid[30][16] = "M3"
    grid[30][17] = "M3"

    # Carved Arcane Rune on Shaft (y=32..36, x=12..14)
    # Glowing arcane rune (cyan E1, E2)
    grid[32][13] = "E1"
    grid[33][12] = "E2"
    grid[33][13] = "E1"
    grid[33][14] = "E2"
    grid[34][13] = "E1"
    grid[35][12] = "E2"
    grid[35][14] = "E2"
    grid[36][13] = "E1"
    # Rune surround carve
    grid[31][13] = "M3"
    grid[37][13] = "M3"
    grid[33][11] = "M3"
    grid[33][15] = "M3"

    # 5. Pedestal Capital (y=26..28, width x=7..19, overhangs shaft by 1px)
    # y=28: Capital underside moulding
    grid[28][7] = "#"
    grid[28][8] = "M2"
    for x in range(9, 15):
        grid[28][x] = "M3"
    for x in range(15, 19):
        grid[28][x] = "M3"
    grid[28][19] = "#"

    # y=27: Capital rim
    grid[27][7] = "#"
    grid[27][8] = "M1"
    for x in range(9, 14):
        grid[27][x] = "M2"
    for x in range(14, 19):
        grid[27][x] = "M3"
    grid[27][19] = "#"

    # y=26: Capital top surface
    grid[26][7] = "#"
    for x in range(8, 13):
        grid[26][x] = "M1"
    for x in range(13, 17):
        grid[26][x] = "M2"
    for x in range(17, 19):
        grid[26][x] = "M3"
    grid[26][19] = "#"

    # 6. Bust Plinth Base / Socle (y=24..25, x=9..17)
    grid[25][8] = "#"
    grid[25][9] = "M1"
    for x in range(10, 14):
        grid[25][x] = "M2"
    for x in range(14, 17):
        grid[25][x] = "M3"
    grid[25][17] = "#"

    grid[24][9] = "#"
    grid[24][10] = "M1"
    for x in range(11, 14):
        grid[24][x] = "M2"
    for x in range(14, 16):
        grid[24][x] = "M3"
    grid[24][16] = "#"

    # 7. Bust Torso & Mysterious Robes (y=17..23)
    # Left shoulder & arm draping (x=7..11)
    # Center chest with Brooch & Lapels (x=12..15)
    # Right shoulder & Cape Anchor (x=16..19)
    bust_rows = {
        17: (
            8,
            "##P1P2P2P3P3##" # x=8..18
        ),
        18: (
            7,
            "#Y1P1P2Y2Y1P2P3P3#." # x=7..18
        ),
        19: (
            7,
            "#Y1P1Y2E1Y1Y2P3P3##" # x=7..18, center brooch gem E1, Y1, Y2
        ),
        20: (
            7,
            "#Y2P1Y2E1Y2Y3P3P4##" # x=7..18, brooch lower
        ),
        21: (
            7,
            "#P2P2P1Y3Y2P3P3P4#" # x=7..18
        ),
        22: (
            8,
            "#P2P2P3P3P3P4P4#" # x=8..18
        ),
        23: (
            8,
            "##P3P3P3P4P4###" # x=8..18
        )
    }

    for y, (start_x, row_str) in bust_rows.items():
        # Parse multi-char tokens
        tokens = []
        i = 0
        while i < len(row_str):
            if row_str[i:i+2] in PALETTE:
                tokens.append(row_str[i:i+2])
                i += 2
            else:
                tokens.append(row_str[i])
                i += 1
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    # 8. Head & Mysterious Cowl Hood (y=7..16, x=9..17)
    hood_map = {
        7:  (12, "####"),         # Peak top outline
        8:  (11, "#P1P1##"),       # Peak
        9:  (10, "#P1P1P2P3#"),
        10: (9,  "#P1P1P2P2P3##"),
        11: (9,  "#Y1Y2Y1Y2Y3P3#"), # Golden embroidered cowl band
        12: (8,  "#P1#KKKKK#P3#"),   # Cowl edge + face void K
        13: (8,  "#P1#KE1E2#P3#"),   # Glowing arcane eyes in void!
        14: (8,  "#P2#KKKKK#P3#"),   # Deep void
        15: (9,  "#P2#KKK#P3#"),    # Lower chin shadow
        16: (9,  "##P2P3P3##"),
    }
    for y, (start_x, row_str) in hood_map.items():
        tokens = []
        i = 0
        while i < len(row_str):
            if row_str[i:i+2] in PALETTE:
                tokens.append(row_str[i:i+2])
                i += 2
            else:
                tokens.append(row_str[i])
                i += 1
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    return grid

def render_to_image(grid, filepath, scale=8):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    if scale > 1:
        img_scaled = img.resize((W * scale, H * scale), Image.NEAREST)
        img_scaled.save(filepath)
    else:
        img.save(filepath)

g = create_static_base()
render_to_image(g, "python/test_static_base.png", scale=8)
print("Saved test_static_base.png")
