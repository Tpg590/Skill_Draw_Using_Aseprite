import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 24, 32, 130),     # Ground shadow (Alpha 130)
    "#": (12, 26, 36, 255),     # Clean dark navy-pine outline (#0c1a24)
    
    # Foliage Hue-Shifting: Lemon-Lime -> Vibrant Green -> Cool Teal -> Deep Navy
    "A": (214, 245, 66, 255),   # Sunny lemon-lime highlight (#d6f542)
    "B": (96, 207, 50, 255),    # Vibrant warm leaf green (#60cf32)
    "C": (38, 142, 60, 255),    # Primary lush green (#268e3c)
    "D": (18, 76, 68, 255),     # Deep cool teal-green shadow (#124c44)
    "E": (10, 38, 50, 255),     # Deep navy-green crevice shadow (#0a2632)
    
    # Woody Trunk & Branches
    "T": (130, 84, 48, 255),    # Wood trunk midtone (#825430)
    "U": (72, 42, 24, 255),     # Wood trunk shadow (#482a18)
    
    # Red Berries
    "P": (255, 120, 140, 255),  # Berry glint highlight (#ff788c)
    "R": (218, 32, 58, 255),    # Berry ripe crimson (#da203a)
    "Q": (116, 14, 34, 255),    # Berry shadow (#740e22)
    
    # Earth Mound (Organic rounded dome, strictly NO dithering)
    "L": (156, 104, 64, 255),   # Earth crest highlight (#9c6840)
    "M": (106, 66, 38, 255),    # Earth body midtone (#6a4226)
    "N": (56, 32, 18, 255),     # Earth under-shadow (#382012)
}

def create_base_ground(grid):
    # 1. Ground contact shadow S (y=42..44, soft ellipse)
    for x in range(10, 38): grid[42][x] = "S"
    for x in range(12, 36): grid[43][x] = "S"
    for x in range(15, 33): grid[44][x] = "S"

    # 2. Organic rounded soil mound (mô đất nhỏ: dome shape)
    # y=37: x=21..27 (crest)
    # y=38: x=18..30
    # y=39: x=15..33
    # y=40: x=13..35
    # y=41: x=12..36
    # y=42: x=14..34
    mound_spans = {
        37: (21, 27),
        38: (18, 30),
        39: (15, 33),
        40: (13, 35),
        41: (12, 36),
        42: (14, 34)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            if y == 37 or y == 38:
                grid[y][x] = "L"
            elif y <= 40:
                grid[y][x] = "M"
            else:
                grid[y][x] = "N"
                
    # Bottom mound outline at y=43
    for x in range(14, 35): grid[43][x] = "#"
    # Top crest outline at y=36
    for x in range(21, 28): grid[36][x] = "#"

    # Moss & grass blades on mound flanks
    grid[37][18] = "#"; grid[37][19] = "B"
    grid[37][29] = "B"; grid[37][30] = "#"
    grid[38][14] = "#"; grid[38][15] = "C"
    grid[38][33] = "C"; grid[38][34] = "#"

def draw_fixed_trunk(grid):
    # Short gnarly bush root base & branching forks (y=33..38)
    # Roots spreading into mound
    grid[37][20] = "#"; grid[37][21] = "T"; grid[37][22] = "T"
    grid[37][25] = "U"; grid[37][26] = "U"; grid[37][27] = "#"
    
    # Gnarly short trunk
    for y in range(34, 38):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "U"
        grid[y][25] = "#"
        
    # Low branch forks
    grid[33][19] = "#"; grid[33][20] = "T"; grid[33][21] = "#"
    grid[34][20] = "T"; grid[34][21] = "T"
    
    grid[33][26] = "#"; grid[33][27] = "U"; grid[33][28] = "#"
    grid[34][25] = "U"; grid[34][26] = "U"

def get_cluster_boundary(nx, ny, angle_offset=0.0):
    # Organic scalloped leaf lobes
    angle = math.atan2(ny, nx) + angle_offset
    # 4-lobe harmonic with secondary 6-lobe modulation
    lobe = 1.0 + 0.12 * math.cos(4 * angle) + 0.08 * math.sin(3 * angle)
    return lobe

def draw_scalloped_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer, skew=0.0, angle_offset=0.0):
    x_min = max(1, int(cx - rx * 1.25 - abs(skew)*ry - 2))
    x_max = min(W - 2, int(cx + rx * 1.25 + abs(skew)*ry + 2))
    y_min = max(1, int(cy - ry * 1.25 - 1))
    y_max = min(H - 2, int(cy + ry * 1.25 + 1))
    
    for y in range(y_min, y_max + 1):
        dx_skew = skew * (cy - y)
        cur_cx = cx + dx_skew
        for x in range(x_min, x_max + 1):
            nx = (x - cur_cx) / rx
            ny = (y - cy) / ry
            d = math.sqrt(nx*nx + ny*ny)
            lobe = get_cluster_boundary(nx, ny, angle_offset)
            
            # Scaled distance relative to organic lobe boundary
            d_norm = d / lobe
            if d_norm <= 1.0:
                if z_layer >= z_buffer[y][x]:
                    z_buffer[y][x] = z_layer
                    
                    # 3D spherical surface normal
                    d2_clamped = min(1.0, d_norm * d_norm)
                    nz = math.sqrt(1.0 - d2_clamped)
                    
                    # Directional light from Upper-Left (-0.50, -0.60, 0.62)
                    intensity = -0.50 * (nx / lobe) - 0.60 * (ny / lobe) + 0.62 * nz
                    
                    # Shading thresholds
                    if intensity > 0.65:
                        c = "A" # Sunny lemon-lime highlight
                    elif intensity > 0.28:
                        c = "B" # Warm vibrant green
                    elif intensity > -0.22:
                        c = "C" # Primary lush leaf green
                    elif intensity > -0.55:
                        c = "D" # Deep cool teal
                    else:
                        c = "E" # Deep navy-green crevice
                        
                    # Bottom-right rim shadow reinforcement
                    if ny > 0.35 and nx > -0.2:
                        c = "E" if c in ("C", "D") else c
                        
                    grid[y][x] = c

