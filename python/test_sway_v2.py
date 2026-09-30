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
    
    # Earth Mound (NO DITHERING! Organic stratified earth)
    "M": (74, 48, 30, 255),     # Soil mound midtone (#4a301e)
    "N": (44, 24, 12, 255),     # Soil mound shadow (#2c180c)
}

def create_base_ground(grid):
    # Fixed Ground contact shadow S (y=42..44)
    for x in range(12, 37): grid[42][x] = "S"
    for x in range(14, 35): grid[43][x] = "S"
    for x in range(17, 31): grid[44][x] = "S"

    # Fixed Soil Mound at base (y=37..42, centered at x=24)
    # Stratified, solid shading - strictly NO checkerboard caro dithering
    mound_spans = {
        37: (20, 28),
        38: (18, 30),
        39: (16, 32),
        40: (15, 33),
        41: (15, 33),
        42: (17, 31)
    }
    for y, (x1, x2) in mound_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            # Top half is lit earth M, bottom half is dark earth N
            if y <= 39:
                grid[y][x] = "M"
            else:
                grid[y][x] = "N"
            
    # Bottom mound outline at y=43
    for x in range(17, 32): grid[43][x] = "#"
    # Top mound outline at y=36
    for x in range(20, 29): grid[36][x] = "#"

    # Little green moss patches on mound corners (solid, 2-3px)
    grid[37][19] = "B"; grid[37][20] = "B"
    grid[37][28] = "B"; grid[37][29] = "B"
    grid[38][17] = "C"; grid[38][18] = "C"
    grid[38][30] = "C"; grid[38][31] = "C"

def draw_fixed_trunk(grid):
    # Fixed woody branching trunk rooted at (24, 38)
    # Main trunk
    for y in range(30, 38):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "T"
        grid[y][25] = "U"
        grid[y][26] = "#"
        
    # Flanged root base
    grid[37][21] = "#"; grid[37][22] = "T"
    grid[37][25] = "U"; grid[37][26] = "U"; grid[37][27] = "#"
    
    # Left branch (going up-left to support left cluster)
    grid[28][18] = "#"; grid[28][19] = "T"; grid[28][20] = "#"
    grid[29][19] = "#"; grid[29][20] = "T"; grid[29][21] = "#"
    grid[30][20] = "#"; grid[30][21] = "T"
    grid[31][21] = "T"; grid[31][22] = "T"
    
    # Right branch (going up-right to support right cluster)
    grid[28][28] = "#"; grid[28][29] = "U"; grid[28][30] = "#"
    grid[29][27] = "#"; grid[29][28] = "U"; grid[29][29] = "#"
    grid[30][26] = "U"; grid[30][27] = "#"
    grid[31][25] = "U"; grid[31][26] = "U"

def draw_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer):
    # Volumetric 3D sphere lighting with top-left directional light
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
                    
                    # Light source vector: top-left (-0.45, -0.65, 0.6)
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
                        c = "E" # Deep navy-green crevice shadow
                        
                    # Bottom-right rim shadow reinforcement
                    if ny > 0.42 and nx > -0.2:
                        c = "E" if c in ("C", "D") else c
                        
                    grid[y][x] = c

def draw_cluster_crease(grid, cx, cy, rx, ry, z_buffer, current_z):
    # Dark crease boundary underneath an upper cluster
    x_min = max(1, int(cx - rx - 1))
    x_max = min(W - 2, int(cx + rx + 1))
    y_min = max(1, int(cy - ry - 1))
    y_max = min(H - 2, int(cy + ry + 1))
    
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d2 = nx*nx + ny*ny
            if 0.82 <= d2 <= 1.15 and ny > 0.32:
                if z_buffer[y][x] < current_z and grid[y][x] not in (".", "S"):
                    grid[y][x] = "#"

def draw_berry(grid, bx, by, airborne=False):
    # 2x2 berry
    if airborne:
        # If in mid-air, draw with clear border so it's a crisp distinct sprite
        # Berry core
        grid[by][bx] = "P"     # Glint
        grid[by][bx + 1] = "R" # Red
        grid[by + 1][bx] = "R"
        grid[by + 1][bx + 1] = "Q" # Shadow
        # Outline around berry
        for dx, dy in ((-1,0),(2,0),(0,-1),(1,-1),(0,2),(1,2),(-1,-1),(2,-1),(-1,2),(2,2)):
            ox, oy = bx + dx, by + dy
            if 0 <= ox < W and 0 <= oy < H and grid[oy][ox] == ".":
                grid[oy][ox] = "#"
    else:
        grid[by][bx] = "P"
        grid[by][bx + 1] = "R"
        grid[by + 1][bx] = "R"
        grid[by + 1][bx + 1] = "Q"

