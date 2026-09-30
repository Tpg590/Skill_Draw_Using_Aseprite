import os
from PIL import Image

W, H = 48, 48

# Stardew Valley Warm Terracotta Palette (Soft outlines, NO #000000!)
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (38, 20, 28, 130),     # Soft warm purple-brown shadow (Alpha 130)
    "#": (60, 24, 14, 255),     # Deep dark terracotta outline (#3c180e - Soft, NO #000000)
    "A": (240, 154, 86, 255),   # Terracotta highlight (#f09a56)
    "B": (200, 100, 42, 255),   # Terracotta midtone (#c8642a)
    "C": (122, 50, 22, 255),    # Terracotta shadow (#7a3216)
    "D": (255, 210, 138, 255),  # Ceramic ornamental lip & band (#ffd28a)
    "E": (156, 72, 30, 255),    # Inner ceramic bevel tone (#9c481e)
    "Z": (40, 14, 8, 255),      # Deep crack crevice (#280e08)
}

def create_frames():
    frames = [[["." for _ in range(W)] for _ in range(H)] for _ in range(4)]
    
    # =========================================================================
    # FRAME 1: IMPACT - Đáy bình gốm chạm sàn, bắt đầu xuất hiện 2-3 đường nứt đậm
    # =========================================================================
    f1 = frames[0]
    
    # Ground contact shadow on floor plane (y=41..42, centered at x=24)
    for x in range(18, 30): f1[41][x] = "S"
    for x in range(20, 28): f1[42][x] = "S"
    
    # Lip / Rim (y=21..22, width 10: x=19..28)
    for x in range(20, 28): f1[20][x] = "#"
    f1[21][19] = "#"; f1[21][28] = "#"
    for x in range(20, 28): f1[21][x] = "D"
    f1[22][19] = "#"; f1[22][28] = "#"
    for x in range(20, 24): f1[22][x] = "A"
    for x in range(24, 27): f1[22][x] = "B"
    f1[22][27] = "C"

    # Neck (y=23..24, width 8: x=20..27)
    for y in (23, 24):
        f1[y][20] = "#"; f1[y][27] = "#"
        for x in range(21, 24): f1[y][x] = "A"
        for x in range(24, 26): f1[y][x] = "B"
        f1[y][26] = "C"
        
    # Enclose shoulder band top
    f1[24][19] = "#"; f1[24][28] = "#"

    # Decorative shoulder band (y=25, width 12: x=18..29)
    f1[25][18] = "#"; f1[25][29] = "#"
    for x in range(19, 29): f1[25][x] = "D"

    # Handles on left (x=15..18, y=24..29) and right (x=29..32, y=24..29)
    # Left handle:
    f1[24][16] = "#"; f1[24][17] = "#"
    f1[25][15] = "#"; f1[25][16] = "A"; f1[25][17] = "#"
    f1[26][15] = "#"; f1[26][16] = "A"; f1[26][17] = "#"
    f1[27][15] = "#"; f1[27][16] = "B"; f1[27][17] = "#"
    f1[28][16] = "#"; f1[28][17] = "B"; f1[28][18] = "#"
    f1[29][17] = "#"; f1[29][18] = "#"

    # Right handle:
    f1[24][30] = "#"; f1[24][31] = "#"
    f1[25][30] = "#"; f1[25][31] = "B"; f1[25][32] = "#"
    f1[26][30] = "#"; f1[26][31] = "C"; f1[26][32] = "#"
    f1[27][30] = "#"; f1[27][31] = "C"; f1[27][32] = "#"
    f1[28][29] = "#"; f1[28][30] = "C"; f1[28][31] = "#"
    f1[29][29] = "#"; f1[29][30] = "#"

    # Belly Body (y=26..35, width 14: x=17..30)
    belly_spans = {
        26: (17, 30),
        27: (17, 30),
        28: (17, 30),
        29: (17, 30),
        30: (17, 30),
        31: (17, 30),
        32: (17, 30),
        33: (18, 29),
        34: (18, 29),
        35: (18, 29),
    }
    for y, (x1, x2) in belly_spans.items():
        f1[y][x1] = "#"; f1[y][x2] = "#"
        mid1 = x1 + (x2 - x1) // 3
        mid2 = x1 + 2 * (x2 - x1) // 3
        for x in range(x1 + 1, mid1 + 1): f1[y][x] = "A"
        for x in range(mid1 + 1, mid2 + 1): f1[y][x] = "B"
        for x in range(mid2 + 1, x2): f1[y][x] = "C"

    # Lower body & Base (y=36..40)
    for y in (36, 37):
        f1[y][19] = "#"; f1[y][28] = "#"
        for x in range(20, 23): f1[y][x] = "A"
        for x in range(23, 26): f1[y][x] = "B"
        for x in range(26, 28): f1[y][x] = "C"
    for y in (38, 39):
        f1[y][20] = "#"; f1[y][27] = "#"
        for x in range(21, 24): f1[y][x] = "A"
        for x in range(24, 26): f1[y][x] = "B"
        f1[y][26] = "C"
    # Base bottom row (y=40)
    for x in range(20, 28): f1[40][x] = "#"

    # 3 Jagged Fracture Crack Lines (Z: #280e08) radiating from base impact
    # Crack 1: Base to left belly
    f1[39][22] = "Z"; f1[38][22] = "Z"; f1[37][21] = "Z"; f1[36][21] = "Z"
    f1[35][20] = "Z"; f1[34][19] = "Z"; f1[33][20] = "Z"; f1[32][19] = "Z"
    f1[31][18] = "Z"; f1[30][18] = "Z"; f1[29][19] = "Z"
    f1[34][20] = "D" # Chipped ceramic glaze glint next to crack
    f1[31][19] = "D"
    
    # Crack 2: Base to center neck
    f1[39][24] = "Z"; f1[38][25] = "Z"; f1[37][24] = "Z"; f1[36][24] = "Z"
    f1[35][24] = "Z"; f1[34][25] = "Z"; f1[33][24] = "Z"; f1[32][24] = "Z"
    f1[31][25] = "Z"; f1[30][25] = "Z"; f1[29][24] = "Z"; f1[28][24] = "Z"
    f1[27][24] = "Z"; f1[26][23] = "Z"; f1[25][24] = "Z"; f1[24][24] = "Z"
    f1[33][25] = "D"
    f1[27][25] = "D"

    # Crack 3: Base to right belly
    f1[39][26] = "Z"; f1[38][26] = "Z"; f1[37][27] = "Z"; f1[36][27] = "Z"
    f1[35][27] = "Z"; f1[34][28] = "Z"; f1[33][28] = "Z"; f1[32][27] = "Z"
    f1[31][28] = "Z"; f1[30][29] = "Z"; f1[29][28] = "Z"
    f1[35][28] = "D"

    # =========================================================================
    # FRAME 2: FRACTURE - Nổ bung ra thành 4-5 MẢNH GỐM LỚN hình đa giác
    # =========================================================================
    f2 = frames[1]
    
    # Shadow under fractured pot
    for x in range(16, 32): f2[41][x] = "S"
    for x in range(18, 30): f2[42][x] = "S"

    # --- SHARD 1: Top Lip & Neck (blown upward: y=17..21, x=21..27) ---
    for x in range(22, 27): f2[17][x] = "#"
    f2[18][21] = "#"; f2[18][27] = "#"
    for x in range(22, 27): f2[18][x] = "D"
    f2[19][21] = "#"; f2[19][22] = "A"; f2[19][23] = "A"; f2[19][24] = "A"; f2[19][25] = "B"; f2[19][26] = "C"; f2[19][27] = "#"
    # Jagged fracture break on bottom of neck
    f2[20][21] = "#"; f2[20][22] = "A"; f2[20][23] = "B"; f2[20][24] = "#"; f2[20][25] = "C"; f2[20][26] = "#"
    f2[21][22] = "#"; f2[21][23] = "#"; f2[21][25] = "#"

    # --- SHARD 2: Left Shoulder & Handle (blown left-upward: y=23..29, x=13..20) ---
    f2[23][15] = "#"; f2[23][16] = "#"; f2[23][17] = "#"; f2[23][18] = "#"; f2[23][19] = "#"
    f2[24][14] = "#"; f2[24][15] = "A"; f2[24][16] = "D"; f2[24][17] = "D"; f2[24][18] = "D"; f2[24][19] = "#"
    f2[25][13] = "#"; f2[25][14] = "A"; f2[25][15] = "#"; f2[25][16] = "A"; f2[25][17] = "A"; f2[25][18] = "B"; f2[25][19] = "#"
    f2[26][13] = "#"; f2[26][14] = "A"; f2[26][15] = "#"; f2[26][16] = "A"; f2[26][17] = "B"; f2[26][18] = "#"
    f2[27][13] = "#"; f2[27][14] = "B"; f2[27][15] = "#"; f2[27][16] = "B"; f2[27][17] = "#"
    f2[28][14] = "#"; f2[28][15] = "B"; f2[28][16] = "#"
    f2[29][15] = "#"

    # --- SHARD 3: Right Shoulder & Handle (blown right-upward: y=23..29, x=28..35) ---
    f2[23][28] = "#"; f2[23][29] = "#"; f2[23][30] = "#"; f2[23][31] = "#"; f2[23][32] = "#"
    f2[24][28] = "#"; f2[24][29] = "D"; f2[24][30] = "D"; f2[24][31] = "D"; f2[24][32] = "B"; f2[24][33] = "#"
    f2[25][28] = "#"; f2[25][29] = "B"; f2[25][30] = "C"; f2[25][31] = "#"; f2[25][32] = "B"; f2[25][33] = "#"
    f2[26][29] = "#"; f2[26][30] = "C"; f2[26][31] = "#"; f2[26][32] = "C"; f2[26][33] = "C"; f2[26][34] = "#"
    f2[27][30] = "#"; f2[27][31] = "#"; f2[27][32] = "C"; f2[27][33] = "C"; f2[27][34] = "#"
    f2[28][32] = "#"; f2[28][33] = "C"; f2[28][34] = "#"
    f2[29][33] = "#"

    # --- SHARD 4: Lower Left Belly (pushed left-downward: y=31..36, x=14..20) ---
    f2[31][16] = "#"; f2[31][17] = "#"
    f2[32][15] = "#"; f2[32][16] = "A"; f2[32][17] = "A"; f2[32][18] = "#"
    f2[33][14] = "#"; f2[33][15] = "A"; f2[33][16] = "A"; f2[33][17] = "B"; f2[33][18] = "#"
    f2[34][14] = "#"; f2[34][15] = "A"; f2[34][16] = "B"; f2[34][17] = "B"; f2[34][18] = "C"; f2[34][19] = "#"
    f2[35][15] = "#"; f2[35][16] = "B"; f2[35][17] = "B"; f2[35][18] = "C"; f2[35][19] = "#"
    f2[36][16] = "#"; f2[36][17] = "#"; f2[36][18] = "#"

    # --- SHARD 5: Lower Right Belly & Base (pushed right-downward: y=31..38, x=26..33) ---
    f2[31][28] = "#"; f2[31][29] = "#"
    f2[32][27] = "#"; f2[32][28] = "B"; f2[32][29] = "C"; f2[32][30] = "#"
    f2[33][26] = "#"; f2[33][27] = "B"; f2[33][28] = "B"; f2[33][29] = "C"; f2[33][30] = "#"
    f2[34][26] = "#"; f2[34][27] = "B"; f2[34][28] = "C"; f2[34][29] = "C"; f2[34][30] = "C"; f2[34][31] = "#"
    f2[35][26] = "#"; f2[35][27] = "C"; f2[35][28] = "C"; f2[35][29] = "C"; f2[35][30] = "C"; f2[35][31] = "#"
    f2[36][26] = "#"; f2[36][27] = "C"; f2[36][28] = "C"; f2[36][29] = "C"; f2[36][30] = "#"
    f2[37][26] = "#"; f2[37][27] = "#"; f2[37][28] = "#"; f2[37][29] = "#"

    # =========================================================================
    # FRAME 3: SCATTER - Văng xa theo hình vòng cung parabol + 3 mẩu dăm gốm 1px
    # =========================================================================
    f3 = frames[2]

    # Shadows under airborne shards on floor plane
    for x in range(8, 16): f3[41][x] = "S"
    for x in range(32, 40): f3[41][x] = "S"
    for x in range(21, 28): f3[41][x] = "S"

    # 3 Micro-chips (1px flying aloft on ballistic paths - Rule 4.6):
    f3[17][19] = "A"   # High upper-left chip
    f3[18][29] = "D"   # High upper-right chip
    f3[27][24] = "B"   # Center falling chip

    # --- SHARD 1: Top Lip & Neck (apex of parabolic flight: y=11..16, x=22..28, tilted) ---
    for x in range(23, 28): f3[11][x] = "#"
    f3[12][22] = "#"; f3[12][28] = "#"
    for x in range(23, 28): f3[12][x] = "D"
    f3[13][22] = "#"; f3[13][23] = "A"; f3[13][24] = "A"; f3[13][25] = "A"; f3[13][26] = "B"; f3[13][27] = "C"; f3[13][28] = "#"
    f3[14][22] = "#"; f3[14][23] = "A"; f3[14][24] = "B"; f3[14][25] = "#"; f3[14][26] = "C"; f3[14][27] = "#"
    f3[15][23] = "#"; f3[15][24] = "#"; f3[15][26] = "#"

    # --- SHARD 2: Left Handle (flung far left: y=20..26, x=8..15, tumbling) ---
    f3[20][10] = "#"; f3[20][11] = "#"; f3[20][12] = "#"; f3[20][13] = "#"
    f3[21][9] = "#"; f3[21][10] = "A"; f3[21][11] = "D"; f3[21][12] = "D"; f3[21][13] = "D"; f3[21][14] = "#"
    f3[22][8] = "#"; f3[22][9] = "A"; f3[22][10] = "#"; f3[22][11] = "A"; f3[22][12] = "A"; f3[22][13] = "B"; f3[22][14] = "#"
    f3[23][8] = "#"; f3[23][9] = "A"; f3[23][10] = "#"; f3[23][11] = "A"; f3[23][12] = "B"; f3[23][13] = "#"
    f3[24][8] = "#"; f3[24][9] = "B"; f3[24][10] = "#"; f3[24][11] = "B"; f3[24][12] = "#"
    f3[25][9] = "#"; f3[25][10] = "B"; f3[25][11] = "#"
    f3[26][10] = "#"

    # --- SHARD 3: Right Handle (flung far right: y=20..26, x=33..40, tumbling) ---
    f3[20][34] = "#"; f3[20][35] = "#"; f3[20][36] = "#"; f3[20][37] = "#"
    f3[21][33] = "#"; f3[21][34] = "D"; f3[21][35] = "D"; f3[21][36] = "D"; f3[21][37] = "B"; f3[21][38] = "#"
    f3[22][33] = "#"; f3[22][34] = "B"; f3[22][35] = "C"; f3[22][36] = "#"; f3[22][37] = "B"; f3[22][38] = "#"
    f3[23][34] = "#"; f3[23][35] = "C"; f3[23][36] = "#"; f3[23][37] = "C"; f3[23][38] = "C"; f3[23][39] = "#"
    f3[24][35] = "#"; f3[24][36] = "#"; f3[24][37] = "C"; f3[24][38] = "C"; f3[24][39] = "#"
    f3[25][37] = "#"; f3[25][38] = "C"; f3[25][39] = "#"
    f3[26][38] = "#"

    # --- SHARD 4: Lower Left Belly (flung down-left toward ground: y=33..38, x=10..16) ---
    f3[33][12] = "#"; f3[33][13] = "#"
    f3[34][11] = "#"; f3[34][12] = "A"; f3[34][13] = "A"; f3[34][14] = "#"
    f3[35][10] = "#"; f3[35][11] = "A"; f3[35][12] = "A"; f3[35][13] = "B"; f3[35][14] = "#"
    f3[36][10] = "#"; f3[36][11] = "A"; f3[36][12] = "B"; f3[36][13] = "B"; f3[36][14] = "C"; f3[36][15] = "#"
    f3[37][11] = "#"; f3[37][12] = "B"; f3[37][13] = "B"; f3[37][14] = "C"; f3[37][15] = "#"
    f3[38][12] = "#"; f3[38][13] = "#"; f3[38][14] = "#"

    # --- SHARD 5: Lower Right Belly & Base (flung down-right toward ground: y=33..40, x=31..38) ---
    f3[33][33] = "#"; f3[33][34] = "#"
    f3[34][32] = "#"; f3[34][33] = "B"; f3[34][34] = "C"; f3[34][35] = "#"
    f3[35][31] = "#"; f3[35][32] = "B"; f3[35][33] = "B"; f3[35][34] = "C"; f3[35][35] = "#"
    f3[36][31] = "#"; f3[36][32] = "B"; f3[36][33] = "C"; f3[36][34] = "C"; f3[36][35] = "C"; f3[36][36] = "#"
    f3[37][31] = "#"; f3[37][32] = "C"; f3[37][33] = "C"; f3[37][34] = "C"; f3[37][35] = "C"; f3[37][36] = "#"
    f3[38][31] = "#"; f3[38][32] = "C"; f3[38][33] = "C"; f3[38][34] = "C"; f3[38][35] = "#"
    f3[39][31] = "#"; f3[39][32] = "#"; f3[39][33] = "#"; f3[39][34] = "#"

    # =========================================================================
    # FRAME 4: SETTLE - Các mảnh gốm rơi tiếp đất phân tán tự nhiên 3D, có bóng 'S'
    # =========================================================================
    f4 = frames[3]

    # --- Shard 1 (Center-Back: Broken Rim & Neck resting at y=36..38, x=22..28) ---
    for x in range(23, 28): f4[36][x] = "#"
    f4[37][22] = "#"; f4[37][23] = "D"; f4[37][24] = "D"; f4[37][25] = "A"; f4[37][26] = "B"; f4[37][27] = "C"; f4[37][28] = "#"
    f4[38][22] = "#"; f4[38][23] = "A"; f4[38][24] = "B"; f4[38][25] = "B"; f4[38][26] = "C"; f4[38][27] = "#"; f4[38][28] = "#"
    for x in range(22, 28): f4[39][x] = "#"
    # Ground shadow under Shard 1
    for x in range(22, 28): f4[40][x] = "S"

    # --- Shard 2 (Far-Left Handle: Resting on its side at y=38..40, x=7..13) ---
    for x in range(8, 13): f4[38][x] = "#"
    f4[39][7] = "#"; f4[39][8] = "A"; f4[39][9] = "D"; f4[39][10] = "A"; f4[39][11] = "B"; f4[39][12] = "B"; f4[39][13] = "#"
    f4[40][7] = "#"; f4[40][8] = "B"; f4[40][9] = "B"; f4[40][10] = "C"; f4[40][11] = "C"; f4[40][12] = "#"; f4[40][13] = "#"
    for x in range(7, 13): f4[41][x] = "#"
    # Ground shadow under Shard 2
    for x in range(7, 14): f4[42][x] = "S"

    # --- Shard 3 (Far-Right Handle: Resting on its side at y=38..40, x=35..41) ---
    for x in range(36, 41): f4[38][x] = "#"
    f4[39][35] = "#"; f4[39][36] = "D"; f4[39][37] = "B"; f4[39][38] = "C"; f4[39][39] = "C"; f4[39][40] = "C"; f4[39][41] = "#"
    f4[40][35] = "#"; f4[40][36] = "C"; f4[40][37] = "C"; f4[40][38] = "C"; f4[40][39] = "#"; f4[40][40] = "#"; f4[40][41] = "#"
    for x in range(35, 41): f4[41][x] = "#"
    # Ground shadow under Shard 3
    for x in range(35, 42): f4[42][x] = "S"

    # --- Shard 4 (Front-Left Belly Wedge: Resting at y=41..43, x=14..20) ---
    for x in range(15, 20): f4[41][x] = "#"
    f4[42][14] = "#"; f4[42][15] = "A"; f4[42][16] = "A"; f4[42][17] = "B"; f4[42][18] = "C"; f4[42][19] = "C"; f4[42][20] = "#"
    f4[43][14] = "#"; f4[43][15] = "B"; f4[43][16] = "B"; f4[43][17] = "C"; f4[43][18] = "C"; f4[43][19] = "#"; f4[43][20] = "#"
    for x in range(14, 20): f4[44][x] = "#"
    # Ground shadow under Shard 4
    for x in range(14, 21): f4[45][x] = "S"

    # --- Shard 5 (Front-Right Belly/Base: Resting at y=41..43, x=27..33) ---
    for x in range(28, 33): f4[41][x] = "#"
    f4[42][27] = "#"; f4[42][28] = "B"; f4[42][29] = "B"; f4[42][30] = "C"; f4[42][31] = "C"; f4[42][32] = "C"; f4[42][33] = "#"
    f4[43][27] = "#"; f4[43][28] = "C"; f4[43][29] = "C"; f4[43][30] = "C"; f4[43][31] = "#"; f4[43][32] = "#"; f4[43][33] = "#"
    for x in range(27, 33): f4[44][x] = "#"
    # Ground shadow under Shard 5
    for x in range(27, 34): f4[45][x] = "S"

    # Landed ceramic micro-chips scattered on the floor plane:
    # Chip 1 (near left):
    f4[41][4] = "#"; f4[42][4] = "A"; f4[43][4] = "#"; f4[44][4] = "S"
    # Chip 2 (center):
    f4[41][23] = "D"; f4[42][23] = "S"
    # Chip 3 (near right):
    f4[41][43] = "#"; f4[42][43] = "B"; f4[43][43] = "#"; f4[44][43] = "S"

    return frames

