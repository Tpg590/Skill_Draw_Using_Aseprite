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
# Crafted with Terraria high-contrast texturing, helical corkscrew grain, overlapping branches, cracked stones and roots
tree_art = [
    # 0..2
    "." * 64,
    "." * 64,
    "............................##..................................",
    # 3..7: North twisted horns & background branch twigs
    "...........................#HH#....................##...........",
    "............##............#HMMH#........##........#DD#..........",
    "...........#DD#..........#HMMMH#.......#DD#......#VVD#..........",
    "...........#VD#..........#HHMMH#......#VDD#.....#VDD#...........",
    "..........#VVD#.........#HMMMD#.......#VDD#....#VDD#.....##.....",
    # 8..14: Antler-like crown forks & background branches in dark D, V
    "..........#VDD#.........#HMMMD#......#VDD#.....#VD#.....#DD#....",
    "...........#VD#.........#HHMMD#.....#VDD#.....#VDD#....#VDD#....",
    "....##......#VD#.......#HMMMDD#....#VDD#.....#VDD#....#VDD#.....",
    "...#DD#......#VD#.....#HHMMMDD#...#VDD#.....#VDD#....#VDD#......",
    "...#VDD#......#VD#...#HMMMDDD#...#VDD#.....#VDD#....#VDD#.......",
    "....#VDD#......#VD#.#HHMMMDDD#..#VDD#.....#VDD#....#VDD#........",
    ".....#VDD#......#VDD#HMMMMDDD##VDD#......#VDD#....#VDD#.........",
    # 15..21: Crown fork splits into twisted antlers; background boughs ducking behind
    "......#VDD#......#VD#HHMMMDDD#VDD#......#VDD#....#VDD#..........",
    ".......#VDD#.....#VD#HHMMMDDD#VD#......#VDD#...##VDD#...........",
    "........#VDD#.....##HMMMMMDDD#VD#.....#VDD#...#DDDD#............",
    ".........#VDD#...#HHMMMMMMMDD##D#....#VDD#...#DDDD#.............",
    "..........#VDD#.#HHMMMMMMMMDD##.....#VDD#...#VDDD#.......##.....",
    "...........#VDD#HHMMMMMMMMMDD#.....#VDD#...#VDDD#.......#DD#....",
    ".....##.....#VD#HHHMMMMMMMMMD#....#VDD#...#VDDD#.......#VDDD#...",
    # 22..28: West and East lateral limbs reaching horizontally with gnarled crooked bends
    "....#DD#.....##HHHHMMMMMMMMMD#...#VDD#...#VVDDD#......#VVDDD#...",
    "...#VDDD#...#HHHHHHMMMMMMMMMDD##VDD#....#VVDDDD#.....#VVDDDD#...",
    "..#VVDDDD###HHHHHHHMMMMMMMMMDD#VDD#....#VVDDDD#.....#VVDDDD#....",
    ".#VVDDDDDDD#HHHHHHHHMMMMMMMMMDD##D#...#VVDDDDD#....#VVDDDDD#....",
    "#VVDDDDDDDD#HHHHHHHHHMMMMMMMMMDD###..#VVDDDDD#....#VVDDDDDD#....",
    "#VVDDDDDD##.#HHHHHHHHMMMMMMMMMDDD###VVDDDDDD#...#VVDDDDD##......",
    ".##VDDDD#....#HHHHHHHMMMMMMMMMDDDD#VVDDDDDD#...#VVDDDD##........",
    # 29..33: Lateral limbs merge into trunk; Corkscrew diagonal helical twist begins
    "...#####......#HHHHHHMMMMMMMMMDDDDD#VVDDDD#...#VVDDDD#..........",
    "...............#HHHHHMMMMMMMMMDDDDD##VVDD#...#VVDDDD#...........",
    "................#HHHMMMMMMMVMMMDDDDD##VV#....#VVDDD#............",
    ".................#HHHMMMMMMMVMMMDDDDD###....#VVDDD#.............",
    "..................#HHMMMMMMMMVMMMDDDDDD#...#VVDDD#..............",
    # 35..38: Trunk spiral furrow V winds across; Foreground branch starts sprouting!
    "..................#HHHMMMMMMMMVMMMDDDDD#..#VVDDD#...............",
    "..................#HHHMMMMMMMMMVMMMDDDD##VVDDD#.................",
    "...................#HHMMMMMMMMMMVMMMDDD#VVDDD#..................",
    "...................#HHHMMMMMMMMMMVMMMDD#VVDD#...................",
    # 39..44: FOREGROUND BRANCH sweeps across front of trunk, casting shadow D on trunk!
    "...................#HHMMMMMMM#####VMMMD#VVDD#...................",
    "...................#HHHMMM#HHHHHM#VMMMD#VVD#....................",
    "....................#HHMM#HHMMMMMH#VMD##VV#.....................",
    "....................#HHH#HHMMMMMMMH#V##VVV#.....................",
    ".....................#H#HHMMMMMMMMMH#VVVV#......................",
    ".....................##HHMMMMMMMMMMMH#VVV#......................",
    # 45..50: Foreground branch tip reaches right; Trunk helix continues downward
    "......................#HHMMMMMDDDMMMMH#VV#...##.................",
    "......................#HHHMMMMDDDDMMMMH#V#..#DD#................",
    ".......................#HHMMMMDDDDDMMMMH#..#VDDD#...............",
    ".......................#HHHMMMMDDDDDMMMH#.#VVDDD#...............",
    "........................#HHHMMMMDDDDDMMH##VVDDDD#...............",
    "........................#HHHHMMMMMDDDDMM#VVDDD##................",
    # 51..55: Lower trunk widening, corkscrew grain spiraling into massive root spurs
    ".........................#HHHHMMMMMDDDMM#VVDD#..................",
    ".........................#HHHHHMMMMMDDMM#VV#....................",
    "........................#HHHHHHHMMMMMDDM##......................",
    ".......................#HHHHHHHHHMMMMMDD#.......................",
    "......................#HHHHHHHHHHHMMMMMDD#......................",
    # 56..61: ROOTS CLAWING AND EMBEDDED INTO CRACKED STONE MASONRY BASE
    ".....................#HHHHHHHHHHHHHMMMMMDD#.....................",
    "......####..........#HHHHHH#VHHHHHHHMMMMMDD#...........####.....",
    "....##HHHH##.......#HHHHHH#..#VHHHHHHMMMMMDD#........##HHHH##...",
    "...#HHMMMMHH#.....#HHHHHH#....#VHHHHHMMMMMMMD#......#HHMMMMHH#..",
    "..#HHMMVVMMHH#...#HHHHHH#......#VHHHHMMMMMMMMD#....#HHMMVVMMHH#.",
    ".#HHMMMVVMMHHH#.#HHHHHH#........#VHHHMMMMMMMMMD#..#HHHMMVVMMMHH#",
    # 62..63: Ground line and contact shadow S
    "################################################################",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
]

print("Art rows count:", len(tree_art))
for idx, r in enumerate(tree_art):
    assert len(r) == 64, f"Row {idx} len {len(r)} != 64: '{r}'"

print("All 64 rows strictly validated at 64 characters!")

img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
for y, row in enumerate(tree_art):
    for x, ch in enumerate(row):
        col = PALETTE.get(ch)
        if col:
            img.putpixel((x, y), col)

img.save("preview_tree_art_1x.png")
img4x = img.resize((256, 256), Image.NEAREST)
img4x.save("preview_tree_art_4x.png")

print("Generated preview_tree_art_1x.png and preview_tree_art_4x.png!")
