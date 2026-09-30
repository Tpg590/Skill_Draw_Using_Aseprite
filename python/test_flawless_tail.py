import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (10, 16, 26, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 16, 26, 255),     # Dark steel boundary outline (#0c101a)
    
    # Cold Blue-Steel Armor (FreeStyle)
    "A": (216, 232, 246, 255),  # Silvery specular highlight (#d8e8f6)
    "B": (138, 160, 186, 255),  # Cold blue-gray steel midtone (#8aa0ba)
    "C": (64, 82, 108, 255),    # Deep navy-slate steel shadow (#40526c)
    "D": (26, 36, 52, 255),     # Dark crevice seam / recess (#1a2434)
    
    # Glowing Cyan Stinger & Plasma OSL
    "W": (255, 255, 255, 255),  # White-hot stinger tip / plasma core (#ffffff)
    "E": (64, 240, 255, 255),   # Radiant cyan plasma (#40f0ff)
    "Q": (20, 164, 216, 255),   # Cyan glow halo / OSL bleed (#14a4d8)
    "T": (12, 84, 136, 255),    # Deep cyan aura shadow (#0c5488)
    
    # Brass Pivot Bolts & Mechanical Accents
    "K": (244, 176, 56, 255),   # Polished brass bolt highlight (#f4b038)
    "J": (148, 92, 24, 255),    # Bronze bolt shadow (#945c18)
    
    # Stone Dais / Foundation
    "M": (130, 142, 154, 255),  # Stone highlight (#828e9a)
    "N": (82, 94, 108, 255),    # Stone midtone (#525e6c)
    "P": (44, 52, 66, 255),     # Stone deep shadow (#2c3442)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_stone_dais_and_turret(grid):
    # 1. Soft Elliptical Ground Shadow on Floor (Y = 44..46)
    for y in (44, 45, 46):
        x_min = 6 if y == 44 else (8 if y == 45 else 11)
        x_max = 28 if y == 44 else (26 if y == 45 else 23)
        for x in range(x_min, x_max + 1):
            grid[y][x] = "S"

    # 2. Stone Oval Dais: Y = 40..43, X = 7..27
    # Outlines above exposed dais:
    for x in range(8, 10):
        grid[39][x] = "#"
    for x in range(23, 27):
        grid[39][x] = "#"

    grid[40][7] = "#"; grid[40][8] = "#"; grid[40][26] = "#"; grid[40][27] = "#"
    for x in range(9, 26):
        grid[40][x] = "M" if x % 4 in (1, 2) else "N"
    
    for y in (41, 42):
        grid[y][7] = "#"; grid[y][27] = "#"
        for x in range(8, 27):
            if y == 41:
                grid[y][x] = "M" if x % 5 in (1, 2) else "N"
            else:
                grid[y][x] = "N" if x % 3 != 0 else "P"
                
    for x in range(7, 28):
        grid[43][x] = "#"

    # 3. Turret Chassis (Mounted on stone dais, centered at X=16)
    # Base bolted flange: Y = 39, X = 10..22
    grid[39][9] = "#"; grid[39][23] = "#"
    for x in range(10, 23):
        grid[39][x] = "D"
    grid[39][11] = "K"; grid[39][12] = "J" # Left bolt
    grid[39][20] = "K"; grid[39][21] = "J" # Right bolt

    # Armored chassis profile: Y = 29..38
    chassis_widths = {
        38: (10, 22),
        37: (11, 21),
        36: (11, 21),
        35: (12, 20),
        34: (12, 20),
        33: (13, 19),
        32: (13, 19),
        31: (14, 18),
        30: (14, 18),
        29: (15, 17),
    }
    for y, (x_min, x_max) in chassis_widths.items():
        grid[y][x_min] = "#"
        grid[y][x_max] = "#"
        for x in range(x_min + 1, x_max):
            if x <= x_min + 2:
                grid[y][x] = "A" if y % 2 == 0 else "B"
            elif x <= 16:
                grid[y][x] = "B"
            elif x <= x_max - 2:
                grid[y][x] = "C"
            else:
                grid[y][x] = "D"

    # Glowing cooling core / energy conduits on chassis (Y = 34..35)
    grid[34][15] = "T"; grid[34][16] = "Q"; grid[34][17] = "E"
    grid[35][15] = "D"; grid[35][16] = "C"; grid[35][17] = "C"

    # Hydraulic stabilizer piston on left side of chassis
    grid[36][12] = "K"; grid[37][12] = "J"

    # Heavy ball-socket turret dome at Y = 25..28
    # Pivot point is FIXED at (16, 25)!
    grid[29][13] = "#"; grid[29][14] = "#"; grid[29][18] = "#"; grid[29][19] = "#"
    grid[28][12] = "#"; grid[28][13] = "#"; grid[28][14] = "A"; grid[28][15] = "B"; grid[28][16] = "B"; grid[28][17] = "C"; grid[28][18] = "D"; grid[28][19] = "#"; grid[28][20] = "#"
    grid[27][13] = "#"; grid[27][14] = "K"; grid[27][15] = "A"; grid[27][16] = "B"; grid[27][17] = "C"; grid[27][18] = "J"; grid[27][19] = "#"
    grid[26][14] = "#"; grid[26][15] = "K"; grid[26][16] = "B"; grid[26][17] = "J"; grid[26][18] = "#"
    grid[25][15] = "#"; grid[25][16] = "#"; grid[25][17] = "#"

