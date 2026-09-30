import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette (Lemon-Lime -> Lush Green -> Navy-Pine)
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 24, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 26, 36, 255),     # Clean dark navy-pine outline (#0c1a24)
    
    # Foliage Hue-Shifting Spherical Clusters
    "A": (214, 245, 66, 255),   # Sunny lemon-lime highlight (#d6f542)
    "B": (96, 207, 50, 255),    # Vibrant light foliage green (#60cf32)
    "C": (38, 142, 60, 255),    # Primary lush leaf green (#268e3c)
    "D": (18, 76, 68, 255),     # Deep cool teal-green shadow (#124c44)
    "E": (10, 38, 50, 255),     # Deep navy-green crevice shadow (#0a2632)
    
    # Woody Trunk & Branches
    "T": (120, 78, 44, 255),    # Wood trunk midtone (#784e2c)
    "U": (66, 38, 20, 255),     # Wood trunk shadow (#422614)
    
    # Red Berries
    "P": (255, 114, 136, 255),  # Berry bright glint (#ff7288)
    "R": (214, 30, 56, 255),    # Berry ripe crimson (#d61e38)
    "Q": (112, 12, 32, 255),    # Berry deep shadow (#700c20)
    
    # Earth Mound
    "M": (74, 48, 30, 255),     # Soil mound midtone (#4a301e)
    "N": (44, 24, 12, 255),     # Soil mound shadow (#2c180c)
}

def create_base_ground(grid):
    # Fixed Soil Mound at base (y=38..42, centered at x=24)
    # Ground shadow S (y=42..44)
    for x in range(12, 37): grid[42][x] = "S"
    for x in range(15, 34): grid[43][x] = "S"
    for x in range(18, 30): grid[44][x] = "S"

    # Soil mound body
    mound_spans = {
        38: (19, 29),
        39: (17, 31),
        40: (16, 32),
        41: (15, 33),
        42: (17, 31)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"; grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            grid[y][x] = "M" if (x + y) % 2 == 0 else "N"
            
    # Bottom mound outline at y=43
    for x in range(18, 31): grid[43][x] = "#"
    # Top mound outline at y=37
    for x in range(20, 29): grid[37][x] = "#"

def draw_fixed_trunk(grid):
    # Fixed trunk rooted at (24, 38) rising to (24, 32)
    for y in range(32, 39):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "T"
        grid[y][25] = "U"
        grid[y][26] = "#"
        
    # Roots flanging into soil
    grid[38][21] = "#"; grid[38][22] = "T"
    grid[38][25] = "U"; grid[38][26] = "U"; grid[38][27] = "#"

def draw_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer):
    # Renders a 3D lit foliage sphere cluster
    # Light comes from upper-left (dx = -0.5, dy = -0.7)
    x_min = max(1, int(cx - rx - 1))
    x_max = min(W - 2, int(cx + rx + 1))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    # First pass: fill cluster volume
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if d2 <= 1.0:
                if z_layer >= z_buffer[y][x]:
                    z_buffer[y][x] = z_layer
                    nz = math.sqrt(max(0.0, 1.0 - d2))
                    # Dot product with light vector (-0.45, -0.65, 0.6)
                    intensity = -0.45 * nx - 0.65 * ny + 0.6 * nz
                    
                    if intensity > 0.82:
                        c = "A" # Sunny lemon-lime highlight
                    elif intensity > 0.42:
                        c = "B" # Light warm green
                    elif intensity > -0.15:
                        c = "C" # Primary lush green
                    elif intensity > -0.52:
                        c = "D" # Deep cool teal-green shadow
                    else:
                        c = "E" # Deepest navy-green under-crevice
                        
                    grid[y][x] = c

def draw_berry(grid, bx, by):
    # 2x2 or 3x3 juicy red berry cluster
    # Outline & highlight
    grid[by][bx] = "P"     # Glint
    grid[by][bx + 1] = "R" # Ripe red
    grid[by + 1][bx] = "R"
    grid[by + 1][bx + 1] = "Q" # Shadow

