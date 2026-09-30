import os
from PIL import Image

W, H = 32, 48
FPS = 8

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "#": (18, 10, 20, 255),    # Near-black Terraria outline with deep violet tint (#120a14)
    "S": (20, 10, 24, 130),    # Soft ground shadow (Alpha 130)
    
    # Iron Torch Brazier & Shaft
    "I": (160, 172, 195, 255), # Iron highlight (#a0acb9)
    "F": (85, 95, 112, 255),   # Iron midtone (#555f70)
    "L": (42, 48, 58, 255),    # Iron shadow (#2a303a)
    
    # Carved Stone Pedestal
    "G": (125, 135, 150, 255), # Stone highlight (#7d8796)
    "D": (72, 80, 90, 255),    # Stone midtone (#48505a)
    "N": (38, 42, 50, 255),    # Stone shadow (#262a32)
    
    # OSL Pink Glow on Metal & Stone
    "O": (255, 130, 230, 255), # Vivid magic pink glow reflection (#ff82e6)
    
    # Magic Violet/Pink Flame
    "W": (255, 255, 255, 255), # White hot core (#ffffff)
    "K": (255, 195, 245, 255), # Pale pink sparks / inner glow (#ffc3f5)
    "P": (245, 65, 195, 255),  # Vivid hot magenta/pink (#f541c3)
    "M": (155, 25, 175, 255),  # Deep violet-purple flame (#9b19af)
    "V": (75, 8, 105, 255),    # Dark magic flame rim/smoke (#4b0869)
}

# Master Sculpted Frame 1 (Flame leans right; Embers: A at y=8, B at y=10, C at y=12)
f1 = [
    # 0..4: Sky
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    # 5..7: Upper air
    "................................",
    "................................",
    "................................",
    # 8..11: Flame tips & Detached Embers (Rule 4.6: 3 detached embers!)
    ".....................KW.........", # y=8: Ember A (KW) at x=21..22
    "....................VPMV........", # y=9: Right flame peak
    "..........KW.......VPPPMV.......", # y=10: Ember B (KW) at x=10..11
    "........VPMV......VPPKPMV.......", # y=11: Left tongue rises
    # 12..16: Dancing magic flame with organic hot core (NO FLAT WHITE BLOCKS!)
    ".........KW......VPPKWKPMV......", # y=12: Ember C (KW) at x=9..10
    "........VPMV....VPPKKWKKPMV.....", # y=13
    ".......VPPPMV..VPPKKWWKKKPMV....", # y=14
    "......VPPKWPMVVPPKKWWWWKKPMV....", # y=15
    "......VPPKWWPKKPPKKWWWWKKPMV....", # y=16
    # 17..20: Lower flame & oil surface
    "......VPPKKWWWWKKKKWWWWKKPMV....", # y=17
    ".......VPPKKWWWWWWWWWWKKPPMV....", # y=18
    "........VPPPKKKWWWWWKKKPPMV.....", # y=19
    ".........VVPPPPKKKKKPPPPMV......", # y=20
    # 21..26: Flared Gothic Iron Brazier Bowl with OSL pink glow on rim
    ".......###OOOOOOOOOOOOO###......", # y=21: Brazier rim with OSL
    "......#IIF#OOOOOOOOOOO#LFF#.....", # y=22: Flared chalice cup
    ".......#IIF###########LFF#......", # y=23: Iron bowl struts
    "........#IIFFFFFFFFFFFLL#.......", # y=24: Curving bowl belly
    ".........###IIFFFFFLL###........", # y=25: Bowl base
    "..............#III#.............", # y=26: Top collar ring
    # 27..38: Iron Torch Shaft / Stem
    "..............#FIL#.............", # y=27
    "..............#FIL#.............", # y=28
    "..............#FIL#.............", # y=29
    "..............#FIL#.............", # y=30
    ".............##FIL##............", # y=31: Mid collar ring
    "............#IIIFLLL#...........", # y=32
    ".............##FIL##............", # y=33
    "..............#FIL#.............", # y=34
    "..............#FIL#.............", # y=35
    "..............#FIL#.............", # y=36
    "..............#FIL#.............", # y=37
    ".............##FIL##............", # y=38: Base collar
    # 39..43: Carved Stone Pedestal (Terraria blocky stone base)
    "...........##########...........", # y=39: Top stone step
    "..........#GGGGGDDDDD#..........", # y=40
    "........################........", # y=41: Bottom stone step
    ".......#GGGGGGGGDDDDDDDN#.......", # y=42
    ".......#GGGGDDDDDDDNNNNN#.......", # y=43: Pedestal base contacts ground
    # 44..46: Soft Oval Ellipse Ground Shadow S (Alpha 130 - Rule 2.2 & 3.1.4!)
    "......SSSSSSSSSSSSSSSSSSSS......", # y=44: Row 1 of ellipse (width 20)
    "........SSSSSSSSSSSSSSSS........", # y=45: Row 2 of ellipse (width 16)
    "...........SSSSSSSSSS...........", # y=46: Row 3 of ellipse (width 10, tapering)
    # 47
    "................................",
]

