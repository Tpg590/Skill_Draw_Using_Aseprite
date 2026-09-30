import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (10, 16, 24, 130),     # Soft ground shadow (Alpha 130)
    "#": (14, 20, 32, 255),     # Clean dark navy-black outline (#0e1420)
    
    # Cold Blue-Steel (FreeStyle mechanical armor)
    "A": (216, 232, 244, 255),  # Silvery light steel highlight (#d8e8f4)
    "B": (140, 162, 186, 255),  # Cold blue-gray steel midtone (#8ca2ba)
    "C": (68, 86, 112, 255),    # Deep navy-slate steel shadow (#445670)
    "D": (32, 44, 64, 255),     # Dark navy crevice / inner seam (#202c40)
    
    # Glowing Cyan Stinger & Plasma OSL
    "W": (255, 255, 255, 255),  # White-hot stinger core (#ffffff)
    "E": (76, 246, 255, 255),   # Radiant cyan plasma (#4cf6ff)
    "Q": (24, 176, 216, 255),   # Cyan glow halo / OSL bleed (#18b0d8)
    
    # Mechanical Accents (Bronze/brass pivot bolts)
    "K": (236, 164, 56, 255),   # Golden brass bolt highlight (#eca438)
    "J": (140, 84, 24, 255),    # Deep bronze bolt shadow (#8c5418)
    
    # Stone Base & Floor
    "M": (120, 132, 140, 255),  # Stone highlight (#78848c)
    "N": (76, 88, 100, 255),    # Stone midtone (#4c5864)
    "P": (44, 52, 64, 255),     # Stone shadow (#2c3440)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_stone_floor_and_turret(grid):
    # 1. Soft Ground Shadow S on stone floor (Y = 44..46)
    for y in (44, 45, 46):
        span = 15 if y == 44 else (12 if y == 45 else 8)
        for x in range(21 - span, 21 + span + 1):
            if 0 <= x < W:
                grid[y][x] = "S"

    # 2. Stone Floor: Y = 41..44, X = 4..43
    for x in range(4, 44):
        grid[41][x] = "#"
        grid[42][x] = "M" if x % 5 in (1, 2) else "N"
        grid[43][x] = "N" if x % 4 != 0 else "P"
        grid[44][x] = "#"
    grid[42][4] = "#"; grid[43][4] = "#"
    grid[42][43] = "#"; grid[43][43] = "#"

    # 3. Turret Pod (ụ máy cơ khí gắn sàn đá):
    # Base flange / mounting feet: Y = 40..41, X = 11..27
    for x in range(11, 27):
        grid[41][x] = "#"
    grid[40][11] = "#"; grid[40][26] = "#"
    for x in range(12, 26):
        grid[40][x] = "D"
    grid[40][13] = "K"; grid[40][14] = "J"
    grid[40][23] = "K"; grid[40][24] = "J"
    
    # Armored chassis body: Y = 32..39
    pod_widths = {
        39: (12, 25),
        38: (13, 24),
        37: (13, 24),
        36: (14, 23),
        35: (14, 23),
        34: (15, 22),
        33: (15, 22),
        32: (16, 21),
    }
    for y, (x_start, x_end) in pod_widths.items():
        grid[y][x_start] = "#"
        grid[y][x_end] = "#"
        for x in range(x_start + 1, x_end):
            if x <= x_start + 2:
                grid[y][x] = "A" if y % 2 == 0 else "B"
            elif x <= 19:
                grid[y][x] = "B"
            elif x <= x_end - 2:
                grid[y][x] = "C"
            else:
                grid[y][x] = "D"
                
    # Center mechanical status visor / cyan cooling port
    grid[36][18] = "Q"; grid[36][19] = "E"
    grid[37][18] = "Q"; grid[37][19] = "E"
    grid[38][18] = "C"; grid[38][19] = "D"
    
    # Ball socket mount: locked pivot at (18, 28)!
    # Y = 28..31
    grid[31][16] = "#"; grid[31][17] = "A"; grid[31][18] = "B"; grid[31][19] = "C"; grid[31][20] = "#"
    grid[30][16] = "#"; grid[30][17] = "K"; grid[30][18] = "B"; grid[30][19] = "D"; grid[30][20] = "#"
    grid[29][17] = "#"; grid[29][18] = "K"; grid[29][19] = "#"
    grid[28][17] = "#"; grid[28][18] = "#"; grid[28][19] = "#"

def draw_rigid_segment(x_start, y_start, theta_deg, is_base=False):
    # Length = 5px (u = 0..4), Thickness = 3px (v = -1..1)
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    seg_pixels = {}
    for u in range(5):
        for v in (-1, 0, 1):
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            ix = int(round(px))
            iy = int(round(py))
            
            # Color assignment for rigid box:
            if v == -1:
                color = "A" # upper armor edge highlight
            elif v == 0:
                if u in (0, 4):
                    color = "K" # brass joint pin
                else:
                    color = "B" # mid steel core
            else:
                color = "C" # lower armor edge shadow
                
            seg_pixels[(ix, iy)] = color
            
    end_x = x_start + 4.0 * cos_t
    end_y = y_start - 4.0 * sin_t
    return seg_pixels, end_x, end_y