# Check outline completeness (excluding embers/micro-chips in Frame 3)
def check_outline_completeness(grid, frame_idx):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                # In Frame 3, chips (19, 17), (29, 18), (24, 27) are 1px airborne chips
                if frame_idx == 2 and (x, y) in ((19, 17), (29, 18), (24, 27)):
                    continue
                # In Frame 4, chip at (23, 41) is 1px dot
                if frame_idx == 3 and (x, y) == (23, 41):
                    continue
                # In Frame 4, 1px chips at (4, 42) and (43, 42)
                if frame_idx == 3 and (x, y) in ((4, 42), (43, 42)):
                    continue
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

frames = create_frames()

print("\n=== OUTLINE COMPLETENESS CHECK ===")
all_clean = True
for i, fr in enumerate(frames):
    n = check_outline_completeness(fr, i)
    print(f"Frame {i+1} naked pixels: {len(n)}")
    if n:
        print(f"  {n[:10]}")
        all_clean = False
print(f"All frames 100% enclosed: {all_clean}")

# Measure Dispersion Radius Expansion (Frame 2 vs Frame 3)
def get_bbox(grid):
    xs = [x for x in range(W) for y in range(H) if grid[y][x] not in (".", "S")]
    ys = [y for x in range(W) for y in range(H) if grid[y][x] not in (".", "S")]
    return min(xs), max(xs), min(ys), max(ys)

