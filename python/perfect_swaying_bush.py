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
    # Fixed Soil Mound at base (y=37..42, centered at x=24)
    # Ground shadow S (y=42..44)
    for x in range(12, 37): grid[42][x] = "S"
    for x in range(14, 35): grid[43][x] = "S"
    for x in range(17, 31): grid[44][x] = "S"

    # Soil mound body
    mound_spans = {
        37: (20, 28),
        38: (18, 30),
        39: (16, 32),
        40: (15, 33),
        41: (15, 33),
        42: (17, 31)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"; grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            grid[y][x] = "M" if (x + y) % 2 == 0 else "N"
            
    # Bottom mound outline at y=43
    for x in range(17, 32): grid[43][x] = "#"
    # Top mound outline at y=36
    for x in range(20, 29): grid[36][x] = "#"

    # Little green moss tufts on soil mound edges
    grid[37][19] = "B"; grid[37][29] = "B"
    grid[38][17] = "C"; grid[38][31] = "C"

def draw_fixed_trunk(grid):
    # Fixed woody branching trunk rooted at (24, 38)
    # Main trunk
    for y in range(32, 38):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "T"
        grid[y][25] = "U"
        grid[y][26] = "#"
        
    # Flanged root base
    grid[37][21] = "#"; grid[37][22] = "T"
    grid[37][25] = "U"; grid[37][26] = "U"; grid[37][27] = "#"
    
    # Left & right branch stubs supporting lower clusters
    grid[32][20] = "#"; grid[32][21] = "T"
    grid[33][21] = "T"; grid[33][22] = "T"
    
    grid[32][27] = "U"; grid[32][28] = "#"
    grid[33][26] = "U"; grid[33][27] = "U"

def draw_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer):
    # Renders a 3D spherical foliage cluster with volumetric lighting
    x_min = max(1, int(cx - rx - 1))
    x_max = min(W - 2, int(cx + rx + 1))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if d2 <= 1.0:
                if z_layer >= z_buffer[y][x]:
                    z_buffer[y][x] = z_layer
                    nz = math.sqrt(max(0.0, 1.0 - d2))
                    # Light from upper-left (-0.45, -0.65, 0.6)
                    intensity = -0.45 * nx - 0.65 * ny + 0.6 * nz
                    
                    if intensity > 0.80:
                        c = "A" # Sunny lemon-lime highlight
                    elif intensity > 0.40:
                        c = "B" # Light warm green
                    elif intensity > -0.15:
                        c = "C" # Primary lush green
                    elif intensity > -0.52:
                        c = "D" # Deep cool teal shadow
                    else:
                        c = "E" # Deepest navy-green under-crevice
                        
                    # If this pixel is near the bottom-right rim of the cluster, reinforce under-shadow
                    if ny > 0.45 and nx > -0.2:
                        c = "E" if c in ("C", "D") else c
                        
                    grid[y][x] = c

def draw_cluster_crease(grid, cx, cy, rx, ry, z_buffer, current_z):
    # Add dark crease outline underneath the upper cluster so it casts shadow on lower clusters
    x_min = max(1, int(cx - rx - 1))
    x_max = min(W - 2, int(cx + rx + 1))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if 0.85 <= d2 <= 1.15 and ny > 0.3:
                if z_buffer[y][x] < current_z and grid[y][x] not in (".", "S"):
                    grid[y][x] = "#"

def draw_berry(grid, bx, by):
    # 2x2 berry with bright glint, ripe red, and dark shadow
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

def smooth_apex_spikes(grid):
    # Check top rows of clusters to prevent single 1px spikes
    for y in range(1, 20):
        for x in range(2, W - 2):
            if grid[y][x] == "#" and grid[y - 1][x] == "." and grid[y][x - 1] == "." and grid[y][x + 1] == ".":
                # Single vertical 1px tip: widen it to smooth curve
                if grid[y + 1][x - 1] == "#" or grid[y + 1][x + 1] == "#":
                    grid[y][x - 1] = "#"
                    grid[y][x + 1] = "#"

def build_bush_frame(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buffer = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Cluster configurations:
    # 4 distinct spherical foliage clumps:
    # Cluster 0: Center-Back fill
    # Cluster 1: Lower-Left
    # Cluster 2: Lower-Right
    # Cluster 3: Top-Apex
    
    if frame_idx == 0:
        # Frame 1: Rest (Tĩnh tự nhiên)
        clusters = [
            (24, 26, 8.0, 6.0, 1), # Center-Back
            (16, 27, 7.5, 6.5, 2), # Lower-Left
            (31, 27, 7.5, 6.5, 2), # Lower-Right
            (23, 18, 8.5, 7.0, 3), # Top-Apex
        ]
        berries = [
            (13, 28), # on left cluster
            (20, 19), # bouncing berry (resting on top cluster)
            (33, 26), # on right cluster
            (27, 30), # lower right
        ]
        
    elif frame_idx == 1:
        # Frame 2: Wind Push (Gió thổi từ trái, cụm trái bị ép sang phải trước)
        clusters = [
            (25, 26, 8.0, 6.0, 1),
            (19, 27, 6.5, 6.5, 2), # Left cluster squashed and shifted right (16->19)
            (33, 27, 7.5, 6.5, 2), # Right cluster pushed outward (31->33)
            (25, 19, 8.5, 7.0, 3), # Top cluster starts leaning right (23->25)
        ]
        berries = [
            (16, 28), # moved right
            (22, 20), # moved right
            (35, 26), # moved right
            (29, 30),
        ]
        
    elif frame_idx == 2:
        # Frame 3: Full Sway (Toàn bộ cụm lá dạt hẳn sang PHẢI, cụm ngọn vươn dài, 1 quả mọng nảy lên)
        clusters = [
            (27, 26, 8.5, 5.5, 1),
            (20, 27, 7.0, 6.0, 2), # Left cluster swept right
            (36, 28, 8.0, 6.5, 2), # Right cluster swept far right (31->36)
            (28, 17, 9.5, 6.0, 3), # Top cluster stretched horizontally to the right!
        ]
        berries = [
            (18, 27),
            (26, 12), # BOUNCES UPWARD into the air! (1 quả mọng đỏ trên cây nảy nhẹ lên)
            (38, 27), # right berry swept far right
            (32, 30),
        ]
        
    else:
        # Frame 4: Rebound (Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái)
        clusters = [
            (23, 26, 8.0, 6.0, 1),
            (15, 26, 7.5, 6.5, 2), # Left cluster springs left (16->15)
            (29, 26, 7.5, 6.5, 2), # Right cluster springs left (31->29)
            (21, 17, 8.5, 7.0, 3), # Top cluster leans slightly left (23->21)
        ]
        berries = [
            (12, 27),
            (19, 18), # settled back down from bounce
            (31, 25),
            (25, 30),
        ]
        
    # Render clusters in order of Z-layer
    for cx, cy, rx, ry, z_layer in clusters:
        draw_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer)
        
    # Add crease shadow for the top cluster on lower clusters
    top_c = clusters[3]
    draw_cluster_crease(grid, top_c[0], top_c[1], top_c[2], top_c[3], z_buffer, top_c[4])
        
    for bx, by in berries:
        draw_berry(grid, bx, by)
        
    outline_enclosing(grid)
    smooth_apex_spikes(grid)
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

# Measure Cluster Sway Shift
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
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_bush_sheet.png")

gif_frames[0].save(
    "python/perfect_bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

print("\nSaved perfect_bush_sheet.png and perfect_bush_anim.gif successfully!")
