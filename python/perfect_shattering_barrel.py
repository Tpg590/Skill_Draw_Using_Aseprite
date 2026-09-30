import os
from PIL import Image

W, H = 48, 48

# Terraria High-Contrast Oak & Iron Palette
PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (20, 10, 24, 130),     # Soft ground shadow (Alpha 130)
    "#": (22, 12, 8, 255),      # Dark woody pitch outline (#160c08, Terraria dark)
    
    # Oak Wood Staves (Terraria High Contrast, Chunky)
    "A": (230, 164, 76, 255),   # Oak lit highlight (#e6a44c)
    "B": (158, 92, 38, 255),    # Oak rich warm body (#9e5c26)
    "C": (74, 34, 12, 255),     # Oak deep shadow / crevice (#4a220c)
    
    # Iron Bands & Rivets (Anchored props)
    "H": (228, 237, 244, 255),  # Rivet glint & Iron highlight (#e4edf4)
    "I": (126, 140, 156, 255),  # Metallic iron midtone (#7e8c9c)
    "J": (52, 60, 72, 255),     # Iron shadow (#343c48)
    
    # Red Wine Liquid
    "W": (172, 20, 44, 255),    # Rich red wine (#ac142c)
    "V": (76, 6, 18, 255),      # Dark wine pool shadow (#4c0612)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def outline_enclosing(grid):
    # Enclose all solid pixels with # against .
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def build_frame1():
    # Frame 1: Pre-Impact (Đáy thùng vừa chạm mặt sàn đá, thân nén dẹp nhẹ Squash, nứt từ đáy)
    grid = empty_grid()
    
    # Ground contact shadow S under the barrel base
    for x in range(14, 34): grid[41][x] = "S"
    for x in range(16, 32): grid[42][x] = "S"
    for x in range(19, 29): grid[43][x] = "S"
    
    # Top rim outline y=20
    for x in range(18, 30): grid[20][x] = "#"
    
    # Lid surface (y=21)
    grid[21][17] = "#"; grid[21][30] = "#"
    grid[21][18] = "C"
    for x in range(19, 23): grid[21][x] = "A"
    for x in range(23, 27): grid[21][x] = "B"
    for x in range(27, 30): grid[21][x] = "C"
    grid[21][24] = "#" # bung hole
    
    # Top lip chime (y=22)
    grid[22][16] = "#"; grid[22][31] = "#"
    for x in range(17, 23): grid[22][x] = "A"
    for x in range(23, 27): grid[22][x] = "B"
    for x in range(27, 31): grid[22][x] = "C"
    grid[22][20] = "#"; grid[22][24] = "#"; grid[22][28] = "#"

    # Squashed belly spans (smooth, wide bulge)
    barrel_spans = {
        23: (16, 31),
        24: (15, 32),
        25: (14, 33), # Upper iron band
        26: (14, 33), # Upper iron band
        27: (14, 33),
        28: (13, 34),
        29: (13, 34), # Max belly bulge
        30: (13, 34),
        31: (13, 34),
        32: (13, 34),
        33: (14, 33),
        34: (14, 33), # Lower iron band
        35: (14, 33), # Lower iron band
        36: (15, 32),
        37: (15, 32),
        38: (16, 31),
        39: (17, 30),
        40: (17, 30), # Impacted base
    }
    
    for y, (x1, x2) in barrel_spans.items():
        grid[y][x1] = "#"; grid[y][x2] = "#"
        if y in (25, 26):
            # Upper iron band: metallic gray with rivets
            for x in range(x1 + 1, x2):
                if y == 25:
                    grid[y][x] = "H" if x in (16, 21, 26, 31) else "I"
                else:
                    grid[y][x] = "I" if x in (16, 21, 26, 31) else "J"
            grid[y][x1 + 1] = "J"; grid[y][x2 - 1] = "J"
        elif y in (34, 35):
            # Lower iron band: metallic gray with rivets
            for x in range(x1 + 1, x2):
                if y == 34:
                    grid[y][x] = "H" if x in (16, 21, 26, 31) else "I"
                else:
                    grid[y][x] = "I" if x in (16, 21, 26, 31) else "J"
            grid[y][x1 + 1] = "J"; grid[y][x2 - 1] = "J"
        else:
            # Oak wood staves
            stave_w = (x2 - x1) / 4.0
            s1 = int(x1 + stave_w)
            s2 = int(x1 + 2 * stave_w)
            s3 = int(x1 + 3 * stave_w)
            for x in range(x1 + 1, x2):
                if x in (s1, s2, s3):
                    grid[y][x] = "C" if x == s1 else ("#" if x == s2 else "C")
                elif x < s1:
                    grid[y][x] = "A" if (x + y) % 3 != 0 else "B"
                elif x < s2:
                    grid[y][x] = "B" if (x + y) % 4 != 0 else "A"
                elif x < s3:
                    grid[y][x] = "B" if (x + y) % 3 != 0 else "C"
                else:
                    grid[y][x] = "C"
                    
    # Bottom rim at y=41
    for x in range(18, 30): grid[41][x] = "#"
    
    # Impact cracks branching upward from floor contact:
    grid[40][23] = "#"; grid[40][24] = "W" # wine seeping
    grid[39][23] = "#"; grid[39][22] = "#"
    grid[38][22] = "#"; grid[38][21] = "#"
    grid[37][21] = "#"
    grid[36][20] = "#"; grid[36][19] = "#"
    grid[35][19] = "#"
    
    grid[40][25] = "#"
    grid[39][25] = "#"; grid[39][26] = "#"
    grid[38][26] = "#"; grid[38][27] = "#"
    grid[37][27] = "#"
    grid[41][24] = "W"
    
    outline_enclosing(grid)
    return grid

