import os
from PIL import Image

W, H = 48, 48
FPS = 8

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "#": (22, 8, 14, 255),     # Deep wine-black outline (#16080e)
    "S": (24, 12, 18, 130),    # Ground shadow (Alpha 130)
    
    # Glass & Highlights
    "P": (255, 255, 255, 255), # Pure white specular highlight (#ffffff)
    "K": (210, 235, 245, 255), # Pale glass reflection (#d2ebf5)
    "J": (80, 95, 110, 255),   # Dark glass outline / shadow (#505f6e)
    
    # Cork Stopper
    "E": (185, 135, 85, 255),  # Cork light wood (#b98755)
    "U": (115, 75, 45, 255),   # Cork dark wood (#734b2d)
    
    # Glowing Red Liquid (Hue-shifting)
    "W": (255, 255, 255, 255), # Core white hot bubble (#ffffff)
    "Y": (255, 225, 90, 255),  # Intense glowing yellow (#ffe15a)
    "R": (255, 55, 70, 255),   # Radiant glowing crimson (#ff3746)
    "B": (195, 20, 50, 255),   # Deep ruby red (#c31432)
    "Q": (105, 10, 30, 255),   # Dark wine red shadow (#690a1e)
    
    # Twisted Withered Roots (OSL Hue-shifting)
    "H": (255, 160, 75, 255),  # OSL intense peach highlight (#ffa04b)
    "O": (230, 95, 35, 255),   # OSL warm fiery orange (#e65f23)
    "T": (160, 50, 25, 255),   # OSL warm terracotta-red (#a03219)
    "M": (90, 36, 26, 255),    # Withered bark warm midtone (#5a241a)
    "D": (48, 20, 18, 255),    # Withered bark deep brown shadow (#301412)
    "V": (24, 10, 12, 255),    # Darkest crevice / undercut shadow (#180a0c)
}

# Master Sculpted Frame 1
f1 = [
    # 0..4
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    # 5..7: Cork Stopper
    "......................####......................",
    "......................#EEU#.....................",
    "......................#EEU#.....................",
    # 8..10: Flared bottle lip
    "....................########....................",
    "...................#PKKKKKKJ#...................",
    "....................#PKKKKJ#....................",
    # 11..13: Slender neck
    ".....................#PKKJ#.....................",
    ".....................#P..J#.....................",
    ".....................#P..J#.....................",
    # 14..18: Flask shoulder expanding smoothly into spherical bulb
    "...................#PK....KJ#...................",
    ".................#PK........KJ#.................",
    "...............#PK..PP........KJ#...............", # y=16: Specular highlight PP starts at x=20..21
    "..............#PK..PP..........KJ#..............", # y=17: PP at x=19..20
    ".............#PK..PP............KJ#.............", # y=18: PP at x=18..19
    # 19..20: Flask bulb upper dome (empty interior)
    "............#PK..PP..............KJ#............", # y=19: PP at x=17..18
    "...........#PK..PP................KJ#...........", # y=20: PP at x=16..17
    # 21..23: Liquid Surface Ellipse (Meniscus) - Quy tắc 3.2.2!
    "...........#K..PP.QQBBBBBBBBBBQQ...J#...........", # y=21: PP crosses back rim of liquid!
    "..........#PK.PP.QBBBRRYYYYYYRRBBQ..J#..........", # y=22: PP on front liquid surface
    "..........#PK.P.QBRRYWWYYYYWWYRRBQ..J#..........", # y=23: P continues down into liquid
    # 24..26: Deep glowing liquid body & Root claw tips (Tapering to 1px)
    "..........#PK.P.BRYYRRRRRRRRRRYYRB..J#..........", # y=24: P at x=14
    ".........#..#.P.BYRRRRRRRRRRRRRRYB..J#..#.......", # y=25: Left claw 1px at x=9; Right claw 1px at x=40
    "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......", # y=26: Left claw 2px; Right claw 2px
    # 27..29: Middle liquid body & roots clasping both flanks
    "........#HO#.#..BRRRRRRRRRRWRRRB...#.#MD#.......", # y=27: Right claw 3px; Bubble 2 (W) at x=28
    ".......#THO#.#..QBRRRRRRRRYRRRB...#..#TMD#......", # y=28: Roots clasping glass flanks
    ".......#THOM#.#.QQBRRWYRRRRRRBQ..#..#OTMD#......", # y=29: Bubble 1 (WY) at x=21..22; OSL color bleed
    # 30..33: Liquid bottom bowl & roots intertwining underneath
    ".......#TTHOM#.##QQBRRYRRRRRBQQ.##..#HOTMD#.....", # y=30: Roots curve around glass bottom
    "........#TTHOM##..QQBBRRRRRRBQQ..##.#HHOTMD#....", # y=31
    "........#DTHOMM##..QQQBBBBQQQ..##..#HHOTMDD#....", # y=32: Liquid bottom round sphere
    ".........#DDTHOMM###.########.###.##HHOTMDD#....", # y=33: Glass bottom sits into twisted roots
    # 34..37: Twisted root braid with crossover (Trunk 1 spirals front, Trunk 2 spirals back)
    "..........#VDDTHOMMM#OHHHHHHO#MMMMHHOTMDDV#.....", # y=34: OSL fiery peach cradle directly under glass
    "...........#VVDDTTHOMHOTTTTTOHMMHHOTMDDVV#......", # y=35: Roots knot together
    "............#VVVDTTOMHOTTTTMTHHHOTMDDVVV#.......", # y=36: Right root crosses in front
    ".............#VVDTTMMOTTTMMMMTHOTMMDVV#.........", # y=37: Center helical twist
    # 38..40: Organic Gnarled Root Trunks (NO 45 DEGREE! Curving with vertical runs and knobby burls)
    "............#VDDTMMMMTTMMMMMDTTOMMDV#...........", # y=38: Roots branch outward
    "...........#VDDTMMMDV##VMMMMMMDV##DTMMDV#.......", # y=39: Two distinct curved root legs + center tendril
    "..........#VDDTMMMDV#...#VMMMMV#...#VDTMMDV#....", # y=40: Vertical / irregular curvature (not 45 deg!)
    # 41..44: Withered root feet gripping ground (5-6px thick bases, irregular gnarled contours)
    "..........#VDTMMMDV#....#VMMMMV#....#VDTMMDV#...", # y=41: Vertical run (x=10..18 and x=36..43)
    ".........#VVDTMMMDV#.....#DMMD#......#VDTMMDV#..", # y=42: Knobby burl
    "........#VVDMMMMDV#......#DMMD#.......#VDMMMDV#.", # y=43: Root feet splaying wide (8-10px)
    ".......#VVDMMMMMDV#......#VMMV#........#VDMMMDV#", # y=44: Gnarled claws gripping earth
    # 45..46: Ground Contact Shadow S (Alpha 130)
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..", # y=45
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....", # y=46
    # 47
    "................................................",
]

