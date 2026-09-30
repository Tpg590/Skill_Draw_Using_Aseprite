import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (26, 22, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (40, 16, 8, 255),      # Clean dark brown/copper outline (#281008)
    
    # Ornate Gold Frame (Hue-shifting gold -> orange -> burnt sienna)
    "A": (255, 240, 144, 255),  # Specular gold highlight (#fff090)
    "B": (255, 204, 48, 255),   # Radiant gold midtone (#ffcc30)
    "C": (216, 120, 16, 255),   # Warm orange/amber shadow (#d87810)
    "D": (128, 56, 16, 255),    # Deep copper/crevice shadow (#803810)
    
    # Golden Sand Particles & Flow
    "G": (255, 230, 80, 255),   # Glowing sand highlight (#ffe650)
    "F": (240, 168, 32, 255),   # Sand grain midtone (#f0a820)
    "O": (184, 104, 16, 255),   # Sand grain shadow (#b86810)
    
    # Clear Glass & Reflection Glints
    "W": (255, 255, 255, 255),  # Pure white glint (#ffffff)
    "L": (224, 244, 255, 220),  # Glass reflection tint (#e0f4ff)
    "T": (160, 200, 224, 160),  # Glass shaded rim (#a0c8e0)
    
    # Ancient Stone Dais / Plinth
    "M": (144, 152, 160, 255),  # Stone highlight (#9098a0)
    "N": (92, 100, 108, 255),   # Stone midtone (#5c646c)
    "P": (52, 56, 64, 255),     # Stone deep shadow (#343840)
}

