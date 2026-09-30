import os
import math
from PIL import Image

W, H = 48, 48

# Stardew Valley Warm & Soft Palette (NO #000000!)
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (38, 24, 44, 130),     # Soft ground shadow (Alpha 130)
    "#": (38, 30, 44, 255),     # Soft dark purple-charcoal outline (#261e2c - NO #000000!)
    
    # Warm Cold Iron / Steel (Chain links & Spiked Ball)
    "H": (216, 226, 234, 255),  # 10 o'clock specular glint & bright edge (#d8e2ea)
    "A": (154, 166, 182, 255),  # Lit metal highlight (#9aa6b6)
    "B": (98, 110, 128, 255),   # Metal body midtone (#626e80)
    "C": (56, 64, 80, 255),     # Metal deep shadow / crevice (#384050)
    
    # Warm Stone Beam & Anchor Bracket
    "K": (164, 148, 134, 255),  # Stone beam highlight (#a49486)
    "G": (118, 102, 88, 255),   # Stone beam midtone (#766658)
    "M": (72, 60, 52, 255),     # Stone beam shadow (#483c34)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_stone_beam_and_pivot(grid):
    # Stone beam spanning across top (y=1..5, x=8..40)
    for x in range(10, 38): grid[1][x] = "#"
    grid[2][9] = "#"; grid[2][38] = "#"
    for x in range(10, 38): grid[2][x] = "K"
    
    grid[3][8] = "#"; grid[3][39] = "#"
    for x in range(9, 39): grid[3][x] = "G"
    
    grid[4][8] = "#"; grid[4][39] = "#"
    for x in range(9, 39): grid[4][x] = "M"
    for x in range(9, 39): grid[5][x] = "#"
    
    # Masonry chiseled seams at x=18, 29
    grid[2][18] = "G"; grid[3][18] = "M"; grid[4][18] = "#"
    grid[2][29] = "G"; grid[3][29] = "M"; grid[4][29] = "#"
    
    # Iron Anchor Bracket (Bản lề sắt gắn chặt vào xà, y=5..7, x=22..26)
    # 100% fixed pivot point across all 4 frames!
    grid[5][22] = "#"; grid[5][23] = "A"; grid[5][24] = "H"; grid[5][25] = "A"; grid[5][26] = "#"
    grid[6][22] = "#"; grid[6][23] = "B"; grid[6][24] = "A"; grid[6][25] = "B"; grid[6][26] = "#"
    grid[7][23] = "#"; grid[7][24] = "C"; grid[7][25] = "#" # Pivot loop at (24, 7)

def draw_interlocking_chain(grid, points):
    # points: list of 4 link centers (cx, cy)
    # Links alternate: Link 1 (profile), Link 2 (front), Link 3 (profile), Link 4 (front)
    # Link 1 passes through pivot loop at (24, 7)
    
    for i, (cx, cy) in enumerate(points):
        ix, iy = int(round(cx)), int(round(cy))
        facing_front = (i % 2 == 1)
        
        if facing_front:
            # Front-facing link: oval with central opening
            # Size: width 5, height 5
            for dx in (-1, 0, 1):
                grid[iy - 2][ix + dx] = "#"
                grid[iy + 2][ix + dx] = "#"
            grid[iy - 1][ix - 2] = "#"; grid[iy - 1][ix + 2] = "#"
            grid[iy][ix - 2] = "#";     grid[iy][ix + 2] = "#"
            grid[iy + 1][ix - 2] = "#"; grid[iy + 1][ix + 2] = "#"
            
            # Left side lit, right side in shadow
            grid[iy - 1][ix - 1] = "H"; grid[iy - 1][ix] = "A"; grid[iy - 1][ix + 1] = "B"
            grid[iy][ix - 1] = "A";     grid[iy][ix] = ".";     grid[iy][ix + 1] = "B"
            grid[iy + 1][ix - 1] = "B"; grid[iy + 1][ix] = "C"; grid[iy + 1][ix + 1] = "C"
        else:
            # Profile-facing link: vertical bar passing through front link's hole
            # Size: width 3, height 5
            grid[iy - 2][ix] = "#"
            grid[iy + 2][ix] = "#"
            for dy in (-1, 0, 1):
                grid[iy + dy][ix - 1] = "#"
                grid[iy + dy][ix + 1] = "#"
                grid[iy + dy][ix] = "A" if dy < 0 else ("B" if dy == 0 else "C")

