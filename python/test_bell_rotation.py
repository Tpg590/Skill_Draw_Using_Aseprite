import os
import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),
    "S": (26, 22, 32, 130),
    "#": (56, 30, 18, 255),     # Soft dark mahogany outline for wood/bronze (#381e12)
    "@": (38, 34, 32, 255),     # Soft dark stone outline (#262220)
    "A": (255, 223, 136, 255),  # Specular gold highlight (#ffdf88)
    "B": (232, 160, 56, 255),   # Bright bronze body (#e8a038)
    "C": (184, 100, 28, 255),   # Warm bronze midtone (#b8641c)
    "D": (116, 56, 16, 255),    # Deep bronze shadow (#743810)
    "E": (66, 26, 8, 255),      # Inner bell cavity shadow (#421a08)
    "F": (212, 146, 66, 255),   # Oak highlight (#d49242)
    "G": (148, 84, 34, 255),    # Oak midtone (#945422)
    "H": (86, 44, 16, 255),     # Oak shadow (#562c10)
    "J": (136, 130, 146, 255),  # Iron highlight (#888292)
    "K": (84, 76, 92, 255),     # Iron midtone (#544c5c)
    "L": (50, 42, 54, 255),     # Iron shadow (#322a36)
    "M": (142, 138, 128, 255),  # Stone highlight (#8e8a80)
    "N": (98, 94, 86, 255),     # Stone midtone (#625e56)
    "P": (62, 58, 52, 255),     # Stone shadow (#3e3a34)
}

# Upright Bell Model in local coordinates (u: -6..6, v: 0..11)
BELL_MAP = {}

# Crown ring (v = 0..1)
for u in (-1, 0, 1): BELL_MAP[(u, 0)] = "K"
for u in (-1, 0, 1): BELL_MAP[(u, 1)] = "B" if u < 0 else ("C" if u == 0 else "D")

# Dome / Shoulder (v = 2..4)
for u in range(-2, 3):
    BELL_MAP[(u, 2)] = "B" if u <= -1 else ("C" if u == 0 else "D")
for u in range(-3, 4):
    BELL_MAP[(u, 3)] = "B" if u <= -1 else ("C" if u <= 1 else "D")
for u in range(-4, 5):
    BELL_MAP[(u, 4)] = "B" if u <= -2 else ("C" if u <= 1 else "D")

# Waist (v = 5..6)
for u in range(-4, 5):
    BELL_MAP[(u, 5)] = "B" if u <= -2 else ("C" if u <= 1 else "D")
for u in range(-4, 5):
    BELL_MAP[(u, 6)] = "B" if u <= -2 else ("C" if u <= 1 else "D")

# Sound bow (v = 7..8)
for u in range(-5, 6):
    BELL_MAP[(u, 7)] = "B" if u <= -2 else ("C" if u <= 1 else "D")
for u in range(-6, 7):
    BELL_MAP[(u, 8)] = "B" if u <= -3 else ("C" if u <= 1 else "D")

# Rim / Lip (v = 9..10)
for u in range(-6, 7):
    BELL_MAP[(u, 9)] = "B" if u <= -3 else ("C" if u <= 1 else "D")
for u in range(-6, 7):
    BELL_MAP[(u, 10)] = "E" if abs(u) <= 4 else "D"