PALETTE_HEX = {
    ".": None,
    "S": "#1a1620",
    "#": "#281008",
    "A": "#fff090",
    "B": "#ffcc30",
    "C": "#d87810",
    "D": "#803810",
    "G": "#ffe650",
    "F": "#f0a820",
    "O": "#b86810",
    "W": "#ffffff",
    "L": "#e0f4ff",
    "T": "#a0c8e0",
    "M": "#9098a0",
    "N": "#5c646c",
    "P": "#343840",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_stone_dais(grid):
    # Ground shadow S (Y = 42..44, X = 10..38)
    for y in (42, 43, 44):
        x_min = 12 if y == 42 else (10 if y == 43 else 14)
        x_max = 36 if y == 42 else (38 if y == 43 else 34)
        for x in range(x_min, x_max + 1):
            grid[y][x] = "S"

    # Dais Top outline: Y = 36, X = 13..35
    for x in range(13, 36):
        grid[36][x] = "#"
        
    # Dais Top surface: Y = 37, X = 12..36
    grid[37][12] = "#"; grid[37][36] = "#"
    for x in range(13, 36):
        grid[37][x] = "M" if (x % 4 in (1, 2)) else "N"
        
    # Dais Front slab: Y = 38..40, X = 11..37
    for y in (38, 39, 40):
        grid[y][11] = "#"; grid[y][37] = "#"
        for x in range(12, 37):
            if y == 38:
                grid[y][x] = "M" if x % 5 in (1, 2) else "N"
            elif y == 39:
                grid[y][x] = "N" if x % 3 != 0 else "P"
            else:
                grid[y][x] = "P"
                
    # Dais Bottom outline: Y = 41, X = 11..37
    for x in range(11, 38):
        grid[41][x] = "#"

def get_base_hourglass():
    hg = {}
    
    # 1. Top Finial
    hg[(24, 7)] = "A"
    hg[(23, 8)] = "A"; hg[(24, 8)] = "B"; hg[(25, 8)] = "C"
    
    # 2. Top Golden Cap Plate (Y = 9..11, X = 16..32)
    for x in range(17, 32):
        hg[(x, 9)] = "A" if x % 2 == 0 else "B"
    for x in range(16, 33):
        hg[(x, 10)] = "B" if x <= 24 else "C"
    for x in range(17, 32):
        hg[(x, 11)] = "C" if x <= 22 else "D"
        
    # 3. Bottom Golden Cap Plate (Y = 33..36, X = 16..32)
    for x in range(17, 32):
        hg[(x, 33)] = "A" if x <= 22 else "B"
    for x in range(16, 33):
        hg[(x, 34)] = "B" if x <= 24 else "C"
    for x in range(16, 33):
        hg[(x, 35)] = "C" if x <= 22 else "D"
    for x in (16, 17, 31, 32):
        hg[(x, 36)] = "D"
        
    # 4. Flanking Columns
    for y in range(12, 33):
        hg[(16, y)] = "A" if y % 4 in (0, 1) else "B"
        hg[(17, y)] = "B" if y % 4 in (0, 1) else "C"
    for y in range(12, 33):
        hg[(31, y)] = "B" if y % 4 in (0, 1) else "C"
        hg[(32, y)] = "C" if y % 4 in (0, 1) else "D"

    # 5. Glass Bulbs & Sand
    bulb_profile = {
        12: (19, 29), 13: (18, 30), 14: (18, 30), 15: (18, 30), 16: (19, 29),
        17: (19, 29), 18: (20, 28), 19: (20, 28), 20: (21, 27), 21: (22, 26),
        22: (23, 25), # Waist neck
        23: (22, 26), 24: (21, 27), 25: (20, 28), 26: (20, 28), 27: (19, 29),
        28: (19, 29), 29: (18, 30), 30: (18, 30), 31: (18, 30), 32: (19, 29),
    }
    
    for y, (xl, xr) in bulb_profile.items():
        hg[(xl, y)] = "W" if y in (14, 15, 27, 28) else "L"
        hg[(xr, y)] = "T"
        
        for x in range(xl + 1, xr):
            if 17 <= y <= 21:
                slope_w = (y - 16) * 1.0
                if 24 - slope_w <= x <= 24 + slope_w:
                    hg[(x, y)] = "G" if x <= 24 else "F"
                else:
                    hg[(x, y)] = "."
            elif 21 <= y <= 27:
                if x == 24:
                    hg[(x, y)] = "G" if y % 2 == 0 else "F"
                else:
                    hg[(x, y)] = "."
            elif 28 <= y <= 32:
                heap_w = (y - 27) * 2.2
                if 24 - heap_w <= x <= 24 + heap_w:
                    if y == 28:
                        hg[(x, y)] = "G"
                    elif x <= 23:
                        hg[(x, y)] = "G"
                    elif x <= 25:
                        hg[(x, y)] = "F"
                    else:
                        hg[(x, y)] = "O"
                else:
                    hg[(x, y)] = "."
            else:
                if y in (13, 14) and x in (21, 22):
                    hg[(x, y)] = "W"
                elif y in (15, 16) and x in (22, 23):
                    hg[(x, y)] = "L"
                else:
                    hg[(x, y)] = "."
                    
    return hg

base_hg = get_base_hourglass()

def render_frame_1():
    grid = empty_grid()
    draw_stone_dais(grid)
    
    for (x, y), c in base_hg.items():
        if c != ".":
            grid[y][x] = c
            
    for (x, y), c in base_hg.items():
        if c != ".":
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                    grid[ny][nx] = "#"
                    
    return grid

def render_frame_2():
    grid = empty_grid()
    draw_stone_dais(grid)
    
    eroded_hg = {}
    for (x, y), c in base_hg.items():
        if x >= 19 and c != ".":
            if x == 19 and y % 3 == 0:
                continue
            eroded_hg[(x, y)] = c
            
    for (x, y), c in eroded_hg.items():
        grid[y][x] = c
        
    for (x, y), c in eroded_hg.items():
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                grid[ny][nx] = "#"
                
    particles_f2 = [
        (20, 9, "G"), (22, 8, "G"), (25, 7, "F"), (27, 7, "O"), (30, 6, "O"),
        (18, 17, "G"), (20, 16, "F"), (23, 14, "G"), (27, 13, "F"), (31, 12, "O"), (35, 11, "O"),
        (18, 28, "G"), (21, 26, "F"), (24, 25, "G"), (28, 23, "F"), (33, 21, "O"), (37, 20, "F"),
        (17, 21, "W"), (22, 21, "G"), (26, 18, "F"), (29, 17, "G"),
    ]
    for px, py, pc in particles_f2:
        if 0 <= px < W and 0 <= py < H:
            grid[py][px] = pc
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                if 0 <= px+dx < W and 0 <= py+dy < H and grid[py+dy][px+dx] == ".":
                    grid[py+dy][px+dx] = "#"
                    
    return grid

def render_frame_3():
    grid = empty_grid()
    draw_stone_dais(grid)
    
    eroded_hg = {}
    for (x, y), c in base_hg.items():
        if x >= 24 and c != ".":
            if x == 24 and y % 2 == 1:
                continue
            if x == 25 and y in (15, 23, 29):
                continue
            if x == 31 and y in (19, 20):
                continue
            eroded_hg[(x, y)] = c
            
    for (x, y), c in eroded_hg.items():
        grid[y][x] = c
        
    for (x, y), c in eroded_hg.items():
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                grid[ny][nx] = "#"
                
    particles_f3 = [
        (23, 7, "G"), (26, 6, "G"), (29, 5, "F"), (32, 5, "F"), (36, 4, "O"), (39, 4, "O"),
        (24, 11, "G"), (27, 9, "G"), (30, 8, "F"), (34, 7, "F"), (38, 6, "O"), (41, 5, "O"),
        (19, 18, "G"), (21, 16, "G"), (23, 15, "G"), (26, 14, "F"), (29, 13, "F"), (33, 11, "O"), (37, 10, "O"), (40, 9, "F"),
        (20, 22, "G"), (22, 20, "G"), (25, 18, "F"), (28, 17, "F"), (32, 15, "O"), (36, 14, "O"), (40, 13, "F"), (43, 12, "O"),
        (21, 28, "G"), (23, 26, "F"), (26, 24, "F"), (30, 22, "O"), (35, 20, "O"), (39, 18, "F"), (42, 17, "O"),
        (27, 12, "W"), (31, 9, "W"), (35, 8, "G"), (38, 8, "F"), (42, 7, "O"),
    ]
    for px, py, pc in particles_f3:
        if 0 <= px < W and 0 <= py < H:
            grid[py][px] = pc
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                if 0 <= px+dx < W and 0 <= py+dy < H and grid[py+dy][px+dx] == ".":
                    grid[py+dy][px+dx] = "#"
                    
    return grid

def render_frame_4():
    grid = empty_grid()
    draw_stone_dais(grid)
    
    # Sand grains sitting directly on top surface of dais:
    grid[37][23] = "G"; grid[37][25] = "F"; grid[37][27] = "O"
    
    vortex_particles = [
        # Vortex base tail:
        (25, 27, "G"), (26, 26, "F"), (27, 25, "G"), (28, 25, "O"),
        (26, 29, "O"), (27, 28, "F"), (28, 27, "G"),
        # Vortex thick body:
        (28, 22, "G"), (29, 21, "G"), (30, 21, "W"), (31, 20, "F"),
        (29, 23, "F"), (30, 22, "G"), (31, 22, "O"), (32, 21, "F"),
        (31, 18, "G"), (32, 17, "W"), (33, 17, "G"), (34, 16, "F"), (35, 16, "O"),
        (33, 19, "F"), (34, 18, "G"), (35, 18, "O"),
        (35, 14, "G"), (36, 13, "W"), (37, 13, "G"), (38, 12, "F"), (39, 12, "O"),
        (36, 15, "F"), (37, 14, "G"), (38, 14, "O"),
        # Crest of vortex rushing out:
        (39, 10, "G"), (40, 9, "W"), (41, 9, "G"), (42, 8, "F"), (43, 8, "O"),
        (41, 11, "F"), (42, 10, "G"), (43, 10, "O"),
        (43, 6, "G"), (44, 5, "W"), (45, 5, "G"), (46, 4, "F"),
        # Floating spray particles:
        (30, 15, "G"), (34, 12, "F"), (38, 9, "G"), (42, 6, "F"), (45, 7, "O"),
        (27, 19, "O"), (32, 14, "O"), (37, 16, "F"),
    ]
    for px, py, pc in vortex_particles:
        if 0 <= px < W and 0 <= py < H:
            grid[py][px] = pc
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                if 0 <= px+dx < W and 0 <= py+dy < H and grid[py+dy][px+dx] == ".":
                    grid[py+dy][px+dx] = "#"
                    
    return grid

def render_frame_5():
    grid = empty_grid()
    draw_stone_dais(grid)
    
    trailing_specks = [
        (39, 8, "G"), (40, 7, "F"), (42, 6, "G"), (44, 5, "F"), (45, 4, "O"),
        (41, 10, "F"), (43, 9, "O"), (46, 6, "G"), (47, 5, "F"),
        (36, 12, "O"), (38, 11, "F"),
    ]
    for px, py, pc in trailing_specks:
        if 0 <= px < W and 0 <= py < H:
            grid[py][px] = pc
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                if 0 <= px+dx < W and 0 <= py+dy < H and grid[py+dy][px+dx] == ".":
                    grid[py+dy][px+dx] = "#"
                    
    return grid

def render_frame_6():
    grid = empty_grid()
    draw_stone_dais(grid)
    return grid

frames = [
    render_frame_1(),
    render_frame_2(),
    render_frame_3(),
    render_frame_4(),
    render_frame_5(),
    render_frame_6()
]

# Validation
for i, g in enumerate(frames):
    for r_idx, row in enumerate(g):
        assert len(row) == W, f"Frame {i+1} row {r_idx} len={len(row)} != {W}"

def check_naked_pixels(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

for i, g in enumerate(frames):
    n = check_naked_pixels(g)
    print(f"Frame {i+1} naked pixels: {len(n)}")

gif_frames = []
for idx, g in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/hourglass_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/hourglass_sheet.png")

gif_frames[0].save(
    "python/hourglass_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS
    loop=0
)
print("Rendered hourglass_sheet.png and hourglass_anim.gif successfully.")