# Frame 2: Flame whips left! Ember A rises to y=5, Ember B rises to y=7, Ember C rises to y=9
f2 = list(f1)
# Embers ascending
f2[5]  = "......................KW........" # Ember A rises to y=5, x=22..23
f2[7]  = ".........KW....................." # Ember B rises to y=7, x=9..10
f2[8]  = "................................" # clear old
f2[9]  = "............KW.................." # Ember C rises to y=9, x=12..13
f2[10] = "................................"
# Flame changes: Left surges, right shrinks (>20% difference)
f2[11] = "........VPMV...................." # Left flame peak
f2[12] = ".......VPPPMV.........VPMV......"
f2[13] = "......VPPKWPMV.......VPPPMV....."
f2[14] = "......VPPKWWPMV.....VPPKPMV....."
f2[15] = "......VPPKKWWPMV...VPPKKWPMV...."
f2[16] = "......VPPKKWWKKPPKKWWKKKKPMV...."
f2[17] = "......VPPKKWWWWWWWWWWKKKKPMV...."
f2[18] = ".......VPPPKKKWWWWWKKKPPMV......"
f2[19] = "........VVPPPPKKKKKPPPPMV......."
f2[20] = ".........VVVPPPPPPPPPVV........."

# Frame 3: Flame splits into twin dancing horns!
# Ember A rises to y=2, Ember B rises to y=4, Ember C rises to y=6
f3 = list(f1)
# Embers ascending
f3[2]  = ".....................KW........." # Ember A rises to y=2, x=21..22
f3[4]  = "..........KW...................." # Ember B rises to y=4, x=10..11
f3[6]  = ".............KW................." # Ember C rises to y=6, x=13..14
f3[8]  = "................................"
f3[10] = "................................"
f3[12] = "................................"
# Flame changes: Dual horn shapes
f3[11] = ".......VPMV.........VPMV........" # Twin horns left and right!
f3[12] = "......VPPPMV.......VPPPMV......."
f3[13] = ".....VPPKWPMV.....VPPKWPMV......"
f3[14] = ".....VPPKWWPMV...VPPKWWPMV......"
f3[15] = ".....VPPKKWWPMVVVPPKKWWPMV......"
f3[16] = "......VPPKKWWKKKKKWWKKKKPMV....."
f3[17] = "......VPPKKWWWWWWWWWWKKKPMV....."
f3[18] = ".......VPPPKKKWWWWWKKKPPMV......"
f3[19] = "........VVPPPPKKKKKPPPPMV......."
f3[20] = ".........VVVPPPPPPPPPVV........."

# Frame 4: Flame swirls central peak!
# Ember A dissolves! Ember B rises to y=1, Ember C rises to y=3
f4 = list(f1)
# Embers ascending
f4[1]  = "...........KW..................." # Ember B rises to y=1, x=11..12 (near top!)
f4[3]  = "..............KW................" # Ember C rises to y=3, x=14..15
f4[8]  = "................................"
f4[10] = "................................"
f4[12] = "................................"
# Flame changes: Central tall swirl
f4[9]  = "...............VPMV............." # Tall center swirl peak!
f4[10] = "..............VPPPMV............"
f4[11] = ".............VPPKWPMV..........."
f4[12] = "......VPMV..VPPKWWPMV..........."
f4[13] = ".....VPPPMVVPPKKWWPMV...VPMV...."
f4[14] = ".....VPPKWKKWWWWKKPMV..VPPPMV..."
f4[15] = "......VPPKKWWWWWKKPMVVVPPKWPMV.."
f4[16] = "......VPPKKWWWWWWWWWWKKKKPMV...."
f4[17] = "......VPPKKWWWWWWWWWWKKKKPMV...."
f4[18] = ".......VPPPKKKWWWWWKKKPPMV......"
f4[19] = "........VVPPPPKKKKKPPPPMV......."
f4[20] = ".........VVVPPPPPPPPPVV........."

frames = [f1, f2, f3, f4]

# Validate row lengths across all frames
for f_idx, fr in enumerate(frames):
    for r_idx, r in enumerate(fr):
        if len(r) != 32:
            raise ValueError(f"Frame {f_idx+1} row {r_idx} has length {len(r)}, expected 32!")

print("All 4 frames successfully validated (32x48)!")

# Calculate flame area difference between consecutive frames (Rule 4.7 verification)
def flame_pixels(fr):
    flame_chars = set("WKPMV")
    pts = set()
    for y in range(8, 21):
        for x in range(W):
            if fr[y][x] in flame_chars:
                pts.add((x, y))
    return pts

for i in range(4):
    p1 = flame_pixels(frames[i])
    p2 = flame_pixels(frames[(i + 1) % 4])
    diff = len(p1 ^ p2) # symmetric difference
    pct = diff / len(p1) * 100
    print(f"Frame {i+1} -> Frame {((i+1)%4)+1} Flame Area Variation: {pct:.1f}% (Rule 4.7 requires >= 15%)")

# Render test sheet
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

os.makedirs("test", exist_ok=True)
sheet_img.save("test/test_torch_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_torch_sheet_4x.png")

print("Generated test/test_torch_sheet_4x.png successfully!")
