import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Palette with Hue-Shifting
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 24, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 26, 36, 255),     # Clean dark navy-pine outline (#0c1a24)
    
    # Foliage Hue-Shifting (Lemon-Lime -> Vibrant Green -> Cool Teal -> Navy Crevice)
    "A": (214, 245, 66, 255),   # Sunny lemon-lime highlight (#d6f542)
    "B": (96, 207, 50, 255),    # Vibrant warm green (#60cf32)
    "C": (38, 142, 60, 255),    # Primary lush leaf green (#268e3c)
    "D": (18, 76, 68, 255),     # Cool deep teal shadow (#124c44)
    "E": (10, 38, 50, 255),     # Deep navy-green crevice shadow (#0a2632)
    
    # Woody Trunk & Branches
    "T": (130, 84, 48, 255),    # Wood trunk midtone (#825430)
    "U": (72, 42, 24, 255),     # Wood trunk shadow (#482a18)
    
    # Red Berries
    "P": (255, 120, 140, 255),  # Berry glint (#ff788c)
    "R": (218, 32, 58, 255),    # Berry ripe crimson (#da203a)
    "Q": (116, 14, 34, 255),    # Berry shadow (#740e22)
    
    # Earth Mound
    "L": (156, 104, 64, 255),   # Soil crest highlight (#9c6840)
    "M": (106, 66, 38, 255),    # Soil body midtone (#6a4226)
    "N": (56, 32, 18, 255),     # Soil under-shadow (#382012)
}