def build_frame2():
    # Frame 2: Ground-Up Rupture
    # Tâm vỡ ở ĐÁY tiếp xúc sàn:
    # - Đáy vỡ toác ngang 2 bên sát sàn (x=8..16 và x=31..39, y=38..41)
    # - Nắp và thành trên văng bổng ngược lên cao hình vòm (x=13..21, x=27..35, y=23..32)
    # - Nắp ở trên cùng (x=19..28, y=16..20)
    # - Rượu vang phun ngược lên từ tâm vỡ ở đáy!
    grid = empty_grid()
    
    # Shadows under floor pieces and wine spill
    for x in range(7, 18): grid[41][x] = "S"
    for x in range(9, 16): grid[42][x] = "S"
    for x in range(30, 41): grid[41][x] = "S"
    for x in range(32, 39): grid[42][x] = "S"
    for x in range(18, 29): grid[42][x] = "S" # Center pool
    for x in range(20, 27): grid[43][x] = "S"

    # 1. Left base chunk: toác ngang sát sàn sang trái (x=8..16, y=38..41)
    grid[38][9] = "#"; grid[38][10] = "#"; grid[38][11] = "#"; grid[38][12] = "#"
    grid[39][8] = "#"; grid[39][9] = "A"; grid[39][10] = "I"; grid[39][11] = "H"; grid[39][12] = "I"; grid[39][13] = "#"
    grid[40][8] = "#"; grid[40][9] = "B"; grid[40][10] = "J"; grid[40][11] = "I"; grid[40][12] = "J"; grid[40][13] = "B"; grid[40][14] = "#"
    grid[41][8] = "#"; grid[41][9] = "#"; grid[41][10] = "#"; grid[41][11] = "#"; grid[41][12] = "#"; grid[41][13] = "#"; grid[41][14] = "#"
    
    # 2. Right base chunk: toác ngang sát sàn sang phải (x=31..39, y=38..41)
    grid[38][35] = "#"; grid[38][36] = "#"; grid[38][37] = "#"; grid[38][38] = "#"
    grid[39][34] = "#"; grid[39][35] = "I"; grid[39][36] = "H"; grid[39][37] = "I"; grid[39][38] = "C"; grid[39][39] = "#"
    grid[40][33] = "#"; grid[40][34] = "B"; grid[40][35] = "J"; grid[40][36] = "I"; grid[40][37] = "J"; grid[40][38] = "C"; grid[40][39] = "#"
    grid[41][33] = "#"; grid[41][34] = "#"; grid[41][35] = "#"; grid[41][36] = "#"; grid[41][37] = "#"; grid[41][38] = "#"; grid[41][39] = "#"

    # 3. Center floor rubble & wine splash pool (x=18..29, y=39..42)
    grid[39][22] = "W"; grid[39][23] = "W"; grid[39][24] = "W"; grid[39][25] = "W"
    grid[40][19] = "#"; grid[40][20] = "C"; grid[40][21] = "W"; grid[40][22] = "W"; grid[40][23] = "V"; grid[40][24] = "W"; grid[40][25] = "W"; grid[40][26] = "C"; grid[40][27] = "#"
    grid[41][18] = "#"; grid[41][19] = "W"; grid[41][20] = "V"; grid[41][21] = "W"; grid[41][22] = "V"; grid[41][23] = "V"; grid[41][24] = "V"; grid[41][25] = "W"; grid[41][26] = "V"; grid[41][27] = "#"
    grid[42][19] = "#"; grid[42][20] = "#"; grid[42][21] = "V"; grid[42][22] = "V"; grid[42][23] = "V"; grid[42][24] = "V"; grid[42][25] = "V"; grid[42][26] = "#"; grid[42][27] = "#"

    # 4. Upper-left stave chunk: tilted upward-left (x=12..19, y=23..32)
    # With iron band and anchored rivet H!
    grid[23][14] = "#"; grid[23][15] = "#"; grid[23][16] = "#"
    grid[24][13] = "#"; grid[24][14] = "A"; grid[24][15] = "A"; grid[24][16] = "B"; grid[24][17] = "#"
    grid[25][12] = "#"; grid[25][13] = "A"; grid[25][14] = "H"; grid[25][15] = "I"; grid[25][16] = "I"; grid[25][17] = "#" # Rivet at (14, 25)
    grid[26][12] = "#"; grid[26][13] = "A"; grid[26][14] = "I"; grid[26][15] = "J"; grid[26][16] = "J"; grid[26][17] = "B"; grid[26][18] = "#"
    grid[27][12] = "#"; grid[27][13] = "A"; grid[27][14] = "A"; grid[27][15] = "B"; grid[27][16] = "B"; grid[27][17] = "C"; grid[27][18] = "#"
    grid[28][13] = "#"; grid[28][14] = "A"; grid[28][15] = "B"; grid[28][16] = "B"; grid[28][17] = "C"; grid[28][18] = "#"
    grid[29][13] = "#"; grid[29][14] = "B"; grid[29][15] = "B"; grid[29][16] = "C"; grid[29][17] = "#"
    grid[30][14] = "#"; grid[30][15] = "B"; grid[30][16] = "C"; grid[30][17] = "#"
    grid[31][15] = "#"; grid[31][16] = "C"; grid[31][17] = "#"
    grid[32][15] = "#"; grid[32][16] = "#"

    # 5. Upper-right stave chunk: tilted upward-right (x=28..35, y=23..32)
    # With iron band and anchored rivet H!
    grid[23][30] = "#"; grid[23][31] = "#"; grid[23][32] = "#"
    grid[24][29] = "#"; grid[24][30] = "B"; grid[24][31] = "C"; grid[24][32] = "C"; grid[24][33] = "#"
    grid[25][29] = "#"; grid[25][30] = "I"; grid[25][31] = "H"; grid[25][32] = "I"; grid[25][33] = "C"; grid[25][34] = "#" # Rivet at (31, 25)
    grid[26][28] = "#"; grid[26][29] = "B"; grid[26][30] = "J"; grid[26][31] = "I"; grid[26][32] = "J"; grid[26][33] = "C"; grid[26][34] = "#"
    grid[27][28] = "#"; grid[27][29] = "B"; grid[27][30] = "B"; grid[27][31] = "C"; grid[27][32] = "C"; grid[27][33] = "C"; grid[27][34] = "#"
    grid[28][28] = "#"; grid[28][29] = "B"; grid[28][30] = "C"; grid[28][31] = "C"; grid[28][32] = "C"; grid[28][33] = "#"
    grid[29][29] = "#"; grid[29][30] = "B"; grid[29][31] = "C"; grid[29][32] = "#"
    grid[30][29] = "#"; grid[30][30] = "B"; grid[30][31] = "C"; grid[30][32] = "#"
    grid[31][30] = "#"; grid[31][31] = "C"; grid[31][32] = "#"
    grid[32][30] = "#"; grid[32][31] = "#"

    # 6. Top Lid chunk: popped up high in center (x=19..28, y=16..20)
    grid[16][22] = "#"; grid[16][23] = "#"; grid[16][24] = "#"; grid[16][25] = "#"
    grid[17][20] = "#"; grid[17][21] = "A"; grid[17][22] = "A"; grid[17][23] = "A"; grid[17][24] = "B"; grid[17][25] = "B"; grid[17][26] = "C"; grid[17][27] = "#"
    grid[18][19] = "#"; grid[18][20] = "A"; grid[18][21] = "A"; grid[18][22] = "B"; grid[18][23] = "#"; grid[18][24] = "B"; grid[18][25] = "C"; grid[18][26] = "C"; grid[18][27] = "#"
    grid[19][20] = "#"; grid[19][21] = "A"; grid[19][22] = "B"; grid[19][23] = "B"; grid[19][24] = "C"; grid[19][25] = "C"; grid[19][26] = "#"
    grid[20][21] = "#"; grid[20][22] = "#"; grid[20][23] = "#"; grid[20][24] = "#"; grid[20][25] = "#"

    # 7. Erupting crimson wine spray shooting upward from center rupture
    grid[26][23] = "W"; grid[26][24] = "W"
    grid[27][22] = "W"; grid[27][23] = "W"; grid[27][24] = "V"; grid[27][25] = "W"
    grid[28][21] = "W"; grid[28][22] = "W"; grid[28][23] = "V"; grid[28][24] = "W"; grid[28][25] = "W"; grid[28][26] = "W"
    grid[29][21] = "W"; grid[29][22] = "W"; grid[29][23] = "V"; grid[29][24] = "V"; grid[29][25] = "W"; grid[29][26] = "W"
    grid[30][22] = "W"; grid[30][23] = "V"; grid[30][24] = "V"; grid[30][25] = "W"
    
    # Flying wine droplets
    grid[21][17] = "#"; grid[21][18] = "W"; grid[21][19] = "#"
    grid[21][29] = "#"; grid[21][30] = "W"; grid[21][31] = "#"
    grid[24][21] = "#"; grid[24][22] = "W"; grid[24][23] = "#"
    grid[24][26] = "#"; grid[24][27] = "W"; grid[24][28] = "#"

    outline_enclosing(grid)
    return grid

