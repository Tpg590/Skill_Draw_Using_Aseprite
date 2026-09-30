import os
import math
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

grid = [["." for _ in range(64)] for _ in range(64)]

def set_px(x, y, ch, force=False):
    if 0 <= x < 64 and 0 <= y < 64:
        if force or grid[y][x] == ".":
            grid[y][x] = ch

def get_px(x, y):
    if 0 <= x < 64 and 0 <= y < 64:
        return grid[y][x]
    return "."

def draw_circle(cx, cy, r, ch, force=False):
    for dy in range(-int(r)-1, int(r)+2):
        for dx in range(-int(r)-1, int(r)+2):
            if dx*dx + dy*dy <= r*r:
                set_px(int(cx + dx), int(cy + dy), ch, force)

def draw_capsule(x0, y0, x1, y1, r, ch, force=False):
    dist = math.hypot(x1 - x0, y1 - y0)
    steps = max(1, int(dist * 3))
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        draw_circle(x, y, r, ch, force)

# ----------------- LAYER 1: STONE FOUNDATION (y=56..61) -----------------
# 4 Rectangular stone blocks
blocks = [
    (8, 57, 19, 61),
    (21, 56, 32, 61),
    (34, 56, 44, 61),
    (46, 57, 56, 61),
]

for x1, y1, x2, y2 in blocks:
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if y == y1:
                set_px(x, y, "H", True) # Chipped lit stone rim
            elif y == y2:
                set_px(x, y, "D", True) # Shadowed bottom bevel
            elif x == x1 or x == x2:
                set_px(x, y, "D", True) # Edge shading
            else:
                set_px(x, y, "M", True) # Mid stone face

# Chiseled cracks in stone blocks (V)
stone_cracks = [
    (13, 57, 15, 60), (17, 59, 18, 61),
    (24, 56, 26, 60), (28, 58, 29, 61),
    (37, 57, 39, 61), (41, 56, 40, 59),
    (49, 58, 51, 61), (53, 57, 54, 60)
]
for x1, y1, x2, y2 in stone_cracks:
    draw_capsule(x1, y1, x2, y2, 0.6, "V", True)

# Mortar joints between blocks
for mx in [20, 33, 45]:
    for my in range(56, 62):
        set_px(mx, my, "#", True)

# ----------------- LAYER 2: BACKGROUND BRANCHES (Darkest D, V) -----------------
# Back-Left branch
bl_path = [(26, 24), (22, 21), (18, 17), (14, 13), (10, 9), (7, 6)]
for i in range(len(bl_path) - 1):
    r = 2.0 - (i * 0.25)
    draw_capsule(bl_path[i][0], bl_path[i][1], bl_path[i+1][0], bl_path[i+1][1], r, "D", True)
# Back-Left twigs
draw_capsule(18, 17, 13, 18, 1.0, "D", True)
draw_capsule(13, 18, 9, 19, 0.7, "D", True)
draw_capsule(14, 13, 13, 7, 0.8, "D", True)

# Back-Right branch
br_path = [(37, 24), (41, 21), (46, 17), (51, 13), (55, 9), (58, 6)]
for i in range(len(br_path) - 1):
    r = 2.0 - (i * 0.25)
    draw_capsule(br_path[i][0], br_path[i][1], br_path[i+1][0], br_path[i+1][1], r, "D", True)
# Back-Right twigs
draw_capsule(46, 17, 51, 18, 1.0, "D", True)
draw_capsule(51, 18, 55, 19, 0.7, "D", True)
draw_capsule(51, 13, 50, 7, 0.8, "D", True)

# Underside shadow V for background branches
draw_capsule(22, 22, 11, 11, 0.6, "V", True)
draw_capsule(41, 22, 53, 11, 0.6, "V", True)

# ----------------- LAYER 3: TRUNK CORE (CORKSCREW HELIX) -----------------
# Trunk spans y=24 to y=52, width 18 to 26 px
for y in range(24, 53):
    t = (y - 24) / (52 - 24)
    # Center slightly wandering for organic gnarl
    cx = 32.0 + math.sin(t * math.pi * 2.0) * 1.5
    w = 8.5 + t * 5.0 # half-width: from 8.5 (w=17) to 13.5 (w=27)
    x_left = int(cx - w)
    x_right = int(cx + w)
    for x in range(x_left, x_right + 1):
        set_px(x, y, "M", True)

