import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 24, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 26, 36, 255),     # Clean dark navy-pine outline (#0c1a24)
    
    # Foliage Hue-Shifting: Lemon-Lime -> Vibrant Green -> Cool Teal -> Navy Crevice
    "A": (214, 245, 66, 255),   # Sunny lemon-lime highlight (#d6f542)
    "B": (96, 207, 50, 255),    # Vibrant light green (#60cf32)
    "C": (38, 142, 60, 255),    # Primary lush leaf green (#268e3c)
    "D": (18, 76, 68, 255),     # Deep cool teal-green shadow (#124c44)
    "E": (10, 38, 50, 255),     # Deep navy-green crevice shadow (#0a2632)
    
    # Woody Trunk & Gnarly Stems
    "T": (130, 84, 48, 255),    # Wood trunk midtone (#825430)
    "U": (72, 42, 24, 255),     # Wood trunk shadow (#482a18)
    
    # Red Berries & Blossom
    "P": (255, 120, 140, 255),  # Berry glint highlight (#ff788c)
    "R": (218, 32, 58, 255),    # Berry ripe crimson (#da203a)
    "Q": (116, 14, 34, 255),    # Berry deep shadow (#740e22)
    
    # Earth Mound (Organic rounded knoll, strictly NO dithering)
    "L": (156, 104, 64, 255),   # Earth crest highlight (#9c6840)
    "M": (106, 66, 38, 255),    # Earth body midtone (#6a4226)
    "N": (56, 32, 18, 255),     # Earth under-shadow (#382012)
}

