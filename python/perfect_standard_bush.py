import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 24, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (12, 26, 36, 255),     # Clean dark navy-pine outline (#0c1a24)
    
    # Foliage Hue-Shifting (Lemon-Lime -> Vibrant Green -> Cool Teal -> Navy Crevice)
    "A": (214, 245, 66, 255),   # Sunny lemon-lime highlight (#d6f542)
    "B": (96, 207, 50, 255),    # Vibrant light foliage green (#60cf32)
    "C": (38, 142, 60, 255),    # Primary lush leaf green (#268e3c)
    "D": (18, 76, 68, 255),     # Deep cool teal-green shadow (#124c44)
    "E": (10, 38, 50, 255),     # Deep navy-green crevice shadow (#0a2632)
    
    # Woody Trunk & Branches
    "T": (130, 84, 48, 255),    # Wood trunk midtone (#825430)
    "U": (72, 42, 24, 255),     # Wood trunk shadow (#482a18)
    
    # Red Berries
    "P": (255, 120, 140, 255),  # Berry glint highlight (#ff788c)
    "R": (218, 32, 58, 255),    # Berry ripe crimson (#da203a)
    "Q": (116, 14, 34, 255),    # Berry deep shadow (#740e22)
    
    # Earth Mound (Mô đất nhỏ: organic dome, strictly NO dithering)
    "L": (156, 104, 64, 255),   # Soil crest highlight (#9c6840)
    "M": (106, 66, 38, 255),    # Soil body midtone (#6a4226)
    "N": (56, 32, 18, 255),     # Soil under-shadow (#382012)
}