# Apply corkscrew helical grain & deep seams (V, H, D)
# Diagonal spiral phase: angle ~35 deg (dx/dy ~ 1.2)
for y in range(24, 53):
    t = (y - 24) / (52 - 24)
    cx = 32.0 + math.sin(t * math.pi * 2.0) * 1.5
    w = 8.5 + t * 5.0
    x_left = int(cx - w)
    x_right = int(cx + w)
    for x in range(x_left, x_right + 1):
        # Helical coordinate: slant = x - 1.1 * y
        phase = (x - 1.1 * y) % 16.0
        # Phase 0..2: Deep spiral seam V
        if phase < 1.8:
            set_px(x, y, "V", True)
        # Phase 1.8..4.5: Lit strand crest H
        elif phase < 4.5:
            set_px(x, y, "H", True)
        # Phase 4.5..12.0: Mid strand M
        elif phase < 12.0:
            set_px(x, y, "M", True)
        # Phase 12.0..16.0: Recessed strand shadow D
        else:
            set_px(x, y, "D", True)

# Trunk side shading (ambient light from top-left)
for y in range(24, 53):
    t = (y - 24) / (52 - 24)
    cx = 32.0 + math.sin(t * math.pi * 2.0) * 1.5
    w = 8.5 + t * 5.0
    x_left = int(cx - w)
    x_right = int(cx + w)
    # Left lit edge
    if get_px(x_left, y) != ".":
        set_px(x_left, y, "H", True)
        set_px(x_left + 1, y, "H", True)
    # Right shaded edge
    if get_px(x_right, y) != ".":
        set_px(x_right, y, "D", True)
        set_px(x_right - 1, y, "D", True)

# ----------------- LAYER 4: ROOTS CLAWING OVER STONE (y=48..61) -----------------
# Left root claw: wraps over Block 1 down to ground
l_root = [(24, 49), (21, 52), (17, 55), (13, 57), (10, 59), (8, 61)]
for i in range(len(l_root) - 1):
    r = 2.5 - (i * 0.25)
    draw_capsule(l_root[i][0], l_root[i][1], l_root[i+1][0], l_root[i+1][1], r, "M", True)
    # Highlight on upper curve
    draw_capsule(l_root[i][0], l_root[i][1] - 0.7, l_root[i+1][0], l_root[i+1][1] - 0.7, r * 0.5, "H", True)
    # Underside shadow
    draw_capsule(l_root[i][0], l_root[i][1] + 0.8, l_root[i+1][0], l_root[i+1][1] + 0.8, r * 0.5, "D", True)

# Center root split plunging into stone gap
c_root1 = [(30, 52), (30, 55), (31, 58), (32, 61)]
for i in range(len(c_root1) - 1):
    draw_capsule(c_root1[i][0], c_root1[i][1], c_root1[i+1][0], c_root1[i+1][1], 1.8, "M", True)
    draw_capsule(c_root1[i][0] - 0.5, c_root1[i][1], c_root1[i+1][0] - 0.5, c_root1[i+1][1], 0.8, "H", True)

c_root2 = [(35, 52), (36, 56), (36, 59), (35, 61)]
for i in range(len(c_root2) - 1):
    draw_capsule(c_root2[i][0], c_root2[i][1], c_root2[i+1][0], c_root2[i+1][1], 1.8, "M", True)
    draw_capsule(c_root2[i][0] + 0.5, c_root2[i][1], c_root2[i+1][0] + 0.5, c_root2[i+1][1], 0.8, "D", True)

# Fissure crevice between center roots
draw_capsule(33, 55, 34, 61, 0.7, "V", True)

# Right root claw: wraps over Block 4
r_root = [(39, 49), (42, 52), (46, 55), (50, 57), (53, 59), (55, 61)]
for i in range(len(r_root) - 1):
    r = 2.5 - (i * 0.25)
    draw_capsule(r_root[i][0], r_root[i][1], r_root[i+1][0], r_root[i+1][1], r, "M", True)
    draw_capsule(r_root[i][0], r_root[i][1] - 0.7, r_root[i+1][0], r_root[i+1][1] - 0.7, r * 0.5, "H", True)
    draw_capsule(r_root[i][0], r_root[i][1] + 0.8, r_root[i+1][0], r_root[i+1][1] + 0.8, r * 0.5, "D", True)

