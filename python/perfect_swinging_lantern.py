import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (18, 14, 24, 150),     # Soft cast shadow (Alpha 150)
    "#": (16, 14, 20, 255),     # Viền sẫm tối Terraria (#100e14)
    
    # Stone Floor Slabs
    "F1": (124, 132, 148, 255), # Stone slab highlight (#7c8494)
    "F2": (74, 80, 94, 255),    # Stone slab midtone (#4a505e)
    "F3": (38, 42, 52, 255),    # Stone slab crevice / shadow (#262a34)
    
    # Cold Iron Stand
    "I1": (154, 160, 176, 255), # Cold iron highlight (#9aa0b0)
    "I2": (84, 90, 104, 255),   # Cold iron midtone (#545a68)
    "I3": (42, 46, 56, 255),    # Cold iron shadow (#2a2e38)

    # Dynamic OSL on Iron (lit by golden lantern)
    "O1": (224, 180, 80, 255),  # Iron highlight lit by gold light (#e0b450)
    "O2": (138, 100, 40, 255),  # Iron midtone lit by warm light (#8a6428)

    # Oil Lantern & Golden Flame (OSL light source)
    "L1": (255, 252, 160, 255), # Blinding white-gold flame core (#ffea90)
    "L2": (252, 168, 32, 255),  # Rich golden-amber lantern glow (#fca820)
    "L3": (208, 90, 16, 255),   # Deep orange flame / heated bronze (#d05a10)
    "G1": (180, 220, 230, 255), # Lantern glass specular highlight (#b4dce6)
}

def create_environment_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Stone Floor (y=43..46, x=2..45)
    for x in range(2, 46):
        grid[43][x] = "#"
        grid[46][x] = "#"
        grid[44][x] = "F2"
        grid[45][x] = "F3"
        
    # Enclose floor left & right edges
    grid[44][2] = "#"
    grid[45][2] = "#"
    grid[44][45] = "#"
    grid[45][45] = "#"
        
    # Stone slab mortared vertical seams at x=14, 28
    grid[44][14] = "#"
    grid[45][14] = "#"
    grid[44][28] = "#"
    grid[45][28] = "#"
    
    # Stone highlights and chisel chips
    for x in (4, 5, 6, 16, 17, 18, 30, 31, 32):
        grid[44][x] = "F1"
    grid[44][9] = "F3"
    grid[44][23] = "F3"
    grid[44][39] = "F3"

    # 2. Fixed Iron Stand Base (y=40..43, x=18..30)
    # y=42: bolted flanged base
    grid[42][18] = "#"
    grid[42][19] = "I1"
    for x in range(20, 28):
        grid[42][x] = "I2"
    grid[42][28] = "I3"
    grid[42][29] = "#"
    grid[42][20] = "I1"
    grid[42][27] = "I1"

    # y=41: stepped base moulding
    grid[41][19] = "#"
    grid[41][20] = "I1"
    for x in range(21, 27):
        grid[41][x] = "I2"
    grid[41][27] = "I3"
    grid[41][28] = "#"

    # y=40: base collar with outline enclosing row 41
    grid[40][20] = "#"
    grid[40][21] = "#"
    grid[40][22] = "I1"
    grid[40][23] = "I2"
    grid[40][24] = "I2"
    grid[40][25] = "I3"
    grid[40][26] = "#"
    grid[40][27] = "#"

    # 3. Fixed Top Horizontal Gallows Arm & Scrollwork Braces (y=6..12)
    # y=6: top finial cap outline
    grid[6][23] = "#"
    grid[6][24] = "#"
    grid[6][25] = "#"
    
    # y=7: ornate top finial on central post
    grid[7][23] = "#"
    grid[7][24] = "I1"
    grid[7][25] = "#"
    
    # y=8: top outline enclosing the horizontal arm from x=16 to 32
    for x in range(16, 33):
        grid[8][x] = "#"
    grid[8][24] = "I1"

    # y=9: main horizontal crossbeam (x=16..32)
    grid[9][15] = "#"
    grid[9][16] = "I1"
    for x in range(17, 31):
        grid[9][x] = "I1" if x % 3 == 0 else "I2"
    grid[9][31] = "I3"
    grid[9][32] = "#"

    # y=10: bottom outline of crossbeam
    grid[10][15] = "#"
    for x in range(16, 33):
        grid[10][x] = "#"
    
    # Ornamental curved braces under the arm (x=18..20, 28..30)
    grid[11][18] = "#"
    grid[11][19] = "I1"
    grid[11][20] = "#"
    grid[11][28] = "#"
    grid[11][29] = "I2"
    grid[11][30] = "#"

    grid[12][19] = "#"
    grid[12][20] = "#"
    grid[12][21] = "#"
    grid[12][27] = "#"
    grid[12][28] = "#"
    grid[12][29] = "#"

    # PIVOT HOOK at (X=24, Y=11): 100% FIXED PIVOT POINT!
    grid[11][23] = "#"
    grid[11][24] = "I1" # Chain eyelet hook
    grid[11][25] = "#"

    return grid

