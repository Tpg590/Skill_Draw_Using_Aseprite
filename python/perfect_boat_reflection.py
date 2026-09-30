import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette (Deep Teal -> Cyan-Green -> Purple-Navy)
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (14, 24, 36, 130),     # Soft aquatic shadow (Alpha 130)
    "#": (10, 18, 28, 255),     # Clean dark navy-teal outline (#0a121c)
    
    # Real Wooden Rowboat (Rich warm oak with golden highlights)
    "A": (232, 164, 76, 255),   # Golden oak highlight (#e8a44c)
    "B": (164, 94, 38, 255),    # Warm oak midtone (#a45e26)
    "C": (84, 40, 14, 255),     # Deep oak shadow / interior floor (#54280e)
    
    # Storm Lantern (Golden radiant flame & OSL)
    "L1": (255, 248, 176, 255), # White-gold flame core (#fff8b0)
    "L2": (246, 166, 35, 255),  # Radiant golden-amber glow (#f6a623)
    "L3": (184, 84, 18, 255),   # Deep orange metal cage (#b85412)
    
    # Reflected Boat in Water (Teal-tinted & desaturated)
    "R1": (74, 120, 120, 255),  # Reflected wood highlight (Teal-oak #4a7878)
    "R2": (40, 76, 80, 255),    # Reflected wood body (Dark teal #284c50)
    "R3": (20, 46, 52, 255),    # Deep aquatic under-crevice (#142e34)
    "RL": (114, 191, 160, 255), # Reflected golden-teal lantern shimmer (#72bfa0)
    
    # Water Surface Ripples (Gợn sóng hồ)
    "W1": (52, 96, 114, 255),   # Water ripple crest highlight (#346072)
    "W2": (24, 52, 64, 255),    # Deep lake water tone (#183440)
}