def draw_stinger(x_start, y_start, theta_deg):
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    stinger_pixels = {}
    # Bulbous plasma capacitor base at u = 0, 1: width 3
    for v in (-1, 0, 1):
        for u in (0, 1):
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            col = "Q" if abs(v) == 1 else "E"
            stinger_pixels[(int(round(px)), int(round(py)))] = col
            
    # Tapered stinger needle at u = 2..4: width 2 -> 1
    for u in (2, 3):
        for v in (-0.5, 0.5):
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            stinger_pixels[(int(round(px)), int(round(py)))] = "E"
            
    # Needle tip at u = 4, 5
    px = x_start + 4.5 * cos_t
    py = y_start - 4.5 * sin_t
    stinger_pixels[(int(round(px)), int(round(py)))] = "W"
    
    px_tip = x_start + 5.5 * cos_t
    py_tip = y_start - 5.5 * sin_t
    stinger_pixels[(int(round(px_tip)), int(round(py_tip)))] = "W"
    
    return stinger_pixels

# Angular Kinematics for 6 Frames (Theta in degrees from horizontal, positive = up):
# F1 (Rest): Base 75, Mid 22, Distal -25, Stinger -50
# F2 (Anticipation): Base 125, Mid 150, Distal 95, Stinger 40
# F3 (Whip Strike): Base 28, Mid 25, Distal 22, Stinger 18 (Full extension diagonal!)
# F4 (Overshoot): Base 28, Mid 5, Distal -35, Stinger -70 (Downward whip crack!)
# F5 (Recovery 1): Base 55, Mid 35, Distal -10, Stinger -30
# F6 (Recovery 2): Base 70, Mid 25, Distal -20, Stinger -45
ANGLES = [
    (75.0,  22.0, -25.0, -50.0), # F1: Rest
    (125.0, 150.0,  95.0,  40.0), # F2: Anticipation
    (28.0,  25.0,  22.0,  18.0), # F3: Whip Strike
    (28.0,   5.0, -35.0, -70.0), # F4: Overshoot
    (55.0,  35.0, -10.0, -30.0), # F5: Recovery 1
    (70.0,  25.0, -20.0, -45.0), # F6: Recovery 2
]

def render_frame(f_idx):
    grid = empty_grid()
    draw_stone_floor_and_turret(grid)
    
    # Locked base pivot point on turret:
    p0_x, p0_y = 18.0, 28.0
    
    th1, th2, th3, th_s = ANGLES[f_idx]
    
    seg1_pts, p1_x, p1_y = draw_rigid_segment(p0_x, p0_y, th1, is_base=True)
    seg2_pts, p2_x, p2_y = draw_rigid_segment(p1_x, p1_y, th2)
    seg3_pts, p3_x, p3_y = draw_rigid_segment(p2_x, p2_y, th3)
    stinger_pts = draw_stinger(p3_x, p3_y, th_s)
    
    all_tail = {}
    all_tail.update(seg1_pts)
    all_tail.update(seg2_pts)
    all_tail.update(seg3_pts)
    all_tail.update(stinger_pts)
    
    # Draw to grid
    for (x, y), col in all_tail.items():
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = col
            
    # Enclose outline '#'
    for (x, y), col in all_tail.items():
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                grid[ny][nx] = "#"
                
    # Extra spark particles in F2 and F3 (Rule 3.3)
    if f_idx == 1:
        # F2: Cyan electric sparks charging at tip
        grid[15][13] = "E"
        grid[14][16] = "Q"
    elif f_idx == 2:
        # F3: Energy discharge sparks along strike path
        grid[18][38] = "E"
        grid[20][39] = "Q"
        
    return grid, (p0_x, p0_y), (p3_x, p3_y)

frames_data = [render_frame(i) for i in range(6)]

def check_naked(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "E", "W", "Q"): # plasma glows don't need black outline
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

print("\n=== VALIDATION CHECKS ===")
for i, (g, p0, p3) in enumerate(frames_data):
    naked = check_naked(g)
    print(f"Frame {i+1}:")
    print(f"  Pivot (X0, Y0) = {p0} (LOCKED 100%)")
    print(f"  Distal Joint (X3, Y3) = ({p3[0]:.1f}, {p3[1]:.1f})")
    print(f"  Naked pixels = {len(naked)}")

# Render images
gif_frames = []
for idx, (g, p0, p3) in enumerate(frames_data):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/scorpion_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/scorpion_sheet.png")

gif_frames[0].save(
    "python/scorpion_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS
    loop=0
)
print("Rendered scorpion_sheet.png and scorpion_anim.gif successfully.")