def apply_dynamic_column(grid, frame_idx):
    for y in range(12, 40):
        grid[y][22] = "#"
        grid[y][26] = "#"
        
        if frame_idx == 0:
            # Frame 1: Lamp on Left (x=18, y=24)
            dist_y = abs(y - 24)
            if dist_y <= 5:
                grid[y][23] = "O1"
                grid[y][24] = "O2"
                grid[y][25] = "I3"
            elif dist_y <= 10:
                grid[y][23] = "O2"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
                
        elif frame_idx == 2:
            # Frame 3: Lamp on Right (x=30, y=24)
            dist_y = abs(y - 24)
            if dist_y <= 5:
                grid[y][23] = "I3"
                grid[y][24] = "O2"
                grid[y][25] = "O1"
            elif dist_y <= 10:
                grid[y][23] = "I3"
                grid[y][24] = "I2"
                grid[y][25] = "O2"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
                
        else:
            # Frame 2 & 4: Lamp at Center (x=24, y=25)
            dist_y = abs(y - 25)
            if dist_y <= 4:
                grid[y][23] = "O1"
                grid[y][24] = "O1"
                grid[y][25] = "O1"
            elif dist_y <= 9:
                grid[y][23] = "O2"
                grid[y][24] = "O1"
                grid[y][25] = "O2"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"

def apply_floor_and_opposing_shadow(grid, frame_idx):
    if frame_idx == 0:
        # Frame 1: Cast shadow to the RIGHT
        for x in range(24, 40):
            grid[44][x] = "S"
            grid[45][x] = "S"
        for x in range(26, 38):
            grid[46][x] = "S"
    elif frame_idx == 2:
        # Frame 3: Cast shadow to the LEFT
        for x in range(8, 25):
            grid[44][x] = "S"
            grid[45][x] = "S"
        for x in range(10, 23):
            grid[46][x] = "S"
    else:
        # Frame 2 & 4: Compact centered shadow at base
        for x in range(20, 29):
            grid[44][x] = "S"
            grid[45][x] = "S"
        for x in range(21, 28):
            grid[46][x] = "S"

