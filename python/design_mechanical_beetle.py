import math
from PIL import Image

W, H = 48, 48

# Single-character Stardew Valley Palette:
# Strict 1 char per pixel, NO #000000!
PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (30, 18, 24, 130),     # Soft contact ground shadow (Alpha 130)
    "#": (42, 22, 16, 255),     # Warm dark espresso outline (#2a1610 - NO #000000!)
    
    # Polished Warm Brass / Gold Filigree
    "A": (255, 230, 128, 255), # Specular brass highlight (#ffe680)
    "B": (230, 168, 32, 255),  # Warm polished brass midtone (#e6a820)
    "C": (156, 100, 16, 255),  # Shaded bronze/brass (#9c6410)
    "D": (92, 54, 12, 255),    # Deep bronze recess (#5c360c)
    
    # Warm Hardwood Carapace Shell (Turtle plates)
    "W": (200, 120, 48, 255),  # Shell highlight wood plate (#c87830)
    "X": (158, 74, 24, 255),   # Shell warm amber midtone (#9e4a18)
    "Z": (90, 36, 12, 255),    # Shell deep mahogany shadow (#5a240c)
    "K": (56, 20, 8, 255),     # Shell seam crevice (#381408)
    
    # Clockwork Gears & Mechanical Claw Legs (Iron/Bronze alloy)
    "H": (180, 190, 200, 255), # Metal leg highlight (#b4bec8)
    "M": (120, 130, 142, 255), # Metal leg midtone (#78828e)
    "L": (68, 76, 88, 255),    # Metal leg shadow (#444c58)
    
    # Glowing Topaz Eyes / Clockwork Energy Core
    "E": (255, 238, 102, 255), # Glowing topaz yellow (#ffee66)
    "Q": (230, 144, 0, 255),   # Deep amber glow (#e69000)
}