def build_frame3():
    # Frame 3: Parabolic Trajectory
    # QUY TẮC 4.1: CẤM NỔ BOM TRÒN!
    # - Tâm vỡ từ sàn: Đáy trượt ngang sàn (y=40..42, x=5..13 và x=35..43)
    # - Nắp và mảnh thành bay bổng lên cao theo VÒM PARABOL (y=9..24):
    #   + Nắp ở đỉnh cao nhất (x=21..29, y=9..14)
    #   + Mảnh thành trái bay theo vòng cung trái (x=8..16, y=16..24)
    #   + Mảnh thành phải bay theo vòng cung phải (x=31..39, y=16..24)
    #   + Vùng bụng giữa (y=25..38) là khoảng không thông thoáng, có vài giọt rượu vang rơi theo quỹ đạo!
    grid = empty_grid()
    
    # 1. Ground contact shadows under distant sliding floor shards
    for x in range(4, 15): grid[41][x] = "S"
    for x in range(6, 13): grid[42][x] = "S"
    for x in range(33, 44): grid[41][x] = "S"
    for x in range(35, 42): grid[42][x] = "S"
    for x in range(18, 29): grid[42][x] = "S" # Center pool
    for x in range(20, 27): grid[43][x] = "S"

    # 2. Left sliding floor shard (x=5..13, y=39..41)
    grid[39][6] = "#"; grid[39][7] = "#"; grid[39][8] = "#"; grid[39][9] = "#"; grid[39][10] = "#"
    grid[40][5] = "#"; grid[40][6] = "A"; grid[40][7] = "I"; grid[40][8] = "H"; grid[40][9] = "I"; grid[40][10] = "B"; grid[40][11] = "#"
    grid[41][5] = "#"; grid[41][6] = "B"; grid[41][7] = "J"; grid[41][8] = "I"; grid[41][9] = "J"; grid[41][10] = "C"; grid[41][11] = "C"; grid[41][12] = "#"
    grid[42][6] = "#"; grid[42][7] = "#"; grid[42][8] = "#"; grid[42][9] = "#"; grid[42][10] = "#"; grid[42][11] = "#"; grid[42][12] = "#"

    # 3. Right sliding floor shard (x=35..43, y=39..41)
    grid[39][37] = "#"; grid[39][38] = "#"; grid[39][39] = "#"; grid[39][40] = "#"; grid[39][41] = "#"
    grid[40][36] = "#"; grid[40][37] = "B"; grid[40][38] = "I"; grid[40][39] = "H"; grid[40][40] = "I"; grid[40][41] = "C"; grid[40][42] = "#"
    grid[41][35] = "#"; grid[41][36] = "B"; grid[41][37] = "C"; grid[41][38] = "J"; grid[41][39] = "I"; grid[41][40] = "J"; grid[41][41] = "C"; grid[41][42] = "#"
    grid[42][36] = "#"; grid[42][37] = "#"; grid[42][38] = "#"; grid[42][39] = "#"; grid[42][40] = "#"; grid[42][41] = "#"; grid[42][42] = "#"

    # 4. Center floor wine puddle & splinter
    grid[40][21] = "W"; grid[40][22] = "W"; grid[40][23] = "W"; grid[40][24] = "V"; grid[40][25] = "W"
    grid[41][19] = "#"; grid[41][20] = "W"; grid[41][21] = "V"; grid[41][22] = "V"; grid[41][23] = "V"; grid[41][24] = "V"; grid[41][25] = "V"; grid[41][26] = "W"; grid[41][27] = "#"
    grid[42][20] = "#"; grid[42][21] = "#"; grid[42][22] = "V"; grid[42][23] = "V"; grid[42][24] = "V"; grid[42][25] = "V"; grid[42][26] = "#"; grid[42][27] = "#"

    # 5. Top Lid Chunk at APEX (x=21..29, y=9..14) - Tossed high into the air!
    grid[9][23] = "#"; grid[9][24] = "#"; grid[9][25] = "#"; grid[9][26] = "#"
    grid[10][22] = "#"; grid[10][23] = "A"; grid[10][24] = "A"; grid[10][25] = "A"; grid[10][26] = "B"; grid[10][27] = "C"; grid[10][28] = "#"
    grid[11][21] = "#"; grid[11][22] = "A"; grid[11][23] = "A"; grid[11][24] = "B"; grid[11][25] = "#"; grid[11][26] = "B"; grid[11][27] = "C"; grid[11][28] = "#"
    grid[12][21] = "#"; grid[12][22] = "A"; grid[12][23] = "B"; grid[12][24] = "B"; grid[12][25] = "C"; grid[12][26] = "C"; grid[12][27] = "C"; grid[12][28] = "#"
    grid[13][22] = "#"; grid[13][23] = "B"; grid[13][24] = "C"; grid[13][25] = "C"; grid[13][26] = "#"; grid[13][27] = "#"
    grid[14][23] = "#"; grid[14][24] = "#"; grid[14][25] = "#"

    # 6. Upper-left stave chunk at high parabolic arc (x=8..16, y=16..24)
    # Tilted ~40°, with iron band + rivet H firmly anchored!
    grid[16][10] = "#"; grid[16][11] = "#"; grid[16][12] = "#"
    grid[17][9] = "#"; grid[17][10] = "A"; grid[17][11] = "A"; grid[17][12] = "B"; grid[17][13] = "#"
    grid[18][8] = "#"; grid[18][9] = "A"; grid[18][10] = "H"; grid[18][11] = "I"; grid[18][12] = "I"; grid[18][13] = "#" # Rivet at (10, 18)
    grid[19][8] = "#"; grid[19][9] = "A"; grid[19][10] = "I"; grid[19][11] = "J"; grid[19][12] = "J"; grid[19][13] = "B"; grid[19][14] = "#"
    grid[20][8] = "#"; grid[20][9] = "A"; grid[20][10] = "B"; grid[20][11] = "B"; grid[20][12] = "C"; grid[20][13] = "#"
    grid[21][9] = "#"; grid[21][10] = "B"; grid[21][11] = "B"; grid[21][12] = "C"; grid[21][13] = "#"
    grid[22][10] = "#"; grid[22][11] = "B"; grid[22][12] = "C"; grid[22][13] = "#"
    grid[23][11] = "#"; grid[23][12] = "C"; grid[23][13] = "#"
    grid[24][11] = "#"; grid[24][12] = "#"

    # 7. Upper-right stave chunk at high parabolic arc (x=31..39, y=16..24)
    # Tilted ~-40°, with iron band + rivet H firmly anchored!
    grid[16][34] = "#"; grid[16][35] = "#"; grid[16][36] = "#"
    grid[17][33] = "#"; grid[17][34] = "B"; grid[17][35] = "C"; grid[17][36] = "C"; grid[17][37] = "#"
    grid[18][33] = "#"; grid[18][34] = "I"; grid[18][35] = "H"; grid[18][36] = "I"; grid[18][37] = "C"; grid[18][38] = "#" # Rivet at (35, 18)
    grid[19][32] = "#"; grid[19][33] = "J"; grid[19][34] = "I"; grid[19][35] = "J"; grid[19][36] = "C"; grid[19][37] = "C"; grid[19][38] = "#"
    grid[20][32] = "#"; grid[20][33] = "B"; grid[20][34] = "C"; grid[20][35] = "C"; grid[20][36] = "C"; grid[20][37] = "#"
    grid[21][33] = "#"; grid[21][34] = "B"; grid[21][35] = "C"; grid[21][36] = "C"; grid[21][37] = "#"
    grid[22][33] = "#"; grid[22][34] = "B"; grid[22][35] = "C"; grid[22][36] = "#"
    grid[23][34] = "#"; grid[23][35] = "C"; grid[23][36] = "#"
    grid[24][34] = "#"; grid[24][35] = "#"

    # 8. Airborne wine droplets and tiny oak splinters arcing in mid-air
    # Flying wine droplets with outlines
    grid[17][19] = "#"; grid[17][20] = "W"; grid[17][21] = "#"
    grid[18][27] = "#"; grid[18][28] = "W"; grid[18][29] = "#"
    grid[22][23] = "#"; grid[22][24] = "W"; grid[22][25] = "#"
    grid[26][21] = "#"; grid[26][22] = "W"; grid[26][23] = "#"
    grid[27][26] = "#"; grid[27][27] = "W"; grid[27][28] = "#"
    
    # 1px wood splinters with outline
    grid[22][18] = "#"; grid[22][19] = "A"; grid[22][20] = "#"
    grid[23][29] = "#"; grid[23][30] = "B"; grid[23][31] = "#"

    outline_enclosing(grid)
    return grid

