import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (44, 30, 24, 130),     # Soft ground shadow (Alpha 130)
    "#": (52, 28, 16, 255),     # Soft dark wood outline (#341c10)
    
    # Sand Dune / Mound
    "D1": (240, 200, 128, 255), # Desert sand bright highlight (#f0c880)
    "D2": (212, 155, 76, 255),  # Golden desert sand base (#d49b4c)
    "D3": (158, 104, 46, 255),  # Desert sand shadow (#9e682e)
    
    # Weathered Wooden Post
    "W1": (196, 147, 90, 255),  # Wood highlight (#c4935a)
    "W2": (140, 88, 40, 255),   # Wood grain midtone (#8c5828)
    "W3": (86, 46, 18, 255),    # Wood deep shadow/crack (#562e12)
    "M1": (216, 200, 176, 255), # Weathered iron nail/plate highlight (#d8c8b0)
    "M2": (112, 96, 84, 255),   # Weathered iron shadow (#706054)

    # Silk Scarf - Turmeric Gold Yellow with Warm Orange Trim
    "C":  (74, 24, 8, 255),     # Soft dark cloth outline (#4a1808)
    "K1": (255, 242, 117, 255), # Saffron silk crest glint (#fff275)
    "K2": (240, 184, 36, 255),  # Golden turmeric silk midtone (#f0b824)
    "K3": (184, 122, 20, 255),  # Amber turmeric silk shadow (#b87a14)
    "O1": (240, 106, 24, 255),  # Warm glowing orange trim crest (#f06a18)
    "O2": (166, 62, 12, 255),   # Terracotta orange trim shadow (#a63e0c)
}

def create_static_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Soft Elliptical Ground Shadow S (y=43..47, centered under sand mound x=3..25)
    for x in range(4, 24):
        grid[44][x] = "S"
    for x in range(3, 25):
        grid[45][x] = "S"
    for x in range(5, 23):
        grid[46][x] = "S"
    for x in range(8, 20):
        grid[47][x] = "S"

    # 2. Desert Sand Dune Mound (y=38..44, width x=4..24)
    # y=44: bottom edge of sand mound
    for x in range(4, 24):
        grid[44][x] = "#"
    for x in range(6, 12):
        grid[44][x] = "D3"
    for x in range(12, 22):
        grid[44][x] = "D3"

    # y=43: lower mound body
    grid[43][4] = "#"
    grid[43][5] = "D2"
    for x in range(6, 12):
        grid[43][x] = "D2"
    for x in range(12, 23):
        grid[43][x] = "D3"
    grid[43][23] = "#"

    # y=42: mid mound body
    grid[42][4] = "#"
    for x in range(5, 9):
        grid[42][x] = "D1"
    for x in range(9, 14):
        grid[42][x] = "D2"
    for x in range(14, 23):
        grid[42][x] = "D3"
    grid[42][23] = "#"

    # y=41: upper mound crest
    grid[41][5] = "#"
    for x in range(6, 10):
        grid[41][x] = "D1"
    for x in range(10, 15):
        grid[41][x] = "D2"
    for x in range(15, 22):
        grid[41][x] = "D3"
    grid[41][22] = "#"

    # y=40: sand mound top slope
    grid[40][6] = "#"
    for x in range(7, 11):
        grid[40][x] = "D1"
    for x in range(11, 15):
        grid[40][x] = "D2"
    for x in range(15, 20):
        grid[40][x] = "D3"
    grid[40][20] = "#"

    # y=39: top ridge of sand around post
    grid[39][7] = "#"
    grid[39][8] = "D1"
    grid[39][9] = "D1"
    for x in range(14, 18):
        grid[39][x] = "D2"
    grid[39][18] = "#"

    # 3. Weathered Wooden Post (x=10..14, y=9..39)
    # Weathered beveled top: y=9..12
    # y=9: peak of post
    grid[9][11] = "#"
    grid[9][12] = "#"
    
    # y=10: bevel
    grid[10][10] = "#"
    grid[10][11] = "W1"
    grid[10][12] = "W2"
    grid[10][13] = "#"

    # y=11: top chamfer
    grid[11][10] = "#"
    grid[11][11] = "W1"
    grid[11][12] = "W2"
    grid[11][13] = "W3"
    grid[11][14] = "#"

    # y=12: post head
    grid[12][9] = "#"
    grid[12][10] = "W1"
    grid[12][11] = "W1"
    grid[12][12] = "W2"
    grid[12][13] = "W3"
    grid[12][14] = "#"

    # Post shaft from y=13 to y=39 (under scarf down to sand)
    for y in range(13, 40):
        grid[y][10] = "#"
        grid[y][11] = "W1"
        grid[y][12] = "W2"
        grid[y][13] = "W3"
        grid[y][14] = "#"

    # Wood grain notches & cracks (Rule 3.1.6: cột dọc chuỗi 2-4 ký tự dọc, đan xen tạo sọc rãnh)
    grid[20][11] = "W2"
    grid[21][11] = "W2"
    grid[26][12] = "W3" # crack
    grid[27][12] = "W3"
    grid[33][11] = "W2"
    grid[34][11] = "W2"

    # Weathered Iron Marker Plate / Arrow nailed to post at y=23..25
    grid[23][9] = "#"
    grid[23][10] = "M1"
    grid[23][11] = "M1"
    grid[23][12] = "M2"
    grid[23][13] = "M2"
    grid[23][14] = "#"
    grid[23][15] = "#" # arrow tip pointing right

    grid[24][8] = "#"
    grid[24][9] = "M1"
    grid[24][10] = "M1"
    grid[24][11] = "M1"
    grid[24][12] = "M2"
    grid[24][13] = "M2"
    grid[24][14] = "#"
    grid[24][15] = "#"
    grid[24][16] = "#" # arrow tip

    grid[25][9] = "#"
    grid[25][10] = "M2"
    grid[25][11] = "M2"
    grid[25][12] = "M2"
    grid[25][13] = "#"
    grid[25][14] = "#"

    # 4. Silk Scarf Wrapped Around Top of Post (y=13..17, x=9..15)
    # Knot and wrap encircling post with golden turmeric cloth & warm orange trim
    # y=13: Upper wrap behind/around post
    grid[13][9] = "C"
    grid[13][10] = "O1"
    grid[13][11] = "K1"
    grid[13][12] = "K2"
    grid[13][13] = "O2"
    grid[13][14] = "C"

    # y=14: Main wrap band across post
    grid[14][9] = "C"
    grid[14][10] = "K1"
    grid[14][11] = "K1"
    grid[14][12] = "K2"
    grid[14][13] = "K3"
    grid[14][14] = "O2"
    grid[14][15] = "C"

    # y=15: Scarf Knot on front of post & lower wrap
    grid[15][9] = "C"
    grid[15][10] = "O1"
    grid[15][11] = "K1"
    grid[15][12] = "K2"
    grid[15][13] = "K3"
    grid[15][14] = "C"

    # y=16: Knot cinch and short dangling tail
    grid[16][10] = "C"
    grid[16][11] = "K1"
    grid[16][12] = "K2"
    grid[16][13] = "C"

    # y=17: Short knot tip hanging down
    grid[17][11] = "C"
    grid[17][12] = "O2"
    grid[17][13] = "C"

    # y=18: tip end
    grid[18][12] = "C"

    return grid

base_grid = create_static_base()

def render_to_png(grid, path, scale=6):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * scale, H * scale), Image.NEAREST).save(path)

render_to_png(base_grid, "python/test_scarf_base.png")
print("Saved test_scarf_base.png")
