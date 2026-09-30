import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (14, 16, 22, 130),     # Ground shadow (Alpha 130)
    "#": (16, 18, 24, 255),     # Terraria near-black heavy outline (#101218)
    
    # Cast Iron / Heavy Armor Steel (Terraria high contrast)
    "A": (224, 234, 244, 255),  # Specular steel highlight / chrome glint (#e0eaf4)
    "B": (146, 160, 178, 255),  # Steel armor midtone (#92a0b2)
    "C": (76, 88, 106, 255),    # Dark steel shadow (#4c586a)
    "D": (38, 44, 56, 255),     # Deep crevice / seam / joint recess (#262c38)
    
    # Hydraulic Chrome Piston & Spikes
    "W": (255, 255, 255, 255),  # Pure white glint / spike tip / steam core (#ffffff)
    "L": (180, 204, 224, 255),  # Chrome cylinder body (#b4cce0)
    
    # Bronze Rivets & Pivot Pins
    "K": (240, 180, 60, 255),   # Polished brass rivet highlight (#f0b43c)
    "J": (148, 96, 24, 255),    # Bronze rivet shadow (#946018)
    
    # Gauge & Exhaust Steam
    "R": (230, 64, 48, 255),    # Pressure gauge warning red (#e64030)
    "V": (196, 222, 242, 255),  # Steam puff midtone (#c4def2)
    "U": (124, 152, 182, 180),  # Steam puff trailing shadow (#7c98b6)
    
    # Industrial Workshop Floor Foundation Plinth
    "M": (136, 144, 154, 255),  # Stone plinth highlight (#88909a)
    "N": (88, 96, 108, 255),    # Stone plinth midtone (#58606c)
    "P": (52, 58, 70, 255),     # Stone plinth shadow (#343a46)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_foundation_and_pedestal(grid, shadow_max_x):
    # 1. Dynamic Ground Shadow S (Rule 4.4: tracks arm reach to shadow_max_x!)
    # Floor contact at Y = 44..46
    for y in (44, 45, 46):
        min_x = 3 if y == 44 else (4 if y == 45 else 6)
        max_x = shadow_max_x if y == 44 else (shadow_max_x - 1 if y == 45 else shadow_max_x - 3)
        for x in range(min_x, max_x + 1):
            if 0 <= x < W:
                grid[y][x] = "S"

    # 2. Workshop Floor Foundation Plinth: Y = 40..43, X = 3..44 (Strictly contained, rounded edges!)
    # Top chamfered edge at Y = 40: X = 5..42
    grid[40][4] = "#"; grid[40][43] = "#"
    for x in range(5, 43):
        grid[40][x] = "M" if x % 4 in (1, 2) else "N"
        
    # Front slab face at Y = 41..42: X = 3..44
    for y in (41, 42):
        grid[y][3] = "#"; grid[y][44] = "#"
        for x in range(4, 44):
            if y == 41:
                grid[y][x] = "M" if x % 5 in (1, 2) else "N"
            else:
                grid[y][x] = "N" if x % 3 != 0 else "P"
                
    # Bottom rim at Y = 43: X = 4..43
    for x in range(4, 44):
        grid[43][x] = "#"

    # 3. Fixed Machine Pedestal (Anchored on the LEFT: X = 4..14, Y = 16..39)
    # Bolted mounting base at Y = 38..39, X = 4..14
    for x in range(4, 15):
        grid[39][x] = "#"
    grid[38][4] = "#"; grid[38][14] = "#"
    for x in range(5, 14):
        grid[38][x] = "D"
    grid[38][6] = "K"; grid[38][7] = "J" # Left anchor bolt
    grid[38][11] = "K"; grid[38][12] = "J" # Right anchor bolt

    # Heavy cast-iron pedestal column: Y = 21..37
    pedestal_profile = {
        37: (5, 13), 36: (5, 13), 35: (5, 13),
        34: (5, 13), 33: (5, 13), 32: (5, 13),
        31: (5, 13), 30: (5, 13), 29: (5, 13),
        28: (5, 13), 27: (5, 13), 26: (5, 13),
        25: (5, 13), 24: (5, 13), 23: (5, 13),
        22: (5, 13), 21: (6, 12),
    }
    for y, (x_min, x_max) in pedestal_profile.items():
        grid[y][x_min] = "#"
        grid[y][x_max] = "#"
        for x in range(x_min + 1, x_max):
            if x <= x_min + 2:
                grid[y][x] = "A" if y % 2 == 0 else "B"
            elif x <= 9:
                grid[y][x] = "B"
            elif x <= x_max - 2:
                grid[y][x] = "C"
            else:
                grid[y][x] = "D"

    # Hydraulic Pressure Dial Gauge on pedestal face: Y = 28..31, X = 7..10
    grid[28][8] = "#"; grid[28][9] = "#"
    grid[29][7] = "#"; grid[29][8] = "W"; grid[29][9] = "W"; grid[29][10] = "#"
    grid[30][7] = "#"; grid[30][8] = "R"; grid[30][9] = "W"; grid[30][10] = "#"
    grid[31][8] = "#"; grid[31][9] = "#"

    # Cooling slots on lower pedestal: Y = 34..35, X = 7..11
    grid[34][8] = "D"; grid[34][9] = "D"; grid[34][10] = "D"
    grid[35][8] = "D"; grid[35][9] = "D"; grid[35][10] = "D"

    # Fixed Base Shoulder Joint Socket (Anchored at Hub 0: (11, 22))
    # Reinforced circular socket housing:
    grid[20][10] = "#"; grid[20][11] = "#"; grid[20][12] = "#"
    grid[21][9] = "#"; grid[21][10] = "A"; grid[21][11] = "A"; grid[21][12] = "B"; grid[21][13] = "#"
    grid[22][9] = "#"; grid[22][10] = "K"; grid[22][11] = "K"; grid[22][12] = "J"; grid[22][13] = "#"
    grid[23][9] = "#"; grid[23][10] = "C"; grid[23][11] = "C"; grid[23][12] = "D"; grid[23][13] = "#"
    grid[24][10] = "#"; grid[24][11] = "#"; grid[24][12] = "#"

