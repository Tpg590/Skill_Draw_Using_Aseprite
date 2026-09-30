import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette (Deep Teal -> Cyan-Green -> Purple-Navy)
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (14, 24, 36, 130),     # Soft aquatic shadow (Alpha 130)
    "#": (10, 18, 28, 255),     # Clean dark navy-teal outline (#0a121c)
    
    # Real Boat Wood (Rich warm oak with golden highlights)
    "A": (232, 158, 68, 255),   # Golden oak highlight (#e89e44)
    "B": (164, 90, 34, 255),    # Warm oak midtone (#a45a22)
    "C": (88, 42, 14, 255),     # Deep oak shadow / interior floor (#582a0e)
    
    # Storm Lantern (Golden radiant flame & OSL)
    "L1": (255, 248, 168, 255), # White-gold flame core (#fff8a8)
    "L2": (246, 166, 35, 255),  # Radiant amber glow (#f6a623)
    "L3": (196, 92, 16, 255),   # Deep orange metal cage (#c45c10)
    
    # Reflected Boat in Water (Teal-tinted & desaturated)
    "R1": (74, 120, 120, 255),  # Reflected wood highlight (Teal-oak #4a7878)
    "R2": (40, 76, 80, 255),    # Reflected wood body (Dark teal #284c50)
    "R3": (20, 46, 52, 255),    # Deep aquatic under-crevice (#142e34)
    "RL": (114, 191, 160, 255), # Reflected golden-teal lantern shimmer (#72bfa0)
    
    # Water Surface Ripples (Gợn sóng hồ)
    "W1": (46, 88, 104, 255),   # Water ripple crest (#2e5868)
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

def draw_real_boat(grid, dy_bob=0, tilt_angle=0.0):
    # Renders the real wooden boat and the glowing storm lantern
    # dy_bob: -1, 0, or 1 vertical pixel offset
    # tilt_angle: slight pitch angle
    
    # Center of rotation: (24, 23)
    # The boat spans: X = 9..38, Y = 13..25 (relative to waterline Y=25)
    
    # 1. Hull & Gunwale coordinates:
    # Stern (left): X=9..11, Y=19..23
    # Midsection: X=12..31, Y=19..24
    # Bow/Prow (right): X=32..38, Y=17..24
    
    base_waterline = 24 + dy_bob
    
    # Keel / bottom line (just above water)
    for x in range(12, 36):
        y = base_waterline
        grid[y][x] = "#"
        grid[y - 1][x] = "C" if x < 28 else "B"
        
    # Stern profile (X=9..12)
    grid[base_waterline - 1][10] = "#"; grid[base_waterline - 1][11] = "#"
    grid[base_waterline - 2][9] = "#";  grid[base_waterline - 2][10] = "B"; grid[base_waterline - 2][11] = "C"
    grid[base_waterline - 3][9] = "#";  grid[base_waterline - 3][10] = "A"; grid[base_waterline - 3][11] = "B"
    grid[base_waterline - 4][9] = "#";  grid[base_waterline - 4][10] = "#"; grid[base_waterline - 4][11] = "#"
    
    # Transom top stern edge
    grid[base_waterline - 4][12] = "A"; grid[base_waterline - 4][13] = "A"

    # Outer Hull Clinker Planks (side facing camera)
    # Planks running along bottom edge
    for x in range(12, 34):
        # Bottom plank (row -2)
        grid[base_waterline - 2][x] = "B" if x % 3 != 0 else "C"
        # Middle plank (row -3)
        grid[base_waterline - 3][x] = "A" if x % 4 != 0 else "B"
        
    # Gunwale (top railing of boat)
    for x in range(11, 35):
        grid[base_waterline - 4][x] = "A"
        grid[base_waterline - 5][x] = "#"
        
    # Interior cockpit / Rowing seat (thanh ghế chèo)
    # Seat bench at X=21..25, Y=base_waterline - 3
    for x in range(21, 26):
        grid[base_waterline - 3][x] = "A"
        grid[base_waterline - 2][x] = "C" # shadow under seat
        
    # Prow / Bow curves upward to the right (X=33..38)
    grid[base_waterline - 1][35] = "#"; grid[base_waterline - 1][36] = "#"
    grid[base_waterline - 2][34] = "B"; grid[base_waterline - 2][35] = "A"; grid[base_waterline - 2][36] = "#"
    grid[base_waterline - 3][34] = "A"; grid[base_waterline - 3][35] = "A"; grid[base_waterline - 3][36] = "B"; grid[base_waterline - 3][37] = "#"
    grid[base_waterline - 4][35] = "A"; grid[base_waterline - 4][36] = "A"; grid[base_waterline - 4][37] = "#"
    grid[base_waterline - 5][36] = "A"; grid[base_waterline - 5][37] = "#"
    grid[base_waterline - 6][36] = "#"; grid[base_waterline - 6][37] = "#"
    
    # Prow Bow Post (cọc mũi thuyền): X=37, Y=base_waterline - 7..-9
    grid[base_waterline - 7][36] = "#"; grid[base_waterline - 7][37] = "B"; grid[base_waterline - 7][38] = "#"
    grid[base_waterline - 8][36] = "#"; grid[base_waterline - 8][37] = "A"; grid[base_waterline - 8][38] = "#"
    grid[base_waterline - 9][36] = "#"; grid[base_waterline - 9][37] = "A"; grid[base_waterline - 9][38] = "#"
    grid[base_waterline - 10][37] = "#"
    
    # Lantern hanging arm extending to X=39
    grid[base_waterline - 9][39] = "#"; grid[base_waterline - 8][39] = "#"
    
    # Storm Lantern (Đèn bão phát sáng vàng rực):
    # Position: X = 38..40, Y = base_waterline - 8 .. -5
    lx = 39
    ly = base_waterline - 7 # center of lantern
    
    # Lantern cap & ring
    grid[ly - 1][lx] = "L3"
    grid[ly - 2][lx] = "#"
    
    # Lantern glass & glowing flame
    grid[ly][lx - 1] = "#"; grid[ly][lx] = "L1"; grid[ly][lx + 1] = "#"
    grid[ly + 1][lx - 1] = "L3"; grid[ly + 1][lx] = "L2"; grid[ly + 1][lx + 1] = "L3"
    grid[ly + 2][lx - 1] = "#"; grid[ly + 2][lx] = "L3"; grid[ly + 2][lx + 1] = "#"
    
    # OSL Golden Glow onto Prow Wood
    grid[base_waterline - 5][35] = "L2"
    grid[base_waterline - 6][36] = "L2"
    grid[base_waterline - 7][36] = "L1"

