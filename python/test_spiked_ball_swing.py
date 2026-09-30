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
    # Stone beam at top (y=1..5, x=10..38, organic block with soft outline)
    for x in range(12, 36): grid[1][x] = "#"
    grid[2][11] = "#"; grid[2][36] = "#"
    for x in range(12, 36): grid[2][x] = "K"
    
    grid[3][10] = "#"; grid[3][37] = "#"
    for x in range(11, 37): grid[3][x] = "G"
    
    grid[4][10] = "#"; grid[4][37] = "#"
    for x in range(11, 37): grid[4][x] = "M"
    for x in range(11, 37): grid[5][x] = "#"
    
    # Chiseled stone mortared seam at x=20, 28
    grid[2][20] = "G"; grid[3][20] = "M"; grid[4][20] = "#"
    grid[2][28] = "G"; grid[3][28] = "M"; grid[4][28] = "#"
    
    # Iron Anchor Bracket (Bản lề sắt gắn chặt vào xà, y=5..7, x=22..26)
    # Fixed 100% across all 4 frames!
    grid[5][22] = "#"; grid[5][23] = "A"; grid[5][24] = "H"; grid[5][25] = "A"; grid[5][26] = "#"
    grid[6][23] = "#"; grid[6][24] = "B"; grid[6][25] = "#"
    grid[7][23] = "#"; grid[7][24] = "C"; grid[7][25] = "#" # Pivot Eyelet Point at (24, 7)

def draw_chain_link(grid, cx, cy, facing_front=True):
    # cx, cy is the center of the link
    ix, iy = int(round(cx)), int(round(cy))
    if facing_front:
        # Front-facing oval link (width 5, height 4)
        for dx in (-1, 0, 1):
            grid[iy - 1][ix + dx] = "#"
            grid[iy + 2][ix + dx] = "#"
        grid[iy][ix - 2] = "#"; grid[iy][ix + 2] = "#"
        grid[iy + 1][ix - 2] = "#"; grid[iy + 1][ix + 2] = "#"
        
        # Inner hole & metal
        grid[iy][ix - 1] = "A"; grid[iy][ix] = "."; grid[iy][ix + 1] = "B"
        grid[iy + 1][ix - 1] = "B"; grid[iy + 1][ix] = "."; grid[iy + 1][ix + 1] = "C"
    else:
        # Profile-facing vertical link (width 3, height 5)
        for dy in (-2, 2):
            grid[iy + dy][ix] = "#"
        for dy in (-1, 0, 1):
            grid[iy + dy][ix - 1] = "#"
            grid[iy + dy][ix + 1] = "#"
            grid[iy + dy][ix] = "A" if dy < 0 else ("B" if dy == 0 else "C")

def draw_spiked_ball(grid, cx, cy):
    # Spherical iron ball (radius 6px) with 3D spikes and 10 o'clock static highlight
    ix, iy = int(round(cx)), int(round(cy))
    r = 5.5
    
    # 1. Top eyelet ring connecting to bottom chain link
    grid[iy - 7][ix] = "#"
    grid[iy - 6][ix - 1] = "#"; grid[iy - 6][ix] = "A"; grid[iy - 6][ix + 1] = "#"
    grid[iy - 5][ix - 1] = "#"; grid[iy - 5][ix] = "B"; grid[iy - 5][ix + 1] = "#"

    # 2. Main spherical ball body
    for y in range(iy - 6, iy + 7):
        for x in range(ix - 6, ix + 7):
            dx = x - ix
            dy = y - iy
            d2 = dx*dx + dy*dy
            if d2 <= r*r:
                dz = math.sqrt(max(0.0, r*r - d2))
                # 3/4 top-down light vector from upper-left (approx 10 o'clock: -0.45, -0.55, 0.70)
                light = -0.45 * (dx / r) - 0.55 * (dy / r) + 0.70 * (dz / r)
                
                # 10 o'clock Specular Glint (around dx = -2, dy = -2)
                if (dx in (-2, -1) and dy in (-3, -2)):
                    col = "H"
                elif light > 0.40:
                    col = "A"
                elif light > -0.15:
                    col = "B"
                else:
                    col = "C"
                grid[y][x] = col

    # 3. 3D Metal Spikes projecting outwards:
    # - Left spike (pointing left)
    grid[iy][ix - 7] = "H"; grid[iy][ix - 8] = "#"
    grid[iy - 1][ix - 6] = "#"; grid[iy + 1][ix - 6] = "#"
    
    # - Right spike (pointing right, in shadow)
    grid[iy][ix + 7] = "C"; grid[iy][ix + 8] = "#"
    grid[iy - 1][ix + 6] = "#"; grid[iy + 1][ix + 6] = "#"
    
    # - Bottom spike (pointing down, deep shadow)
    grid[iy + 7][ix] = "C"; grid[iy + 8][ix] = "#"
    grid[iy + 6][ix - 1] = "#"; grid[iy + 6][ix + 1] = "#"
    
    # - Top-left spike (pointing up-left, lit)
    grid[iy - 5][ix - 5] = "A"; grid[iy - 6][ix - 6] = "#"
    
    # - Top-right spike (pointing up-right)
    grid[iy - 5][ix + 5] = "B"; grid[iy - 6][ix + 6] = "#"
    
    # - Bottom-left spike (pointing down-left)
    grid[iy + 5][ix - 5] = "B"; grid[iy + 6][ix - 6] = "#"
    
    # - Bottom-right spike (pointing down-right)
    grid[iy + 5][ix + 5] = "C"; grid[iy + 6][ix + 6] = "#"
    
    # - Front-center spike (pointing directly at camera / 3D depth)
    grid[iy + 1][ix + 1] = "A"
    grid[iy + 2][ix + 1] = "B"
    grid[iy + 1][ix + 2] = "C"