# ----------------- LAYER 5: SIDE BRANCHES (WEST & EAST) -----------------
# West limb (Left)
w_limb = [(23, 26), (19, 27), (15, 28), (11, 28), (8, 26), (5, 23), (2, 20)]
for i in range(len(w_limb) - 1):
    r = 2.4 - (i * 0.25)
    draw_capsule(w_limb[i][0], w_limb[i][1], w_limb[i+1][0], w_limb[i+1][1], r, "M", True)
    draw_capsule(w_limb[i][0], w_limb[i][1] - 0.6, w_limb[i+1][0], w_limb[i+1][1] - 0.6, r * 0.5, "H", True)
    draw_capsule(w_limb[i][0], w_limb[i][1] + 0.6, w_limb[i+1][0], w_limb[i+1][1] + 0.6, r * 0.5, "D", True)

# West twigs
draw_capsule(15, 28, 12, 32, 1.2, "M", True)
draw_capsule(12, 32, 8, 34, 0.7, "M", True)
draw_capsule(8, 26, 5, 29, 0.8, "M", True)
draw_capsule(2, 20, 1, 16, 0.7, "H", True)

# East limb (Right)
e_limb = [(41, 26), (45, 27), (49, 28), (53, 28), (57, 26), (60, 23), (62, 20)]
for i in range(len(e_limb) - 1):
    r = 2.4 - (i * 0.25)
    draw_capsule(e_limb[i][0], e_limb[i][1], e_limb[i+1][0], e_limb[i+1][1], r, "M", True)
    draw_capsule(e_limb[i][0], e_limb[i][1] - 0.6, e_limb[i+1][0], e_limb[i+1][1] - 0.6, r * 0.5, "H", True)
    draw_capsule(e_limb[i][0], e_limb[i][1] + 0.6, e_limb[i+1][0], e_limb[i+1][1] + 0.6, r * 0.5, "D", True)

# East twigs
draw_capsule(49, 28, 53, 32, 1.2, "M", True)
draw_capsule(53, 32, 57, 34, 0.7, "M", True)
draw_capsule(57, 26, 60, 29, 0.8, "M", True)
draw_capsule(62, 20, 63, 16, 0.7, "H", True)

# ----------------- LAYER 6: CROWN ANTLER HORNS (NORTH) -----------------
# Left Crown Horn
l_horn = [(26, 23), (23, 19), (20, 14), (18, 9), (20, 4)]
for i in range(len(l_horn) - 1):
    r = 2.2 - (i * 0.3)
    draw_capsule(l_horn[i][0], l_horn[i][1], l_horn[i+1][0], l_horn[i+1][1], r, "M", True)
    draw_capsule(l_horn[i][0] - 0.5, l_horn[i][1], l_horn[i+1][0] - 0.5, l_horn[i+1][1], r * 0.5, "H", True)
    draw_capsule(l_horn[i][0] + 0.5, l_horn[i][1], l_horn[i+1][0] + 0.5, l_horn[i+1][1], r * 0.5, "D", True)
draw_capsule(23, 19, 25, 12, 1.0, "M", True)
draw_capsule(25, 12, 26, 6, 0.7, "H", True)

# Right Crown Horn
r_horn = [(38, 23), (41, 19), (44, 14), (46, 9), (44, 4)]
for i in range(len(r_horn) - 1):
    r = 2.2 - (i * 0.3)
    draw_capsule(r_horn[i][0], r_horn[i][1], r_horn[i+1][0], r_horn[i+1][1], r, "M", True)
    draw_capsule(r_horn[i][0] - 0.5, r_horn[i][1], r_horn[i+1][0] - 0.5, r_horn[i+1][1], r * 0.5, "H", True)
    draw_capsule(r_horn[i][0] + 0.5, r_horn[i][1], r_horn[i+1][0] + 0.5, r_horn[i+1][1], r * 0.5, "D", True)