def draw_spiked_ball(grid, cx, cy, eyelet_cx, eyelet_cy):
    ix, iy = int(round(cx)), int(round(cy))
    e_ix, e_iy = int(round(eyelet_cx)), int(round(eyelet_cy))
    
    # 1. Top eyelet loop on ball (interlocking with Link 4)
    for dy in (-1, 0, 1):
        grid[e_iy + dy][e_ix - 1] = "#"
        grid[e_iy + dy][e_ix + 1] = "#"
        grid[e_iy + dy][e_ix] = "A" if dy <= 0 else "B"
    grid[e_iy - 2][e_ix] = "#"
    grid[e_iy + 2][e_ix] = "#"
    
    # Stalk connecting eyelet to ball core
    for y in range(e_iy + 1, iy - 5):
        grid[y][ix - 1] = "#"
        grid[y][ix] = "B"
        grid[y][ix + 1] = "#"

    # 2. Spherical Ball Core (radius 6px)
    r = 5.6
    for y in range(iy - 6, iy + 7):
        for x in range(ix - 6, ix + 7):
            dx = x - ix
            dy = y - iy
            d2 = dx*dx + dy*dy
            if d2 <= r*r:
                dz = math.sqrt(max(0.0, r*r - d2))
                # 3/4 top-down directional lighting from 10 o'clock (-0.45, -0.55, 0.70)
                light = -0.45 * (dx / r) - 0.55 * (dy / r) + 0.70 * (dz / r)
                
                # STATIC 10 O'CLOCK SPECULAR HIGHLIGHT (Quy tắc 1.3: Cố định góc 10h)
                if dx in (-2, -1) and dy in (-3, -2):
                    col = "H"
                elif light > 0.42:
                    col = "A"
                elif light > -0.15:
                    col = "B"
                else:
                    col = "C"
                grid[y][x] = col

    # 3. Chunky conical 3D spikes:
    # Left spike (lit upper side)
    grid[iy - 1][ix - 7] = "#"; grid[iy][ix - 7] = "A"; grid[iy + 1][ix - 7] = "#"
    grid[iy][ix - 8] = "H"; grid[iy][ix - 9] = "#"
    grid[iy - 1][ix - 6] = "#"; grid[iy + 1][ix - 6] = "#"
    
    # Right spike (in shadow)
    grid[iy - 1][ix + 7] = "#"; grid[iy][ix + 7] = "C"; grid[iy + 1][ix + 7] = "#"
    grid[iy][ix + 8] = "C"; grid[iy][ix + 9] = "#"
    grid[iy - 1][ix + 6] = "#"; grid[iy + 1][ix + 6] = "#"
    
    # Bottom spike (deep shadow)
    grid[iy + 7][ix - 1] = "#"; grid[iy + 7][ix] = "C"; grid[iy + 7][ix + 1] = "#"
    grid[iy + 8][ix] = "C"; grid[iy + 9][ix] = "#"
    grid[iy + 6][ix - 1] = "#"; grid[iy + 6][ix + 1] = "#"
    
    # Top-Left spike (facing light)
    grid[iy - 6][ix - 6] = "A"; grid[iy - 7][ix - 7] = "#"
    grid[iy - 5][ix - 6] = "#"; grid[iy - 6][ix - 5] = "#"
    
    # Top-Right spike
    grid[iy - 6][ix + 6] = "B"; grid[iy - 7][ix + 7] = "#"
    grid[iy - 5][ix + 6] = "#"; grid[iy - 6][ix + 5] = "#"
    
    # Bottom-Left spike
    grid[iy + 6][ix - 6] = "B"; grid[iy + 7][ix - 7] = "#"
    grid[iy + 5][ix - 6] = "#"; grid[iy + 6][ix - 5] = "#"
    
    # Bottom-Right spike
    grid[iy + 6][ix + 6] = "C"; grid[iy + 7][ix + 7] = "#"
    grid[iy + 5][ix + 6] = "#"; grid[iy + 6][ix + 5] = "#"
    
    # Front-Center 3D protruding studs (giving genuine 3/4 spherical volume!)
    grid[iy + 1][ix - 2] = "A"; grid[iy + 2][ix - 2] = "B"
    grid[iy][ix + 2] = "A";     grid[iy + 1][ix + 2] = "B"; grid[iy + 2][ix + 2] = "C"