def draw_rigid_segment(x0, y0, length, angle_deg, thickness=5):
    # Generates a solid rectangular metal segment with circular end-cap and locator pin
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    fx, fy = cos_t, -sin_t # Forward direction (upwards in pixel grid is -Y)
    nx, ny = -sin_t, -cos_t # Normal direction (towards top highlight)
    
    half_th = (thickness - 1) / 2.0
    seg_pixels = {}
    
    # Sub-pixel grid sweep to guarantee 100% solid connectivity
    steps_u = int(round(length * 2)) + 1
    steps_v = int(round(thickness * 2)) + 1
    
    for su in range(steps_u):
        u = (su / (steps_u - 1)) * length
        for sv in range(steps_v):
            v = -half_th + (sv / (steps_v - 1)) * (2 * half_th)
            
            px = x0 + u * fx + v * nx
            py = y0 + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            
            # Shading by cross-section:
            if v > 0.8:
                col = "A" # Top armor highlight
            elif v < -0.8:
                col = "C" # Bottom armor shadow
            else:
                col = "B" # Midtone steel core
                
            seg_pixels[(ix, iy)] = col
            
    # Draw circular joint hub & brass pin at the end of the segment:
    x_end = x0 + length * fx
    y_end = y0 + length * fy
    
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            jx = int(round(x_end + dx))
            jy = int(round(y_end + dy))
            if dx == 0 and dy == 0:
                seg_pixels[(jx, jy)] = "K" # Center brass hinge pin
            elif dy == -1:
                seg_pixels[(jx, jy)] = "A" # Top joint rim
            elif dy == 1:
                seg_pixels[(jx, jy)] = "J" # Bottom joint shadow
            else:
                seg_pixels[(jx, jy)] = "B"
                
    outline = {}
    for (x, y) in seg_pixels:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) not in seg_pixels:
                outline[(nx_, ny_)] = "#"
                
    return seg_pixels, outline, x_end, y_end

def draw_piston_rod(x0, y0, length, angle_deg, thickness=3):
    if length <= 0:
        return {}, {}, x0, y0
        
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    fx, fy = cos_t, -sin_t
    nx, ny = -sin_t, -cos_t
    
    rod_pixels = {}
    steps_u = int(round(length * 2)) + 1
    for su in range(steps_u):
        u = (su / (steps_u - 1)) * length
        for v in (-1.0, 0.0, 1.0):
            px = x0 + u * fx + v * nx
            py = y0 + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            if v > 0.3:
                rod_pixels[(ix, iy)] = "W" # Gleaming chrome reflection
            elif v < -0.3:
                rod_pixels[(ix, iy)] = "B" # Bottom cylinder shade
            else:
                rod_pixels[(ix, iy)] = "L" # Polished chrome body
                
    outline = {}
    for (x, y) in rod_pixels:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) not in rod_pixels:
                outline[(nx_, ny_)] = "#"
                
    x_end = x0 + length * fx
    y_end = y0 + length * fy
    return rod_pixels, outline, x_end, y_end

