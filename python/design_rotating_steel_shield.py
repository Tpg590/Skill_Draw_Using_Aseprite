import os
import math
from PIL import Image

W, H = 48, 48

# Terraria Style Metallic Palette (Silver-Bright Steel, Golden Cross, Brown Leather Straps)
PALETTE = {
    ".": None,
    "S": (16, 20, 26, 130),     # Floating ground contact shadow (Alpha 130)
    "#": (14, 18, 24, 255),     # Near-black Terraria outline (#0e1218)
    
    # Steel Shield Metal (Silver/Bright Steel, high contrast)
    "P": (240, 248, 255, 255), # Specular bright white steel highlight (#f0f8ff)
    "A": (185, 200, 218, 255), # Light silver plate (#b9c8da)
    "B": (115, 132, 154, 255), # Mid steel plate (#73849a)
    "C": (60, 74, 94, 255),    # Dark shaded steel (#3c4a5e)
    "D": (30, 38, 50, 255),    # Deep dark metal cavity / shadow (#1e2632)
    
    # Golden Heraldic Cross (Front Embossed Emblem)
    "J": (255, 230, 95, 255),  # Pure gold specular highlight (#ffe65f)
    "G": (215, 155, 25, 255),  # Rich gold midtone (#d79b19)
    "K": (130, 85, 12, 255),   # Shaded antique bronze/gold border (#82550c)
    
    # Leather Arm Straps (Back Interior Straps)
    "E": (185, 115, 60, 255),  # Leather strap highlight (#b9733c)
    "U": (125, 70, 30, 255),   # Leather strap rich brown (#7d461e)
    "Z": (68, 34, 12, 255),    # Leather deep crease / shadow (#44220c)
}