draw_capsule(41, 19, 39, 12, 1.0, "M", True)
draw_capsule(39, 12, 38, 6, 0.7, "H", True)

# Center Spire
c_spire = [(32, 22), (31, 16), (32, 10), (31, 4), (30, 2)]
for i in range(len(c_spire) - 1):
    r = 1.8 - (i * 0.3)
    draw_capsule(c_spire[i][0], c_spire[i][1], c_spire[i+1][0], c_spire[i+1][1], r, "M", True)
    draw_capsule(c_spire[i][0] - 0.4, c_spire[i][1], c_spire[i+1][0] - 0.4, c_spire[i+1][1], r * 0.4, "H", True)

# ----------------- LAYER 7: FOREGROUND OVERLAPPING BRANCH (SOUTH) -----------------
# Cast shadow on trunk beneath the foreground branch
# Path: from (28, 34) down-right to (48, 41)
fg_path = [(28, 34), (31, 35), (35, 36), (39, 37), (43, 39), (47, 40), (51, 42)]

# First paint cast shadow on trunk 2-3 px below the branch path
for pt in [(31, 37), (35, 38), (39, 39), (43, 41), (46, 42)]:
    draw_circle(pt[0], pt[1], 1.5, "D", True)
    draw_circle(pt[0], pt[1] - 0.5, 0.8, "V", True)

# Now draw the foreground branch on top!
for i in range(len(fg_path) - 1):
    r = 2.2 - (i * 0.15)
    draw_capsule(fg_path[i][0], fg_path[i][1], fg_path[i+1][0], fg_path[i+1][1], r, "M", True)
    # Bright highlight H on top crest of foreground branch
    draw_capsule(fg_path[i][0], fg_path[i][1] - 0.7, fg_path[i+1][0], fg_path[i+1][1] - 0.7, r * 0.5, "H", True)
    # Dark shadow D on bottom edge of foreground branch
    draw_capsule(fg_path[i][0], fg_path[i][1] + 0.7, fg_path[i+1][0], fg_path[i+1][1] + 0.7, r * 0.5, "D", True)

# Foreground branch twigs
draw_capsule(47, 40, 52, 38, 1.0, "M", True)
draw_capsule(52, 38, 56, 36, 0.6, "H", True)
draw_capsule(51, 42, 55, 45, 0.9, "M", True)
draw_capsule(55, 45, 57, 47, 0.6, "D", True)

# ----------------- LAYER 8: OUTLINE PASS (#) -----------------
# Complete Terraria outline # around all solid pixels
to_outline = []
for y in range(64):
    for x in range(64):
        if grid[y][x] == ".":
            # Check 8 neighbors for tight silhouette
            is_border = False
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 64 and 0 <= ny < 64:
                        if grid[ny][nx] not in [".", "S", "#"]:
                            is_border = True
                            break
                if is_border: break
            if is_border:
                to_outline.append((x, y))

for x, y in to_outline:
    grid[y][x] = "#"

# Also outline the foreground branch where it overlaps the trunk!
# The foreground branch borders on the trunk need # to pop out
for pt in [(28, 32), (32, 33), (36, 34), (40, 35), (44, 37), (29, 36), (33, 38), (37, 39), (41, 41)]:
    if get_px(pt[0], pt[1]) not in [".", "S"]:
        set_px(pt[0], pt[1], "#", True)

# ----------------- LAYER 9: GROUND SHADOW S (Alpha 130) -----------------
# Beneath stone blocks and roots
for x in range(6, 59):
    if get_px(x, 62) == ".":
        set_px(x, 62, "S", True)
for x in range(10, 55):
    if get_px(x, 63) == ".":
        set_px(x, 63, "S", True)

print("Full masterpiece painted.")

# Render image
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
for y in range(64):
    for x in range(64):
        ch = grid[y][x]
        col = PALETTE.get(ch)
        if col:
            img.putpixel((x, y), col)

img.save("masterpiece_tree_1x.png")
img4x = img.resize((256, 256), Image.NEAREST)
img4x.save("masterpiece_tree_4x.png")

print("Generated masterpiece_tree_1x.png and masterpiece_tree_4x.png!")
