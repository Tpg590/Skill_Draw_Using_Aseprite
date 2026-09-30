import os
from PIL import Image

W, H = 32, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (20, 10, 16, 130),     # Soft ground shadow (Alpha 130)
    "#": (24, 6, 10, 255),      # Terraria near-black outline (#18060a)
    
    # Crimson Wax (Terraria chunky crimson candle)
    "A": (232, 56, 56, 255),    # Wax highlight (#e83838)
    "B": (170, 24, 40, 255),    # Wax midtone (#aa1828)
    "C": (102, 10, 24, 255),    # Wax shadow (#660a18)
    "D": (56, 4, 12, 255),      # Wax deep crevice (#38040c)
    
    # Flame & OSL
    "W": (255, 255, 255, 255),  # Flame white core (#ffffff)
    "Y": (255, 232, 80, 255),   # Flame bright yellow (#ffe850)
    "O": (248, 120, 24, 255),   # Flame vibrant orange (#f87818)
    "R": (200, 32, 16, 255),    # Flame outer red (#c82010)
    "G": (255, 190, 64, 255),   # OSL golden molten wax rim (#ffbe40)
    "K": (20, 8, 10, 255),      # Charred wick (#14080a)
    
    # Metal Plate (Aged Brass / Pewter)
    "M": (216, 184, 120, 255),  # Metal highlight (#d8b878)
    "N": (152, 120, 64, 255),   # Metal midtone (#987840)
    "P": (88, 64, 32, 255),     # Metal shadow (#584020)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_metal_plate_and_shadow(grid):
    # 1. Soft Ground Shadow S (Alpha 130) on table surface: Y = 44..46
    shadow_spans = {
        44: 12, # X = 4..28
        45: 10, # X = 6..26
        46: 6,  # X = 10..22
    }
    for y, span in shadow_spans.items():
        for x in range(16 - span, 16 + span + 1):
            if 0 <= x < W:
                grid[y][x] = "S"

    # 2. Metal Plate: Y = 40..44, X = 4..27
    for x in range(4, 10):
        grid[40][x] = "#"
    for x in range(22, 28):
        grid[40][x] = "#"
        
    grid[41][4] = "#"; grid[41][27] = "#"
    for x in range(5, 27):
        grid[41][x] = "M" if x < 16 else "N"
        
    grid[42][4] = "#"; grid[42][27] = "#"
    grid[42][5] = "M"; grid[42][6] = "M"
    for x in range(7, 25):
        grid[42][x] = "N" if x < 18 else "P"
    grid[42][25] = "P"; grid[42][26] = "#"
    
    grid[43][5] = "#"; grid[43][26] = "#"
    for x in range(6, 26):
        grid[43][x] = "P" if x > 14 else "N"
    for x in range(6, 26):
        grid[44][x] = "#"