def build_frame4():
    # Frame 4: Settled Debris
    # Toàn bộ mảnh gỗ rơi nằm yên trên sàn, mỗi mảnh có bóng râm tiếp đất 'S' nhỏ bên dưới.
    grid = empty_grid()
    
    # Ground shadows under all resting debris pieces
    for x in range(6, 16): grid[41][x] = "S"
    for x in range(8, 14): grid[42][x] = "S"
    
    for x in range(16, 23): grid[42][x] = "S"
    
    for x in range(19, 29): grid[43][x] = "S" # Center wine pool
    
    for x in range(23, 32): grid[41][x] = "S"
    for x in range(25, 30): grid[42][x] = "S"
    
    for x in range(33, 43): grid[41][x] = "S"
    for x in range(35, 41): grid[42][x] = "S"
    
    grid[42][3] = "S"; grid[42][4] = "S"
    grid[42][44] = "S"; grid[42][45] = "S"

    # 1. Left pile: broken curved stave with iron band and rivet lying flat (x=6..15, y=38..41)
    grid[38][7] = "#"; grid[38][8] = "#"; grid[38][9] = "#"; grid[38][10] = "#"; grid[38][11] = "#"; grid[38][12] = "#"
    grid[39][6] = "#"; grid[39][7] = "A"; grid[39][8] = "A"; grid[39][9] = "I"; grid[39][10] = "H"; grid[39][11] = "I"; grid[39][12] = "B"; grid[39][13] = "#" # Rivet at (10, 39)
    grid[40][5] = "#"; grid[40][6] = "A"; grid[40][7] = "B"; grid[40][8] = "B"; grid[40][9] = "J"; grid[40][10] = "I"; grid[40][11] = "J"; grid[40][12] = "C"; grid[40][13] = "C"; grid[40][14] = "#"
    grid[41][5] = "#"; grid[41][6] = "#"; grid[41][7] = "#"; grid[41][8] = "#"; grid[41][9] = "#"; grid[41][10] = "#"; grid[41][11] = "#"; grid[41][12] = "#"; grid[41][13] = "#"; grid[41][14] = "#"

    # 2. Center-left split stave shard (x=16..22, y=39..42)
    grid[39][18] = "#"; grid[39][19] = "#"; grid[39][20] = "#"
    grid[40][16] = "#"; grid[40][17] = "A"; grid[40][18] = "B"; grid[40][19] = "B"; grid[40][20] = "C"; grid[40][21] = "#"
    grid[41][16] = "#"; grid[41][17] = "B"; grid[41][18] = "B"; grid[41][19] = "C"; grid[41][20] = "C"; grid[41][21] = "C"; grid[41][22] = "#"
    grid[42][16] = "#"; grid[42][17] = "#"; grid[42][18] = "#"; grid[42][19] = "#"; grid[42][20] = "#"; grid[42][21] = "#"; grid[42][22] = "#"

    # 3. Top lid chunk settled tilted on the ground (x=23..32, y=36..40)
    grid[36][25] = "#"; grid[36][26] = "#"; grid[36][27] = "#"; grid[36][28] = "#"
    grid[37][24] = "#"; grid[37][25] = "A"; grid[37][26] = "A"; grid[37][27] = "B"; grid[37][28] = "B"; grid[37][29] = "#"
    grid[38][23] = "#"; grid[38][24] = "A"; grid[38][25] = "B"; grid[38][26] = "#"; grid[38][27] = "B"; grid[38][28] = "C"; grid[38][29] = "C"; grid[38][30] = "#" # bung hole
    grid[39][23] = "#"; grid[39][24] = "B"; grid[39][25] = "B"; grid[39][26] = "C"; grid[39][27] = "C"; grid[39][28] = "C"; grid[39][29] = "#"; grid[39][30] = "#"
    grid[40][24] = "#"; grid[40][25] = "#"; grid[40][26] = "#"; grid[40][27] = "#"; grid[40][28] = "#"; grid[40][29] = "#"

    # 4. Right stave pile: broken stave with iron band and rivet lying flat (x=33..42, y=38..41)
    grid[38][34] = "#"; grid[38][35] = "#"; grid[38][36] = "#"; grid[38][37] = "#"; grid[38][38] = "#"; grid[38][39] = "#"
    grid[39][33] = "#"; grid[39][34] = "B"; grid[39][35] = "I"; grid[39][36] = "H"; grid[39][37] = "I"; grid[39][38] = "C"; grid[39][39] = "C"; grid[39][40] = "#" # Rivet at (36, 39)
    grid[40][33] = "#"; grid[40][34] = "B"; grid[40][35] = "J"; grid[40][36] = "I"; grid[40][37] = "J"; grid[40][38] = "C"; grid[40][39] = "C"; grid[40][40] = "C"; grid[40][41] = "#"
    grid[41][33] = "#"; grid[41][34] = "#"; grid[41][35] = "#"; grid[41][36] = "#"; grid[41][37] = "#"; grid[41][38] = "#"; grid[41][39] = "#"; grid[41][40] = "#"; grid[41][41] = "#"

    # 5. Deep red wine spill pooled across the center stones (x=19..28, y=41..43)
    grid[41][20] = "W"; grid[41][21] = "W"; grid[41][22] = "V"; grid[41][23] = "W"; grid[41][24] = "W"; grid[41][25] = "V"
    grid[42][19] = "#"; grid[42][20] = "W"; grid[42][21] = "V"; grid[42][22] = "V"; grid[42][23] = "V"; grid[42][24] = "V"; grid[42][25] = "V"; grid[42][26] = "W"; grid[42][27] = "#"
    grid[43][20] = "#"; grid[43][21] = "#"; grid[43][22] = "V"; grid[43][23] = "V"; grid[43][24] = "V"; grid[43][25] = "V"; grid[43][26] = "#"; grid[43][27] = "#"

    # 6. Tiny far-flung wood splinters
    grid[41][3] = "#"; grid[41][4] = "A"; grid[41][5] = "#"
    grid[41][43] = "#"; grid[41][44] = "C"; grid[41][45] = "#"

    outline_enclosing(grid)
    return grid

frames = [build_frame1(), build_frame2(), build_frame3(), build_frame4()]

# Outline and rivet safety checks
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

def check_rivet_anchoring(grid, f_idx):
    violating = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code in ("H", "I"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        violating.append((x, y, code, nx, ny))
    return violating

print("\n=== VERIFICATION: OUTLINE & RIVET ANCHORING ===")
for i, fr in enumerate(frames):
    n = check_outline_completeness(fr)
    v = check_rivet_anchoring(fr, i)
    print(f"Frame {i+1}: naked pixels = {len(n)}, unanchored metal = {len(v)}")

# Save preview images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_barrel_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_barrel_sheet.png")

gif_frames[0].save(
    "python/perfect_barrel_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS = 125ms
    loop=0
)
print("Rendered perfect_barrel_sheet.png and perfect_barrel_anim.gif successfully!")
