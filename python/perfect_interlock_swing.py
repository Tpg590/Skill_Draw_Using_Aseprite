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
    # 100% fixed pivot point at (24, 7) across all 4 frames!
    grid[5][22] = "#"; grid[5][23] = "A"; grid[5][24] = "H"; grid[5][25] = "A"; grid[5][26] = "#"
    grid[6][22] = "#"; grid[6][23] = "B"; grid[6][24] = "A"; grid[6][25] = "B"; grid[6][26] = "#"
    grid[7][23] = "#"; grid[7][24] = "C"; grid[7][25] = "#" # Pivot loop at (24, 7)

def draw_front_link(grid, cx, cy):
    # Front-facing chunky chain link (width 5, height 5)
    ix, iy = int(round(cx)), int(round(cy))
    # Outer ring
    for dx in (-1, 0, 1):
        grid[iy - 2][ix + dx] = "#"
        grid[iy + 2][ix + dx] = "#"
    grid[iy - 1][ix - 2] = "#"; grid[iy - 1][ix + 2] = "#"
    grid[iy][ix - 2] = "#";     grid[iy][ix + 2] = "#"
    grid[iy + 1][ix - 2] = "#"; grid[iy + 1][ix + 2] = "#"
    
    # Shading & inner opening
    grid[iy - 1][ix - 1] = "H"; grid[iy - 1][ix] = "A"; grid[iy - 1][ix + 1] = "B"
    grid[iy][ix - 1] = "A";     grid[iy][ix] = ".";     grid[iy][ix + 1] = "C"
    grid[iy + 1][ix - 1] = "B"; grid[iy + 1][ix] = "C"; grid[iy + 1][ix + 1] = "C"

def draw_profile_link(grid, cx, cy, tilt=0):
    # Profile-facing vertical chain link (width 3, height 5)
    ix, iy = int(round(cx)), int(round(cy))
    grid[iy - 2][ix] = "#"
    grid[iy + 2][ix] = "#"
    for dy in (-1, 0, 1):
        x_off = int(round(dy * tilt))
        grid[iy + dy][ix - 1 + x_off] = "#"
        grid[iy + dy][ix + 1 + x_off] = "#"
        grid[iy + dy][ix + x_off] = "A" if dy < 0 else ("B" if dy == 0 else "C")

def draw_ball_eyelet(grid, cx, cy):
    # Top ring of spiked ball (width 5, height 4)
    ix, iy = int(round(cx)), int(round(cy))
    grid[iy - 1][ix] = "#"
    grid[iy][ix - 2] = "#"; grid[iy][ix - 1] = "A"; grid[iy][ix] = "."; grid[iy][ix + 1] = "B"; grid[iy][ix + 2] = "#"
    grid[iy + 1][ix - 2] = "#"; grid[iy + 1][ix - 1] = "B"; grid[iy + 1][ix] = "C"; grid[iy + 1][ix + 1] = "C"; grid[iy + 1][ix + 2] = "#"
    grid[iy + 2][ix - 1] = "#"; grid[iy + 2][ix] = "B"; grid[iy + 2][ix + 1] = "#"