# Build 4 Animated Frames (Bubble rising and glowing pulse)
# Strictly maintaining Y-axis lock on all glass, roots, shadow S!
f2 = list(f1)
# Bubble 1 rises from y=29 to y=27
f2[27] = "........#HO#.#..BRRWYRRRRRRWRRRB...#.#MD#......."
f2[28] = ".......#THO#.#..QBRRYRRRRRRYRRRB...#..#TMD#......"
f2[29] = ".......#THOM#.#.QQBRRRRRRRRRRRBQ..#..#OTMD#......"
# Bubble 2 rises from y=27 to y=25
f2[25] = ".........#..#.P.BYRRRRRRRRRRWRRRYB..J#..#......."
f2[26] = "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......"
# New bubble forms at y=31
f2[31] = "........#TTHOM##..QQBBRRRRWRRBQQ..##.#HHOTMD#...."

f3 = list(f1)
# Bubble 1 reaches surface y=23
f3[23] = "..........#PK.P.QBRWYWWYYYYWWYRRBQ..J#.........."
# Bubble 2 reaches surface rim y=22 and pops with specular shine!
f3[22] = "..........#PK.PP.QBBBRRYYYYYYWWBBQ..J#.........."
# Bubble 3 rises to y=29
f3[29] = ".......#THOM#.#.QQBRRRRRRRRWYRBQ..#..#OTMD#......"
# Bubble 2 clear from y=27
f3[27] = "........#HO#.#..BRRRRRRRRRRRRRRB...#.#MD#......."

f4 = list(f1)
# Surface settles
f4[22] = "..........#PK.PP.QBBBRRYYYYYYRRBBQ..J#.........."
f4[23] = "..........#PK.P.QBRRYWWYYYYWWYRRBQ..J#.........."
# Bubble 3 rises to y=27
f4[27] = "........#HO#.#..BRRRRRRRRRRWYRRB...#.#MD#......."
f4[28] = ".......#THO#.#..QBRRRRRRRRRRRRRB...#..#TMD#......"
f4[29] = ".......#THOM#.#.QQBRRRRRRRRRRRBQ..#..#OTMD#......"
# Tiny micro-bubble at y=32
f4[32] = "........#DTHOMM##..QQQBBWBBQQQ..##..#HHOTMDD#...."

frames = [f1, f2, f3, f4]

# Render spritesheet and animated GIF
sheet_img = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
pil_frames = []

for f_idx, frame_data in enumerate(frames):
    f_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = f_img.load()
    for y in range(H):
        row = frame_data[y]
        for x in range(W):
            pix[x, y] = PALETTE.get(row[x], (0, 0, 0, 0))
    sheet_img.paste(f_img, (f_idx * W, 0))
    pil_frames.append(f_img)

# Save test outputs
sheet_img.save("test/test_flask_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_flask_sheet_4x.png")

# Save GIF
pil_frames[0].save(
    "test/test_flask_anim.gif",
    save_all=True,
    append_images=pil_frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    disposal=2
)

# 4x GIF for viewing
pil_frames_4x = [f.resize((W * 4, H * 4), Image.NEAREST) for f in pil_frames]
pil_frames_4x[0].save(
    "test/test_flask_anim_4x.gif",
    save_all=True,
    append_images=pil_frames_4x[1:],
    duration=int(1000 / FPS),
    loop=0,
    disposal=2
)

print("Generated all test files in test/ successfully!")