def draw_candle_body(grid):
    for y in range(22, 42):
        grid[y][9] = "#"
        grid[y][22] = "#"
        
    for y in range(23, 42):
        grid[y][10] = "A"
        grid[y][11] = "A" if y % 3 != 0 else "B"
        grid[y][12] = "B"
        for x in range(13, 17):
            grid[y][x] = "B"
        grid[y][17] = "C" if (y // 2) % 2 == 0 else "B"
        grid[y][18] = "C"
        grid[y][19] = "C"
        grid[y][20] = "D"
        grid[y][21] = "D"

    for x in range(10, 22):
        grid[41][x] = "#"

    # Molten wax cup / top rim: Y = 20..22
    for x in range(10, 22):
        grid[22][x] = "A" if x < 15 else "B"
    grid[22][9] = "#"; grid[22][22] = "#"
    
    grid[21][9] = "#"
    grid[21][10] = "A"
    for x in range(11, 18):
        grid[21][x] = "G"
    grid[21][18] = "A"
    grid[21][19] = "B"
    grid[21][20] = "C"
    grid[21][21] = "D"
    grid[21][22] = "#"
    
    for x in range(10, 22):
        grid[20][x] = "#"
    for x in range(12, 19):
        grid[20][x] = "G" if x in (14, 15, 16) else "A"
    for x in range(11, 21):
        if x != 15:
            grid[19][x] = "#"

    # Wick: X = 15, Y = 17..20
    grid[20][15] = "K"
    grid[19][15] = "K"
    grid[18][15] = "K"
    grid[17][15] = "O"
    grid[18][14] = "#"; grid[18][16] = "#"
    grid[19][14] = "#"; grid[19][16] = "#"

def draw_flame(grid, f_idx):
    if f_idx == 0:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[12][15] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][14] = "Y"; grid[13][16] = "Y"
        grid[12][14] = "Y"; grid[12][16] = "Y"; grid[11][15] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][13] = "O"; grid[12][17] = "O"; grid[11][14] = "O"; grid[11][16] = "O"
        grid[10][15] = "O"; grid[9][15] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[11][13] = "R"; grid[11][17] = "R"; grid[10][14] = "R"; grid[10][16] = "R"
        grid[8][15] = "R"; grid[7][15] = "R"
        
    elif f_idx == 1:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[13][16] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][14] = "Y"; grid[12][15] = "Y"; grid[12][16] = "Y"
        grid[11][16] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][14] = "O"; grid[12][17] = "O"; grid[11][15] = "O"; grid[10][16] = "O"; grid[9][16] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[10][15] = "R"; grid[10][17] = "R"; grid[8][16] = "R"; grid[7][16] = "R"
        
    elif f_idx == 2:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[12][15] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][14] = "Y"; grid[13][16] = "Y"
        grid[12][14] = "Y"; grid[12][16] = "Y"; grid[11][15] = "Y"; grid[10][15] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][13] = "O"; grid[12][17] = "O"; grid[10][14] = "O"; grid[10][16] = "O"
        grid[9][15] = "O"; grid[8][15] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[11][13] = "R"; grid[11][17] = "R"; grid[7][15] = "R"; grid[6][15] = "R"
        grid[4][16] = "Y"
        
    elif f_idx == 3:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[13][14] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][16] = "Y"; grid[12][14] = "Y"; grid[12][15] = "Y"
        grid[11][14] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][13] = "O"; grid[12][16] = "O"; grid[11][15] = "O"; grid[10][14] = "O"; grid[9][14] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[10][13] = "R"; grid[10][15] = "R"; grid[8][14] = "R"; grid[7][14] = "R"
        
    elif f_idx == 4:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[13][16] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][14] = "Y"; grid[12][15] = "Y"; grid[12][16] = "Y"
        grid[11][16] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][14] = "O"; grid[12][17] = "O"; grid[11][15] = "O"; grid[10][16] = "O"; grid[9][16] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[10][15] = "R"; grid[10][17] = "R"; grid[8][16] = "R"; grid[7][16] = "R"
        grid[5][15] = "O"
        
    elif f_idx == 5:
        grid[14][15] = "W"; grid[13][15] = "W"; grid[12][15] = "W"; grid[15][15] = "W"
        grid[14][14] = "Y"; grid[14][16] = "Y"; grid[13][14] = "Y"; grid[13][16] = "Y"
        grid[12][14] = "Y"; grid[12][16] = "Y"; grid[11][15] = "Y"
        grid[15][14] = "O"; grid[15][16] = "O"; grid[13][13] = "O"; grid[13][17] = "O"
        grid[12][13] = "O"; grid[12][17] = "O"; grid[11][14] = "O"; grid[11][16] = "O"
        grid[10][15] = "O"; grid[9][15] = "O"
        grid[16][14] = "R"; grid[16][16] = "R"; grid[14][13] = "R"; grid[14][17] = "R"
        grid[11][13] = "R"; grid[11][17] = "R"; grid[10][14] = "R"; grid[10][16] = "R"
        grid[8][15] = "R"; grid[7][15] = "R"