def draw_spiked_ball(grid, cx, cy):
    ix, iy = int(round(cx)), int(round(cy))
    
    # 1. Spherical Ball Core (radius 6px)
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

    # 2. Chunky conical 3D spikes:
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
    
    # 2. Interlocking Kinematics per frame:
    # 4 distinct interlocking links:
    # Link 1 (profile), Link 2 (front), Link 3 (profile), Link 4 (front)
    # Plus Ball Eyelet connecting directly to Link 4!
    
    if f_idx == 0:
        # Frame 1 (Swing Left): Quả cầu gai vung sang cực đại bên TRÁI. Sợi xích hơi uốn cong sang trái.
        l1 = (23.5, 9.0, -0.3)
        l2 = (20.5, 12.0)
        l3 = (17.5, 15.0, -0.3)
        l4 = (14.5, 18.0)
        eyelet = (12.5, 21.0)
        ball = (12.0, 27.5)
        is_high = True
        
    elif f_idx == 1:
        # Frame 2 (Passing Center / Follow-Through):
        # Móc treo và 2 mắt xích trên ĐÃ RƠI VỀ GIỮA (x=24, 23),
        # nhưng quả cầu gai và 2 mắt xích dưới VẪN TRỄ NHỊP Ở PHÍA SAU (uốn chữ C mềm)!
        l1 = (24.0, 9.0, 0.0)    # Link 1: thẳng đứng ngay dưới chốt!
        l2 = (23.0, 12.0)        # Link 2: rơi về gần giữa
        l3 = (20.0, 15.0, -0.4)  # Link 3: trễ nhịp ở bên trái, nghiêng chéo đón l2
        l4 = (16.0, 18.0)        # Link 4: trễ nhịp ở bên trái, đón l3
        eyelet = (13.5, 21.0)    # Eyelet: trễ nhịp
        ball = (13.5, 28.5)      # Spiked ball: trễ nhịp ở bên trái, tạo thành chữ C mềm mại!
        is_high = False
        
    elif f_idx == 2:
        # Frame 3 (Swing Right): Quả cầu gai vung sang cực đại bên PHẢI.
        l1 = (24.5, 9.0, 0.3)
        l2 = (27.5, 12.0)
        l3 = (30.5, 15.0, 0.3)
        l4 = (33.5, 18.0)
        eyelet = (35.5, 21.0)
        ball = (36.0, 27.5)
        is_high = True
        
    else:
        # Frame 4 (Return Center):
        # Móc treo và 2 mắt xích trên ĐÃ LẮC VỀ GIỮA / BẮT ĐẦU SANG TRÁI,
        # nhưng quả cầu và 2 mắt xích dưới VẪN TRỄ NHỊP Ở PHÍA PHẢI (uốn chữ C ngược)!
        l1 = (24.0, 9.0, 0.0)    # Link 1: thẳng đứng ngay dưới chốt!
        l2 = (25.0, 12.0)        # Link 2: rơi về gần giữa
        l3 = (28.0, 15.0, 0.4)   # Link 3: trễ nhịp ở bên phải, nghiêng chéo đón l2
        l4 = (32.0, 18.0)        # Link 4: trễ nhịp ở bên phải, đón l3
        eyelet = (34.5, 21.0)    # Eyelet: trễ nhịp
        ball = (34.5, 28.5)      # Spiked ball: trễ nhịp ở bên phải, tạo thành chữ C ngược mềm mại!
        is_high = False
        
    # Draw 4 interlocking chain links in Z-order
    # Draw front links first, then profile links threading through them:
    draw_front_link(grid, l2[0], l2[1])
    draw_front_link(grid, l4[0], l4[1])
    draw_ball_eyelet(grid, eyelet[0], eyelet[1])
    
    draw_profile_link(grid, l1[0], l1[1], l1[2])
    draw_profile_link(grid, l3[0], l3[1], l3[2])
    
    # Bridge the connection between Link 4 and Ball Eyelet so they physically interlock
    # Eyelet top enters inside Link 4 bottom hole!
    ix4, iy4 = int(round(l4[0])), int(round(l4[1]))
    iex, iey = int(round(eyelet[0])), int(round(eyelet[1]))
    grid[iy4 + 1][ix4] = "C" # Link 4 bottom bar
    grid[iey - 1][iex] = "A" # Eyelet top bar loops over Link 4!
    
    # Draw Spiked Ball
    draw_spiked_ball(grid, ball[0], ball[1])
    
    # Draw Ground Shadow S
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/interlock_spiked_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/interlock_spiked_sheet.png")

gif_frames[0].save(
    "python/interlock_spiked_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered interlock_spiked_sheet.png and interlock_spiked_anim.gif successfully!")
