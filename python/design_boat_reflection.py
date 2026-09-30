import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (14, 24, 36, 130),     # Soft aquatic shadow (Alpha 130)
    "#": (10, 18, 28, 255),     # Clean dark navy-teal outline (#0a121c)
    
    # Real Wooden Rowboat (Rich warm oak with golden highlights)
    "A": (232, 164, 76, 255),   # Golden oak highlight (#e8a44c)
    "B": (164, 94, 38, 255),    # Warm oak midtone (#a45e26)
    "C": (84, 40, 14, 255),     # Deep oak shadow / interior floor (#54280e)
    "D": (48, 22, 10, 255),     # Deepest interior crevice (#30160a)
    
    # Storm Lantern (Golden radiant flame & OSL)
    "L1": (255, 248, 176, 255), # White-gold flame core (#fff8b0)
    "L2": (246, 166, 35, 255),  # Radiant golden-amber glow (#f6a623)
    "L3": (184, 84, 18, 255),   # Deep orange metal cage (#b85412)
    
    # Reflected Boat in Water (Teal-tinted & desaturated)
    "R1": (82, 134, 134, 255),  # Reflected wood highlight (Teal-oak #528686)
    "R2": (42, 82, 88, 255),    # Reflected wood body (Dark teal #2a5258)
    "R3": (20, 46, 52, 255),    # Deep aquatic under-crevice (#142e34)
    "RL1": (170, 230, 195, 255),# Reflected lantern core shimmer (#aae6c3)
    "RL2": (105, 185, 155, 255),# Reflected golden-teal lantern glow (#69b99b)
    
    # Water Surface Ripples (Gợn sóng hồ)
    "W1": (56, 107, 128, 255),  # Water ripple crest highlight (#386b80)
    "W2": (26, 56, 72, 255),    # Deep lake water tone (#1a3848)
}

