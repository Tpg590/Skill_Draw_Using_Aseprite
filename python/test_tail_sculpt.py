import math
from PIL import Image

W, H = 48, 48

# Color Palette (FreeStyle Blue-Steel + Glowing Cyan Plasma)
PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (10, 16, 26, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 18, 28, 255),     # Clean dark navy-black outline (#0c121c)
    
    # Cold Blue-Steel (Plating & Segments)
    "A": (214, 230, 244, 255),  # Silvery light steel highlight (#d6e6f4)
    "B": (136, 158, 184, 255),  # Cold blue-gray steel midtone (#889eb8)
    "C": (64, 82, 108, 255),    # Deep navy-slate steel shadow (#40526c)
    "D": (28, 38, 56, 255),     # Dark navy crevice / inner seam (#1c2638)
    
    # Glowing Cyan Stinger & Plasma OSL
    "W": (255, 255, 255, 255),  # White-hot stinger core / tip (#ffffff)
    "E": (64, 240, 255, 255),   # Radiant cyan plasma (#40f0ff)
    "Q": (20, 160, 210, 255),   # Cyan glow halo / OSL bleed (#14a0d2)
    "T": (12, 80, 130, 255),    # Deep cyan aura shadow (#0c5082)
    
    # Brass / Bronze Pivot Pins & Rivets
    "K": (240, 172, 60, 255),   # Golden brass highlight (#f0ac3c)
    "J": (144, 88, 24, 255),    # Deep bronze shadow (#905818)
    
    # Stone Plinth / Dais
    "M": (126, 138, 150, 255),  # Stone highlight (#7e8a96)
    "N": (80, 92, 106, 255),    # Stone midtone (#505c6a)
    "P": (44, 52, 66, 255),     # Stone deep shadow (#2c3442)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_stone_plinth_and_turret(grid):
    # 1. Ground Shadow (Ellipse on floor, not spanning whole canvas!)
    # X = 5..31, Y = 44..46
    for y in (44, 45, 46):
        x_min = 6 if y == 44 else (8 if y == 45 else 11)
        x_max = 28 if y == 44 else (26 if y == 45 else 23)
        for x in range(x_min, x_max + 1):
            grid[y][x] = "S"

    # 2. Stone Oval Plinth: Y = 41..44, X = 7..27 (Width 21px, strictly contained!)
    # Top surface (Y=41): X = 9..25
    grid[41][8] = "#"
    grid[41][26] = "#"
    for x in range(9, 26):
        grid[41][x] = "M" if x % 4 in (1, 2) else "N"
    
    # Front edge (Y=42..43): X = 7..27
    for y in (42, 43):
        grid[y][7] = "#"
        grid[y][27] = "#"
        for x in range(8, 27):
            if y == 42:
                grid[y][x] = "M" if x % 5 in (1, 2) else "N"
            else:
                grid[y][x] = "N" if x % 3 != 0 else "P"
                
    # Plinth bottom edge (Y=44): X = 8..26
    for x in range(8, 27):
        grid[44][x] = "#"

    # 3. Turret Chassis (Heavy Military Sci-Fi Pod):
    # Centered at X = 17. Base mounting flange at Y = 40, X = 11..23
    grid[40][10] = "#"; grid[40][24] = "#"
    for x in range(11, 24):
        grid[40][x] = "D"
    grid[40][12] = "K"; grid[40][13] = "J" # Left mounting bolt
    grid[40][21] = "K"; grid[40][22] = "J" # Right mounting bolt

    # Armor body: Y = 32..39
    body_profile = {
        39: (11, 23),
        38: (12, 22),
        37: (12, 22),
        36: (13, 21),
        35: (13, 21),
        34: (14, 20),
        33: (14, 20),
        32: (15, 19),
    }
    for y, (x_min, x_max) in body_profile.items():
        grid[y][x_min] = "#"
        grid[y][x_max] = "#"
        for x in range(x_min + 1, x_max):
            if x <= x_min + 2:
                grid[y][x] = "A" if y % 2 == 0 else "B"
            elif x <= 17:
                grid[y][x] = "B"
            elif x <= x_max - 2:
                grid[y][x] = "C"
            else:
                grid[y][x] = "D"

    # Armored panel seam & cooling vent on chassis:
    grid[35][16] = "D"; grid[35][17] = "D"; grid[35][18] = "D"
    grid[36][16] = "T"; grid[36][17] = "Q"; grid[36][18] = "E" # Cyan energy core
    grid[37][16] = "D"; grid[37][17] = "C"; grid[37][18] = "C"

    # Ball socket dome: Y = 28..31, X = 15..19
    # Fixed hinge pivot is at (17, 28)!
    grid[31][15] = "#"; grid[31][16] = "A"; grid[31][17] = "B"; grid[31][18] = "C"; grid[31][19] = "#"
    grid[30][15] = "#"; grid[30][16] = "K"; grid[30][17] = "B"; grid[30][18] = "D"; grid[30][19] = "#"
    grid[29][16] = "#"; grid[29][17] = "K"; grid[29][18] = "#"
    grid[28][16] = "#"; grid[28][17] = "#"; grid[28][18] = "#"