PALETTE_HEX = {
    ".": None,
    "S": "#1e1218",
    "#": "#2a1610",
    "A": "#ffe680",
    "B": "#e6a820",
    "C": "#9c6410",
    "D": "#5c360c",
    "W": "#c87830",
    "X": "#9e4a18",
    "Z": "#5a240c",
    "K": "#381408",
    "H": "#b4bec8",
    "M": "#78828e",
    "L": "#444c58",
    "E": "#ffee66",
    "Q": "#e69000",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_ground_shadow(grid, body_y_off, fl_lifted, fr_lifted, bl_lifted, br_lifted):
    extra_w = 1 if body_y_off == 1 else 0
    
    shadow_profile = {
        32: (17 - extra_w, 30 + extra_w),
        33: (15 - extra_w, 32 + extra_w),
        34: (14 - extra_w, 33 + extra_w),
        35: (14 - extra_w, 33 + extra_w),
        36: (15 - extra_w, 32 + extra_w),
        37: (16 - extra_w, 31 + extra_w),
        38: (18 - extra_w, 29 + extra_w),
    }
    for sy, (s_min, s_max) in shadow_profile.items():
        for sx in range(s_min, s_max + 1):
            if 0 <= sx < W and 0 <= sy < H:
                grid[sy][sx] = "S"
                
    # 4 Foot contact ground shadows:
    # 1. Front-Left ground at X=10, Y=37..38
    if fl_lifted:
        grid[38][10] = "S"
    else:
        for dx in (-1, 0, 1):
            for dy in (0, 1):
                grid[37 + dy][10 + dx] = "S"
                
    # 2. Front-Right ground at X=37, Y=37..38
    if fr_lifted:
        grid[38][37] = "S"
    else:
        for dx in (-1, 0, 1):
            for dy in (0, 1):
                grid[37 + dy][37 + dx] = "S"
                
    # 3. Back-Left ground at X=7, Y=26..27
    if bl_lifted:
        grid[27][7] = "S"
    else:
        for dx in (-1, 0, 1):
            grid[26][7 + dx] = "S"
            grid[27][7 + dx] = "S"
            
    # 4. Back-Right ground at X=40, Y=26..27
    if br_lifted:
        grid[27][40] = "S"
    else:
        for dx in (-1, 0, 1):
            grid[26][40 + dx] = "S"
            grid[27][40 + dx] = "S"

def draw_claw_leg(hip_x, hip_y, knee_x, knee_y, foot_x, foot_y):
    leg_pixels = {}
    
    # 1. Thigh segment (hip to knee): thickness ~3px
    steps_thigh = 14
    for s in range(steps_thigh + 1):
        t = s / steps_thigh
        cx = hip_x + t * (knee_x - hip_x)
        cy = hip_y + t * (knee_y - hip_y)
        for dx in (-0.5, 0.0, 0.5):
            for dy in (-0.5, 0.0, 0.5):
                ix = int(round(cx + dx))
                iy = int(round(cy + dy))
                col = "H" if dy < 0 else ("L" if dy > 0 else "M")
                leg_pixels[(ix, iy)] = col
                
    # 2. Knee circular joint disc (brass pin)
    kx = int(round(knee_x))
    ky = int(round(knee_y))
    leg_pixels[(kx, ky)] = "B"
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if abs(dx) + abs(dy) == 1:
                leg_pixels[(kx + dx, ky + dy)] = "C" if dy > 0 else "A"
                
    # 3. Shin / Claw segment (knee to foot)
    steps_shin = 16
    for s in range(steps_shin + 1):
        t = s / steps_shin
        cx = knee_x + t * (foot_x - knee_x)
        cy = knee_y + t * (foot_y - knee_y)
        width = 1.3 * (1.0 - 0.75 * t)
        for d in (-width, 0.0, width):
            ix = int(round(cx + d))
            iy = int(round(cy))
            col = "H" if d < 0 else ("L" if d > 0 else "M")
            leg_pixels[(ix, iy)] = col
            
    # Sharp brass claw tip
    fx = int(round(foot_x))
    fy = int(round(foot_y))
    leg_pixels[(fx, fy)] = "A"
    
    outline = {}
    for (x, y) in leg_pixels:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in leg_pixels:
                outline[(nx, ny)] = "#"
                
    return leg_pixels, outline

def draw_carapace_and_head(y_off):
    cy = 23 + y_off
    hy = 14 + y_off
    
    body_pixels = {}
    
    # 1. Head profile: Y = hy - 3 .. hy + 2, X = 20..27
    head_profile = {
        hy - 3: (22, 25),
        hy - 2: (21, 26),
        hy - 1: (20, 27),
        hy:     (20, 27),
        hy + 1: (20, 27),
        hy + 2: (21, 26),
    }
    for y, (x_min, x_max) in head_profile.items():
        for x in range(x_min, x_max + 1):
            if y == hy - 3:
                body_pixels[(x, y)] = "A"
            elif y <= hy - 1:
                body_pixels[(x, y)] = "B"
            else:
                body_pixels[(x, y)] = "C" if x in (x_min, x_max) else "B"
                
    # Brass Pincers / Antenna horns:
    body_pixels[(19, hy - 4)] = "A"; body_pixels[(19, hy - 3)] = "B"; body_pixels[(20, hy - 2)] = "C"
    body_pixels[(28, hy - 4)] = "A"; body_pixels[(28, hy - 3)] = "B"; body_pixels[(27, hy - 2)] = "C"
    
    # Glowing Topaz Clockwork Eyes:
    body_pixels[(21, hy - 1)] = "E"; body_pixels[(21, hy)] = "Q"
    body_pixels[(26, hy - 1)] = "E"; body_pixels[(26, hy)] = "Q"
    
    # 2. Main Carapace Shell (Turtle plates with brass rim):
    carapace_profile = {
        cy - 8: (19, 28),
        cy - 7: (17, 30),
        cy - 6: (16, 31),
        cy - 5: (15, 32),
        cy - 4: (14, 33),
        cy - 3: (14, 33),
        cy - 2: (14, 33),
        cy - 1: (14, 33),
        cy:     (14, 33),
        cy + 1: (14, 33),
        cy + 2: (14, 33),
        cy + 3: (15, 32),
        cy + 4: (16, 31),
        cy + 5: (17, 30),
        cy + 6: (18, 29),
        cy + 7: (20, 27),
    }
    
    for y, (x_min, x_max) in carapace_profile.items():
        for x in range(x_min, x_max + 1):
            is_rim = (x in (x_min, x_min + 1, x_max - 1, x_max) or y in (cy - 8, cy + 7))
            if is_rim:
                if y <= cy - 5:
                    col = "A" if (x + y) % 3 == 0 else "B"
                elif y <= cy + 2:
                    col = "B" if x < 24 else "C"
                else:
                    col = "C" if (x + y) % 2 == 0 else "D"
                body_pixels[(x, y)] = col
            else:
                is_seam = (x in (20, 27) and y in range(cy - 6, cy + 6)) or \
                          (y in (cy - 3, cy + 2) and x in range(x_min + 2, x_max - 1))
                if is_seam:
                    body_pixels[(x, y)] = "K"
                else:
                    dist_top = y - (cy - 8)
                    dist_left = x - x_min
                    if dist_top <= 4 and dist_left <= 6:
                        body_pixels[(x, y)] = "W"
                    elif dist_top <= 8 and dist_left <= 11:
                        body_pixels[(x, y)] = "X"
                    elif dist_top <= 12:
                        body_pixels[(x, y)] = "X" if x < 24 else "Z"
                    else:
                        body_pixels[(x, y)] = "Z"

    # Central Brass Clockwork Hatch & Winding Socket at (24, cy - 1)
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            if dx*dx + dy*dy <= 4:
                hx = 24 + dx
                hy_ = cy - 1 + dy
                if dx == 0 and dy == 0:
                    body_pixels[(hx, hy_)] = "D"
                elif dy <= -1:
                    body_pixels[(hx, hy_)] = "A"
                elif dy >= 1:
                    body_pixels[(hx, hy_)] = "C"
                else:
                    body_pixels[(hx, hy_)] = "B"
                    
    outline = {}
    for (x, y) in body_pixels:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in body_pixels:
                outline[(nx, ny)] = "#"
                
    return body_pixels, outline

def render_beetle_frame(f_idx):
    grid = empty_grid()
    
    if f_idx == 0:
        y_off = 0
        fl_lift, br_lift = False, False
        fr_lift, bl_lift = True, True
    elif f_idx == 1:
        y_off = 1
        fl_lift, br_lift = False, False
        fr_lift, bl_lift = False, False
    elif f_idx == 2:
        y_off = 0
        fl_lift, br_lift = True, True
        fr_lift, bl_lift = False, False
    else:
        y_off = 0
        fl_lift, br_lift = False, False
        fr_lift, bl_lift = False, False
        
    # 1. Ground contact shadows
    draw_ground_shadow(grid, y_off, fl_lift, fr_lift, bl_lift, br_lift)
    
    # 2. Back-Left Leg (BL)
    bl_hip = (16, 20 + y_off)
    bl_knee = (6, 18 if bl_lift else 20)
    bl_foot = (8, 23 if bl_lift else 26)
    bl_pts, bl_out = draw_claw_leg(bl_hip[0], bl_hip[1], bl_knee[0], bl_knee[1], bl_foot[0], bl_foot[1])
    
    # 3. Back-Right Leg (BR)
    br_hip = (31, 20 + y_off)
    br_knee = (41, 18 if br_lift else 20)
    br_foot = (39, 23 if br_lift else 26)
    br_pts, br_out = draw_claw_leg(br_hip[0], br_hip[1], br_knee[0], br_knee[1], br_foot[0], br_foot[1])
    
    # 4. Front-Left Leg (FL)
    fl_hip = (15, 24 + y_off)
    fl_knee = (6, 29 if fl_lift else 30)
    fl_foot = (10, 34 if fl_lift else 37)
    fl_pts, fl_out = draw_claw_leg(fl_hip[0], fl_hip[1], fl_knee[0], fl_knee[1], fl_foot[0], fl_foot[1])
    
    # 5. Front-Right Leg (FR)
    fr_hip = (32, 24 + y_off)
    fr_knee = (41, 29 if fr_lift else 30)
    fr_foot = (37, 34 if fr_lift else 37)
    fr_pts, fr_out = draw_claw_leg(fr_hip[0], fr_hip[1], fr_knee[0], fr_knee[1], fr_foot[0], fr_foot[1])
    
    # 6. Carapace Body & Head
    body_pts, body_out = draw_carapace_and_head(y_off)
    
    # Composite layers:
    for out in (bl_out, br_out):
        for (x, y), c in out.items():
            if 0 <= x < W and 0 <= y < H and grid[y][x] in (".", "S"):
                grid[y][x] = c
    for pts in (bl_pts, br_pts):
        for (x, y), c in pts.items():
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = c
                
    for out in (fl_out, fr_out):
        for (x, y), c in out.items():
            if 0 <= x < W and 0 <= y < H and grid[y][x] in (".", "S"):
                grid[y][x] = c
    for pts in (fl_pts, fr_pts):
        for (x, y), c in pts.items():
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = c
                
    for (x, y), c in body_out.items():
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = c
    for (x, y), c in body_pts.items():
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = c
            
    if f_idx == 1:
        grid[22 + y_off - 1][22] = "A"
        grid[22 + y_off - 1][25] = "A"
        
    return grid

frames = [render_beetle_frame(i) for i in range(4)]

# Check row length and naked pixels
for i, g in enumerate(frames):
    for r_idx, row in enumerate(g):
        assert len(row) == W, f"Frame {i+1} row {r_idx} len={len(row)} != {W}"

def check_naked_pixels(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "E", "Q"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

for i, g in enumerate(frames):
    n = check_naked_pixels(g)
    print(f"Frame {i+1} naked pixels: {len(n)}")

print("Validation passed. Ready to export.")