def draw_scalloped_crease(grid, cx, cy, rx, ry, z_buffer, current_z, skew=0.0, angle_offset=0.0):
    x_min = max(1, int(cx - rx * 1.25 - abs(skew)*ry - 2))
    x_max = min(W - 2, int(cx + rx * 1.25 + abs(skew)*ry + 2))
    y_min = max(1, int(cy - ry * 1.25 - 1))
    y_max = min(H - 2, int(cy + ry * 1.25 + 1))
    
    for y in range(y_min, y_max + 1):
        dx_skew = skew * (cy - y)
        cur_cx = cx + dx_skew
        for x in range(x_min, x_max + 1):
            nx = (x - cur_cx) / rx
            ny = (y - cy) / ry
            d = math.sqrt(nx*nx + ny*ny)
            lobe = get_cluster_boundary(nx, ny, angle_offset)
            d_norm = d / lobe
            if 0.82 <= d_norm <= 1.15 and ny > 0.28:
                if z_buffer[y][x] < current_z and grid[y][x] not in (".", "S"):
                    grid[y][x] = "#"

def draw_berry(grid, bx, by, airborne=False):
    grid[by][bx] = "P"     # Glint
    grid[by][bx + 1] = "R" # Crimson red
    grid[by + 1][bx] = "R"
    grid[by + 1][bx + 1] = "Q" # Dark shadow
    if airborne:
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

