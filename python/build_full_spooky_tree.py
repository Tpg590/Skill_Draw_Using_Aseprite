# Full detailed design of 64x64 Spooky Twisted Tree in Terraria style
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

# Helper to build rows cleanly
# 64 chars per row
tree_data = [
    # 0..2 (Sky above highest tips)
    "." * 64,
    "." * 64,
    "............................##..................................",
    # 3..7 (Crown horns and background twigs)
    "...........................#HH#...................##............",
    "............##............#HMMH#.................#DD#...........",
    "...........#DD#..........#HMMMH#........##......#VDD#...........",
    "...........#VD#..........#HMMMH#.......#DD#....#VDD#............",
    "..........#VVD#.........#HHMMMH#......#VDD#....#VD#.............",
    # 8..15 (Crown forks, background branch boughs stretching up-left and up-right)
    "..........#VDD#.........#HMMMD#.......#VDD#...#VDD#......##.....",
    "...........#VD#.........#HMMMD#......#VDD#...#VDD#......#DD#....",
    "....##......#VD#........#HMMMD#.....#VDD#....#VDD#.....#VDD#....",
    "...#DD#......#VD#......#HHMMMD#....#VDD#....#VDD#.....#VDD#.....",
    "...#VDD#......#VD#.....#HMMMDD#...#VDD#....#VDD#.....#VDD#......",
    "....#VDD#......#VD#...#HHMMMDD#..#VDD#....#VDD#.....#VDD#.......",
    ".....#VDD#......#VD#..#HMMMDDD#.#VDD#.....#VDD#....#VDD#........",
    "......#VDD#......#VDD#HHMMMDDD##VDD#.....#VDD#....#VDD#.........",
    # 16..23 (Main crown forks split: Left Horn, Center Horn, Right Horn)
    ".......#VDD#......#VD#HHMMMDDD#VDD#.....#VDD#...##VDD#..........",
    "........#VDD#.....#VD#HHMMMDDD#VD#.....#VDD#...#DDDD#...........",
    ".........#VDD#.....##HMMMMMDDD#VD#....#VDD#...#DDDD#............",
    "..........#VDD#...#HHMMMMMMMDD##D#...#VDD#...#VDDD#.............",
    "...........#VDD#.#HHMMMMMMMMDD##....#VDD#...#VDDD#......##......",
    "............#VDD#HHMMMMMMMMMDD#....#VDD#...#VDDD#......#DD#.....",
    "......##.....#VD#HHHMMMMMMMMMD#...#VDD#...#VDDD#......#VDDD#....",
    ".....#DD#.....##HHHHMMMMMMMMMD#..#VDD#...#VVDDD#.....#VVDDD#....",
    # 24..30 (West and East heavy gnarled limbs branch out horizontally)
    "....#VDDD#...#HHHHHHMMMMMMMMMDD##VDD#...#VVDDDD#....#VVDDDD#....",
    "...#VVDDDD###HHHHHHHMMMMMMMMMDD#VDD#...#VVDDDD#....#VVDDDD#.....",
    "..#VVDDDDDDD#HHHHHHHHMMMMMMMMMDD##D#..#VVDDDDD#...#VVDDDDD#.....",
    ".#VVDDDDDDDD#HHHHHHHHHMMMMMMMMMDD###.#VVDDDDD#...#VVDDDDDD#.....",
    "#VVDDDDDD##..#HHHHHHHHMMMMMMMMMDDD###VVDDDDDD#..#VVDDDDD##......",
    ".##VDDDD#.....#HHHHHHHMMMMMMMMMDDDD#VVDDDDDD#..#VVDDDD##........",
    "...#####.......#HHHHHHMMMMMMMMMDDDDD#VVDDDD#..#VVDDDD#..........",
    # 31..37 (Upper Corkscrew Trunk: Braided diagonal helix begins)
    "................#HHHHHMMMMMMMMMDDDDD##VVDD#..#VVDDDD#...........",
    ".................#HHHMMMMMMMVMMMDDDDD##VV#...#VVDDD#............",
    "..................#HHHMMMMMMMVMMMDDDDD###...#VVDDD#.............",
    "...................#HHMMMMMMMMVMMMDDDDDD#..#VVDDD#..............",
    "...................#HHHMMMMMMMMVMMMDDDDD#.#VVDDD#...............",
    # 36 (Foreground branch begins sprouting on front face of trunk)
    "...................#HHHMMMMMMMMMVMMMDDDD##VVDDD#................",
    "....................#HHMMMMMMMMMMVMMMDDD#VVDDD#.................",
    # 38..45 (Foreground branch crosses OVER the trunk, casting shadow D on trunk!)
    "....................#HHHMMMMMMMMMMVMMMDD#VVDD#..................",
    ".....................#HHMMMMMM#####VMMMD#VVDD#...................",
    ".....................#HHHMMM#HHHHHM#VMMD#VVD#...................",
    "......................#HHMM#HHMMMMMH#VMD##VV#...................",
    "......................#HHH#HHMMMMMMMH#V##VVV#...................",
    ".......................#H#HHMMMMMMMMMH#VVVV#....................",
    ".......................##HHMMMMMMMMMMMH#VVV#....................",
    "........................#HHMMMMMDDDMMMMH#VV#...##...............",
    # 46..51 (Foreground branch tip extends out right, trunk helix continues)
    "........................#HHHMMMMDDDDMMMMH#V#..#DD#..............",
    ".........................#HHMMMMDDDDDMMMMH#..#VDDD#.............",
    ".........................#HHHMMMMDDDDDMMMH#.#VVDDD#.............",
    "..........................#HHHMMMMDDDDDMMH##VVDDDD#.............",
    "..........................#HHHHMMMMMDDDDMM#VVDDD##..............",
    "...........................#HHHHMMMMMDDDMM#VVDD#................",
    # 52..56 (Lower trunk flaring out into massive roots)
    "...........................#HHHHHMMMMMDDMM#VV#..................",
    "..........................#HHHHHHHMMMMMDDM##....................",
    ".........................#HHHHHHHHHMMMMMDD#.....................",
    "........................#HHHHHHHHHHHMMMMMDD#....................",
    ".......................#HHHHHHHHHHHHHMMMMMDD#...................",
    # 57..61 (Massive roots gripping and fracturing stone masonry base)
    "......................#HHHHHH#VHHHHHHHMMMMMDD#..................",
    ".....####............#HHHHHH#..#VHHHHHHMMMMMDD#...........####..",
    "...##HHHH##.........#HHHHHH#....#VHHHHHMMMMMMMD#........##HHHH##",
    "..#HHMMMMHH#.......#HHHHHH#......#VHHHHMMMMMMMMD#......#HHMMMMHH",
    ".#HHMMVVMMHH#.....#HHHHHH#........#VHHHMMMMMMMMMD#....#HHMMVVMMH",
    "################################################################",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
]

print("Rows defined:", len(tree_data))
for i, r in enumerate(tree_data):
    assert len(r) == 64, f"Row {i} len {len(r)} != 64: '{r}'"

print("All rows valid 64 chars!")