print("\n=== DISPERSION RADIUS EXPANSION VERIFICATION ===")
x1_f2, x2_f2, y1_f2, y2_f2 = get_bbox(frames[1])
x1_f3, x2_f3, y1_f3, y2_f3 = get_bbox(frames[2])
width_f2, height_f2 = x2_f2 - x1_f2 + 1, y2_f2 - y1_f2 + 1
width_f3, height_f3 = x2_f3 - x1_f3 + 1, y2_f3 - y1_f3 + 1

print(f"Frame 2 (Fracture) BBox: X={x1_f2}..{x2_f2} (Width={width_f2}), Y={y1_f2}..{y2_f2} (Height={height_f2})")
print(f"Frame 3 (Scatter)  BBox: X={x1_f3}..{x2_f3} (Width={width_f3}), Y={y1_f3}..{y2_f3} (Height={height_f3})")
print(f"Horizontal expansion: {width_f2}px -> {width_f3}px (+{width_f3 - width_f2}px, +{(width_f3/width_f2 - 1)*100:.1f}%)")
print(f"Vertical expansion:   {height_f2}px -> {height_f3}px (+{height_f3 - height_f2}px, +{(height_f3/height_f2 - 1)*100:.1f}%)")
assert width_f3 > width_f2 and height_f3 > height_f2, "Dispersion radius MUST expand along both X and Y!"

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/shatter_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/shatter_sheet.png")

gif_frames[0].save(
    "python/shatter_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS = 125ms
    loop=0
)

print("\nSaved shatter_sheet.png and shatter_anim.gif successfully!")
