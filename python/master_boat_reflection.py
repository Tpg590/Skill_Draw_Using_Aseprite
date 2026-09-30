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

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_real_boat(grid, dy_bob=0):
    # Base waterline for the boat
    yw = 24 + dy_bob
    
    # 1. Stern (left: X=9..12)
    # Transom edge
    grid[yw - 4][9] = "#"; grid[yw - 4][10] = "#"
    grid[yw - 3][8] = "#"; grid[yw - 3][9] = "A"; grid[yw - 3][10] = "B"; grid[yw - 3][11] = "#"
    grid[yw - 2][9] = "#"; grid[yw - 2][10] = "B"; grid[yw - 2][11] = "C"; grid[yw - 2][12] = "#"
    grid[yw - 1][10] = "#"; grid[yw - 1][11] = "C"; grid[yw - 1][12] = "#"
    grid[yw][11] = "#"; grid[yw][12] = "#"
    
    # 2. Far Gunwale (mạn thuyền phía xa, nhìn vào lòng thuyền):
    for x in range(11, 33):
        grid[yw - 5][x] = "#"
        grid[yw - 4][x] = "C" # far inner wall in shadow
        
    # Interior cockpit floor & ribs (lòng thuyền):
    for x in range(12, 33):
        grid[yw - 3][x] = "C" if x % 4 == 0 else "#"
        
    # Wooden rowing bench (ghế ngồi ngang): X=21..25
    for x in range(21, 26):
        grid[yw - 4][x] = "A"
        grid[yw - 3][x] = "B"
        grid[yw - 2][x] = "C" # shadow under bench
        
    # Stern bench: X=11..14
    for x in range(11, 15):
        grid[yw - 4][x] = "A"

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

def draw_water_reflection(grid, dy_bob=0, f_phase=0):
    # Calculates the INVERTED Y reflection on the water surface:
    # 1. Inverted Y: Keel at waterline, gunwales below, lantern at the very bottom!
    # 2. 60-70% vertical height compression
    # 3. Aquatic teal & desaturated color palette
    # 4. Zigzag wave ripple distortion (+/- 1px horizontal displacement per row)
    
    yw = 24 + dy_bob
    
    # Reflection spans from row yw + 1 down to yw + 8 (height = 8px, ~65% of boat height 12px)
    # Zigzag wave distortion offsets for each depth k = 1..8
    # Shift alternates dynamically across frames
    
    # Row 1: yw + 1 (Reflection of Keel & lower hull, depth 1)
    k1_shift = int(round(math.sin(1.0 + f_phase * 1.57)))
    for x in range(13, 34):
        rx = x + k1_shift
        if 0 <= rx < W: grid[yw + 1][rx] = "R3"
        
    # Row 2: yw + 2 (Reflection of lower clinker plank, depth 2)
    k2_shift = int(round(math.sin(2.3 + f_phase * 1.57)))
    for x in range(12, 35):
        rx = x + k2_shift
        if 0 <= rx < W: grid[yw + 2][rx] = "R2"
    # Stem post reflection
    if 0 <= 35 + k2_shift < W: grid[yw + 2][35 + k2_shift] = "R1"
    if 0 <= 36 + k2_shift < W: grid[yw + 2][36 + k2_shift] = "R1"
        
    # Row 3: yw + 3 (Thin water ripple break cutting through reflection)
    k3_shift = int(round(math.sin(3.5 + f_phase * 1.57)))
    for x in range(10, 36):
        rx = x + k3_shift
        if 0 <= rx < W:
            grid[yw + 3][rx] = "W1" if x % 3 == 0 else "R2"
    # Prow reflection
    if 0 <= 36 + k3_shift < W: grid[yw + 3][36 + k3_shift] = "R1"
    
    # Row 4: yw + 4 (Reflection of middle hull & near gunwale, depth 4)
    k4_shift = int(round(math.sin(4.8 + f_phase * 1.57)))
    for x in range(11, 35):
        rx = x + k4_shift
        if 0 <= rx < W:
            grid[yw + 4][rx] = "R1" if x % 4 in (0, 1) else "R2"
    # Reflected lantern light shimmer begins:
    if 0 <= 39 + k4_shift < W: grid[yw + 4][39 + k4_shift] = "RL"
    if 0 <= 40 + k4_shift < W: grid[yw + 4][40 + k4_shift] = "L2"
    
    # Row 5: yw + 5 (Thin water ripple break)
    k5_shift = int(round(math.sin(6.0 + f_phase * 1.57)))
    for x in range(14, 33):
        rx = x + k5_shift
        if 0 <= rx < W:
            grid[yw + 5][rx] = "W2" if x % 2 == 0 else "R2"
    # Reflected lantern shimmer
    if 0 <= 39 + k5_shift < W: grid[yw + 5][39 + k5_shift] = "RL"
    if 0 <= 40 + k5_shift < W: grid[yw + 5][40 + k5_shift] = "RL"
    
    # Row 6: yw + 6 (Reflection of top gunwale & prow post, depth 6)
    k6_shift = int(round(math.sin(7.3 + f_phase * 1.57)))
    for x in range(16, 30):
        rx = x + k6_shift
        if 0 <= rx < W and x % 3 != 0:
            grid[yw + 6][rx] = "R2"
    # Reflected stem & lantern
    if 0 <= 37 + k6_shift < W: grid[yw + 6][37 + k6_shift] = "R1"
    if 0 <= 39 + k6_shift < W: grid[yw + 6][39 + k6_shift] = "RL"
    if 0 <= 40 + k6_shift < W: grid[yw + 6][40 + k6_shift] = "RL"
    
    # Row 7: yw + 7 (Reflection of hanging lantern at bottom apex, depth 7)
    k7_shift = int(round(math.sin(8.5 + f_phase * 1.57)))
    if 0 <= 39 + k7_shift < W: grid[yw + 7][39 + k7_shift] = "RL"
    if 0 <= 40 + k7_shift < W: grid[yw + 7][40 + k7_shift] = "RL"
    
    # Row 8: yw + 8 (Trailing lantern light shimmer dancing down into deep water)
    k8_shift = int(round(math.sin(9.8 + f_phase * 1.57)))
    if 0 <= 40 + k8_shift < W and (yw + 8) < H:
        grid[yw + 8][40 + k8_shift] = "W1"