PALETTE_HEX = {
    ".": None,
    "S": "#10141a",
    "#": "#0e1218",
    "P": "#f0f8ff",
    "A": "#b9c8da",
    "B": "#73849a",
    "C": "#3c4a5e",
    "D": "#1e2632",
    "J": "#ffe65f",
    "G": "#d79b19",
    "K": "#82550c",
    "E": "#b9733c",
    "U": "#7d461e",
    "Z": "#44220c",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_shadow(grid, w_half):
    # Rule 3.3 & 4.1: Ground shadow fixed at Y=40..41
    for y in (40, 41):
        cur_w = w_half if y == 40 else max(2, w_half - 2)
        for x in range(24 - cur_w, 24 + cur_w + 1):
            set_p(grid, x, y, "S")

# FRAME 1: FRONT FULL VIEW (W = 20px, X = 14..33, Y = 12..33)
def build_f1():
    g = empty_grid()
    draw_shadow(g, 9)
    
    profile = {
        12: (17, 30), # W=14
        13: (15, 32), # W=18
        14: (14, 33), # W=20
        15: (14, 33),
        16: (14, 33),
        17: (14, 33),
        18: (14, 33),
        19: (14, 33),
        20: (14, 33),
        21: (14, 33),
        22: (15, 32),
        23: (15, 32),
        24: (16, 31),
        25: (16, 31),
        26: (17, 30),
        27: (18, 29),
        28: (19, 28),
        29: (20, 27),
        30: (21, 26),
        31: (22, 25),
        32: (23, 24),
        33: (23, 24),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            # Steel face shading: Left specular highlight rim, midtone center, shadow right
            if x <= x1 + 2:
                set_p(g, x, y, "P" if (y <= 22 and x == x1 + 1) else "A")
            elif x >= x2 - 2:
                set_p(g, x, y, "C" if x == x2 - 1 else "B")
            else:
                set_p(g, x, y, "B" if x < 24 else "C")

    # Top bevel highlight
    for x in range(18, 24):
        set_p(g, x, 13, "P")

    # EMBOSSED GOLDEN CROSS (Front Emblem):
    # Vertical beam: X=23..24, Y=15..28
    for y in range(15, 29):
        set_p(g, 22, y, "K")
        set_p(g, 23, y, "J")
        set_p(g, 24, y, "G")
        set_p(g, 25, y, "K")
    # Horizontal beam: X=17..30, Y=18..19
    for x in range(17, 31):
        set_p(g, x, 17, "K")
        set_p(g, x, 18, "J" if x < 24 else "G")
        set_p(g, x, 19, "G" if x < 24 else "K")
        set_p(g, x, 20, "K")
    # Gold cross center shine
    set_p(g, 23, 18, "J")
    set_p(g, 23, 19, "J")
    set_p(g, 24, 18, "G")
    set_p(g, 24, 19, "G")

    # Steel rivets on corners
    set_p(g, 16, 14, "P")
    set_p(g, 31, 14, "A")
    set_p(g, 16, 22, "A")
    set_p(g, 31, 22, "B")

    return g

# FRAME 2: FRONT TURNED OBLIQUE (45° Rotate, W = 13px, X = 18..30)
def build_f2():
    g = empty_grid()
    draw_shadow(g, 6)
    
    # Projected width = 13px (compressed horizontally by ~0.65)
    profile = {
        12: (20, 28), # W=9
        13: (19, 29), # W=11
        14: (18, 30), # W=13
        15: (18, 30),
        16: (18, 30),
        17: (18, 30),
        18: (18, 30),
        19: (18, 30),
        20: (18, 30),
        21: (18, 30),
        22: (19, 29),
        23: (19, 29),
        24: (19, 29),
        25: (20, 28),
        26: (20, 28),
        27: (21, 27),
        28: (21, 27),
        29: (22, 26),
        30: (22, 26),
        31: (23, 25),
        32: (23, 24),
        33: (23, 24),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if x <= x1 + 2:
                set_p(g, x, y, "P" if x == x1 + 1 else "A")
            elif x >= x2 - 2:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "B")

    # Compressed Golden Cross:
    # Vertical beam: X=24..25, Y=15..28
    for y in range(15, 29):
        set_p(g, 23, y, "K")
        set_p(g, 24, y, "J")
        set_p(g, 25, y, "G")
        set_p(g, 26, y, "K")
    # Horizontal beam (compressed width X=20..28):
    for x in range(20, 29):
        set_p(g, x, 17, "K")
        set_p(g, x, 18, "J" if x < 25 else "G")
        set_p(g, x, 19, "G" if x < 25 else "K")
        set_p(g, x, 20, "K")

    return g

# FRAME 3: PURE SIDE VIEW (90° Rotate, W = 4px, X = 22..25)
# CRITICAL REQUIREMENT 2:
# Bảo toàn độ dày mép: Khi nhìn nghiêng 90 độ, khiên phải có độ dày 3-4 pixel thể hiện khối kim loại thật sự,
# cấm vẽ thành một đường chỉ 1px mỏng tang như tờ giấy!
# C-Curve: Front edge bulges forward in a cylindrical curve!
def build_f3():
    g = empty_grid()
    draw_shadow(g, 3) # Narrow shadow
    
    # 3-4 pixel solid metal thickness profile with convex C-curve:
    # Front face on right (X=24..25), back rim on left (X=21..22)
    profile = {
        12: (22, 24), # W=3
        13: (22, 25), # W=4
        14: (22, 25), # W=4
        15: (22, 25), # W=4
        16: (22, 25), # W=4
        17: (23, 26), # W=4 (C-curve bulges forward to X=26)
        18: (23, 26), # W=4
        19: (23, 26), # W=4
        20: (23, 26), # W=4
        21: (23, 26), # W=4
        22: (23, 26), # W=4
        23: (22, 25), # W=4
        24: (22, 25), # W=4
        25: (22, 25), # W=4
        26: (22, 25), # W=4
        27: (22, 24), # W=3
        28: (22, 24), # W=3
        29: (22, 24), # W=3
        30: (22, 24), # W=3
        31: (22, 24), # W=3
        32: (23, 24), # W=2
        33: (23, 24), # Pointed tip
    }
    for y, (x1, x2) in profile.items():
        # Back edge outline
        set_p(g, x1, y, "#")
        # Front outer edge outline
        set_p(g, x2, y, "#")
        # Inside solid 3-4px metal thickness!
        for x in range(x1 + 1, x2):
            if x == x2 - 1:
                # Front specular highlight edge running along entire front rim!
                set_p(g, x, y, "P" if y in range(15, 26) else "A")
            elif x == x1 + 1:
                # Solid metal interior
                set_p(g, x, y, "B" if y in range(16, 24) else "C")
            else:
                set_p(g, x, y, "A")

    # Cross section of the golden emblem plate visible on the front rim!
    set_p(g, 25, 18, "J")
    set_p(g, 25, 19, "G")
    
    # Back strap mount pin visible on the back rim
    set_p(g, 22, 17, "U")
    set_p(g, 22, 23, "U")

    return g

# FRAME 4: BACK TURNED OBLIQUE (135° Rotate, W = 13px, X = 18..30)
# Looking into the back cavity: leather straps become visible in perspective!
def build_f4():
    g = empty_grid()
    draw_shadow(g, 6)
    
    profile = {
        12: (20, 28),
        13: (19, 29),
        14: (18, 30),
        15: (18, 30),
        16: (18, 30),
        17: (18, 30),
        18: (18, 30),
        19: (18, 30),
        20: (18, 30),
        21: (18, 30),
        22: (19, 29),
        23: (19, 29),
        24: (19, 29),
        25: (20, 28),
        26: (20, 28),
        27: (21, 27),
        28: (21, 27),
        29: (22, 26),
        30: (22, 26),
        31: (23, 25),
        32: (23, 24),
        33: (23, 24),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            # Inner hollow metal cavity (Dark brushed metal)
            if x in (x1 + 1, x2 - 1) or y in (12, 13, 32, 33):
                set_p(g, x, y, "B" if x == x1 + 1 else "C") # Raised border rim
            else:
                set_p(g, x, y, "D" if x > 23 else "C")      # Deep dark hollow

    # Crossed Leather Straps in perspective (quai đeo da nâu):
    # Strap 1: top-left to bottom-right
    for (x, y) in [(20, 16), (21, 17), (22, 18), (23, 19), (24, 20), (25, 21), (26, 22), (27, 23)]:
        set_p(g, x, y, "E")
        set_p(g, x, y + 1, "U")
    # Strap 2: top-right to bottom-left
    for (x, y) in [(27, 16), (26, 17), (25, 18), (24, 19), (23, 20), (22, 21), (21, 22), (20, 23)]:
        set_p(g, x, y, "U")
        set_p(g, x, y + 1, "Z")
    # Center buckle rivet
    set_p(g, 24, 19, "G")
    set_p(g, 24, 20, "J")

    return g

# FRAME 5: BACK FULL VIEW (180° Rotate, W = 20px, X = 14..33, Y = 12..33)
# FULL VIEW OF SHIELD INTERIOR WITH TWO CROSSED LEATHER STRAPS!
def build_f5():
    g = empty_grid()
    draw_shadow(g, 9)
    
    profile = {
        12: (17, 30),
        13: (15, 32),
        14: (14, 33),
        15: (14, 33),
        16: (14, 33),
        17: (14, 33),
        18: (14, 33),
        19: (14, 33),
        20: (14, 33),
        21: (14, 33),
        22: (15, 32),
        23: (15, 32),
        24: (16, 31),
        25: (16, 31),
        26: (17, 30),
        27: (18, 29),
        28: (19, 28),
        29: (20, 27),
        30: (21, 26),
        31: (22, 25),
        32: (23, 24),
        33: (23, 24),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            # Thick outer rim bevel around perimeter
            is_rim = (x in (x1 + 1, x1 + 2, x2 - 2, x2 - 1) or y in (12, 13, 31, 32, 33))
            if is_rim:
                set_p(g, x, y, "A" if x < 24 else "B")
            else:
                # Deep recessed inner cavity
                set_p(g, x, y, "D" if x > 23 else "C")

    # 2 QUAI ĐEO BẰNG DA MÀU NÂU BẮT CHÉO (Two crossed brown leather straps):
    # Strap 1: Diagonal from top-left (16, 16) to bottom-right (30, 26)
    strap1_pts = [
        (16, 16), (17, 16), (17, 17), (18, 17), (19, 18), (20, 19),
        (21, 20), (22, 20), (23, 21), (24, 22), (25, 23), (26, 23),
        (27, 24), (28, 25), (29, 25), (30, 26)
    ]
    for x, y in strap1_pts:
        set_p(g, x, y, "E")
        set_p(g, x, y + 1, "U")
        set_p(g, x, y - 1, "Z")

    # Strap 2: Diagonal from top-right (30, 16) to bottom-left (16, 26)
    strap2_pts = [
        (30, 16), (29, 16), (29, 17), (28, 17), (27, 18), (26, 19),
        (25, 20), (24, 20), (23, 21), (22, 22), (21, 23), (20, 23),
        (19, 24), (18, 25), (17, 25), (16, 26)
    ]
    for x, y in strap2_pts:
        set_p(g, x, y, "E")
        set_p(g, x, y + 1, "U")
        set_p(g, x, y - 1, "Z")

    # Center brass buckle & rivet plate at intersection (23..24, 21..22)
    set_p(g, 23, 20, "K")
    set_p(g, 24, 20, "K")
    set_p(g, 23, 21, "J")
    set_p(g, 24, 21, "G")
    set_p(g, 23, 22, "G")
    set_p(g, 24, 22, "K")

    # Corner mounting brass rivets on inner rim
    set_p(g, 16, 15, "J")
    set_p(g, 31, 15, "G")
    set_p(g, 16, 27, "J")
    set_p(g, 31, 27, "G")

    return g

# FRAME 6: ROTATING OBLIQUE BACK TO FRONT (W = 13px, X = 18..30)
# Front face returns into view from opposite angle, golden cross visible in perspective!
def build_f6():
    g = empty_grid()
    draw_shadow(g, 6)
    
    profile = {
        12: (19, 27),
        13: (18, 28),
        14: (17, 29),
        15: (17, 29),
        16: (17, 29),
        17: (17, 29),
        18: (17, 29),
        19: (17, 29),
        20: (17, 29),
        21: (17, 29),
        22: (18, 28),
        23: (18, 28),
        24: (18, 28),
        25: (19, 27),
        26: (19, 27),
        27: (20, 26),
        28: (20, 26),
        29: (21, 25),
        30: (21, 25),
        31: (22, 24),
        32: (23, 24),
        33: (23, 24),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if x <= x1 + 2:
                set_p(g, x, y, "A")
            elif x >= x2 - 2:
                set_p(g, x, y, "P" if x == x2 - 1 else "B")
            else:
                set_p(g, x, y, "B")

    # Golden cross emerging in perspective:
    # Vertical beam: X=22..23, Y=15..28
    for y in range(15, 29):
        set_p(g, 21, y, "K")
        set_p(g, 22, y, "J")
        set_p(g, 23, y, "G")
        set_p(g, 24, y, "K")
    # Horizontal beam (compressed width X=19..26):
    for x in range(19, 27):
        set_p(g, x, 17, "K")
        set_p(g, x, 18, "J" if x < 23 else "G")
        set_p(g, x, 19, "G" if x < 23 else "K")
        set_p(g, x, 20, "K")

    return g

frames = [build_f1(), build_f2(), build_f3(), build_f4(), build_f5(), build_f6()]

# Strict verification of requirements:
print("--- VERIFICATION OF SHIELD REQUIREMENTS ---")
# 1. Front vs Back distinctness
f1_gold_count = sum(1 for row in frames[0] for c in row if c in ("J", "G", "K"))
f1_leather_count = sum(1 for row in frames[0] for c in row if c in ("E", "U", "Z"))
f5_gold_count = sum(1 for row in frames[4] for c in row if c in ("J", "G", "K"))
f5_leather_count = sum(1 for row in frames[4] for c in row if c in ("E", "U", "Z"))
print(f"Frame 1 (Front): Gold pixels = {f1_gold_count}, Leather pixels = {f1_leather_count}")
print(f"Frame 5 (Back): Gold pixels = {f5_gold_count}, Leather pixels = {f5_leather_count}")
assert f1_gold_count > 30 and f1_leather_count == 0, "Frame 1 must have gold cross and no leather straps!"
assert f5_leather_count > 30, "Frame 5 must have prominent crossed leather straps!"

# 2. Side thickness at Frame 3
f3_widths = []
for y in range(14, 27):
    row = frames[2][y]
    solid_indices = [x for x, c in enumerate(row) if c not in (".", "S")]
    if solid_indices:
        w_row = max(solid_indices) - min(solid_indices) + 1
        f3_widths.append(w_row)
avg_w_f3 = sum(f3_widths) / len(f3_widths)
print(f"Frame 3 (Side view): Average thickness across main body = {avg_w_f3:.2f}px (Range: {min(f3_widths)}..{max(f3_widths)})")
assert min(f3_widths) >= 3, f"Frame 3 edge thickness cannot be 1px! Found {min(f3_widths)}"

os.makedirs("test", exist_ok=True)
images = []
for idx, f in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            val = PALETTE.get(c)
            if val:
                img.putpixel((x, y), val)
    img.save(f"test/shield_f{idx+1}.png")
    images.append(img)

images[0].save(
    "test/shield_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=167,
    loop=0,
    disposal=2
)

print("Shield test frames generated successfully.")