def create_base_ground(grid):
    # 1. Ground contact shadow S (y=42..44, soft ellipse)
    for x in range(11, 37): grid[42][x] = "S"
    for x in range(13, 35): grid[43][x] = "S"
    for x in range(16, 32): grid[44][x] = "S"

    # 2. Organic rounded soil mound (mô đất nhỏ: y=38..42)
    mound_spans = {
        38: (19, 29),
        39: (16, 32),
        40: (14, 34),
        41: (13, 35),
        42: (15, 33)
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
    for x in range(15, 34): grid[43][x] = "#"
    # Top mound outline at y=37
    for x in range(19, 30): grid[37][x] = "#"

    # Moss & grass blades on soil mound
    grid[38][17] = "#"; grid[38][18] = "B"
    grid[38][30] = "B"; grid[38][31] = "#"
    grid[39][14] = "#"; grid[39][15] = "C"
    grid[39][33] = "C"; grid[39][34] = "#"

def draw_fixed_trunk(grid):
    # Short gnarly bush trunk & roots rooted on the mound (y=32..38)
    # Root base spreading into soil
    grid[38][21] = "#"; grid[38][22] = "T"; grid[38][23] = "T"
    grid[38][24] = "U"; grid[38][25] = "U"; grid[38][26] = "#"
    
    # Gnarly short trunk
    for y in range(33, 38):
        grid[y][22] = "#"
        grid[y][23] = "T"
        grid[y][24] = "U"
        grid[y][25] = "#"
        
    # Left & right branch stubs reaching out
    grid[32][19] = "#"; grid[32][20] = "T"; grid[32][21] = "#"
    grid[33][20] = "T"; grid[33][21] = "T"
    
    grid[32][26] = "#"; grid[32][27] = "U"; grid[32][28] = "#"
    grid[33][25] = "U"; grid[33][26] = "U"

def draw_round_cluster(grid, cx, cy, rx, ry, z_layer, z_buffer, skew=0.0):
    # Cluster diameter = 2*rx is strictly 8..14px (rx = 4.0..7.0, ry = 3.5..6.0)
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
                    
                    if intensity > 0.72:
                        c = "A" # Sunny lemon-lime highlight (đỉnh cụm ngả vàng)
                    elif intensity > 0.32:
                        c = "B" # Vibrant light foliage green
                    elif intensity > -0.20:
                        c = "C" # Primary lush green
                    elif intensity > -0.52:
                        c = "D" # Deep cool teal
                    else:
                        c = "E" # Deepest navy-green crevice (đáy cụm viền xanh tối)
                        
                    # Bottom-right rim shadow reinforcement
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
    grid[by][bx] = "P"     # Glint
    grid[by][bx + 1] = "R" # Crimson red
    grid[by + 1][bx] = "R"
    grid[by + 1][bx + 1] = "Q" # Dark red shadow
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

def build_bush_frame(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    z_buf = [[0 for _ in range(W)] for _ in range(H)]
    
    # 1. Base ground and trunk are 100% FIXED
    create_base_ground(grid)
    draw_fixed_trunk(grid)
    
    # 2. Clusters: 4 distinct round spherical clusters with diameter strictly 8-14px!
    # Cluster 0: Center-Back (cx, cy, rx, ry, z, skew)
    # Cluster 1: Left Cluster (diam = 2*rx = 11.6px)
    # Cluster 2: Right Cluster (diam = 2*rx = 11.6px)
    # Cluster 3: Top-Apex Cluster (diam = 2*rx = 12.8px)
    
    if frame_idx == 0:
        # Frame 1 (Rest): Natural static canopy, balanced
        clusters = [
            (24, 27, 5.0, 4.2, 1, 0.0), # Center-Back (diam 10.0 x 8.4)
            (17, 27, 5.8, 5.2, 2, 0.0), # Left Cluster (diam 11.6 x 10.4)
            (31, 27, 5.8, 5.2, 2, 0.0), # Right Cluster (diam 11.6 x 10.4)
            (24, 19, 6.4, 5.4, 3, 0.0), # Top-Apex Cluster (diam 12.8 x 10.8)
        ]
        berries = [
            (14, 27, False), # left cluster berry
            (24, 17, False), # top bouncing berry (resting on top cluster)
            (33, 26, False), # right cluster berry
            (27, 30, False), # lower center berry
        ]
        
    elif frame_idx == 1:
        # Frame 2 (Wind Push): Gió thổi, cụm lá bên TRÁI bị đẩy ép nghiêng sang phải trước tiên
        clusters = [
            (25, 27, 5.0, 4.2, 1, 0.15),
            (20, 27, 4.6, 5.4, 2, 0.20), # Left cluster squashed horizontally (rx: 5.8->4.6) & pushed right (17->20)
            (33, 27, 5.8, 5.2, 2, 0.15), # Right cluster nudged slightly (31->33)
            (26, 19, 6.4, 5.4, 3, 0.25), # Top cluster starts leaning right (24->26)
        ]
        berries = [
            (18, 27, False), # left berry pushed right
            (26, 15, False), # top berry agitated, lifting up slightly
            (35, 26, False), # right berry pushed right
            (29, 30, False),
        ]
        
    elif frame_idx == 2:
        # Frame 3 (Full Sway): Toàn bộ cụm dạt hẳn sang PHẢI, cụm ngọn vươn dài theo chiều gió, 1 quả mọng nảy nhẹ lên!
        clusters = [
            (27, 27, 5.5, 4.0, 1, 0.30),
            (22, 27, 5.0, 4.8, 2, 0.30), # Left cluster swept right
            (36, 27, 6.0, 5.0, 2, 0.25), # Right cluster swept far right (31->36)
            (29, 18, 7.0, 4.6, 3, 0.45), # Top cluster stretched horizontally (rx: 6.4->7.0, diam=14.0px max!)
        ]
        berries = [
            (20, 27, False),
            (29, 10, True),  # BOUNCES UPWARD into the air above the canopy! (nảy nhẹ lên 3-4px)
            (38, 26, False), # right berry swept far right
            (32, 30, False),
        ]
        
    else:
        # Frame 4 (Rebound): Gió ngừng, các cụm lá đàn hồi nảy ngược nhẹ về bên trái rồi về lại vị trí cân bằng
        clusters = [
            (22, 27, 5.0, 4.2, 1, -0.15),
            (15, 27, 5.8, 5.2, 2, -0.15), # Left cluster overshoots left (17->15)
            (29, 27, 5.8, 5.2, 2, -0.15), # Right cluster overshoots left (31->29)
            (22, 19, 6.4, 5.4, 3, -0.20), # Top cluster overshoots left (24->22)
        ]
        berries = [
            (12, 27, False),
            (22, 17, False), # Settled back down onto top cluster
            (31, 25, False),
            (25, 30, False),
        ]
        
    # Render clusters in Z-order
    for cx, cy, rx, ry, z, sk in clusters:
        draw_round_cluster(grid, cx, cy, rx, ry, z, z_buf, sk)
        
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

frames = [build_bush_frame(i) for i in range(4)]

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

# Sway statistics & diameter verification
print("\n=== DIAMETER AND SWAY VERIFICATION ===")
for i, fr in enumerate(frames):
    leaf_xs = [x for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    leaf_ys = [y for x in range(W) for y in range(H) if fr[y][x] in ("A", "B", "C", "D", "E")]
    mean_x = sum(leaf_xs) / len(leaf_xs) if leaf_xs else 0
    print(f"Frame {i+1}: Canopy Mean X = {mean_x:.1f} (X span: {min(leaf_xs)}..{max(leaf_xs)}, Y span: {min(leaf_ys)}..{max(leaf_ys)})")

# Render images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/standard_bush_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/standard_bush_sheet.png")

gif_frames[0].save(
    "python/standard_bush_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered standard_bush_sheet.png and standard_bush_anim.gif successfully!")