def create_base_ground(grid):
    # 1. Ground contact shadow S (y=42..44, soft ellipse)
    for x in range(10, 38): grid[42][x] = "S"
    for x in range(12, 36): grid[43][x] = "S"
    for x in range(15, 33): grid[44][x] = "S"

    # 2. Organic rounded soil mound (y=39..42)
    # y=39: x=17..31
    # y=40: x=14..34
    # y=41: x=13..35
    # y=42: x=15..33
    mound_spans = {
        39: (17, 31),
        40: (14, 34),
        41: (13, 35),
        42: (15, 33)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            if y == 39:
                grid[y][x] = "L"
            elif y == 40:
                grid[y][x] = "M"
            else:
                grid[y][x] = "N"
                
    # Bottom mound outline at y=43
    for x in range(15, 34): grid[43][x] = "#"
    # Top mound outline at y=38
    for x in range(17, 32): grid[38][x] = "#"

    # Moss & grass blades sprouting on soil mound
    grid[38][16] = "#"; grid[38][17] = "B"
    grid[38][31] = "B"; grid[38][32] = "#"
    grid[39][13] = "#"; grid[39][14] = "C"
    grid[39][34] = "C"; grid[39][35] = "#"
    grid[40][13] = "#"; grid[40][35] = "#"

def draw_fixed_trunk(grid):
    # Short gnarly woody base rooted in the mound (y=34..39)
    # Root base
    grid[39][21] = "#"; grid[39][22] = "T"; grid[39][23] = "T"
    grid[39][24] = "U"; grid[39][25] = "U"; grid[39][26] = "#"
    
    # Short stout trunk
    for y in range(35, 39):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "U"
        grid[y][25] = "#"
        
    # Gnarly branch elbows peeking beneath the foliage
    grid[34][19] = "#"; grid[34][20] = "T"; grid[34][21] = "#"
    grid[35][20] = "#"; grid[35][21] = "T"
    
    grid[34][26] = "#"; grid[34][27] = "U"; grid[34][28] = "#"
    grid[35][25] = "U"; grid[35][26] = "#"

def draw_cluster_stamp(grid, cx, cy, rx, ry, z_layer, z_buffer, skew=0.0):
    # Cluster diameter = 8-14px (rx = 4.5..7.0, ry = 4.0..6.5)
    x_min = max(1, int(cx - rx - abs(skew)*ry - 2))
    x_max = min(W - 2, int(cx + rx + abs(skew)*ry + 2))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    for y in range(y_min, y_max + 1):
        dx_skew = skew * (cy - y)
        cur_cx = cx + dx_skew
        for x in range(x_min, x_max + 1):
            nx = (x - cur_cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if d2 <= 1.0:
                if z_layer >= z_buffer[y][x]:
                    z_buffer[y][x] = z_layer
                    nz = math.sqrt(max(0.0, 1.0 - d2))
                    
                    # Directional light from Upper-Left (-0.48, -0.62, 0.62)
                    intensity = -0.48 * nx - 0.62 * ny + 0.62 * nz
                    
                    if intensity > 0.76:
                        c = "A" # Sunny lemon-lime highlight
                    elif intensity > 0.36:
                        c = "B" # Warm vibrant green
                    elif intensity > -0.16:
                        c = "C" # Primary lush green
                    elif intensity > -0.52:
                        c = "D" # Deep cool teal
                    else:
                        c = "E" # Deepest navy-green crevice
                        
                    # Bottom-right rim under-shadow
                    if ny > 0.38 and nx > -0.2:
                        c = "E" if c in ("C", "D") else c
                        
                    grid[y][x] = c

def draw_crease(grid, cx, cy, rx, ry, z_buffer, current_z, skew=0.0):
    x_min = max(1, int(cx - rx - abs(skew)*ry - 2))
    x_max = min(W - 2, int(cx + rx + abs(skew)*ry + 2))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    for y in range(y_min, y_max + 1):
        dx_skew = skew * (cy - y)
        cur_cx = cx + dx_skew
        for x in range(x_min, x_max + 1):
            nx = (x - cur_cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if 0.80 <= d2 <= 1.15 and ny > 0.30:
                if z_buffer[y][x] < current_z and grid[y][x] not in (".", "S"):
                    grid[y][x] = "#"

def draw_berry(grid, bx, by, airborne=False):
    # 2x2 berry with highlight, red body, and shadow
    grid[by][bx] = "P"     # Glint
    grid[by][bx + 1] = "R" # Ripe red
    grid[by + 1][bx] = "R"
    grid[by + 1][bx + 1] = "Q" # Shadow
    if airborne:
        # Outline around airborne berry
        for dx, dy in ((-1,0),(2,0),(0,-1),(1,-1),(0,2),(1,2),(-1,-1),(2,-1),(-1,2),(2,2)):
            ox, oy = bx + dx, by + dy
            if 0 <= ox < W and 0 <= oy < H and grid[oy][ox] == ".":
                grid[oy][ox] = "#"

def outline_enclosing(grid):
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def smooth_apex(grid):
    for y in range(1, 30):
        for x in range(2, W - 2):
            if grid[y][x] == "#" and grid[y - 1][x] == "." and grid[y][x - 1] == "." and grid[y][x + 1] == ".":
                if grid[y + 1][x - 1] == "#" or grid[y + 1][x + 1] == "#":
                    grid[y][x - 1] = "#"
                    grid[y][x + 1] = "#"

def build_dense_bush(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buf = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Clusters: 4 lush overlapping foliage clusters with diameter 10-14px!
    # Cluster 0: Center-Back (cx, cy, rx, ry, z, skew)
    # Cluster 1: Left Cluster (diam ~12-13px)
    # Cluster 2: Right Cluster (diam ~12-13px)
    # Cluster 3: Top-Apex Cluster (diam ~13-14px)
    # Lower clusters sit at cy = 29..30, so foliage extends down to y=35..36!
    # This hugs the mound and roots, creating a true dense, lush bush!
    
    if frame_idx == 0:
        # Frame 1 (Rest): Natural static canopy, perfectly balanced
        clusters = [
            (24, 28, 6.0, 5.0, 1, 0.0), # Center-Back
            (16, 29, 6.2, 5.5, 2, 0.0), # Left Cluster (diam 12.4 x 11.0)
            (32, 29, 6.2, 5.5, 2, 0.0), # Right Cluster (diam 12.4 x 11.0)
            (24, 20, 6.8, 5.8, 3, 0.0), # Top-Apex Cluster (diam 13.6 x 11.6)
        ]
        berries = [
            (13, 29, False), # on left cluster
            (23, 18, False), # jumping berry (nestled on top cluster)
            (34, 28, False), # on right cluster
            (27, 32, False), # on lower cluster
        ]
        
    elif frame_idx == 1:
        # Frame 2 (Wind Push): Gió thổi từ trái, cụm lá bên TRÁI bị đẩy ép nghiêng sang phải trước tiên
        clusters = [
            (26, 28, 6.0, 5.0, 1, 0.15),
            (20, 29, 5.0, 5.8, 2, 0.20), # Left cluster squashed horizontally (rx 6.2->5.0) & pushed right (16->20)
            (34, 29, 6.2, 5.5, 2, 0.15), # Right cluster nudged slightly (32->34)
            (26, 20, 6.8, 5.8, 3, 0.25), # Top cluster starts leaning right (24->26)
        ]
        berries = [
            (17, 29, False), # Left berry pushed right
            (25, 16, False), # Top berry agitated, lifting up
            (36, 28, False), # Right berry pushed right
            (29, 32, False),
        ]
        
    elif frame_idx == 2:
        # Frame 3 (Full Sway): Toàn bộ cụm lá dạt hẳn sang PHẢI, ngọn vươn dài theo chiều gió, 1 quả mọng nảy nhẹ lên!
        clusters = [
            (28, 28, 6.5, 4.8, 1, 0.30),
            (22, 29, 5.5, 5.2, 2, 0.30), # Left cluster swept right
            (37, 29, 6.5, 5.5, 2, 0.25), # Right cluster swept far right (32->37)
            (29, 19, 7.8, 5.0, 3, 0.45), # Top cluster stretched horizontally (rx 6.8->7.8) and wind-sheared right!
        ]
        berries = [
            (19, 29, False),
            (29, 11, True),  # BOUNCES UPWARD into the air above the top canopy! (nảy nhẹ lên 3px)
            (39, 28, False), # Swept far right
            (32, 32, False),
        ]
        
    else:
        # Frame 4 (Rebound): Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái rồi về lại vị trí cân bằng
        clusters = [
            (22, 28, 6.0, 5.0, 1, -0.15),
            (14, 28, 6.2, 5.5, 2, -0.15), # Left cluster overshoots left (16->14)
            (30, 28, 6.2, 5.5, 2, -0.15), # Right cluster overshoots left (32->30)
            (22, 20, 6.8, 5.8, 3, -0.20), # Top cluster overshoots left (24->22)
        ]
        berries = [
            (11, 28, False),
            (21, 18, False), # Settled back down onto top cluster
            (32, 27, False),
            (25, 32, False),
        ]
        
    # Render clusters in Z-order
    for cx, cy, rx, ry, z, sk in clusters:
        draw_cluster_stamp(grid, cx, cy, rx, ry, z, z_buf, sk)
        
    # Crease under top cluster
    top = clusters[3]
    draw_crease(grid, top[0], top[1], top[2], top[3], z_buf, top[4], top[5])
    
    # Berries
    for bx, by, airborne in berries:
        draw_berry(grid, bx, by, airborne)
        
    outline_enclosing(grid)
    smooth_apex(grid)
    outline_enclosing(grid)
    
    return grid

dense_frames = [build_dense_bush(i) for i in range(4)]

# Check naked pixels
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

for i, fr in enumerate(dense_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Sway statistics
for i, fr in enumerate(dense_frames):
    leaf_xs = [x for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    leaf_ys = [y for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    mean_x = sum(leaf_xs) / len(leaf_xs) if leaf_xs else 0
    print(f"Frame {i+1}: Canopy Mean X = {mean_x:.1f} (span X: {min(leaf_xs)}..{max(leaf_xs)}), span Y: {min(leaf_ys)}..{max(leaf_ys)}")

# Render images
gif_frames = []
for idx, fr in enumerate(dense_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/dense_bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/dense_bush_sheet.png")

gif_frames[0].save(
    "python/dense_bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered dense_bush_sheet.png and dense_bush_anim.gif successfully!")