def draw_ground_shadow(grid, ball_x):
    # Elliptical soft contact shadow S at floor level (y=42..44)
    sx = int(round(ball_x))
    for x in range(sx - 5, sx + 6):
        grid[42][x] = "S"
    for x in range(sx - 4, sx + 5):
        grid[43][x] = "S"
    for x in range(sx - 2, sx + 3):
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
    
    # Fixed stone beam and anchor bracket (Pivot locked at (24, 7))
    draw_stone_beam_and_pivot(grid)
    
    # 4 Chain Links & Spiked Ball Coordinates per frame:
    if f_idx == 0:
        # Frame 1 (Swing Left): Quả cầu vung sang cực đại bên TRÁI. Sợi xích uốn nhẹ sang trái.
        links = [
            (23.2, 10.5, False), # Link 1 (profile)
            (20.8, 14.5, True),  # Link 2 (front)
            (17.8, 19.0, False), # Link 3 (profile)
            (15.2, 23.5, True),  # Link 4 (front)
        ]
        ball_pos = (14.0, 30.0)
        
    elif f_idx == 1:
        # Frame 2 (Passing Center / Follow-Through):
        # Móc treo và 2 mắt xích trên ĐÃ RƠI VỀ GIỮA, nhưng quả cầu và mắt xích dưới VẪN TRỄ NHỊP Ở PHÍA SAU (uốn chữ C mềm)!
        links = [
            (24.0, 10.5, False), # Link 1: straight under pivot! (x=24.0)
            (23.2, 14.8, True),  # Link 2: near center (x=23.2)
            (20.0, 19.5, False), # Link 3: LAGGING behind on the left! (x=20.0)
            (17.2, 24.5, True),  # Link 4: LAGGING behind on the left! (x=17.2)
        ]
        ball_pos = (16.5, 31.5) # Spiked ball lagging behind on the left, curving in a smooth C-shape!
        
    elif f_idx == 2:
        # Frame 3 (Swing Right): Quả cầu vung sang cực đại bên PHẢI.
        links = [
            (24.8, 10.5, False), # Link 1
            (27.2, 14.5, True),  # Link 2
            (30.2, 19.0, False), # Link 3
            (32.8, 23.5, True),  # Link 4
        ]
        ball_pos = (34.0, 30.0)
        
    else:
        # Frame 4 (Return Center):
        # Móc treo và 2 mắt xích trên ĐÃ LẮC VỀ GIỮA / BẮT ĐẦU SANG TRÁI, nhưng quả cầu VẪN TRỄ NHỊP Ở PHÍA PHẢI (uốn chữ C ngược)!
        links = [
            (24.0, 10.5, False), # Link 1: straight under pivot! (x=24.0)
            (24.8, 14.8, True),  # Link 2: near center (x=24.8)
            (28.0, 19.5, False), # Link 3: LAGGING behind on the right! (x=28.0)
            (30.8, 24.5, True),  # Link 4: LAGGING behind on the right! (x=30.8)
        ]
        ball_pos = (31.5, 31.5) # Spiked ball lagging behind on the right, curving in an inverted C-shape!
        
    # Draw Chain Links
    for cx, cy, facing in links:
        draw_chain_link(grid, cx, cy, facing)
        
    # Draw Spiked Ball
    draw_spiked_ball(grid, ball_pos[0], ball_pos[1])
    
    # Draw Ground Shadow S
    draw_ground_shadow(grid, ball_pos[0])
    
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/swing_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/test_spiked_swing_sheet.png")

gif_frames[0].save(
    "python/test_spiked_swing_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered test_spiked_swing_sheet.png and test_spiked_swing_anim.gif successfully!")