def draw_ground_shadow(grid, ball_x, is_high_swing=False):
    # Soft elliptical shadow S at floor level (y=42..44)
    # When ball is high (F1, F3), shadow is slightly smaller (radius 4)
    # When ball is low (F2, F4), shadow is slightly larger (radius 5.5)
    sx = int(round(ball_x))
    r_x = 4 if is_high_swing else 5
    for x in range(sx - r_x, sx + r_x + 1):
        grid[42][x] = "S"
    for x in range(sx - (r_x - 1), sx + r_x):
        grid[43][x] = "S"
    for x in range(sx - (r_x - 3), sx + (r_x - 2)):
        grid[44][x] = "S"

def outline_enclosing(grid):
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def build_frame(f_idx):
    grid = empty_grid()
    
    # 1. Stone beam & locked pivot point (24, 7)
    draw_stone_beam_and_pivot(grid)
    
    # 2. Kinematics per frame:
    if f_idx == 0:
        # Frame 1 (Swing Left): Quả cầu gai vung sang cực đại bên TRÁI.
        # Sợi xích hơi uốn cong hướng sang trái.
        points = [
            (23.2, 9.2),   # Link 1 (profile)
            (21.0, 12.8),  # Link 2 (front)
            (18.0, 16.5),  # Link 3 (profile)
            (15.0, 20.2),  # Link 4 (front)
        ]
        eyelet = (13.0, 23.5)
        ball = (12.5, 29.5)
        is_high = True
        
    elif f_idx == 1:
        # Frame 2 (Passing Center / Follow-Through):
        # Móc treo và 2 mắt xích trên ĐÃ RƠI VỀ GIỮA, nhưng quả cầu gai và mắt xích dưới VẪN TRỄ NHỊP (chữ C mềm)!
        points = [
            (24.0, 9.2),   # Link 1: straight under pivot! (x=24.0)
            (23.5, 12.8),  # Link 2: near center (x=23.5)
            (20.5, 16.6),  # Link 3: LAGGING behind on left (x=20.5)
            (17.2, 20.6),  # Link 4: LAGGING behind on left (x=17.2)
        ]
        eyelet = (15.2, 24.2)
        ball = (14.5, 30.5) # Lagging behind in a smooth C-curve!
        is_high = False
        
    elif f_idx == 2:
        # Frame 3 (Swing Right): Quả cầu gai vung sang cực đại bên PHẢI.
        points = [
            (24.8, 9.2),   # Link 1
            (27.0, 12.8),  # Link 2
            (30.0, 16.5),  # Link 3
            (33.0, 20.2),  # Link 4
        ]
        eyelet = (35.0, 23.5)
        ball = (35.5, 29.5)
        is_high = True
        
    else:
        # Frame 4 (Return Center):
        # Móc treo và 2 mắt xích trên ĐÃ LẮC VỀ GIỮA / BẮT ĐẦU SANG TRÁI, nhưng quả cầu VẪN TRỄ NHỊP (chữ C ngược)!
        points = [
            (24.0, 9.2),   # Link 1: straight under pivot! (x=24.0)
            (24.5, 12.8),  # Link 2: near center (x=24.5)
            (27.5, 16.6),  # Link 3: LAGGING behind on right (x=27.5)
            (30.8, 20.6),  # Link 4: LAGGING behind on right (x=30.8)
        ]
        eyelet = (32.8, 24.2)
        ball = (33.5, 30.5) # Lagging behind in an inverted C-curve!
        is_high = False
        
    # Draw interlocking chain links
    draw_interlocking_chain(grid, points)
    
    # Draw spiked ball and eyelet
    draw_spiked_ball(grid, ball[0], ball[1], eyelet[0], eyelet[1])
    
    # Draw ground shadow S
    draw_ground_shadow(grid, ball[0], is_high)
    
    # Enclose with soft outline
    outline_enclosing(grid)
    
    return grid

frames = [build_frame(i) for i in range(4)]

# Check naked pixels
def check_outline(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n=== OUTLINE CHECK ===")
for i, fr in enumerate(frames):
    n = check_outline(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Render images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_spiked_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_spiked_sheet.png")

gif_frames[0].save(
    "python/perfect_spiked_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered perfect_spiked_sheet.png and perfect_spiked_anim.gif successfully!")
