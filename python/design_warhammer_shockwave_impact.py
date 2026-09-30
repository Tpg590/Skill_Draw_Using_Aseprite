import os
import math
from PIL import Image

W, H = 48, 48

# Stardew Valley Style Palette:
PALETTE = {
    ".": None,
    "S": (26, 16, 18, 130),       # Soft ground shadow (Alpha 130)
    "#": (36, 22, 16, 255),       # Soft dark espresso/slate outline (#241610 - NO #000000!)
    
    # Baked Terracotta / Slate Warhammer Head
    "P": (245, 185, 145, 255),   # Bright terracotta highlight (#f5b991)
    "A": (210, 130, 85, 255),    # Warm terracotta mid-highlight (#d28255)
    "B": (160, 80, 45, 255),     # Rich terracotta midtone (#a0502d)
    "C": (105, 45, 22, 255),     # Deep terracotta shadow (#692d16)
    "D": (58, 24, 12, 255),      # Deepest stone fissure / underside (#3a180c)
    
    # Steel Binding Bands & Rivets on Hammer
    "I": (205, 215, 225, 255),   # Steel band highlight (#cdd7e1)
    "T": (135, 145, 158, 255),   # Steel band midtone (#87919e)
    "K": (70, 78, 88, 255),      # Steel band shadow (#464e58)
    
    # Wooden Shaft
    "E": (200, 155, 100, 255),   # Oak shaft highlight (#c89b64)
    "U": (140, 95, 50, 255),     # Oak shaft midtone (#8c5f32)
    "Z": (80, 50, 22, 255),      # Oak shaft shadow (#503216)
    
    # Stone Floor & Crack Crevices
    "F": (115, 95, 82, 255),     # Stone floor surface (#735f52)
    "G": (85, 68, 58, 255),      # Stone floor shadow (#55443a)
    "X": (28, 18, 14, 255),      # Deep radial crack fissure (#1c120e)
    
    # Hollow Shockwave Dust & Spark
    "W": (255, 250, 225, 255),   # White-hot spark / shock crest (#fffae1)
    "Y": (245, 195, 120, 255),   # Warm dust shockwave ring (#f5c378)
    "O": (160, 100, 55, 255),    # Shockwave outer dust border (#a06437)
}

