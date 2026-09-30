import os
from PIL import Image

PALETTE = {
    ".": None,
    "#": (24, 15, 20, 255),       # Viền tối sẫm Terraria (Near-black outline)
    "S": (18, 10, 16, 130),       # Bóng râm tiếp đất (Ground shadow, Alpha 130)
    "H": (191, 163, 130, 255),    # Gỗ sáng / Vết nứt đón sáng (Pale aged bark highlight)
    "M": (130, 99, 77, 255),      # Màu gỗ chính / Gạch đá (Mid aged brown/gray wood & stone)
    "D": (74, 50, 38, 255),       # Gỗ tối / Cành phía sau (Deep shadow wood & background branches)
    "V": (42, 24, 18, 255),       # Rãnh xoắn sâu / Khe nứt gạch (Deepest twist crevice & fissure)
}

# 64 rows of 64 characters
# Let's craft the exact lines
rows = [
    # 0..2 (Empty sky)
    "." * 64,
    "." * 64,
    "............................##..................................",
    # 3 (Tips of North horns & background branches)
    "...........................#HH#...................##............",
    "............##............#HMMH#.................#DD#...........",
    "...........#DD#..........#HMMMH#........##......#VDD#...........",
    "...........#VD#..........#HMMMH#.......#DD#....#VDD#............",
    "..........#VVD#.........#HHMMMH#......#VDD#....#VD#.............",
    # 8 (Branches branching & stretching in 4 directions)
    "..........#VDD#.........#HMMMD#.......#VDD#...#VDD#......##.....",
    "...........#VD#.........#HMMMD#......#VDD#...#VDD#......#DD#....",
    "....##......#VD#........#HMMMD#.....#VDD#....#VDD#.....#VDD#....",
    "...#DD#......#VD#......#HHMMMD#....#VDD#....#VDD#.....#VDD#.....",
    "...#VDD#......#VD#.....#HMMMDD#...#VDD#....#VDD#.....#VDD#......",
    "....#VDD#......#VD#...#HHMMMDD#..#VDD#....#VDD#.....#VDD#.......",
    ".....#VDD#......#VD#..#HMMMDDD#.#VDD#.....#VDD#....#VDD#........",
    "......#VDD#......#VDD#HHMMMDDD##VDD#.....#VDD#....#VDD#.........",
    # 16 (Crown branch junctions; West & East branches starting)
    ".......#VDD#......#VD#HHMMMDDD#VDD#.....#VDD#...##VDD#..........",
    "........#VDD#.....#VD#HHMMMDDD#VD#.....#VDD#...#DDDD#...........",
    ".........#VDD#.....##HMMMMMDDD#VD#....#VDD#...#DDDD#............",
    "..........#VDD#...#HHMMMMMMMDD##D#...#VDD#...#VDDD#.............",
    "...........#VDD#.#HHMMMMMMMMDD##....#VDD#...#VDDD#......##......",
    "............#VDD#HHMMMMMMMMMDD#....#VDD#...#VDDD#......#DD#.....",
    "......##.....#VD#HHHMMMMMMMMMD#...#VDD#...#VDDD#......#VDDD#....",
    ".....#DD#.....##HHHHMMMMMMMMMD#..#VDD#...#VVDDD#.....#VVDDD#....",
    # 24 (Major West & East limbs extending horizontally)
    "....#VDDD#...#HHHHHHMMMMMMMMMDD##VDD#...#VVDDDD#....#VVDDDD#....",
    "...#VVDDDD###HHHHHHHMMMMMMMMMDD#VDD#...#VVDDDD#....#VVDDDD#.....",
    "..#VVDDDDDDD#HHHHHHHHMMMMMMMMMDD##D#..#VVDDDDD#...#VVDDDDD#.....",
    ".#VVDDDDDDDD#HHHHHHHHHMMMMMMMMMDD###.#VVDDDDD#...#VVDDDDDD#.....",
    "#VVDDDDDD##..#HHHHHHHHMMMMMMMMMDDD###VVDDDDDD#..#VVDDDDD##......",
    ".##VDDDD#.....#HHHHHHHMMMMMMMMMDDDD#VVDDDDDD#..#VVDDDD##........",
    "...#####.......#HHHHHHMMMMMMMMMDDDDD#VVDDDD#..#VVDDDD#..........",
    # 31 (Trunk corkscrew helical twist begins)
    "................#HHHHHMMMMMMMMMDDDDD##VVDD#..#VVDDDD#...........",
    ".................#HHHMMMMMMMVMMMDDDDD##VV#...#VVDDD#............",
    "..................#HHHMMMMMMMVMMMDDDDD###...#VVDDD#.............",
    # 34 (Foreground branch sprouts & sweeps across front of trunk)
    "...................#HHMMMMMMMMVMMMDDDDDD#..#VVDDD#..............",
    "...................#HHHMMMMMMMMVMMMDDDDD#.#VVDDD#...............",
    "...................#HHHMMMMMMMMMVMMMDDDD##VVDDD#................",
    "....................#HHMMMMMMMMMMVMMMDDD#VVDDD#.................",
    "....................#HHHMMMMMMMMMMVMMMDD#VVDD#..................",
    # 39 (Foreground branch in front of trunk, casting shadow D on trunk!)
    "....................#HHMMMMMMM#####VMMMD#VVDD#..................",
    "....................#HHHMMM#HHHHHM#VMMMD#VVD#...................",
    ".....................#HHMM#HHMMMMMH#VMD##VV#....................",
    ".....................#HHH#HHMMMMMMMH#V##VVV#....................",
    "......................#H#HHMMMMMMMMMH#VVVV#.....................",
    "......................##HHMMMMMMMMMMMH#VVV#.....................",
    # 45 (Foreground branch tip extends out right, casting shadow D on lower trunk)
    ".......................#HHMMMMMDDDMMMMH#VV#...##................",
    ".......................#HHHMMMMDDDDMMMMH#V#..#DD#...............",
    "........................#HHMMMMDDDDDMMMMH#..#VDDD#..............",
    "........................#HHHMMMMDDDDDMMMH#.#VVDDD#..............",
    ".........................#HHHMMMMDDDDDMMH##VVDDDD#..............",
    ".........................#HHHHMMMMMDDDDMM#VVDDD##...............",
    # 51 (Trunk corkscrew continues, widening into root spurs)
    "..........................#HHHHMMMMMDDDMM#VVDD#.................",
    "..........................#HHHHHMMMMMDDMM#VV#...................",
    ".........................#HHHHHHHMMMMMDDM##.....................",
    "........................#HHHHHHHHHMMMMMDD#......................",
    ".......................#HHHHHHHHHHHMMMMMDD#.....................",
    "......................#HHHHHHHHHHHHHMMMMMDD#....................",
    # 57 (Massive roots gripping and fracturing stone masonry base)
    ".....................#HHHHHH#VHHHHHHHMMMMMDD#...................",
    ".....####...........#HHHHHH#..#VHHHHHHMMMMMDD#...........####...",
    "...##HHHH##........#HHHHHH#....#VHHHHHMMMMMMMD#........##HHHH##.",
    "..#HHMMMMHH#......#HHHHHH#......#VHHHHMMMMMMMMD#......#HHMMMMHH#",
    ".#HHMMVVMMHH#....#HHHHHH#........#VHHHMMMMMMMMMD#....#HHMMVVMMHH",
    "################################################################",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
]

print("Rows defined:", len(rows))
for i, r in enumerate(rows):
    assert len(r) == 64, f"Row {i} len {len(r)} != 64: '{r}'"

print("All 64 rows strictly validated at 64 characters!")

# Render test preview
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
for y, row in enumerate(rows):
    for x, ch in enumerate(row):
        col = PALETTE.get(ch)
        if col:
            img.putpixel((x, y), col)

img.save("preview_tree_1x.png")
img4x = img.resize((256, 256), Image.NEAREST)
img4x.save("preview_tree_4x.png")

print("Generated preview_tree_1x.png and preview_tree_4x.png!")