def draw_water_reflection(grid, dy_bob=0, frame_phase=0):
    # Calculates inverted Y reflection with:
    # 1. 60-70% vertical height compression
    # 2. Desaturated teal/aquatic color transformation
    # 3. Horizontal zigzag wave rippling (shifting by +/- 1 pixel)
    
    waterline = 24 + dy_bob
    
    # Sample pixels of the real boat above waterline
    boat_pixels = {}
    for y in range(0, waterline + 1):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S"):
                boat_pixels[(x, y)] = code
                
    # Invert and compress:
    # Delta y from waterline: dy = waterline - y (for y <= waterline)
    # Reflected y: refl_y = waterline + 1 + round(dy * 0.65)
    
    # Wave ripple shift per row below waterline:
    # Alternating zigzag wave pattern shifting dynamically with frame_phase
    for (bx, by), code in boat_pixels.items():
        dy = waterline - by
        if dy <= 0: continue # ignore pixels at/below waterline
        
        # 65% compression ratio (strictly within 60% - 70%)
        refl_dist = int(round(dy * 0.65))
        refl_y = waterline + refl_dist
        if refl_y >= H: continue
        
        # Horizontal wave distortion (zigzag +/- 1px)
        # Shift depends on depth and frame phase
        shift = int(round(math.sin(refl_dist * 1.3 + frame_phase * 1.57)))
        refl_x = bx + shift
        if 0 <= refl_x < W:
            # Map color to aquatic teal tone
            refl_color = COLOR_MAP_REFL.get(code, "R2")
            # If row is even/odd water ripple crest, add subtle water tint
            grid[refl_y][refl_x] = refl_color

def draw_water_ripples(grid, dy_bob=0, frame_phase=0):
    # Draws concentric oval water ripples around the boat (within bounds, NO canvas-wide lines!)
    waterline = 24 + dy_bob
    
    # Primary water ripple ring touching boat waterline (y = waterline, waterline + 1)
    # Left stern wake
    grid[waterline][7] = "W1"; grid[waterline][8] = "W2"
    grid[waterline + 1][8] = "W1"; grid[waterline + 1][9] = "W2"
    
    # Right bow wake
    grid[waterline][39] = "W2"; grid[waterline][40] = "W1"
    grid[waterline + 1][38] = "W2"; grid[waterline + 1][39] = "W1"

    # Expanding ripples at water surface below boat:
    # Ripple 1: y = waterline + 3
    r1_y = waterline + 3
    if r1_y < H:
        phase_shift = (frame_phase % 2)
        for x in (11 + phase_shift, 12 + phase_shift, 20 - phase_shift, 21 - phase_shift, 32 + phase_shift, 33 + phase_shift):
            if grid[r1_y][x] == ".":
                grid[r1_y][x] = "W1"
                
    # Ripple 2: y = waterline + 6
    r2_y = waterline + 6
    if r2_y < H:
        for x in (14, 15, 24, 25, 34, 35):
            if grid[r2_y][x] == ".":
                grid[r2_y][x] = "W2"
                
    # Soft aquatic ground/water shadow S under the entire reflection footprint
    # Elliptical pool: x=8..42, y=waterline+7..waterline+10
    sy_start = waterline + 7
    for y in range(sy_start, min(H, sy_start + 4)):
        span_w = 14 - (y - sy_start) * 2
        for x in range(24 - span_w, 24 + span_w):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def outline_enclosing(grid):
    # Enclose real boat and reflection edges with clean outline
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "W1", "W2"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def build_frame(f_idx):
    grid = empty_grid()
    
    # Bobbing parameters per frame:
    # Frame 1: Neutral rest (dy=0)
    # Frame 2: Dip down (dy=+1)
    # Frame 3: Neutral recovery (dy=0)
    # Frame 4: Rise up (dy=-1)
    dy_bob_table = [0, 1, 0, -1]
    dy_bob = dy_bob_table[f_idx]
    
    # 1. Draw Real Boat
    draw_real_boat(grid, dy_bob=dy_bob)
    
    # 2. Draw Inverted Water Reflection (with 65% height compression & wave rippling)
    draw_water_reflection(grid, dy_bob=dy_bob, frame_phase=f_idx)
    
    # 3. Draw Water Ripples and Ambient Shadow
    draw_water_ripples(grid, dy_bob=dy_bob, frame_phase=f_idx)
    
    # 4. Clean Enclosing Outline
    outline_enclosing(grid)
    
    return grid

frames = [build_frame(i) for i in range(4)]

# Check naked pixels
def check_outline(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "W1", "W2"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n=== OUTLINE CHECK ===")
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/boat_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/test_boat_sheet.png")

gif_frames[0].save(
    "python/test_boat_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered test_boat_sheet.png and test_boat_anim.gif successfully!")