def draw_dripping_wax(grid, f_idx):
    if f_idx == 0:
        grid[20][22] = "#"; grid[20][23] = "#"
        grid[21][22] = "A"; grid[21][23] = "G"; grid[21][24] = "#"
        grid[22][22] = "A"; grid[22][23] = "B"; grid[22][24] = "C"; grid[22][25] = "#"
        grid[23][22] = "B"; grid[23][23] = "B"; grid[23][24] = "C"; grid[23][25] = "#"
        grid[24][22] = "B"; grid[24][23] = "C"; grid[24][24] = "#"
        grid[25][22] = "#"; grid[25][23] = "#"
        
    elif f_idx == 1:
        for y in range(22, 28):
            grid[y][22] = "B"
            grid[y][23] = "#"
        grid[28][22] = "A"; grid[28][23] = "B"; grid[28][24] = "#"
        grid[29][22] = "A"; grid[29][23] = "B"; grid[29][24] = "C"; grid[29][25] = "#"
        grid[30][22] = "B"; grid[30][23] = "B"; grid[30][24] = "C"; grid[30][25] = "#"
        grid[31][22] = "C"; grid[31][23] = "C"; grid[31][24] = "#"
        grid[32][22] = "#"; grid[32][23] = "#"
        
    elif f_idx == 2:
        grid[32][22] = "B"; grid[32][23] = "#"
        grid[33][22] = "B"; grid[33][23] = "#"
        grid[34][22] = "A"; grid[34][23] = "B"; grid[34][24] = "#"
        grid[35][22] = "A"; grid[35][23] = "B"; grid[35][24] = "C"; grid[35][25] = "#"
        grid[36][22] = "A"; grid[36][23] = "B"; grid[36][24] = "C"; grid[36][25] = "#"
        grid[37][22] = "B"; grid[37][23] = "B"; grid[37][24] = "C"; grid[37][25] = "#"
        grid[38][22] = "#"; grid[38][23] = "C"; grid[38][24] = "#"
        grid[39][23] = "#"
        
    elif f_idx == 3:
        # Frame 4: CỰC KHÓ (Đứt giọt - Detachment)
        for y in range(34, 42):
            grid[y][22] = "#"
            
        grid[34][21] = "B"
        grid[35][21] = "C"
        
        # Transparent air gap at X = 23 (separating candle wall at X=22 from falling drop at X=24..26)
        for y in range(35, 40):
            grid[y][23] = "."
            
        # Free-falling detached droplet in mid-air: Y = 36..39, X = 24..26
        grid[36][25] = "#"
        grid[37][24] = "#"; grid[37][25] = "A"; grid[37][26] = "#"
        grid[38][24] = "#"; grid[38][25] = "B"; grid[38][26] = "#"
        grid[39][24] = "#"; grid[39][25] = "#"; grid[39][26] = "#"
        
        # Plate rim at Y=40 is outline '#'
        for x in range(22, 28):
            grid[40][x] = "#"
            
    elif f_idx == 4:
        # Frame 5: Impact & Squash on metal plate: Y = 41..42, X = 20..26
        grid[40][22] = "#"; grid[40][23] = "#"; grid[40][24] = "#"; grid[40][25] = "#"
        grid[41][20] = "#"; grid[41][21] = "A"; grid[41][22] = "A"; grid[41][23] = "B"; grid[41][24] = "B"; grid[41][25] = "C"; grid[41][26] = "#"
        grid[42][20] = "#"; grid[42][21] = "B"; grid[42][22] = "B"; grid[42][23] = "C"; grid[42][24] = "C"; grid[42][25] = "#"
        grid[43][21] = "#"; grid[43][22] = "#"; grid[43][23] = "#"; grid[43][24] = "#"
        
    elif f_idx == 5:
        # Frame 6: Cooled wax puddle + new bead nucleating
        grid[41][21] = "#"; grid[41][22] = "B"; grid[41][23] = "B"; grid[41][24] = "C"; grid[41][25] = "#"
        grid[42][21] = "#"; grid[42][22] = "C"; grid[42][23] = "C"; grid[42][24] = "D"; grid[42][25] = "#"
        grid[43][22] = "#"; grid[43][23] = "#"; grid[43][24] = "#"
        
        grid[20][22] = "#"
        grid[21][22] = "G"; grid[21][23] = "#"
        grid[22][22] = "A"; grid[22][23] = "B"; grid[22][24] = "#"
        grid[23][22] = "#"; grid[23][23] = "#"

def check_naked_solid(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "W", "Y", "O", "R"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

def build_full_frame(f_idx):
    grid = empty_grid()
    draw_metal_plate_and_shadow(grid)
    draw_candle_body(grid)
    draw_flame(grid, f_idx)
    draw_dripping_wax(grid, f_idx)
    return grid

frames = [build_full_frame(i) for i in range(6)]

print("\n=== VALIDATION CHECKS (SOLID ONLY) ===")
for i, fr in enumerate(frames):
    naked = check_naked_solid(fr)
    print(f"Frame {i+1}: naked solid pixels = {len(naked)}")
    if naked:
        print("  Sample naked:", naked[:5])

# Frame 4 Detachment Check:
f4 = frames[3]
gap_col = [f4[y][23] for y in range(35, 40)]
drop_pixels = [(x, y, f4[y][x]) for y in range(36, 40) for x in range(24, 27) if f4[y][x] not in (".",)]
print(f"\nFrame 4 Air Gap (X=23, Y=35..39): {gap_col}")
print(f"Frame 4 Detached Drop Pixels count: {len(drop_pixels)}")

# Render images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/candle_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 6, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/candle_sheet.png")

gif_frames[0].save(
    "python/candle_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("Rendered candle_sheet.png and candle_anim.gif successfully.")