def draw_swinging_lantern_frame_1(grid):
    # Frame 1: Swung Left (-28 deg)
    chain_links = [
        (23, 12), (23, 13),
        (22, 14), (21, 15),
        (20, 16), (19, 17),
        (18, 18)
    ]
    for cx, cy in chain_links:
        grid[cy][cx] = "I1" if cx % 2 == 0 else "I2"
        if grid[cy][cx - 1] == ".": grid[cy][cx - 1] = "#"
        if grid[cy][cx + 1] == ".": grid[cy][cx + 1] = "#"

    # Lantern Cap
    cap_rows = [
        (17, 19, ["#", "I1", "I2", "#"]),
        (16, 20, ["#", "I1", "I1", "I2", "I3", "#"]),
        (15, 21, ["#", "#", "I1", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in cap_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    # Glass Chamber & Golden Flame
    glass_rows = [
        (15, 22, ["#", "G1", "L2", "L1", "G1", "#"]),
        (14, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (14, 24, ["#", "G1", "L3", "L2", "L1", "G1", "#"]),
        (15, 25, ["#", "L3", "L3", "L2", "L3", "#"]),
    ]
    for start_x, y, row in glass_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    # Lantern Metal Base
    base_rows = [
        (15, 26, ["#", "I1", "I2", "I2", "I3", "#"]),
        (16, 27, ["#", "#", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in base_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Floating embers (Rule 4.6)
    grid[17][13] = "L2"
    grid[15][11] = "L1"

def draw_swinging_lantern_frame_2(grid):
    # Frame 2: Center (0 deg, swinging right)
    for cy in range(12, 19):
        grid[cy][24] = "I1" if cy % 2 == 0 else "I2"
        grid[cy][23] = "#"
        grid[cy][25] = "#"

    cap_rows = [
        (23, 19, ["#", "I1", "I2", "#"]),
        (22, 20, ["#", "I1", "I1", "I2", "I3", "#"]),
        (21, 21, ["#", "#", "I1", "I2", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in cap_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    glass_rows = [
        (21, 22, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (20, 23, ["#", "G1", "L2", "L1", "L1", "L2", "G1", "#"]),
        (20, 24, ["#", "G1", "L3", "L2", "L1", "L2", "G1", "#"]),
        (21, 25, ["#", "L3", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    base_rows = [
        (21, 26, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
        (22, 27, ["#", "#", "I2", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in base_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    grid[18][22] = "L2"
    grid[16][20] = "L1"

def draw_swinging_lantern_frame_3(grid):
    # Frame 3: Swung Right (+28 deg)
    chain_links = [
        (25, 12), (25, 13),
        (26, 14), (27, 15),
        (28, 16), (29, 17),
        (30, 18)
    ]
    for cx, cy in chain_links:
        grid[cy][cx] = "I1" if cx % 2 == 0 else "I2"
        if grid[cy][cx - 1] == ".": grid[cy][cx - 1] = "#"
        if grid[cy][cx + 1] == ".": grid[cy][cx + 1] = "#"

    cap_rows = [
        (29, 19, ["#", "I1", "I2", "#"]),
        (28, 20, ["#", "I1", "I1", "I2", "I3", "#"]),
        (27, 21, ["#", "I1", "I2", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in cap_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    glass_rows = [
        (27, 22, ["#", "G1", "L1", "L2", "G1", "#"]),
        (26, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (26, 24, ["#", "G1", "L1", "L2", "L3", "G1", "#"]),
        (27, 25, ["#", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    base_rows = [
        (27, 26, ["#", "I1", "I2", "I2", "I3", "#"]),
        (28, 27, ["#", "#", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in base_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    grid[17][35] = "L2"
    grid[15][37] = "L1"

def draw_swinging_lantern_frame_4(grid):
    # Frame 4: Center (0 deg, swinging left)
    for cy in range(12, 19):
        grid[cy][24] = "I1" if cy % 2 == 0 else "I2"
        grid[cy][23] = "#"
        grid[cy][25] = "#"

    cap_rows = [
        (23, 19, ["#", "I1", "I2", "#"]),
        (22, 20, ["#", "I1", "I1", "I2", "I3", "#"]),
        (21, 21, ["#", "#", "I1", "I2", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in cap_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    glass_rows = [
        (21, 22, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (20, 23, ["#", "G1", "L2", "L2", "L1", "L1", "G1", "#"]),
        (20, 24, ["#", "G1", "L3", "L2", "L2", "L1", "G1", "#"]),
        (21, 25, ["#", "L3", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    base_rows = [
        (21, 26, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
        (22, 27, ["#", "#", "I2", "I2", "I3", "#", "#"]),
    ]
    for start_x, y, row in base_rows:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    grid[18][26] = "L2"
    grid[16][28] = "L1"

def build_perfect_lantern_frame(frame_idx):
    grid = create_environment_base()
    apply_floor_and_opposing_shadow(grid, frame_idx)
    apply_dynamic_column(grid, frame_idx)
    
    if frame_idx == 0:
        draw_swinging_lantern_frame_1(grid)
    elif frame_idx == 1:
        draw_swinging_lantern_frame_2(grid)
    elif frame_idx == 2:
        draw_swinging_lantern_frame_3(grid)
    else:
        draw_swinging_lantern_frame_4(grid)
        
    return grid

perfect_lantern_frames = [build_perfect_lantern_frame(i) for i in range(4)]

# Check outline completeness (excluding embers L1/L2)
def check_outline_completeness(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "L1", "L2"):
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n--- OUTLINE COMPLETENESS CHECK ---")
for i, fr in enumerate(perfect_lantern_frames):
    n = check_outline_completeness(fr)
    print(f"Perfect Lantern Frame {i+1} naked pixels (excluding embers): {len(n)}")

# Verify Pivot Hook
print("\n--- PIVOT POINT VERIFICATION ---")
for i, fr in enumerate(perfect_lantern_frames):
    print(f"Frame {i+1} Pivot at (24, 11): code = {fr[11][24]}")

# Verify Floor Shadow
print("\n--- OPPOSING CAST SHADOW VERIFICATION ---")
for i, fr in enumerate(perfect_lantern_frames):
    shadow_xs = [x for x in range(W) for y in (44, 45, 46) if fr[y][x] == "S"]
    mean_sx = sum(shadow_xs) / len(shadow_xs) if shadow_xs else 0
    print(f"Frame {i+1}: Shadow Mean X = {mean_sx:.1f} (Min X={min(shadow_xs)}, Max X={max(shadow_xs)})")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(perfect_lantern_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_lantern_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/perfect_lantern_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_lantern_sheet.png")

print("\nSaved perfect_lantern_sheet.png and perfect_lantern_anim.gif")