def create_base_ground(grid):
    # Soft ground shadow S (y=42..44)
    for x in range(11, 37): grid[42][x] = "S"
    for x in range(13, 35): grid[43][x] = "S"
    for x in range(16, 32): grid[44][x] = "S"

    # Small soil mound (mô đất nhỏ: y=38..42)
    mound_spans = {
        38: (19, 29),
        39: (16, 32),
        40: (14, 34),
        41: (15, 33),
        42: (17, 31)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            if y == 38:
                grid[y][x] = "L"
            elif y <= 40:
                grid[y][x] = "M"
            else:
                grid[y][x] = "N"
            
    # Bottom mound outline at y=43
    for x in range(17, 32): grid[43][x] = "#"
    # Top mound outline at y=37
    for x in range(19, 30): grid[37][x] = "#"

    # Little moss patches on soil mound
    grid[38][18] = "B"; grid[38][19] = "B"
    grid[38][29] = "B"; grid[38][30] = "B"
    grid[39][15] = "C"; grid[39][16] = "C"
    grid[39][32] = "C"; grid[39][33] = "C"

def draw_fixed_trunk(grid):
    # Gnarly short trunk and root base rooted on the mound (y=32..38)
    # Root flare
    grid[38][21] = "#"; grid[38][22] = "T"; grid[38][23] = "T"
    grid[38][24] = "U"; grid[38][25] = "U"; grid[38][26] = "#"
    
    for y in range(33, 38):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "U"
        grid[y][25] = "#"
        
    # Left branch reaching to left cluster
    grid[31][18] = "#"; grid[31][19] = "T"; grid[31][20] = "#"
    grid[32][19] = "#"; grid[32][20] = "T"; grid[32][21] = "#"
    grid[33][21] = "T"; grid[33][22] = "T"
    
    # Right branch reaching to right cluster
    grid[31][27] = "#"; grid[31][28] = "U"; grid[31][29] = "#"
    grid[32][26] = "#"; grid[32][27] = "U"; grid[32][28] = "#"
    grid[33][25] = "U"; grid[33][26] = "U"

def draw_cluster_stamp(grid, cx, cy, rx, ry, z_layer, z_buffer, skew=0.0):
    # Cluster diameter = 2*rx = 8..14px (rx = 4..7)
    # Volumetric 3D sphere lighting with top-left directional light
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
                    
                    # Directional light from Upper-Left (-0.5, -0.6, 0.62)
                    intensity = -0.5 * nx - 0.6 * ny + 0.62 * nz
                    
                    if intensity > 0.78:
                        c = "A" # Sunny lemon-lime highlight
                    elif intensity > 0.38:
                        c = "B" # Warm light green
                    elif intensity > -0.15:
                        c = "C" # Primary lush green
                    elif intensity > -0.50:
                        c = "D" # Deep cool teal
                    else:
                        c = "E" # Deepest navy crevice
                        
                    # Rim under-shadow
                    if ny > 0.40 and nx > -0.25:
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
            if 0.82 <= d2 <= 1.15 and ny > 0.32:
                if z_buffer[y][x] < current_z and grid[y][x] not in (".", "S"):
                    grid[y][x] = "#"

def draw_berry(grid, bx, by, airborne=False):
    # 2x2 berry
    grid[by][bx] = "P"     # Glint
    grid[by][bx + 1] = "R" # Red
    grid[by + 1][bx] = "R"
    grid[by + 1][bx + 1] = "Q" # Dark red shadow
    if airborne:
        # Crisp outline around airborne berry
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

def build_bush(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buf = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Clusters: 3-4 clusters with diameter 8-14px!
    # Cluster 0: Center-Back (cx, cy, rx, ry, z, skew)
    # Cluster 1: Left
    # Cluster 2: Right
    # Cluster 3: Top-Apex
    
    if frame_idx == 0:
        # Frame 1 (Rest): Natural static canopy, balanced
        # Clusters with diameter 10..13px (rx = 5.0..6.5, ry = 4.5..5.5)
        clusters = [
            (24, 25, 5.5, 4.5, 1, 0.0), # Center-Back
            (17, 26, 6.0, 5.2, 2, 0.0), # Left cluster (diam ~12px)
            (31, 26, 6.0, 5.2, 2, 0.0), # Right cluster (diam ~12px)
            (24, 18, 6.5, 5.5, 3, 0.0), # Top-Apex cluster (diam ~13px)
        ]
        berries = [
            (14, 26, False), # Left cluster
            (24, 16, False), # Top bouncing berry (resting on top cluster)
            (33, 25, False), # Right cluster
            (27, 29, False), # Lower cluster
        ]
        
    elif frame_idx == 1:
        # Frame 2 (Wind Push): Gió thổi từ trái, cụm lá bên TRÁI bị đẩy ép nghiêng sang phải trước tiên
        clusters = [
            (25, 25, 5.5, 4.5, 1, 0.15),
            (20, 26, 4.8, 5.5, 2, 0.20), # Left cluster squashed horizontally (rx: 6.0->4.8) & pushed right (17->20)
            (33, 26, 6.0, 5.2, 2, 0.15), # Right cluster nudged slightly (31->33)
            (26, 18, 6.5, 5.5, 3, 0.25), # Top cluster begins tilting right (24->26)
        ]
        berries = [
            (18, 26, False),
            (26, 14, False), # Top berry agitated, lifting up
            (35, 25, False),
            (29, 29, False),
        ]
        
    elif frame_idx == 2:
        # Frame 3 (Full Sway): Toàn bộ cụm dạt sang PHẢI, ngọn vươn dài theo chiều gió, 1 quả mọng nảy nhẹ lên!
        clusters = [
            (27, 25, 6.0, 4.2, 1, 0.3),
            (22, 26, 5.2, 5.0, 2, 0.3), # Left cluster swept right
            (36, 26, 6.5, 5.2, 2, 0.25),# Right cluster swept far right (31->36)
            (29, 17, 7.5, 4.5, 3, 0.45),# Top cluster elongated (rx: 6.5->7.5, ry: 5.5->4.5) & wind-sheared right!
        ]
        berries = [
            (20, 26, False),
            (29, 10, True),  # BOUNCES UPWARD into the air above the top canopy!
            (38, 25, False),
            (31, 29, False),
        ]
        
    else:
        # Frame 4 (Rebound): Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái rồi về lại vị trí cân bằng
        clusters = [
            (22, 25, 5.5, 4.5, 1, -0.15),
            (15, 25, 6.0, 5.2, 2, -0.15), # Left cluster overshoots left (17->15)
            (29, 25, 6.0, 5.2, 2, -0.15), # Right cluster overshoots left (31->29)
            (22, 18, 6.5, 5.5, 3, -0.20), # Top cluster overshoots left (24->22)
        ]
        berries = [
            (12, 25, False),
            (22, 16, False), # Settled back down onto top cluster
            (30, 24, False),
            (25, 29, False),
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

bush_frames = [build_bush(i) for i in range(4)]

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

for i, fr in enumerate(bush_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Sway statistics
for i, fr in enumerate(bush_frames):
    leaf_xs = [x for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    leaf_ys = [y for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    mean_x = sum(leaf_xs) / len(leaf_xs) if leaf_xs else 0
    print(f"Frame {i+1}: Canopy Mean X = {mean_x:.1f} (span: {min(leaf_xs)}..{max(leaf_xs)}), Y span: {min(leaf_ys)}..{max(leaf_ys)}")

# Render images
gif_frames = []
for idx, fr in enumerate(bush_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/sculpt_bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/sculpt_bush_sheet.png")

gif_frames[0].save(
    "python/sculpt_bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered sculpt_bush_sheet.png and sculpt_bush_anim.gif")
