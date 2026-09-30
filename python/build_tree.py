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
tree_rows = [
    # 0..2 (Sky)
    "................................................................",
    "................................................................",
    "................................................................",
    # 3 (Tips of twisted top horns and background twigs)
    "............................##..................................",
    "....................##.....#MM#.............##..................",
    "...................#DD#...#HMM#............#DD#.................",
    "............##......#DD#..#HHM#...........#VD#.........##.......",
    "...........#DD#......#DD#.#HHM#..........#VD#.........#DD#......",
    "..........#VDD#.......#DD##HMM#.........#VD#.........#VVD#......",
    "..........#VVD#........#DD#MMM#........#VDD#.........#VD#.......",
    "...........#VD#.........#D#MMM#.......#VVD#.........#VDD#.......",
    "............#VD#........#D#MMH#......#VDD#.........#VDD#........",
    ".............#VD#......#DD#MMH#.....#VDD#..........#VD#.........",
    "..............#VD#....#DD##HMH#....#VDD#..........#VD#..........",
    "...............#VDD###DD#.#HMH#...#VDD#..........#VDD#..........",
    "................#VDDDD#...#HMH#..#VDD#..........#VDD#...........",
    # 16 (Crown branch junctions and background limbs merging)
    ".................#VDD#....#HMH#.##VDD#..........#VDD#...........",
    "..................#VD#...#HHMH##VVDD#..........#VDD#............",
    "...................#D#...#HMMH##VDD#..........#VDD#.............",
    "........##..........##..#HMMM##VDD#..........#VDD#......##......",
    ".......#DD#............#HHMMH##VD#..........#VDD#......#DD#.....",
    "......#VVDD#..........#HHMMM##VD#..........#VVD#......#VDDD#....",
    "...###VVDDDD#........#HHMMM##VD#..........#VVD#......#VVDDD#....",
    "..#DDDDDDDDD#.......#HHMMMM#VD#..........#VVD#......#VVDDDD#....",
    ".#DDDDD#VDDD#......#HHMMMM##VD#.........#VVD#......#VVDDDD#.....",
    "#DDDDD#..#VDD#....#HHMMMMH#VD#.........#VVD#......#VVDDDD#......",
    "#DDDD#....#VDD#..#HHMMMMMH#VD#........#VVD#......#VVDDDD#.......",
    ".#DD#......#VDD##HHMMMMMMH#VD#.......#VVD#......#VVDDDD#........",
    # 28 (Upper trunk - major twisted braid begins)
    "............#VDD#HMMMMMMMH#V#.......#VVD#......#VVDDDD#.........",
    ".............#VD#HMMMMMMMM##.......#VVD#......#VVDDD#...........",
    "..............##HMMMMMMMMM#.......#VVD#.......#VVDD#............",
    "...............#HMMMMMMMMM#......#VVD#.........#VVD#............",
    "...............#HMMMMMMMMMM#....#VVD#...........##..............",
    "..............#HHMMMMMMMMMM#...#VVD#............................",
    "..............#HHMMMMMMMMMMM###VVD#.............................",
    # 35 (Foreground branch sprouts & crosses front of trunk)
    "..............#HMMMHVMMMMMMMVVVDD#..............................",
    "..............#HMMMH#VMMMMMMMH##................................",
    "..............#HMMMH##VMMMMMMMH#.....###........................",
    ".............#HHMMMH#.#VMMMMMMMH#...#HHM###.....................",
    ".............#HHMMMH#..#VMMMMMMMH#.#HHMMMMH#....................",
    # 40 (Foreground branch crosses and overlaps trunk, casting shadow)
    ".............#HMMMH#...#VMMMMMMMMH#HHMMMMMMH#...................",
    "............#HHMMMH#....#VMMMMMMMM#HHMMMMMMMH#..................",
    "............#HHMMMH#.....#VMMMMMM#HHMMMMMMMMMH#.................",
    "............#HMMMH#.......#VMMMM#HHMMMMMMMMMMMH#................",
    "...........#HHMMMH#........#VMM#HHMMMMMDDDMMMMH#................",
    "...........#HHMMMH#.........#V#HHMMMMMDDDDMMMMMH#...............",
    # 46 (Foreground branch tips off, trunk continues twisting downward)
    "...........#HMMMH#..........##HHMMMMMDDDDDMMMMMH#...............",
    "..........#HHMMMH#...........#HHMMMMDDDDDDMMMMMH#...............",
    "..........#HHMMMH#............#HHMMDDDDDDMMMMMH#................",
    "..........#HMMMH#..............#HHMDDDDDMMMMM##.................",
    ".........#HHMMMH#...............#HHDDDDMMMM##...................",
    ".........#HHMMMH#................#HHDDDMM##.....................",
    # 52 (Lower trunk flaring out into massive roots)
    ".........#HMMMMH#.................#####.........................",
    "........#HHMMMMMH#..............................................",
    "........#HHMMMMMMH#.......##....................................",
    ".......#HHMMMMMMMMH#.....#MM#.........##........................",
    # 56 (Roots gripping and cracking stone masonry base)
    "......#HHMMMMMMMMMMH#...#HMMM#.......#MM#.......................",
    ".....#HHMMM##VMMMMMMH#.#HHMMMM#.....#HMMM#......##..............",
    "....#HHMMM#..#VMMMMMMH#HHMMMMMM#...#HHMMMM#....#MM#.............",
    "...#HHMMM#....#VMMMMMM#HHMMMMMMH#.#HHMMMMMM#..#HMMM#............",
    "..#HHMMM#......#VMMMM#HHMMMMMMMMH#HHMMMMMMMM##HHMMMM#...........",
    ".#HHMMM#........#VMM#HHMMMMMMMMMH#HHMMMMMMMMH#HHMMMM#...........",
    "################################################################",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
]

print("Tree rows count:", len(tree_rows))
for i, r in enumerate(tree_rows):
    assert len(r) == 64, f"Row {i} len {len(r)} != 64"
print("All rows verified at length 64!")