# Clapper ball (v = 10..11)
BELL_MAP[(0, 10)] = "D"
BELL_MAP[(0, 11)] = "D"
BELL_MAP[(-1, 11)] = "C"

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_environment(grid):
    # Stone platform: Y = 40..43
    for x in range(3, 45):
        grid[40][x] = "@"
    for x in range(4, 44):
        grid[41][x] = "M" if x % 5 != 0 else "N"
        grid[42][x] = "N" if x % 4 != 0 else "P"
        grid[43][x] = "P" if x % 3 != 0 else "@"
        grid[44][x] = "@"
    for y in (41, 42, 43):
        grid[y][3] = "@"; grid[y][44] = "@"
        
    # Wooden posts (Left: 5..9, Right: 38..42)
    for y in range(10, 40):
        grid[y][5] = "#"; grid[y][6] = "F"; grid[y][7] = "G"; grid[y][8] = "H"; grid[y][9] = "#"
        grid[y][38] = "#"; grid[y][39] = "F"; grid[y][40] = "G"; grid[y][41] = "H"; grid[y][42] = "#"
        
    # Stone plinths
    for x in range(4, 11):
        grid[39][x] = "@"
        grid[40][x] = "M" if x in (5, 6) else "N"
    for x in range(37, 44):
        grid[39][x] = "@"
        grid[40][x] = "N" if x in (38, 39) else "P"
        
    # Crossbeam (Y=6..10, X=3..44)
    for x in range(3, 45):
        grid[6][x] = "#"
        grid[7][x] = "F"
        grid[8][x] = "G"
        grid[9][x] = "H"
        grid[10][x] = "#"
    grid[7][3] = "#"; grid[8][3] = "#"; grid[9][3] = "#"
    grid[7][44] = "#"; grid[8][44] = "#"; grid[9][44] = "#"
    
    # Solid Corner braces (wooden 45-deg brackets with complete enclosing outline)
    # Left brace
    grid[11][10] = "F"; grid[11][11] = "#"
    grid[12][10] = "F"; grid[12][11] = "G"; grid[12][12] = "#"
    grid[13][10] = "#"; grid[13][11] = "G"; grid[13][12] = "H"; grid[13][13] = "#"
    grid[14][11] = "#"; grid[14][12] = "#"; grid[14][13] = "#"
    
    # Right brace
    grid[11][37] = "F"; grid[11][36] = "#"
    grid[12][37] = "F"; grid[12][36] = "G"; grid[12][35] = "#"
    grid[13][37] = "#"; grid[13][36] = "G"; grid[13][35] = "H"; grid[13][34] = "#"
    grid[14][36] = "#"; grid[14][35] = "#"; grid[14][34] = "#"
    
    # Central Iron Pivot Hanger (fixed 100% at X=24, Y=10)
    grid[7][23] = "K"; grid[7][24] = "J"; grid[7][25] = "K"
    grid[8][23] = "L"; grid[8][24] = "K"; grid[8][25] = "L"
    grid[9][23] = "L"; grid[9][24] = "L"; grid[9][25] = "L"
    grid[10][23] = "#"; grid[10][24] = "K"; grid[10][25] = "#"
    grid[11][23] = "#"; grid[11][24] = "J"; grid[11][25] = "#"
    grid[12][24] = "#"