COLOR_MAP_REFL = {
    "#": "R3",
    "A": "R1",
    "B": "R2",
    "C": "R3",
    "L1": "RL",
    "L2": "RL",
    "L3": "R2",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_real_boat(grid, dy_bob=0):
    yw = 24 + dy_bob
    
    # 1. Stern (left transom: X=9..12)
    grid[yw - 4][9] = "#"; grid[yw - 4][10] = "#"
    grid[yw - 3][8] = "#"; grid[yw - 3][9] = "A"; grid[yw - 3][10] = "B"; grid[yw - 3][11] = "#"
    grid[yw - 2][9] = "#"; grid[yw - 2][10] = "B"; grid[yw - 2][11] = "C"; grid[yw - 2][12] = "#"
    grid[yw - 1][10] = "#"; grid[yw - 1][11] = "C"; grid[yw - 1][12] = "#"
    grid[yw][11] = "#"; grid[yw][12] = "#"
    
    # 2. Far Gunwale (mạn thuyền phía xa, nhìn vào lòng thuyền):
    for x in range(11, 33):
        grid[yw - 5][x] = "#"
        grid[yw - 4][x] = "C" # far inner wall in shadow
        
    # Interior cockpit floorboards & ribs (lòng thuyền):
    for x in range(12, 33):
        grid[yw - 3][x] = "C" if x % 3 == 0 else "B"
        
    # Stern seat bench: X=11..14
    for x in range(11, 15):
        grid[yw - 4][x] = "A"
        grid[yw - 3][x] = "B"
        
    # Middle rowing seat bench: X=21..25
    for x in range(21, 26):
        grid[yw - 4][x] = "A"
        grid[yw - 3][x] = "B"
        grid[yw - 2][x] = "C" # shadow under seat

    # 3. Near Gunwale & Hull Planks (mạn thuyền gần, hứng sáng):
    # Top railing of near gunwale
    for x in range(10, 35):
        grid[yw - 3][x] = "A"
        grid[yw - 4][x] = "#"
        
    # Middle clinker plank
    for x in range(12, 34):
        grid[yw - 2][x] = "B" if x % 3 != 0 else "A"
        
    # Bottom clinker plank & Keel
    for x in range(13, 33):
        grid[yw - 1][x] = "C" if x % 4 != 0 else "B"
        grid[yw][x] = "#" # Keel meeting water
        
    # 4. Prow / Bow (mũi thuyền vươn cao sang phải): X=33..38
    grid[yw - 4][34] = "A"; grid[yw - 4][35] = "#"
    grid[yw - 3][34] = "A"; grid[yw - 3][35] = "B"; grid[yw - 3][36] = "#"
    grid[yw - 2][33] = "B"; grid[yw - 2][34] = "B"; grid[yw - 2][35] = "C"; grid[yw - 2][36] = "#"
    grid[yw - 1][33] = "C"; grid[yw - 1][34] = "#"
    
    # Stem post curving up
    grid[yw - 5][35] = "A"; grid[yw - 5][36] = "#"
    grid[yw - 6][36] = "A"; grid[yw - 6][37] = "#"
    grid[yw - 7][37] = "A"; grid[yw - 7][38] = "#"
    grid[yw - 8][37] = "#"; grid[yw - 8][38] = "#"
    
    # Lantern Hanging Davit / Arm (cần treo đèn sắt):
    grid[yw - 8][39] = "#"; grid[yw - 8][40] = "#"
    grid[yw - 7][40] = "#"
    
    # 5. Storm Lantern (Đèn bão phát sáng vàng rực):
    # Center of lantern: X=40, Y=yw-5
    lx, ly = 40, yw - 5
    
    # Top dome cap & ring
    grid[ly - 2][lx] = "#"
    grid[ly - 1][lx - 1] = "#"; grid[ly - 1][lx] = "L3"; grid[ly - 1][lx + 1] = "#"
    
    # Glowing glass chamber & white-gold core
    grid[ly][lx - 1] = "L3"; grid[ly][lx] = "L1"; grid[ly][lx + 1] = "L3"
    grid[ly + 1][lx - 1] = "L3"; grid[ly + 1][lx] = "L2"; grid[ly + 1][lx + 1] = "L3"
    
    # Lantern base
    grid[ly + 2][lx - 1] = "#"; grid[ly + 2][lx] = "L3"; grid[ly + 2][lx + 1] = "#"
    
    # OSL Golden Glow onto Prow Wood
    grid[yw - 6][36] = "L2"
    grid[yw - 7][36] = "L1"

def outline_boat_only(grid, dy_bob=0):
    yw = 24 + dy_bob
    for y in range(0, yw + 1):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def draw_inverted_reflection(grid, dy_bob=0, f_phase=0):
    # 1. Collect all pixels of the real boat (y <= yw)
    yw = 24 + dy_bob
    boat_pixels = {}
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S"):
                boat_pixels[(x, y)] = c
                
    # 2. Invert along waterline with 65% vertical compression:
    # dy = yw - y (distance above waterline)
    # y_refl = yw + round(dy * 0.65)
    # x_refl = x + wave_shift
    
    # Group reflected pixels by row to apply wave ripples and water breaks
    refl_rows = {}
    for (bx, by), code in boat_pixels.items():
        dy = yw - by
        if dy <= 0: continue # ignore pixels at waterline itself
        
        # 65% compression ratio (strictly within 60% - 70%)
        refl_dy = int(round(dy * 0.65))
        refl_y = yw + refl_dy
        if refl_y >= H: continue
        
        # Calculate horizontal zigzag wave shift (+/- 1px)
        wave_shift = int(round(math.sin(refl_dy * 1.25 + f_phase * 1.57)))
        refl_x = bx + wave_shift
        
        if 0 <= refl_x < W:
            color = COLOR_MAP_REFL.get(code, "R2")
            if refl_y not in refl_rows:
                refl_rows[refl_y] = []
            refl_rows[refl_y].append((refl_x, color))
            
    # Draw reflected pixels into grid
    for ry, items in refl_rows.items():
        depth = ry - yw
        # On some rows, thin water ripple gaps create fluid transparency
        skip_gap = (depth in (3, 5) and (depth + f_phase) % 2 == 0)
        
        for rx, col in items:
            if skip_gap and col not in ("RL", "L2"):
                # Break through with water tone
                grid[ry][rx] = "W2" if rx % 2 == 0 else "W1"
            else:
                grid[ry][rx] = col
                
    # Extra trailing golden-teal reflection from the lantern (depth 7..9)
    # Shimmers directly underneath lantern at X ~ 40 + wave_shift
    for d in (7, 8):
        ry = yw + d
        if ry < H:
            w_shift = int(round(math.sin(d * 1.25 + f_phase * 1.57)))
            lx_refl = 40 + w_shift
            if 0 <= lx_refl < W:
                grid[ry][lx_refl] = "RL"
            if 0 <= lx_refl + 1 < W:
                grid[ry][lx_refl + 1] = "W1"

def draw_water_surface(grid, dy_bob=0, f_phase=0):
    yw = 24 + dy_bob
    
    # Primary water contact line at keel
    for x in range(12, 34):
        if grid[yw + 1][x] == ".":
            grid[yw + 1][x] = "R3"
            
    # Left stern wake
    grid[yw][7] = "W1"; grid[yw][8] = "W2"
    grid[yw + 1][8] = "W1"; grid[yw + 1][9] = "W2"
    
    # Right bow wake
    grid[yw][38] = "W2"; grid[yw][39] = "W1"
    grid[yw + 1][37] = "W2"; grid[yw + 1][38] = "W1"

    # Concentric oval ripples spreading out from boat (within bounds, NO canvas-wide lines!)
    r1_y = yw + 5
    if r1_y < H:
        for x in (7, 8, 36, 37):
            if grid[r1_y][x] == ".": grid[r1_y][x] = "W1"
            
    r2_y = yw + 7
    if r2_y < H:
        for x in (9, 10, 34, 35):
            if grid[r2_y][x] == ".": grid[r2_y][x] = "W2"
            
    # Soft aquatic ground/water shadow S under the entire boat reflection
    sy_start = yw + 8
    for y in range(sy_start, min(H, sy_start + 4)):
        span = 14 - (y - sy_start) * 2
        for x in range(24 - span, 24 + span):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def build_frame(f_idx):
    grid = empty_grid()
    
    # Harmonic bobbing offset:
    # Frame 1: Neutral (0)
    # Frame 2: Dip down (+1)
    # Frame 3: Neutral (0)
    # Frame 4: Rise up (-1)
    dy_bob_table = [0, 1, 0, -1]
    dy_bob = dy_bob_table[f_idx]
    
    # 1. Draw Real Boat
    draw_real_boat(grid, dy_bob=dy_bob)
    
    # 2. Enclose real boat with clean outline
    outline_boat_only(grid, dy_bob=dy_bob)
    
    # 3. Draw Inverted Water Reflection (Computed from real boat, 65% compressed, inverted Y, aquatic teal colors, zigzag wave distortion)
    draw_inverted_reflection(grid, dy_bob=dy_bob, f_phase=f_idx)
    
    # 4. Draw Water Surface Ripples and Ambient Lake Shadow S
    draw_water_surface(grid, dy_bob=dy_bob, f_phase=f_idx)
    
    return grid

frames = [build_frame(i) for i in range(4)]

# Check outline of real boat
def check_real_boat(grid, dy_bob):
    yw = 24 + dy_bob
    naked = []
    for y in range(0, yw + 1):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "W1", "W2"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n=== REAL BOAT OUTLINE CHECK ===")
for i, fr in enumerate(frames):
    n = check_real_boat(fr, [0, 1, 0, -1][i])
    print(f"Frame {i+1} naked pixels on real boat: {len(n)}")

# Height and reflection verification
print("\n=== HEIGHT AND REFLECTION VERIFICATION ===")
for i, fr in enumerate(frames):
    yw = 24 + [0, 1, 0, -1][i]
    boat_ys = [y for x in range(W) for y in range(0, yw + 1) if fr[y][x] not in (".", "S")]
    refl_ys = [y for x in range(W) for y in range(yw + 1, H) if fr[y][x] in ("R1", "R2", "R3", "RL")]
    boat_h = yw - min(boat_ys) if boat_ys else 0
    refl_h = max(refl_ys) - yw if refl_ys else 0
    ratio = (refl_h / boat_h) * 100 if boat_h else 0
    print(f"Frame {i+1}: Real Boat Height = {boat_h}px (min Y = {min(boat_ys)}), Reflected Height = {refl_h}px (max Y = {max(refl_ys)}), Ratio = {ratio:.1f}%")

# Render preview images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_boat_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_boat_sheet.png")

gif_frames[0].save(
    "python/perfect_boat_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered perfect_boat_sheet.png and perfect_boat_anim.gif successfully!")
