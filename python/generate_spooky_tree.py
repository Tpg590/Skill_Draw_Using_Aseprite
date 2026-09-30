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

# 64 rows x 64 columns
# Let's craft the tree row by row
rows = [
    # 0..2 (Empty sky)
    "." * 64,
    "." * 64,
    "............................##..................................",
    # 3 (Tips of high crown horns and distant background twigs)
    "...........................#HH#...................##............",
    "............##............#HMMH#.................#DD#...........",
    "...........#DD#..........#HMMMH#........##......#VDD#...........",
    "...........#VD#..........#HMMMH#.......#DD#....#VDD#............",
    "..........#VVD#.........#HHMMMH#......#VDD#....#VD#.............",
    "..........#VDD#.........#HMMMD#.......#VDD#...#VDD#......##.....",
    "...........#VD#.........#HMMMD#......#VDD#...#VDD#......#DD#....",
    "....##......#VD#........#HMMMD#.....#VDD#....#VDD#.....#VDD#....",
    "...#DD#......#VD#......#HHMMMD#....#VDD#....#VDD#.....#VDD#.....",
    "...#VDD#......#VD#.....#HMMMDD#...#VDD#....#VDD#.....#VDD#......",
    "....#VDD#......#VD#...#HHMMMDD#..#VDD#....#VDD#.....#VDD#.......",
    ".....#VDD#......#VD#..#HMMMDDD#.#VDD#.....#VDD#....#VDD#........",
    "......#VDD#......#VDD#HHMMMDDD##VDD#.....#VDD#....#VDD#.........",
    # 16 (Crown splits into horns; background branches branch out)
    ".......#VDD#......#VD#HHMMMDDD#VDD#.....#VDD#...##VDD#..........",
    "........#VDD#.....#VD#HHMMMDDD#VD#.....#VDD#...#DDDD#...........",
    ".........#VDD#.....##HMMMMMDDD#VD#....#VDD#...#DDDD#............",
    "..........#VDD#...#HHMMMMMMMDD##D#...#VDD#...#VDDD#.............",
    "...........#VDD#.#HHMMMMMMMMDD##....#VDD#...#VDDD#..............",
    "............#VDD#HHMMMMMMMMMDD#....#VDD#...#VDDD#......##.......",
    "......##.....#VD#HHHMMMMMMMMMD#...#VDD#...#VDDD#......#DD#......",
    ".....#DD#.....##HHHHMMMMMMMMMD#..#VDD#...#VVDDD#.....#VDDD#.....",
    "....#VDDD#...#HHHHHHMMMMMMMMMDD##VDD#...#VVDDDD#....#VVDDD#.....",
    "...#VVDDDD###HHHHHHHMMMMMMMMMDD#VDD#...#VVDDDD#....#VVDDDD#.....",
    "..#VVDDDDDDD#HHHHHHHHMMMMMMMMMDD##D#..#VVDDDDD#...#VVDDDDD#.....",
    ".#VVDDDDDDDD#HHHHHHHHHMMMMMMMMMDD###.#VVDDDDD#...#VVDDDDDD#.....",
    # 28 (Main West & East lateral boughs merge into twisting trunk)
    "#VVDDDDDD##..#HHHHHHHHMMMMMMMMMDDD###VVDDDDDD#..#VVDDDDD##......",
    ".##VDDDD#.....#HHHHHHHMMMMMMMMMDDDD#VVDDDDDD#..#VVDDDD##........",
    "...#####.......#HHHHHHMMMMMMMMMDDDDD#VVDDDD#..#VVDDDD#..........",
    "................#HHHHHMMMMMMMMMDDDDD##VVDD#..#VVDDDD#...........",
    ".................#HHHHMMMMMMMMMDDDDD#.#VV#...#VVDDD#............",
    # 33 (Corkscrew trunk: Diagonal spiral seam V wraps across from left)
    "..................#HHHMMMMMMMMMDDDDD#..##...#VVDDD#.............",
    "..................#HHHMMMMMMMMMDDDDD#......#VVDDD#..............",
    "...................#HHMMMMMMMMMDDDDD#.....#VVDDD#...............",
    # 36 (Foreground branch begins sprouting on front-right of trunk)
    "...................#HHHMMMMMMMMMDDDD#....#VVDDD#................",
    "....................#HHMMMMMMMMMDDDD#...#VVDDD#.................",
    "....................#HHHMMMMMMMMMDDD#...#VVDD#..................",
    ".....................#HHMMMMMMMMMDDD#..#VVDD#...................",
    # 40 (Trunk twist & Foreground branch crossing in front with shadow D)
    ".....................#HHHMMMMMMMMMDD#..#VVD#....................",
    "......................#HHMMMMMMMMMDD#.##VV#.....................",
    "......................#HHHMMMMMMMMMD##VVV#......................",
    ".......................#HHMMMMMMMMMD#VVV#.......................",
    ".......................#HHHMMMMMMMM#VVV#........................",
    "........................#HHMMMMMMMM#VV#.........................",
    "........................#HHHMMMMMMM#V#..........................",
    ".........................#HHMMMMMMM##...........................",
    ".........................#HHHMMMMMM#............................",
    "..........................#HHMMMMMM#............................",
    "..........................#HHHMMMMM#............................",
    # 51 (Lower trunk widening towards root base)
    "...........................#HHMMMMM#............................",
    "...........................#HHHMMMM#............................",
    "............................#HHMMMM#............................",
    "............................#HHHMMM#............................",
    ".............................#HHMMM#............................",
    # 56 (Roots branching into ground stone base)
    ".............................#HHHMM#............................",
    "..............................#HHMM#............................",
    "..............................#HHHM#............................",
    "...............................#HHM#............................",
    "...............................#HHH#............................",
    "................................#HH#............................",
    "................................#HH#............................",
    ".................................##............................."
]

print("Rows defined:", len(rows))