def outline_enclosing(grid):
    # Ensure all foliage, trunk, and berries are enclosed by # against .
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def build_bush_frame(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buffer = [[0 for _ in range(W)] for _ in range(H)]
    
    # Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 3-4 Foliage Clusters Configuration per Frame:
    # Cluster 0: Center-Back base clump
    # Cluster 1: Left clump
    # Cluster 2: Right clump
    # Cluster 3: Top / Apex clump
    
    if frame_idx == 0:
        # Frame 1: Rest (Tĩnh tự nhiên)
        clusters = [
            (24, 25, 7.5, 6.0, 1), # Back center
            (16, 24, 6.5, 5.5, 2), # Left
            (31, 25, 6.5, 5.5, 2), # Right
            (23, 16, 7.5, 6.5, 3), # Top apex
        ]
        berries = [
            (13, 26), # on left cluster
            (21, 19), # on top cluster
            (33, 24), # on right cluster
            (27, 28), # on lower-right
        ]
        
    elif frame_idx == 1:
        # Frame 2: Wind Push (Gió thổi từ trái, cụm trái bị ép sang phải trước)
        clusters = [
            (25, 25, 7.5, 6.0, 1), # Back center shifts slightly
            (19, 24, 5.5, 5.5, 2), # Left cluster squashed and pushed right (16->19)
            (33, 25, 6.5, 5.5, 2), # Right cluster pushed right (31->33)
            (25, 17, 7.5, 6.5, 3), # Top cluster starts leaning right (23->25)
        ]
        berries = [
            (16, 26), # left berry moved right
            (23, 20), # top berry
            (35, 24), # right berry moved right
            (29, 28),
        ]
        
    elif frame_idx == 2:
        # Frame 3: Full Sway (Toàn bộ cụm lá dạt hẳn sang PHẢI, cụm ngọn vươn dài, 1 quả mọng nảy lên)
        clusters = [
            (27, 25, 8.0, 5.5, 1), # Back center pushed right
            (20, 24, 6.0, 5.0, 2), # Left cluster swept right
            (36, 26, 7.0, 5.5, 2), # Right cluster swept far right (31->36)
            (28, 15, 8.5, 5.5, 3), # Top cluster stretched horizontally to the right!
        ]
        berries = [
            (18, 25),
            (27, 12), # BOUNCES UPWARD into the air! (1 quả mọng đỏ trên cây nảy nhẹ lên)
            (38, 25), # right berry swept far right
            (32, 28),
        ]
        
    else:
        # Frame 4: Rebound (Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái)
        clusters = [
            (23, 25, 7.5, 6.0, 1), # Rebounds slightly left
            (15, 23, 6.5, 5.5, 2), # Left cluster springs left (16->15, high)
            (29, 24, 6.5, 5.5, 2), # Right cluster springs left (31->29)
            (21, 15, 7.5, 6.5, 3), # Top cluster leans slightly left (23->21)
        ]
        berries = [
            (12, 25),
            (19, 18), # settled back down from bounce
            (31, 23),
            (25, 28),
        ]
        
    for cx, cy, rx, ry, z_layer in clusters:
        draw_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer)
        
    for bx, by in berries:
        draw_berry(grid, bx, by)
        
    outline_enclosing(grid)
    
    return grid

test_frames = [build_bush_frame(i) for i in range(4)]

# Check outline completeness
def check_outline_completeness(grid):
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

print("\n=== OUTLINE COMPLETENESS CHECK ===")
all_clean = True
for i, fr in enumerate(test_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")
    if n:
        print(f"  {n[:10]}")
        all_clean = False
print(f"All frames 100% enclosed: {all_clean}")

# Measure Cluster Sway Shift (Leftmost/Rightmost/Top cluster shifts)
print("\n=== SWAY DYNAMICS VERIFICATION ===")
for i, fr in enumerate(test_frames):
    leaf_xs = [x for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    leaf_ys = [y for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    mean_x = sum(leaf_xs) / len(leaf_xs) if leaf_xs else 0
    min_y = min(leaf_ys) if leaf_ys else 0
    print(f"Frame {i+1}: Canopy Mean X = {mean_x:.1f} (Min X={min(leaf_xs)}, Max X={max(leaf_xs)}), Top Apex Y={min_y}")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(test_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/bush_sheet.png")

gif_frames[0].save(
    "python/bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

print("\nSaved bush_sheet.png and bush_anim.gif successfully!")