def render_bell_rotated(grid, theta_deg, lag_dx=0.0):
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    p_x, p_y = 24.0, 12.0
    L_chain = 7.0
    
    # Crown position
    crown_x = p_x + L_chain * sin_t + lag_dx
    crown_y = p_y + L_chain * cos_t
    
    # 1. Chain links
    num_chain_pts = 7
    for step in range(1, num_chain_pts):
        t = step / num_chain_pts
        bx = (1 - t)**2 * 24.0 + 2 * (1 - t) * t * (24.0 + lag_dx * 1.2) + t**2 * crown_x
        by = (1 - t)**2 * 12.0 + 2 * (1 - t) * t * (12.0 + L_chain * 0.5) + t**2 * crown_y
        ix, iy = int(round(bx)), int(round(by))
        if 0 <= ix < W and 0 <= iy < H and grid[iy][ix] == ".":
            grid[iy][ix] = "J" if step % 2 == 0 else "K"
            
    # Outline chain
    for y in range(12, int(crown_y) + 2):
        for x in range(W):
            if grid[y][x] in ("J", "K"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"
                        
    # 2. Bell Model
    min_x = int(math.floor(crown_x - 10))
    max_x = int(math.ceil(crown_x + 10))
    min_y = int(math.floor(crown_y - 2))
    max_y = int(math.ceil(crown_y + 15))
    
    raw_bell = {}
    for y in range(max(0, min_y), min(H, max_y + 1)):
        for x in range(max(0, min_x), min(W, max_x + 1)):
            dx = x - crown_x
            dy = y - crown_y
            
            # Correct screen-space inverse rotation (Y points down):
            # u = dx * cos_t - dy * sin_t
            # v = dx * sin_t + dy * cos_t
            u = dx * cos_t - dy * sin_t
            v = dx * sin_t + dy * cos_t
            
            iu = int(round(u))
            iv = int(round(v))
            
            if (iu, iv) in BELL_MAP:
                raw_bell[(x, y)] = BELL_MAP[(iu, iv)]
                
    # Dynamic Specular Highlight (Rule 1.3: Facing Top-Left 10 o'clock)
    for (x, y), code in raw_bell.items():
        if code in ("B", "C"):
            is_top_left = ((x - 1, y) not in raw_bell or (x, y - 1) not in raw_bell)
            if is_top_left and y < crown_y + 7 and x <= crown_x:
                raw_bell[(x, y)] = "A"
                
    # Place bell pixels into grid
    for (x, y), col in raw_bell.items():
        grid[y][x] = col
        
    # Outline the bell: any bell pixel neighboring '.' gets '#'
    bell_pts = list(raw_bell.keys())
    for (x, y) in bell_pts:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H:
                if grid[ny][nx] == ".":
                    grid[ny][nx] = "#"
                    
    # Return bell center of mass X (v = 7)
    bell_center_x = crown_x + 7.0 * sin_t
    return int(round(bell_center_x))

def draw_shadow(grid, bell_x, f_idx):
    # Rule 4.4 & Requirement 2: X_shadow = X_bell
    sx = bell_x
    span = 5 if f_idx in (1, 5) else 6
    
    for y in (41, 42, 43):
        cur_span = span if y == 42 else span - 1
        for x in range(sx - cur_span, sx + cur_span + 1):
            if 0 <= x < W:
                grid[y][x] = "S"
                
    # Static shadows under wooden posts (Y=44..45)
    for y in (44, 45):
        for x in range(4, 12):
            if grid[y][x] == ".": grid[y][x] = "S"
        for x in range(36, 44):
            if grid[y][x] == ".": grid[y][x] = "S"

# 8 Frames Symmetrical Oscillations:
CONFIGS = [
    (-12.5,  0.0), # F1: Sweep Left
    (-25.4,  0.0), # F2: Extreme Left (X < 24 - 4)
    (-12.5,  1.0), # F3: Return Left (chain lag right)
    (  0.0,  0.5), # F4: Center Eq
    (+12.5,  0.0), # F5: Sweep Right
    (+25.4,  0.0), # F6: Extreme Right (X > 24 + 4)
    (+12.5, -1.0), # F7: Return Right (chain lag left)
    (  0.0, -0.5), # F8: Center Eq
]

def check_naked(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "@"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

frames_data = []
gif_frames = []
for idx, (th, lag) in enumerate(CONFIGS):
    g = empty_grid()
    draw_environment(g)
    bx = render_bell_rotated(g, th, lag)
    draw_shadow(g, bx, idx)
    frames_data.append((g, bx))
    
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

print("\n=== VALIDATION RESULTS ===")
for i, (g, bx) in enumerate(frames_data):
    naked = check_naked(g)
    # Check shadow center
    shadow_xs = [x for x in range(W) for y in (41, 42, 43) if g[y][x] == "S" and 10 <= x <= 38]
    mean_sx = sum(shadow_xs) / len(shadow_xs) if shadow_xs else 0
    delta_x = bx - 24
    print(f"Frame {i+1}:")
    print(f"  Bell Center X = {bx} (Delta X = {delta_x:+d}px)")
    print(f"  Shadow Mean X = {mean_sx:.1f} (Target = {bx})")
    print(f"  Naked pixels: {len(naked)}")

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 8, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/test_bell_sheet.png")

gif_frames[0].save(
    "python/test_bell_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)
print("\nGenerated test_bell_sheet.png and test_bell_anim.gif successfully.")