PALETTE_HEX = {
    ".": None,
    "S": "#1a1012",
    "#": "#241610",
    "P": "#f5b991",
    "A": "#d28255",
    "B": "#a0502d",
    "C": "#692d16",
    "D": "#3a180c",
    "I": "#cdd7e1",
    "T": "#87919e",
    "K": "#464e58",
    "E": "#c89b64",
    "U": "#8c5f32",
    "Z": "#503216",
    "F": "#735f52",
    "G": "#55443a",
    "X": "#1c120e",
    "W": "#fffae1",
    "Y": "#f5c378",
    "O": "#a06437",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_stone_floor(grid):
    for x in range(9, 40):
        set_p(grid, x, 37, "F")
        set_p(grid, x, 38, "F" if (x % 7 != 0) else "G")
    for y in range(39, 42):
        for x in range(9, 40):
            set_p(grid, x, y, "G" if (x % 7 != 0) else "#")
    for y in range(37, 42):
        set_p(grid, 8, y, "#")
        set_p(grid, 40, y, "#")
    for x in range(8, 41):
        set_p(grid, x, 42, "#")
    for x in range(11, 38):
        set_p(grid, x, 43, "S")

def draw_hollow_shockwave(grid, cx, cy, rx, ry, col_in="W", col_mid="Y", col_out="O"):
    # Precise hollow 3/4 ellipse
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            d = math.hypot(dx, dy)
            if 0.88 <= d <= 1.08:
                if d <= 0.95:
                    set_p(grid, x, y, col_in)
                elif d <= 1.02:
                    set_p(grid, x, y, col_mid)
                else:
                    set_p(grid, x, y, col_out)

def draw_radial_cracks(grid, cx, cy, stage):
    if stage == 1:
        seeds = [(cx - 2, cy), (cx + 2, cy), (cx - 1, cy + 1), (cx + 1, cy + 1)]
        for x, y in seeds:
            set_p(grid, x, y, "X")
    elif stage == 2:
        c1 = [(cx - 2, cy), (cx - 4, cy + 1), (cx - 5, cy + 1), (cx - 7, cy + 2), (cx - 9, cy + 2)]
        for x, y in c1:
            set_p(grid, x, y, "X")
            set_p(grid, x, y - 1, "D")
        c2 = [(cx + 2, cy), (cx + 4, cy + 1), (cx + 6, cy + 1), (cx + 8, cy + 2), (cx + 10, cy + 2)]
        for x, y in c2:
            set_p(grid, x, y, "X")
            set_p(grid, x, y - 1, "D")
        c3 = [(cx - 3, cy - 1), (cx - 6, cy - 1), (cx - 8, cy - 2)]
        for x, y in c3:
            set_p(grid, x, y, "X")
            set_p(grid, x + 1, y, "D")
        c4 = [(cx + 3, cy - 1), (cx + 6, cy - 1), (cx + 8, cy - 2)]
        for x, y in c4:
            set_p(grid, x, y, "X")
            set_p(grid, x - 1, y, "D")
    elif stage == 3:
        c1 = [(cx - 2, cy), (cx - 4, cy + 1), (cx - 5, cy + 1), (cx - 7, cy + 2), (cx - 10, cy + 2), (cx - 12, cy + 3)]
        for x, y in c1:
            set_p(grid, x, y, "X")
        c2 = [(cx + 2, cy), (cx + 4, cy + 1), (cx + 6, cy + 1), (cx + 8, cy + 2), (cx + 11, cy + 2), (cx + 13, cy + 3)]
        for x, y in c2:
            set_p(grid, x, y, "X")
        c3 = [(cx - 3, cy - 1), (cx - 6, cy - 1), (cx - 9, cy - 2)]
        for x, y in c3:
            set_p(grid, x, y, "X")
        c4 = [(cx + 3, cy - 1), (cx + 6, cy - 1), (cx + 9, cy - 2)]
        for x, y in c4:
            set_p(grid, x, y, "X")
    elif stage == 4:
        faint = [(cx - 3, cy), (cx - 6, cy + 1), (cx + 3, cy), (cx + 6, cy + 1), (cx - 5, cy - 1), (cx + 5, cy - 1)]
        for x, y in faint:
            set_p(grid, x, y, "G")

def draw_hammer(grid, hx, hy, angle_mode):
    if angle_mode == 0:
        # Raised high in air (Frame 1, 6)
        for s in range(16):
            t = s / 15.0
            sx = int(round(22 + t * 13))
            sy = int(round(12 + t * 14))
            set_p(grid, sx, sy, "U")
            set_p(grid, sx - 1, sy, "E")
            set_p(grid, sx + 1, sy, "Z")
            
        for y in range(7, 16):
            for x in range(14, 25):
                set_p(grid, x, y, "B")
        for x in range(14, 25):
            set_p(grid, x, 7, "P")
        for y in range(7, 16):
            set_p(grid, 14, y, "P")
            set_p(grid, 24, y, "C")
            
        for y in range(7, 16):
            set_p(grid, 19, y, "I")
            set_p(grid, 20, y, "T")
            set_p(grid, 21, y, "K")
            
        for x in range(13, 26):
            set_p(grid, x, 6, "#")
            set_p(grid, x, 16, "#")
        for y in range(6, 17):
            set_p(grid, 13, y, "#")
            set_p(grid, 25, y, "#")

    else:
        # Slammed down vertically on floor
        for y in range(hy - 24, hy - 8):
            set_p(grid, hx, y, "U")
            set_p(grid, hx - 1, y, "E")
            set_p(grid, hx + 1, y, "Z")
            set_p(grid, hx - 2, y, "#")
            set_p(grid, hx + 2, y, "#")
        set_p(grid, hx - 1, hy - 25, "#")
        set_p(grid, hx, hy - 25, "I")
        set_p(grid, hx + 1, hy - 25, "#")

        for y in range(hy - 8, hy + 1):
            for x in range(hx - 6, hx + 7):
                set_p(grid, x, y, "B")
        for x in range(hx - 5, hx + 6):
            set_p(grid, x, hy - 8, "P")
        for y in range(hy - 8, hy + 1):
            set_p(grid, hx - 6, y, "P" if y < hy - 4 else "A")
            set_p(grid, hx + 6, y, "C")
            
        for y in range(hy - 8, hy + 1):
            set_p(grid, hx - 1, y, "I")
            set_p(grid, hx, y, "T")
            set_p(grid, hx + 1, y, "K")

        for x in range(hx - 7, hx + 8):
            set_p(grid, x, hy - 9, "#")
            set_p(grid, x, hy + 1, "#")
        for y in range(hy - 9, hy + 2):
            set_p(grid, hx - 7, y, "#")
            set_p(grid, hx + 7, y, "#")

def build_warhammer_frame(frame_num):
    grid = empty_grid()
    draw_stone_floor(grid)
    
    cx, cy = 24, 36
    
    if frame_num == 1:
        for x in range(cx - 4, cx + 5):
            set_p(grid, x, cy + 1, "S")
        draw_hammer(grid, cx, cy, angle_mode=0)
        
    elif frame_num == 2:
        draw_radial_cracks(grid, cx, cy, stage=1)
        for x in range(cx - 8, cx + 9):
            set_p(grid, x, cy + 1, "S")
        draw_hammer(grid, cx, cy, angle_mode=1)
        # Impact point flash sparks
        set_p(grid, cx - 2, cy, "W")
        set_p(grid, cx + 2, cy, "W")
        set_p(grid, cx, cy + 1, "W")

    elif frame_num == 3:
        # Frame 3:
        # 1. Radial cracks on floor
        draw_radial_cracks(grid, cx, cy, stage=2)
        # 2. Hammer planted on floor
        draw_hammer(grid, cx, cy, angle_mode=1)
        # 3. Hollow shockwave ring encircling impact (rx = 9.8, ry = 5.0 -> W = 21px, H = 11px, Ratio = 0.52)
        draw_hollow_shockwave(grid, cx, cy, rx=9.8, ry=5.0, col_in="W", col_mid="Y", col_out="O")
        # 4. Flying stone debris in the air (P, A, B, #)
        set_p(grid, 15, 25, "P")
        set_p(grid, 16, 25, "B")
        set_p(grid, 15, 26, "#")
        set_p(grid, 33, 24, "P")
        set_p(grid, 34, 24, "B")
        set_p(grid, 34, 25, "#")
        set_p(grid, 20, 21, "P")
        set_p(grid, 21, 21, "A")
        set_p(grid, 21, 22, "#")

    elif frame_num == 4:
        # Frame 4: Expanded shockwave ring (rx = 13.8, ry = 7.0 -> W = 28px, H = 14px, Ratio = 0.50)
        draw_radial_cracks(grid, cx, cy, stage=3)
        draw_hammer(grid, cx, cy - 1, angle_mode=2)
        draw_hollow_shockwave(grid, cx, cy, rx=13.8, ry=7.0, col_in="Y", col_mid="O", col_out="G")
        set_p(grid, 13, 29, "A")
        set_p(grid, 14, 29, "#")
        set_p(grid, 35, 28, "A")
        set_p(grid, 36, 28, "#")
        set_p(grid, 20, 26, "A")

    elif frame_num == 5:
        draw_radial_cracks(grid, cx, cy, stage=4)
        draw_hammer(grid, cx, cy, angle_mode=1)
        set_p(grid, 12, cy + 1, "B")
        set_p(grid, 13, cy + 1, "#")
        set_p(grid, 36, cy + 1, "B")
        set_p(grid, 37, cy + 1, "#")
        set_p(grid, 20, cy + 2, "B")

    elif frame_num == 6:
        draw_radial_cracks(grid, cx, cy, stage=4)
        for x in range(cx - 5, cx + 6):
            set_p(grid, x, cy + 1, "S")
        draw_hammer(grid, cx, cy, angle_mode=0)

    return grid

frames = [build_warhammer_frame(i) for i in range(1, 7)]

# Strict verification of requirements:
print("--- VERIFICATION OF WARHAMMER SHOCKWAVE ---")
f3_shock_x = []
f3_shock_y = []
for y in range(30, 43):
    for x in range(W):
        if frames[2][y][x] in ("W", "Y", "O"):
            f3_shock_x.append(x)
            f3_shock_y.append(y)
f3_w = max(f3_shock_x) - min(f3_shock_x) + 1
f3_h = max(f3_shock_y) - min(f3_shock_y) + 1
ratio_f3 = f3_h / f3_w
print(f"Frame 3 Shockwave: Width = {f3_w}px, Height = {f3_h}px, Ratio Y/X = {ratio_f3:.2f}")
assert 19 <= f3_w <= 22, f"Shockwave width should be ~20px, got {f3_w}"
assert 10 <= f3_h <= 12, f"Shockwave height should be ~10px, got {f3_h}"
assert 0.45 <= ratio_f3 <= 0.60, f"Shockwave must be a 3/4 flat ellipse (0.5..0.6), got {ratio_f3}"

center_pixels = [frames[2][36][x] for x in range(24 - 4, 24 + 5)]
solid_wave_in_center = sum(1 for c in center_pixels if c in ("W", "Y", "O"))
print(f"Center shockwave pixels count: {solid_wave_in_center}")
assert solid_wave_in_center == 0, "Shockwave ring must be hollow inside!"

os.makedirs("test", exist_ok=True)
images = []
for idx, f in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            val = PALETTE.get(c)
            if val:
                img.putpixel((x, y), val)
    img.save(f"test/hammer_f{idx+1}.png")
    images.append(img)

images[0].save(
    "test/hammer_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=125,
    loop=0,
    disposal=2
)

print("Warhammer test frames generated successfully.")
