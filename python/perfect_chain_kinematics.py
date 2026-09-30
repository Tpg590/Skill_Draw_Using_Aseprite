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

def draw_continuous_chain(grid, joints):
    # joints has 5 points: J0 (pivot: 24, 7), J1, J2, J3, J4 (eyelet)
    # 4 links:
    # Link 1: J0 -> J1 (profile link)
    # Link 2: J1 -> J2 (front link)
    # Link 3: J2 -> J3 (profile link)
    # Link 4: J3 -> J4 (front link)
    
    for i in range(4):
        p1 = joints[i]
        p2 = joints[i+1]
        facing_front = (i % 2 == 1)
        
        # Render link from p1 to p2
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0: continue
        ux, uy = dx / length, dy / length # tangent vector
        vx, vy = -uy, ux                  # normal vector
        
        # Sample points along the link
        steps = int(math.ceil(length * 2))
        for s in range(-1, steps + 2):
            t = s / float(steps)
            cx = x1 + t * dx
            cy = y1 + t * dy
            
            if facing_front:
                # Front-facing link: oval ring with width 2.0 to each side
                for w_offset in (-1.8, -1.0, 0.0, 1.0, 1.8):
                    px = int(round(cx + w_offset * vx))
                    py = int(round(cy + w_offset * vy))
                    if 0 <= px < W and 0 <= py < H:
                        if abs(w_offset) >= 1.5 or s in (-1, steps + 1):
                            grid[py][px] = "#"
                        elif abs(w_offset) >= 0.8:
                            grid[py][px] = "A" if w_offset < 0 else "B"
                        else:
                            # Central hole (clear background if in middle of link)
                            if 1 <= s <= steps - 1:
                                grid[py][px] = "."
                            else:
                                grid[py][px] = "B"
            else:
                # Profile link: narrower bar (width 1.0)
                for w_offset in (-1.0, 0.0, 1.0):
                    px = int(round(cx + w_offset * vx))
                    py = int(round(cy + w_offset * vy))
                    if 0 <= px < W and 0 <= py < H:
                        if abs(w_offset) >= 0.9 or s in (-1, steps + 1):
                            grid[py][px] = "#"
                        else:
                            grid[py][px] = "A" if ux < 0 else "B"

def draw_spiked_ball(grid, cx, cy, eyelet_pt):
    ix, iy = int(round(cx)), int(round(cy))
    ex, ey = int(round(eyelet_pt[0])), int(round(eyelet_pt[1]))
    
    # 1. Connect eyelet loop directly to top of ball
    for dy in range(ey - 1, iy - 4):
        grid[dy][ex - 1] = "#"
        grid[dy][ex] = "B"
        grid[dy][ex + 1] = "#"
    grid[ey - 2][ex] = "#"
    
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
    
    # 2. Continuous chain joints & ball coordinates per frame:
    if f_idx == 0:
        # Frame 1 (Swing Left): Quả cầu vung sang cực đại bên TRÁI. Sợi xích hơi uốn cong sang trái.
        joints = [
            (24.0, 7.0),   # J0: Pivot
            (22.2, 10.8),  # J1
            (19.5, 14.8),  # J2
            (16.5, 19.0),  # J3
            (13.8, 23.2),  # J4: Eyelet
        ]
        ball = (12.2, 29.2)
        is_high = True
        
    elif f_idx == 1:
        # Frame 2 (Passing Center / Follow-Through):
        # Móc treo và 2 mắt xích trên ĐÃ RƠI VỀ GIỮA, nhưng quả cầu gai và mắt xích dưới VẪN TRỄ NHỊP (chữ C mềm)!
        joints = [
            (24.0, 7.0),   # J0: Pivot
            (24.0, 11.0),  # J1: thẳng đứng ngay dưới chốt!
            (22.8, 15.0),  # J2: chớm cong sang trái
            (19.8, 19.0),  # J3: trễ nhịp ở bên trái
            (16.5, 23.2),  # J4: Eyelet trễ nhịp ở bên trái
        ]
        ball = (14.8, 29.5) # Spiked ball lagging behind in a smooth C-curve!
        is_high = False
        
    elif f_idx == 2:
        # Frame 3 (Swing Right): Quả cầu vung sang cực đại bên PHẢI.
        joints = [
            (24.0, 7.0),   # J0: Pivot
            (25.8, 10.8),  # J1
            (28.5, 14.8),  # J2
            (31.5, 19.0),  # J3
            (34.2, 23.2),  # J4: Eyelet
        ]
        ball = (35.8, 29.2)
        is_high = True
        
    else:
        # Frame 4 (Return Center):
        # Móc treo và 2 mắt xích trên ĐÃ LẮC VỀ GIỮA / BẮT ĐẦU SANG TRÁI, nhưng quả cầu VẪN TRỄ NHỊP (chữ C ngược)!
        joints = [
            (24.0, 7.0),   # J0: Pivot
            (24.0, 11.0),  # J1: thẳng đứng ngay dưới chốt!
            (25.2, 15.0),  # J2: chớm cong sang phải
            (28.2, 19.0),  # J3: trễ nhịp ở bên phải
            (31.5, 23.2),  # J4: Eyelet trễ nhịp ở bên phải
        ]
        ball = (33.2, 29.5) # Spiked ball lagging behind in an inverted C-curve!
        is_high = False
        
    # Draw continuous interlocking chain
    draw_continuous_chain(grid, joints)
    
    # Draw spiked ball and eyelet
    draw_spiked_ball(grid, ball[0], ball[1], joints[4])
    
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_kinematic_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_kinematic_sheet.png")

gif_frames[0].save(
    "python/perfect_kinematic_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered perfect_kinematic_sheet.png and perfect_kinematic_anim.gif successfully!")