def draw_water_wakes_and_shadow(grid, dy_bob=0, f_phase=0):
    yw = 24 + dy_bob
    
    # Left stern wake
    grid[yw][7] = "W1"; grid[yw][8] = "W2"
    grid[yw + 1][8] = "W1"; grid[yw + 1][9] = "W2"
    
    # Right bow wake
    grid[yw][38] = "W2"; grid[yw][39] = "W1"
    grid[yw + 1][37] = "W2"; grid[yw + 1][38] = "W1"

    # Concentric oval ripples spreading out from boat:
    # Outer Ripple 1:
    r1_y = yw + 5
    if r1_y < H:
        for x in (7, 8, 36, 37):
            if grid[r1_y][x] == ".": grid[r1_y][x] = "W1"
            
    # Outer Ripple 2:
    r2_y = yw + 7
    if r2_y < H:
        for x in (10, 11, 33, 34):
            if grid[r2_y][x] == ".": grid[r2_y][x] = "W2"
            
    # Soft aquatic ground shadow S under the entire boat reflection
    sy_start = yw + 8
    for y in range(sy_start, min(H, sy_start + 4)):
        span = 13 - (y - sy_start) * 2
        for x in range(24 - span, 24 + span):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def outline_boat_only(grid, dy_bob=0):
    yw = 24 + dy_bob
    # Enclose only the real boat (y <= yw) with crisp clean outline #
    for y in range(0, yw + 1):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

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
    
    # 2. Enclose real boat with clean dark outline #
    outline_boat_only(grid, dy_bob=dy_bob)
    
    # 3. Draw Inverted Water Reflection (65% compressed, inverted Y, aquatic teal colors, zigzag wave distortion)
    draw_water_reflection(grid, dy_bob=dy_bob, f_phase=f_idx)
    
    # 4. Draw Water Wakes and Ambient Lake Shadow S
    draw_water_wakes_and_shadow(grid, dy_bob=dy_bob, f_phase=f_idx)
    
    return grid

frames = [build_frame(i) for i in range(4)]

# Check naked pixels on real boat (y <= 25)
def check_outline(grid):
    naked = []
    for y in range(26):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "W1", "W2"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n=== REAL BOAT OUTLINE CHECK ===")
for i, fr in enumerate(frames):
    n = check_outline(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Render preview images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/master_boat_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/master_boat_sheet.png")

gif_frames[0].save(
    "python/master_boat_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered master_boat_sheet.png and master_boat_anim.gif successfully!")