def outline_enclosing(grid):
    # Clean perimeter outline
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def smooth_apex_spikes(grid):
    for y in range(1, 25):
        for x in range(2, W - 2):
            if grid[y][x] == "#" and grid[y - 1][x] == "." and grid[y][x - 1] == "." and grid[y][x + 1] == ".":
                if grid[y + 1][x - 1] == "#" or grid[y + 1][x + 1] == "#":
                    grid[y][x - 1] = "#"
                    grid[y][x + 1] = "#"

def build_frame(f_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buf = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Foliage clusters and berries per frame:
    if f_idx == 0:
        # Frame 1 (Rest): Natural static canopy
        clusters = [
            (24, 25, 7.5, 6.0, 1), # Center-Back
            (16, 26, 7.5, 6.5, 2), # Lower-Left
            (32, 26, 7.5, 6.5, 2), # Lower-Right
            (24, 17, 8.5, 7.0, 3), # Top-Apex
        ]
        berries = [
            (13, 27, False), # Left cluster
            (23, 16, False), # Top jumper berry (resting)
            (34, 25, False), # Right cluster
            (27, 29, False), # Center-lower
        ]
        
    elif f_idx == 1:
        # Frame 2 (Wind Push): Gió thổi từ trái, cụm lá bên TRÁI bị đẩy ép nghiêng sang phải trước tiên
        clusters = [
            (26, 25, 7.5, 6.0, 1),
            (20, 26, 6.0, 6.5, 2), # Left cluster squashed horizontally (rx: 7.5 -> 6.0) & shoved right (16 -> 20)
            (34, 26, 7.5, 6.5, 2), # Right cluster slightly nudged (32 -> 34)
            (26, 17, 8.5, 7.0, 3), # Top cluster starts leaning right (24 -> 26)
        ]
        berries = [
            (17, 27, False), # Left berry pushed right
            (25, 14, False), # Jumper berry lifting / agitated
            (36, 25, False), # Right berry moved right
            (29, 29, False),
        ]
        
    elif f_idx == 2:
        # Frame 3 (Full Sway): Toàn bộ cụm lá dạt hẳn sang PHẢI, cụm ngọn vươn dài theo chiều gió. 1 quả mọng nảy lên.
        clusters = [
            (28, 25, 8.0, 5.5, 1),
            (22, 26, 6.5, 6.0, 2), # Left cluster swept right (revealing left branch!)
            (37, 26, 8.0, 6.5, 2), # Right cluster swept far right (32 -> 37)
            (30, 16, 10.0, 5.5, 3),# Top cluster stretched horizontally to the right! (rx=10, cy=16)
        ]
        berries = [
            (19, 26, False),
            (30, 8, True),   # AIRBORNE! Bounces upward into the air! Distinct airborne berry
            (39, 26, False), # Swept far right
            (32, 29, False),
        ]
        
    else:
        # Frame 4 (Rebound): Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái rồi về lại vị trí cân bằng
        clusters = [
            (22, 25, 7.5, 6.0, 1),
            (14, 25, 7.5, 6.5, 2), # Left cluster springs back past rest (16 -> 14)
            (29, 25, 7.5, 6.5, 2), # Right cluster springs back past rest (32 -> 29)
            (21, 17, 8.5, 7.0, 3), # Top cluster overshoots left (24 -> 21)
        ]
        berries = [
            (11, 26, False),
            (21, 15, False), # Settled back down onto top cluster
            (31, 24, False),
            (25, 29, False),
        ]
        
    # Render clusters in Z-order
    for cx, cy, rx, ry, z in clusters:
        draw_cluster(grid, cx, cy, rx, ry, z, z_buf)
        
    # Crease under top cluster
    top = clusters[3]
    draw_cluster_crease(grid, top[0], top[1], top[2], top[3], z_buf, top[4])
    
    # Berries
    for bx, by, airborne in berries:
        draw_berry(grid, bx, by, airborne)
        
    outline_enclosing(grid)
    smooth_apex_spikes(grid)
    outline_enclosing(grid)
    
    return grid

frames = [build_frame(i) for i in range(4)]

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

for i, fr in enumerate(frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Sway statistics
for i, fr in enumerate(frames):
    leaf_xs = [x for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    leaf_ys = [y for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    mean_x = sum(leaf_xs) / len(leaf_xs) if leaf_xs else 0
    min_x, max_x = min(leaf_xs), max(leaf_xs)
    print(f"Frame {i+1}: Mean X = {mean_x:.1f} (span: {min_x}..{max_x})")

# Render images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/sway_v2_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/sway_v2_sheet.png")

gif_frames[0].save(
    "python/sway_v2_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered sway_v2_sheet.png and sway_v2_anim.gif")