def get_rigid_box(x_start, y_start, theta_deg, seg_idx):
    # Length = 5px (u = 0.0 .. 4.5), Thickness = 3px (v = -1.2 .. 1.2)
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    fx, fy = cos_t, -sin_t
    nx, ny = -sin_t, -cos_t # points towards "up" (highlight)
    
    seg_map = {}
    
    # Fill solid interior
    for u_idx in range(10): # 0.0 to 4.5 by 0.5
        u = u_idx * 0.5
        for v_idx in (-1.0, -0.5, 0.0, 0.5, 1.0):
            v = v_idx
            px = x_start + u * fx + v * nx
            py = y_start + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            
            # Color assignment
            if v > 0.3:
                c = "A" # Upper specular armor plate
            elif v < -0.3:
                c = "C" # Lower shadowed armor plate
            else:
                if u <= 0.8:
                    c = "K" if seg_idx > 0 else "B" # Brass hinge pin
                elif u >= 3.8:
                    c = "K" # Brass hinge pin
                else:
                    c = "B" # Core steel
            seg_map[(ix, iy)] = c
            
    outline = {}
    for (x, y) in seg_map:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) not in seg_map:
                outline[(nx_, ny_)] = "#"
                
    end_x = x_start + 4.5 * fx
    end_y = y_start + 4.5 * fy
    return seg_map, outline, end_x, end_y

def get_stinger(x_start, y_start, theta_deg):
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    fx, fy = cos_t, -sin_t
    nx, ny = -sin_t, -cos_t
    
    stinger_map = {}
    outline = {}
    
    # 1. Armored collar & plasma capacitor bulb at u = 0.0 .. 2.0, thickness 4px
    for u in (0.0, 0.5, 1.0, 1.5, 2.0):
        for v in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
            px = x_start + u * fx + v * nx
            py = y_start + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            if u <= 0.5 and abs(v) >= 1.0:
                stinger_map[(ix, iy)] = "D" # Mounting bracket
            elif abs(v) >= 1.2:
                stinger_map[(ix, iy)] = "Q" # Cyan glow halo
            else:
                stinger_map[(ix, iy)] = "E" # Bright cyan plasma
                
    # 2. Hardened titanium needle blade at u = 2.5 .. 4.5, thickness 2px -> 1px
    for u in (2.5, 3.0, 3.5, 4.0, 4.5):
        for v in (-0.5, 0.0, 0.5):
            px = x_start + u * fx + v * nx
            py = y_start + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            if v > 0.0:
                stinger_map[(ix, iy)] = "A" # Upper blade glint
            else:
                stinger_map[(ix, iy)] = "E" # Inner energized canal
                
    # 3. White-hot hypodermic tip at u = 5.0 .. 6.5, thickness 1px
    for u in (5.0, 5.8, 6.5):
        px = x_start + u * fx
        py = y_start + u * fy
        ix = int(round(px))
        iy = int(round(py))
        stinger_map[(ix, iy)] = "W" # Piercing tip
        
    for (x, y) in stinger_map:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) not in stinger_map and stinger_map[(x, y)] in ("D", "A", "B", "C"):
                outline[(nx_, ny_)] = "#"
                
    return stinger_map, outline