COLOR_MAP_REFL = {
    "#": "R3",
    "A": "R1",
    "B": "R2",
    "C": "R3",
    "D": "R3",
    "L1": "RL1",
    "L2": "RL2",
    "L3": "R2",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_boat(grid, yw):
    # yw is waterline where keel sits
    # Height of boat will be from yw - 10 down to yw (11 pixels tall)
    
    # 1. Stern (left transom & curved sheer line)
    # y = yw - 5: stern upper tip
    grid[yw - 5][8] = "#"; grid[yw - 5][9] = "#"
    # y = yw - 4: stern bench & transom
    grid[yw - 4][7] = "#"; grid[yw - 4][8] = "A"; grid[yw - 4][9] = "B"; grid[yw - 4][10] = "#"
    # y = yw - 3: stern lower
    grid[yw - 3][8] = "#"; grid[yw - 3][9] = "B"; grid[yw - 3][10] = "C"; grid[yw - 3][11] = "#"
    # y = yw - 2: stern bottom curve
    grid[yw - 2][9] = "#"; grid[yw - 2][10] = "C"; grid[yw - 2][11] = "#"
    # y = yw - 1: keel junction
    grid[yw - 1][10] = "#"; grid[yw - 1][11] = "#"
    
    # 2. Far Gunwale (mạn thuyền xa):
    for x in range(10, 34):
        grid[yw - 6][x] = "#"
        grid[yw - 5][x] = "C" # inner shadow wall
        
    # Interior floorboards & shadow
    for x in range(11, 33):
        grid[yw - 4][x] = "D" if x % 3 == 0 else "C"
        
    # Stern bench (ghế lái phía sau): X=9..13
    for x in range(9, 14):
        grid[yw - 5][x] = "A"
        grid[yw - 4][x] = "B"
        
    # Middle rowing seat bench (ghế chèo giữa): X=20..25
    for x in range(20, 26):
        grid[yw - 5][x] = "A"
        grid[yw - 4][x] = "B"
        grid[yw - 3][x] = "C" # shadow under bench
        
    # 3. Near Gunwale & Hull Planking (mạn thuyền gần):
    # Top railing of near gunwale (bright highlight)
    for x in range(8, 35):
        grid[yw - 4][x] = "#"
        grid[yw - 3][x] = "A"
        
    # Upper clinker plank (warm midtone)
    for x in range(10, 35):
        grid[yw - 2][x] = "B" if x % 3 != 0 else "A"
        
    # Lower clinker plank (rich wood shadow)
    for x in range(11, 34):
        grid[yw - 1][x] = "C" if x % 4 != 0 else "B"
        
    # Keel on water line
    for x in range(12, 33):
        grid[yw][x] = "#"
        
    # 4. Bow / Prow (mũi thuyền vươn cao sang phải):
    grid[yw - 4][35] = "A"; grid[yw - 4][36] = "#"
    grid[yw - 3][35] = "A"; grid[yw - 3][36] = "B"; grid[yw - 3][37] = "#"
    grid[yw - 2][35] = "B"; grid[yw - 2][36] = "C"; grid[yw - 2][37] = "#"
    grid[yw - 1][34] = "C"; grid[yw - 1][35] = "#"
    
    # Stem post sweeping upward:
    grid[yw - 5][36] = "A"; grid[yw - 5][37] = "#"
    grid[yw - 6][37] = "A"; grid[yw - 6][38] = "#"
    grid[yw - 7][38] = "A"; grid[yw - 7][39] = "#"
    grid[yw - 8][38] = "#"; grid[yw - 8][39] = "#"
    
    # Hanging iron davit arm extending right to hold lantern:
    grid[yw - 9][39] = "#"; grid[yw - 9][40] = "#"; grid[yw - 9][41] = "#"
    grid[yw - 8][41] = "#" # hook
    
    # 5. Storm Lantern hanging at X=41:
    lx, ly = 41, yw - 6
    # Cap / Roof
    grid[ly - 1][lx - 1] = "#"; grid[ly - 1][lx] = "L3"; grid[ly - 1][lx + 1] = "#"
    # Glass chamber with flame
    grid[ly][lx - 1] = "L3"; grid[ly][lx] = "L1"; grid[ly][lx + 1] = "L3"
    grid[ly + 1][lx - 1] = "L3"; grid[ly + 1][lx] = "L2"; grid[ly + 1][lx + 1] = "L3"
    # Lantern base
    grid[ly + 2][lx - 1] = "#"; grid[ly + 2][lx] = "L3"; grid[ly + 2][lx + 1] = "#"
    
    # OSL Glow from lantern onto prow stem post:
    grid[yw - 7][38] = "L2"
    grid[yw - 6][37] = "L2"
    grid[yw - 5][36] = "L3"

def outline_boat(grid, yw):
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def check_naked_boat(grid, yw):
    naked = []
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        naked.append((x, y, c, nx, ny))
    return naked

def draw_inverted_reflection(grid, yw, f_phase):
    # Real boat is at Y in [yw - 10, yw], height = 11 px.
    # Reflected height must be strictly 60% - 70% of real boat height:
    # 11 * 0.65 = 7.15 -> exactly 7 rows: depth d in 1..7 (Y = yw + 1 to yw + 7).
    # Ratio = 7 / 11 = 63.64% (Strictly within [60%, 70%]).
    
    # Calculate zigzag wave shift for each depth row
    # Sine wave traveling downward: delta_x = round(sin(d * 1.57 - f_phase * 1.57))
    shifts = [int(round(math.sin(d * 1.57 - f_phase * 1.57))) for d in range(1, 8)]
    
    # Define the inverted boat rows (inverted Y: keel at top, gunwales in middle, lantern pointing down):
    
    # d = 1 (Y = yw + 1): Inverted keel & water contact
    # Shifted by shifts[0]
    s1 = shifts[0]
    for x in range(11 + s1, 34 + s1):
        if 0 <= x < W: grid[yw + 1][x] = "R3"
    # Water ripples flanking keel
    if 0 <= 9 + s1 < W: grid[yw + 1][9 + s1] = "W1"
    if 0 <= 10 + s1 < W: grid[yw + 1][10 + s1] = "W2"
    if 0 <= 34 + s1 < W: grid[yw + 1][34 + s1] = "W2"
    if 0 <= 35 + s1 < W: grid[yw + 1][35 + s1] = "W1"
    
    # d = 2 (Y = yw + 2): Inverted lower hull plank
    s2 = shifts[1]
    for x in range(10 + s2, 35 + s2):
        if 0 <= x < W:
            grid[yw + 2][x] = "R2" if x % 3 != 0 else "R3"
    if 0 <= 8 + s2 < W: grid[yw + 2][8 + s2] = "W1"
    if 0 <= 36 + s2 < W: grid[yw + 2][36 + s2] = "W1"
    
    # d = 3 (Y = yw + 3): Inverted mid hull & near gunwale
    s3 = shifts[2]
    for x in range(9 + s3, 36 + s3):
        if 0 <= x < W:
            grid[yw + 3][x] = "R1" if (x + s3) % 4 in (1, 2) else "R2"
    # Stem post curve beginning on right
    if 0 <= 36 + s3 < W: grid[yw + 3][36 + s3] = "R1"
    if 0 <= 37 + s3 < W: grid[yw + 3][37 + s3] = "R3"
    
    # d = 4 (Y = yw + 4): Inverted upper sheer line & far gunwale
    s4 = shifts[3]
    for x in range(9 + s4, 34 + s4):
        if 0 <= x < W:
            grid[yw + 4][x] = "R2" if x % 2 == 0 else "R3"
    # Prow curving down-right:
    for x in range(35 + s4, 38 + s4):
        if 0 <= x < W: grid[yw + 4][x] = "R1"
    if 0 <= 38 + s4 < W: grid[yw + 4][38 + s4] = "R3"
    
    # d = 5 (Y = yw + 5): Inverted stern tip and upper prow stem post + lantern top
    s5 = shifts[4]
    # Stern tip fading on left
    for x in range(10 + s5, 15 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Mid hull thinning/water breaking
    for x in range(21 + s5, 27 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Inverted prow stem post:
    for x in range(36 + s5, 39 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R2"
    # Inverted lantern top:
    for x in range(40 + s5, 43 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "RL2"
        
    # d = 6 (Y = yw + 6): Inverted Lantern Golden Shimmer (Core flame upside down)
    s6 = shifts[5]
    # A few fading wood ripple pixels under center
    if 0 <= 22 + s6 < W: grid[yw + 6][22 + s6] = "W2"
    if 0 <= 23 + s6 < W: grid[yw + 6][23 + s6] = "R3"
    # Inverted prow tip:
    if 0 <= 38 + s6 < W: grid[yw + 6][38 + s6] = "R3"
    # Bright golden-teal lantern flame reflection:
    if 0 <= 39 + s6 < W: grid[yw + 6][39 + s6] = "RL2"
    if 0 <= 40 + s6 < W: grid[yw + 6][40 + s6] = "RL1"
    if 0 <= 41 + s6 < W: grid[yw + 6][41 + s6] = "RL1"
    if 0 <= 42 + s6 < W: grid[yw + 6][42 + s6] = "RL2"
    
    # d = 7 (Y = yw + 7): Inverted Lantern Hook & Tip Shimmer (bottom-most point of inverted reflection)
    s7 = shifts[6]
    # Lantern tip glow in water:
    if 0 <= 40 + s7 < W: grid[yw + 7][40 + s7] = "RL2"
    if 0 <= 41 + s7 < W: grid[yw + 7][41 + s7] = "RL2"
    if 0 <= 42 + s7 < W: grid[yw + 7][42 + s7] = "W1"

def draw_water_effects(grid, yw, f_phase):
    # Surrounding lake ripples (W1, W2) in soft oval bounds
    # Ripple ring 1
    y1 = yw + 4
    if y1 < H:
        for x in (5, 6, 7):
            if grid[y1][x] == ".": grid[y1][x] = "W1" if x == 6 else "W2"
        for x in (41, 42, 43):
            if grid[y1][x] == ".": grid[y1][x] = "W2" if x == 43 else "W1"
            
    # Ripple ring 2
    y2 = yw + 6
    if y2 < H:
        for x in (8, 9):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
        for x in (44, 45):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
            
    # Soft aquatic shadow S underneath the reflection:
    sy_start = yw + 8
    for y in range(sy_start, min(H, sy_start + 4)):
        span = 14 - (y - sy_start) * 2
        for x in range(24 - span, 24 + span):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def build_full_frame(f_idx):
    grid = empty_grid()
    # Harmonic bobbing offset:
    # F1: 0 (yw = 23)
    # F2: +1 (yw = 24)
    # F3: 0 (yw = 23)
    # F4: -1 (yw = 22)
    bob_offsets = [0, 1, 0, -1]
    yw = 23 + bob_offsets[f_idx]
    
    # 1. Boat
    draw_boat(grid, yw)
    outline_boat(grid, yw)
    
    # 2. Reflection
    draw_inverted_reflection(grid, yw, f_idx)
    
    # 3. Water effects
    draw_water_effects(grid, yw, f_idx)
    
    return grid, yw

print("Ready to run frame generation.")
frames_data = []
for i in range(4):
    g, yw = build_full_frame(i)
    frames_data.append((g, yw))

print("\n=== VERIFICATION CHECKS ===")
for i, (g, yw) in enumerate(frames_data):
    naked = check_naked_boat(g, yw)
    boat_ys = [y for x in range(W) for y in range(0, yw + 1) if g[y][x] not in (".", "S")]
    refl_ys = [y for x in range(W) for y in range(yw + 1, H) if g[y][x] in ("R1", "R2", "R3", "RL1", "RL2")]
    
    boat_h = yw - min(boat_ys) + 1 if boat_ys else 0
    refl_h = max(refl_ys) - yw if refl_ys else 0
    ratio = (refl_h / boat_h) * 100 if boat_h else 0
    
    print(f"Frame {i+1}:")
    print(f"  Naked pixels on real boat: {len(naked)}")
    print(f"  Real Boat Y range: [{min(boat_ys)}, {yw}], Height = {boat_h}px")
    print(f"  Reflected Y range: [{yw + 1}, {max(refl_ys)}], Height = {refl_h}px")
    print(f"  Compression Ratio: {ratio:.2f}% (Target: 60% - 70%)")

# Render images
gif_frames = []
for idx, (g, yw) in enumerate(frames_data):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/design_boat_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/design_boat_sheet.png")

gif_frames[0].save(
    "python/design_boat_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("\nGenerated design_boat_sheet.png and design_boat_anim.gif successfully!")