def build_organic_bush(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buf = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Clusters: 4 distinct organic spherical clusters with diameter 10-14px!
    if frame_idx == 0:
        # Frame 1 (Rest): Natural static canopy, perfectly balanced
        clusters = [
            (24, 27, 5.5, 4.5, 1, 0.0, 0.0), # Center-Back
            (16, 28, 5.8, 5.2, 2, 0.0, 0.4), # Left Cluster (diam ~12px)
            (32, 28, 5.8, 5.2, 2, 0.0, 0.8), # Right Cluster (diam ~12px)
            (24, 19, 6.5, 5.5, 3, 0.0, 0.2), # Top-Apex Cluster (diam ~13px)
        ]
        berries = [
            (13, 28, False), # left cluster
            (23, 17, False), # jumping berry nestled on top cluster
            (34, 27, False), # right cluster
            (27, 31, False), # lower center
        ]
        
    elif frame_idx == 1:
        # Frame 2 (Wind Push): Gió thổi từ trái, cụm lá bên TRÁI bị đẩy ép nghiêng sang phải trước tiên
        clusters = [
            (26, 27, 5.5, 4.5, 1, 0.15, 0.0),
            (20, 28, 4.8, 5.5, 2, 0.20, 0.5), # Left squashed horizontally (rx: 5.8->4.8) & pushed right (16->20)
            (34, 28, 5.8, 5.2, 2, 0.15, 0.8), # Right nudged slightly (32->34)
            (26, 19, 6.5, 5.5, 3, 0.25, 0.3), # Top begins tilting right (24->26)
        ]
        berries = [
            (17, 28, False),
            (25, 15, False), # Jumper agitated, lifting up
            (36, 27, False),
            (29, 31, False),
        ]
        
    elif frame_idx == 2:
        # Frame 3 (Full Sway): Toàn bộ cụm lá dạt sang PHẢI, ngọn vươn dài theo chiều gió, 1 quả mọng nảy nhẹ lên!
        clusters = [
            (28, 27, 6.0, 4.2, 1, 0.30, 0.0),
            (22, 28, 5.2, 5.0, 2, 0.30, 0.6), # Left cluster swept right
            (37, 28, 6.2, 5.2, 2, 0.25, 0.9), # Right cluster swept far right (32->37)
            (29, 18, 7.5, 4.6, 3, 0.45, 0.4), # Top cluster elongated horizontally and wind-sheared right!
        ]
        berries = [
            (19, 28, False),
            (29, 10, True),  # BOUNCES UPWARD into the air above the top canopy!
            (39, 27, False), # Swept far right
            (32, 31, False),
        ]
        
    else:
        # Frame 4 (Rebound): Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái rồi về lại vị trí cân bằng
        clusters = [
            (22, 27, 5.5, 4.5, 1, -0.15, 0.0),
            (14, 27, 5.8, 5.2, 2, -0.15, 0.3), # Left cluster overshoots left (16->14)
            (30, 27, 5.8, 5.2, 2, -0.15, 0.7), # Right cluster overshoots left (32->30)
            (22, 19, 6.5, 5.5, 3, -0.20, 0.1), # Top cluster overshoots left (24->22)
        ]
        berries = [
            (11, 27, False),
            (21, 17, False), # Settled back down onto top cluster
            (32, 26, False),
            (25, 31, False),
        ]
        
    # Render clusters in Z-order
    for cx, cy, rx, ry, z, sk, ao in clusters:
        draw_scalloped_cluster(grid, cx, cy, rx, ry, z, z_buf, sk, ao)
        
    # Crease under top cluster
    top = clusters[3]
    draw_scalloped_crease(grid, top[0], top[1], top[2], top[3], z_buf, top[4], top[5], top[6])
    
    # Berries
    for bx, by, airborne in berries:
        draw_berry(grid, bx, by, airborne)
        
    outline_enclosing(grid)
    smooth_apex(grid)
    outline_enclosing(grid)
    
    return grid

organic_frames = [build_organic_bush(i) for i in range(4)]

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

for i, fr in enumerate(organic_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Render images
gif_frames = []
for idx, fr in enumerate(organic_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/organic_bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/organic_bush_sheet.png")

gif_frames[0].save(
    "python/organic_bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered organic_bush_sheet.png and organic_bush_anim.gif successfully!")