# 6 Animation Frames:
# F1 (Rest): Natural C-curve arching right
# F2 (Anticipation): Deep recoil left, tight spring fold
# F3 (Whip Strike): Laser-straight diagonal thrust forward
# F4 (Overshoot): Whip-crack kinetic snap downward
# F5 (Recovery 1): Smooth joint uncoiling
# F6 (Recovery 2): Retracting into resting pose
ANGLES = [
    (75.0,   26.0, -20.0, -45.0), # F1: Rest
    (125.0, 150.0,  95.0,  40.0), # F2: Anticipation
    (26.0,   24.0,  22.0,  18.0), # F3: Whip Strike
    (28.0,    6.0, -32.0, -72.0), # F4: Overshoot
    (54.0,   32.0, -10.0, -32.0), # F5: Recovery 1
    (70.0,   26.0, -16.0, -40.0), # F6: Recovery 2
]

def render_frame_full(f_idx):
    grid = empty_grid()
    draw_stone_dais_and_turret(grid)
    
    # Locked base pivot point at (16, 25)
    p0_x, p0_y = 16.0, 25.0
    
    th1, th2, th3, th_s = ANGLES[f_idx]
    
    seg1_map, seg1_out, p1_x, p1_y = get_rigid_box(p0_x, p0_y, th1, 0)
    seg2_map, seg2_out, p2_x, p2_y = get_rigid_box(p1_x, p1_y, th2, 1)
    seg3_map, seg3_out, p3_x, p3_y = get_rigid_box(p2_x, p2_y, th3, 2)
    stinger_map, stinger_out = get_stinger(p3_x, p3_y, th_s)
    
    # Layer 1: Outlines
    for out in (seg1_out, seg2_out, seg3_out, stinger_out):
        for (x, y), c in out.items():
            if 0 <= x < W and 0 <= y < H and grid[y][x] == ".":
                grid[y][x] = c
                
    # Layer 2: Segment Bodies
    for s_map in (seg1_map, seg2_map, seg3_map, stinger_map):
        for (x, y), c in s_map.items():
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = c
                
    # Layer 3: Dynamic Particles & OSL (Rules 1.1 & 3.3)
    if f_idx == 1:
        # F2: Electric sparks charging around stinger
        grid[12][12] = "E"
        grid[11][15] = "Q"
        grid[15][10] = "T"
    elif f_idx == 2:
        # F3: High-speed strike shockwave / plasma exhaust particles
        grid[15][39] = "E"
        grid[16][42] = "W"
        grid[18][41] = "Q"
        grid[20][38] = "T"
    elif f_idx == 3:
        # F4: Kinetic snap residual spark
        grid[29][34] = "Q"
        grid[30][35] = "E"
        
    return grid

frames = [render_frame_full(i) for i in range(6)]

def check_naked_pixels(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "E", "W", "Q", "T"): # OSL glow particles don't require black outline
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

for i, g in enumerate(frames):
    n = check_naked_pixels(g)
    print(f"Frame {i+1} naked pixels: {len(n)}")

gif_frames = []
for idx, g in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/flawless_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/flawless_sheet.png")

gif_frames[0].save(
    "python/flawless_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS
    loop=0
)
print("Rendered flawless_sheet.png and flawless_anim.gif.")