def draw_rigid_segment(x_start, y_start, theta_deg):
    # Rigid box segment: length 5px (u = 0..4), thickness 3px (v = -1..1)
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    seg_pixels = {}
    # Sample across length and thickness with sub-pixel sampling to guarantee solid coverage
    # u spans 0 to 4 (5px length)
    # v spans -1 to 1 (3px thickness)
    for u_step in range(9): # 0.0, 0.5, 1.0, ..., 4.0
        u = u_step * 0.5
        for v_step in (-1.0, -0.5, 0.0, 0.5, 1.0):
            v = v_step
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            ix = int(round(px))
            iy = int(round(py))
            
            # Shading logic:
            if v_step < -0.2:
                col = "A" # Upper armor highlight
            elif v_step > 0.2:
                col = "C" # Lower armor shadow
            else:
                if u_step in (0, 8):
                    col = "K" # Brass pivot bolt at ends
                elif u_step in (1, 7):
                    col = "J" # Bolt rim shade
                else:
                    col = "B" # Cold steel core
            seg_pixels[(ix, iy)] = col
            
    end_x = x_start + 4.0 * cos_t
    end_y = y_start - 4.0 * sin_t
    return seg_pixels, end_x, end_y

def draw_stinger_spike(x_start, y_start, theta_deg):
    theta = math.radians(theta_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    
    stinger_pixels = {}
    # 1. Bulbous plasma capacitor base (length 2px, thickness 4px)
    for u_step in (0.0, 0.5, 1.0, 1.5):
        u = u_step
        for v in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            ix = int(round(px))
            iy = int(round(py))
            if abs(v) >= 1.0:
                stinger_pixels[(ix, iy)] = "Q" # Cyan glow halo
            else:
                stinger_pixels[(ix, iy)] = "E" # Bright cyan plasma core
                
    # 2. Tapered needle shaft (length 3px, width 2px -> 1px)
    for u_step in (2.0, 2.5, 3.0, 3.5):
        u = u_step
        for v in (-0.5, 0.5):
            px = x_start + u * cos_t + v * (-sin_t)
            py = y_start - u * sin_t + v * (-cos_t)
            ix = int(round(px))
            iy = int(round(py))
            stinger_pixels[(ix, iy)] = "E"
            
    # 3. Razor-sharp white needle tip (length 2px, width 1px)
    for u in (4.0, 4.8, 5.5):
        px = x_start + u * cos_t
        py = y_start - u * sin_t
        ix = int(round(px))
        iy = int(round(py))
        stinger_pixels[(ix, iy)] = "W" # White-hot piercing needle tip
        
    return stinger_pixels

ANGLES = [
    (72.0,   25.0, -22.0, -48.0), # F1: Rest (natural C-curve)
    (122.0, 148.0,  92.0,  38.0), # F2: Anticipation (coiled deep left)
    (28.0,   25.0,  22.0,  18.0), # F3: Whip Strike (laser-straight diagonal)
    (30.0,    8.0, -32.0, -72.0), # F4: Overshoot (whip-crack downward snap)
    (54.0,   32.0, -12.0, -32.0), # F5: Recovery 1 (uncoiling back)
    (68.0,   26.0, -18.0, -42.0), # F6: Recovery 2 (settling into rest)
]

def render_tail_frame(f_idx):
    grid = empty_grid()
    draw_stone_plinth_and_turret(grid)
    
    # Strictly locked base hinge pin on turret socket:
    p0_x, p0_y = 17.0, 28.0
    
    th1, th2, th3, th_s = ANGLES[f_idx]
    
    seg1_pts, p1_x, p1_y = draw_rigid_segment(p0_x, p0_y, th1)
    seg2_pts, p2_x, p2_y = draw_rigid_segment(p1_x, p1_y, th2)
    seg3_pts, p3_x, p3_y = draw_rigid_segment(p2_x, p2_y, th3)
    stinger_pts = draw_stinger_spike(p3_x, p3_y, th_s)
    
    all_tail = {}
    all_tail.update(seg1_pts)
    all_tail.update(seg2_pts)
    all_tail.update(seg3_pts)
    all_tail.update(stinger_pts)
    
    # Draw tail parts onto grid
    for (x, y), col in all_tail.items():
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = col
            
    # Draw dark outline '#' around segments (except plasma glows)
    for (x, y), col in all_tail.items():
        if col in ("A", "B", "C", "D", "K", "J"):
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                    grid[ny][nx] = "#"
                    
    # Dynamic Particles & OSL (Rules 1.1 & 3.3)
    if f_idx == 1:
        # F2: Electric sparks charging around stinger
        grid[14][13] = "E"
        grid[13][16] = "Q"
        grid[17][11] = "T"
    elif f_idx == 2:
        # F3: High-speed strike shockwave / plasma exhaust particles
        grid[17][37] = "E"
        grid[18][39] = "W"
        grid[20][38] = "Q"
        grid[22][35] = "T"
    elif f_idx == 3:
        # F4: Kinetic snap residual spark
        grid[31][33] = "Q"
        grid[32][34] = "E"
        
    return grid, (p0_x, p0_y), (p3_x, p3_y)

frames = [render_tail_frame(i) for i in range(6)]

gif_frames = []
for idx, (g, p0, p3) in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/sculpt_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/sculpt_sheet.png")

gif_frames[0].save(
    "python/sculpt_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS
    loop=0
)
print("Rendered sculpt_sheet.png and sculpt_anim.gif.")