def draw_spiked_fist(x0, y0, angle_deg):
    # Heavy rectangular fist block (7x7px) with 3 forward steel spikes
    theta = math.radians(angle_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    fx, fy = cos_t, -sin_t
    nx, ny = -sin_t, -cos_t
    
    fist_pixels = {}
    
    # 1. Mounting wrist collar (u = 0..1, v = -3..3)
    for u in (0.0, 0.5, 1.0):
        for v in range(-3, 4):
            px = x0 + u * fx + v * nx
            py = y0 + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            fist_pixels[(ix, iy)] = "D" if u == 0 else "C"
            
    # 2. Main fist armored casing (u = 1.5..5.5, v = -3..3)
    for u_step in range(9): # 1.5 to 5.5
        u = 1.5 + u_step * 0.5
        for v_step in range(13): # -3 to 3
            v = -3.0 + v_step * 0.5
            px = x0 + u * fx + v * nx
            py = y0 + u * fy + v * ny
            ix = int(round(px))
            iy = int(round(py))
            
            # Shading:
            if v > 1.8:
                col = "A" # Upper knuckle glint
            elif v < -1.8:
                col = "C" # Lower fist shadow
            elif 3.5 <= u <= 4.5 and abs(v) <= 1.0:
                col = "K" # Knuckle reinforcement brass plate
            else:
                col = "B" # Solid steel core
            fist_pixels[(ix, iy)] = col
            
    # 3. Knuckle face plate & 3 forward conical spikes (u = 5.5..8.5)
    # Upper spike at v = 2.0, Mid spike at v = 0.0, Lower spike at v = -2.0
    for v_spike in (2.0, 0.0, -2.0):
        # Spike base at u = 5.5..6.5 (width 2px)
        for u in (5.5, 6.0, 6.5):
            for dv in (-0.5, 0.5):
                px = x0 + u * fx + (v_spike + dv) * nx
                py = y0 + u * fy + (v_spike + dv) * ny
                fist_pixels[(int(round(px)), int(round(py)))] = "A" if dv > 0 else "B"
        # Spike sharp tip at u = 7.0..8.5 (width 1px)
        for u in (7.0, 7.8, 8.5):
            px = x0 + u * fx + v_spike * nx
            py = y0 + u * fy + v_spike * ny
            fist_pixels[(int(round(px)), int(round(py)))] = "W" # Razor white tip
            
    outline = {}
    for (x, y) in fist_pixels:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = x + dx, y + dy
            if (nx_, ny_) not in fist_pixels:
                outline[(nx_, ny_)] = "#"
                
    return fist_pixels, outline

print("Component drawing functions defined.")

# Frame animation parameters:
# (th1, th2, th_fist, p_ext, shadow_max_x)
FRAME_PARAMS = [
    # F1: Rest (Z-fold close to pedestal)
    (45.0,  -45.0,   0.0, 1.0, 31),
    # F2: Anticipation (coiled back, compressed piston, gauge red)
    (65.0,  -65.0,   0.0, 0.0, 26),
    # F3: Piston Punch (laser straight horizontal thrust, max reach)
    ( 0.0,    0.0,   0.0, 9.0, 44),
    # F4: Recoil (bounces back 2px, steam bursts from valve)
    (12.0,   -8.0,   0.0, 7.0, 42),
    # F5: Retract 1 (folding back, piston retracts, steam fades)
    (28.0,  -25.0,   0.0, 4.0, 37),
    # F6: Retract 2 (settling into resting pose)
    (40.0,  -38.0,   0.0, 2.0, 33),
]

def render_robot_frame(f_idx):
    grid = empty_grid()
    th1, th2, th_fist, p_ext, shadow_x = FRAME_PARAMS[f_idx]
    
    # 1. Base pedestal and dynamic ground shadow
    draw_foundation_and_pedestal(grid, shadow_x)
    
    # Fixed base shoulder pivot:
    p0_x, p0_y = 11.0, 22.0
    
    # 2. Segment 1 (Upper Arm, length 8px)
    seg1_pts, seg1_out, p1_x, p1_y = draw_rigid_segment(p0_x, p0_y, 8.0, th1, thickness=5)
    
    # 3. Segment 2 (Forearm cylinder, length 8px)
    seg2_pts, seg2_out, p2_x, p2_y = draw_rigid_segment(p1_x, p1_y, 8.0, th2, thickness=5)
    
    # 4. Chrome Piston Rod (length p_ext)
    rod_pts, rod_out, p3_x, p3_y = draw_piston_rod(p2_x, p2_y, p_ext, th_fist, thickness=3)
    
    # 5. Spiked Steel Fist
    fist_pts, fist_out = draw_spiked_fist(p3_x, p3_y, th_fist)
    
    # Layer 1: Outlines for all moving parts
    for out in (seg1_out, seg2_out, rod_out, fist_out):
        for (x, y), c in out.items():
            if 0 <= x < W and 0 <= y < H and grid[y][x] == ".":
                grid[y][x] = c
                
    # Layer 2: Colored Bodies
    # Draw in mechanical order: Seg 1 -> Seg 2 -> Piston -> Fist
    for s_pts in (seg1_pts, seg2_pts, rod_pts, fist_pts):
        for (x, y), c in s_pts.items():
            if 0 <= x < W and 0 <= y < H:
                grid[y][x] = c

    # Rule 4.6 (Bảo tồn rãnh khớp cơ khí):
    # Clearly emphasize the dark circular seam at Elbow Hub 1 (p1_x, p1_y)
    # and Wrist Collar Hub 2 (p2_x, p2_y)
    e_x, e_y = int(round(p1_x)), int(round(p1_y))
    if 0 <= e_x < W and 0 <= e_y < H:
        grid[e_y][e_x] = "K" # Center brass hinge pin
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx_, ny_ = e_x + dx, e_y + dy
            if 0 <= nx_ < W and 0 <= ny_ < H and grid[ny_][nx_] == "B":
                grid[ny_][nx_] = "D" # Circular seam ring around joint

    w_x, w_y = int(round(p2_x)), int(round(p2_y))
    if 0 <= w_x < W and 0 <= w_y < H:
        for dy in (-2, -1, 0, 1, 2):
            if 0 <= w_y + dy < H:
                grid[w_y + dy][w_x] = "D" # Cylinder mouth collar seam

    # Dynamic Steam / Exhaust & Impact Particles (Rule 3.3)
    if f_idx == 1:
        # F2: Pressure dial needle into red warning!
        grid[30][8] = "R"; grid[29][9] = "R"
    elif f_idx == 2:
        # F3: High-speed air slash impact lines in front of fist
        grid[20][45] = "W"; grid[21][46] = "A"
        grid[22][46] = "W"; grid[23][47] = "A"
        grid[24][46] = "W"; grid[25][45] = "A"
    elif f_idx == 3:
        # F4: Steam bursting from relief valve on cylinder!
        steam_pixels = [
            (e_x + 1, e_y - 2, "W"), (e_x + 2, e_y - 3, "W"),
            (e_x + 3, e_y - 3, "V"), (e_x + 4, e_y - 4, "V"),
            (e_x + 2, e_y - 4, "V"), (e_x + 3, e_y - 5, "U"),
            (e_x + 5, e_y - 4, "U"), (e_x + 6, e_y - 3, "U"),
        ]
        for sx, sy, sc in steam_pixels:
            if 0 <= sx < W and 0 <= sy < H:
                grid[sy][sx] = sc
    elif f_idx == 4:
        # F5: Steam dissipating into drifting particles
        steam_f5 = [
            (e_x + 4, e_y - 5, "V"), (e_x + 5, e_y - 6, "V"),
            (e_x + 7, e_y - 6, "U"), (e_x + 8, e_y - 5, "U"),
        ]
        for sx, sy, sc in steam_f5:
            if 0 <= sx < W and 0 <= sy < H:
                grid[sy][sx] = sc
                
    return grid

frames = [render_robot_frame(i) for i in range(6)]

def check_naked_pixels(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "W", "V", "U"): # Steam and air slash tips don't require black outline
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/robot_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/robot_sheet.png")

gif_frames[0].save(
    "python/robot_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS
    loop=0
)
print("Rendered robot_sheet.png and robot_anim.gif.")

