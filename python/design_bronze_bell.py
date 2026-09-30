import os
import math
from PIL import Image

W, H = 48, 48

PALETTE_RGBA = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (26, 22, 32, 130),     # Soft ground shadow (Alpha 130)
    "#": (56, 30, 18, 255),     # Soft dark mahogany outline for wood/bronze (#381e12)
    "@": (38, 34, 32, 255),     # Soft dark stone outline (#262220)
    
    # Bronze Bell (Warm polished bronze)
    "A": (255, 223, 136, 255),  # Specular gold highlight (#ffdf88)
    "B": (232, 160, 56, 255),   # Bright bronze body (#e8a038)
    "C": (184, 100, 28, 255),   # Warm bronze midtone (#b8641c)
    "D": (116, 56, 16, 255),    # Deep bronze shadow (#743810)
    "E": (66, 26, 8, 255),      # Inner bell cavity shadow (#421a08)
    
    # Oak Gallows Frame (Warm oak timber)
    "F": (212, 146, 66, 255),   # Oak highlight (#d49242)
    "G": (148, 84, 34, 255),    # Oak midtone (#945422)
    "H": (86, 44, 16, 255),     # Oak shadow (#562c10)
    
    # Iron Chain & Mounts
    "J": (136, 130, 146, 255),  # Iron highlight (#888292)
    "K": (84, 76, 92, 255),     # Iron midtone (#544c5c)
    "L": (50, 42, 54, 255),     # Iron shadow (#322a36)
    
    # Stone Floor Base (Rustic stone blocks)
    "M": (142, 138, 128, 255),  # Stone highlight (#8e8a80)
    "N": (98, 94, 86, 255),     # Stone midtone (#625e56)
    "P": (62, 58, 52, 255),     # Stone shadow (#3e3a34)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_static_environment(grid):
    # 1. Stone platform / floor at bottom: Y = 40..43
    for x in range(3, 45):
        grid[40][x] = "@"
        
    for x in range(4, 44):
        grid[41][x] = "M" if x % 5 != 0 else "N"
        grid[42][x] = "N" if x % 4 != 0 else "P"
        grid[43][x] = "P" if x % 3 != 0 else "@"
        grid[44][x] = "@"
        
    # Stone bevel edges
    grid[41][3] = "@"; grid[42][3] = "@"; grid[43][3] = "@"
    grid[41][44] = "@"; grid[42][44] = "@"; grid[43][44] = "@"
    
    # 2. Wooden upright columns (cột gỗ đứng):
    # Left post: X = 5..9, Y = 10..39
    # Right post: X = 38..42, Y = 10..39
    for y in range(10, 40):
        # Left post
        grid[y][5] = "#"
        grid[y][6] = "F" # Facing sun from left
        grid[y][7] = "G"
        grid[y][8] = "H"
        grid[y][9] = "#"
        
        # Right post
        grid[y][38] = "#"
        grid[y][39] = "F"
        grid[y][40] = "G"
        grid[y][41] = "H"
        grid[y][42] = "#"
        
    # Post base stone plinths (chân bục đá):
    for x in range(4, 11):
        grid[39][x] = "@"
        grid[40][x] = "M" if x in (5, 6) else "N"
    for x in range(37, 44):
        grid[39][x] = "@"
        grid[40][x] = "N" if x in (38, 39) else "P"
        
    # 3. Top Crossbeam (xà ngang gỗ sồi): Y = 6..10, X = 3..44
    for x in range(3, 45):
        grid[6][x] = "#"
        grid[7][x] = "F"
        grid[8][x] = "G"
        grid[9][x] = "H"
        grid[10][x] = "#"
    grid[7][3] = "#"; grid[8][3] = "#"; grid[9][3] = "#"
    grid[7][44] = "#"; grid[8][44] = "#"; grid[9][44] = "#"
    
    # Diagonal corner braces (giá đỡ chéo):
    grid[11][10] = "F"; grid[11][11] = "#"
    grid[12][11] = "G"; grid[12][12] = "#"
    grid[13][12] = "H"; grid[13][13] = "#"
    grid[14][13] = "#"
    
    grid[11][37] = "F"; grid[11][36] = "#"
    grid[12][36] = "G"; grid[12][35] = "#"
    grid[13][35] = "H"; grid[13][34] = "#"
    grid[14][34] = "#"
    
    # 4. Central Iron Pivot Hanger (Khóa khớp treo cố định 100% tại X=24, Y=10):
    grid[6][23] = "K"; grid[6][24] = "J"; grid[6][25] = "K"
    grid[7][23] = "K"; grid[7][24] = "J"; grid[7][25] = "K"
    grid[8][23] = "L"; grid[8][24] = "K"; grid[8][25] = "L"
    grid[9][23] = "L"; grid[9][24] = "L"; grid[9][25] = "L"
    grid[10][23] = "#"; grid[10][24] = "K"; grid[10][25] = "#"
    grid[11][23] = "L"; grid[11][24] = "."; grid[11][25] = "L"
    grid[12][23] = "#"; grid[12][24] = "K"; grid[12][25] = "#"

def draw_bell_and_chain(grid, f_idx):
    cx_table = [21, 18, 21, 24, 27, 30, 27, 24]
    cy_table = [26, 25, 26, 26, 26, 25, 26, 26]
    tilt_table = [-1, -2, -1, 0, 1, 2, 1, 0]
    
    cx = cx_table[f_idx]
    cy = cy_table[f_idx]
    tilt = tilt_table[f_idx]
    t_y = cy - 7
    
    # 1. Chain links
    if tilt == 0:
        for y in range(13, t_y):
            grid[y][23] = "L" if y % 2 == 0 else "#"
            grid[y][24] = "J" if y % 2 == 0 else "K"
            grid[y][25] = "L" if y % 2 == 0 else "#"
    elif tilt == -2:
        grid[13][23] = "J"; grid[13][24] = "#"
        grid[14][22] = "#"; grid[14][23] = "K"
        grid[15][21] = "J"; grid[15][22] = "#"
        grid[16][20] = "#"; grid[16][21] = "K"
        grid[17][19] = "J"; grid[17][20] = "#"
    elif tilt == -1:
        if f_idx == 0:
            grid[13][24] = "J"; grid[13][25] = "#"
            grid[14][23] = "#"; grid[14][24] = "K"
            grid[15][22] = "J"; grid[15][23] = "#"
            grid[16][22] = "#"; grid[16][23] = "K"
            grid[17][21] = "J"; grid[17][22] = "#"
            grid[18][21] = "#"; grid[18][22] = "K"
        else:
            grid[13][24] = "J"; grid[13][25] = "#"
            grid[14][24] = "#"; grid[14][25] = "K"
            grid[15][23] = "J"; grid[15][24] = "#"
            grid[16][23] = "#"; grid[16][24] = "K"
            grid[17][22] = "J"; grid[17][23] = "#"
            grid[18][21] = "#"; grid[18][22] = "K"
    elif tilt == 2:
        grid[13][24] = "#"; grid[13][25] = "J"
        grid[14][25] = "K"; grid[14][26] = "#"
        grid[15][26] = "#"; grid[15][27] = "J"
        grid[16][27] = "K"; grid[16][28] = "#"
        grid[17][28] = "#"; grid[17][29] = "J"
    elif tilt == 1:
        if f_idx == 4:
            grid[13][24] = "#"; grid[13][25] = "J"
            grid[14][24] = "K"; grid[14][25] = "#"
            grid[15][25] = "#"; grid[15][26] = "J"
            grid[16][25] = "K"; grid[16][26] = "#"
            grid[17][26] = "#"; grid[17][27] = "J"
            grid[18][26] = "K"; grid[18][27] = "#"
        else:
            grid[13][23] = "#"; grid[13][24] = "J"
            grid[14][23] = "K"; grid[14][24] = "#"
            grid[15][24] = "#"; grid[15][25] = "J"
            grid[16][24] = "K"; grid[16][25] = "#"
            grid[17][25] = "#"; grid[17][26] = "J"
            grid[18][26] = "K"; grid[18][27] = "#"

    # 2. Bell Model
    if tilt == 0:
        grid[cy - 7][cx - 1] = "#"; grid[cy - 7][cx] = "K"; grid[cy - 7][cx + 1] = "#"
        grid[cy - 6][cx - 2] = "#"; grid[cy - 6][cx - 1] = "B"; grid[cy - 6][cx] = "C"; grid[cy - 6][cx + 1] = "D"; grid[cy - 6][cx + 2] = "#"
        
        # Specular A upper left
        grid[cy - 5][cx - 3] = "#"; grid[cy - 5][cx - 2] = "A"; grid[cy - 5][cx - 1] = "B"; grid[cy - 5][cx] = "B"; grid[cy - 5][cx + 1] = "C"; grid[cy - 5][cx + 2] = "D"; grid[cy - 5][cx + 3] = "#"
        grid[cy - 4][cx - 4] = "#"; grid[cy - 4][cx - 3] = "A"; grid[cy - 4][cx - 2] = "B"; grid[cy - 4][cx - 1] = "B"; grid[cy - 4][cx] = "C"; grid[cy - 4][cx + 1] = "C"; grid[cy - 4][cx + 2] = "D"; grid[cy - 4][cx + 3] = "D"; grid[cy - 4][cx + 4] = "#"
        
        grid[cy - 3][cx - 4] = "#"; grid[cy - 3][cx - 3] = "B"; grid[cy - 3][cx - 2] = "B"; grid[cy - 3][cx - 1] = "C"; grid[cy - 3][cx] = "C"; grid[cy - 3][cx + 1] = "D"; grid[cy - 3][cx + 2] = "D"; grid[cy - 3][cx + 3] = "D"; grid[cy - 3][cx + 4] = "#"
        grid[cy - 2][cx - 4] = "#"; grid[cy - 2][cx - 3] = "B"; grid[cy - 2][cx - 2] = "B"; grid[cy - 2][cx - 1] = "C"; grid[cy - 2][cx] = "C"; grid[cy - 2][cx + 1] = "D"; grid[cy - 2][cx + 2] = "D"; grid[cy - 2][cx + 3] = "D"; grid[cy - 2][cx + 4] = "#"
        
        grid[cy - 1][cx - 5] = "#"; grid[cy - 1][cx - 4] = "B"; grid[cy - 1][cx - 3] = "B"; grid[cy - 1][cx - 2] = "C"; grid[cy - 1][cx - 1] = "C"; grid[cy - 1][cx] = "C"; grid[cy - 1][cx + 1] = "D"; grid[cy - 1][cx + 2] = "D"; grid[cy - 1][cx + 3] = "D"; grid[cy - 1][cx + 4] = "D"; grid[cy - 1][cx + 5] = "#"
        grid[cy][cx - 6] = "#"; grid[cy][cx - 5] = "B"; grid[cy][cx - 4] = "B"; grid[cy][cx - 3] = "C"; grid[cy][cx - 2] = "C"; grid[cy][cx - 1] = "C"; grid[cy][cx] = "D"; grid[cy][cx + 1] = "D"; grid[cy][cx + 2] = "D"; grid[cy][cx + 3] = "D"; grid[cy][cx + 4] = "D"; grid[cy][cx + 5] = "D"; grid[cy][cx + 6] = "#"
        
        grid[cy + 1][cx - 6] = "#"; grid[cy + 1][cx - 5] = "A"; grid[cy + 1][cx - 4] = "B"; grid[cy + 1][cx - 3] = "B"; grid[cy + 1][cx - 2] = "C"; grid[cy + 1][cx - 1] = "C"; grid[cy + 1][cx] = "C"; grid[cy + 1][cx + 1] = "D"; grid[cy + 1][cx + 2] = "D"; grid[cy + 1][cx + 3] = "D"; grid[cy + 1][cx + 4] = "D"; grid[cy + 1][cx + 5] = "D"; grid[cy + 1][cx + 6] = "#"
        
        grid[cy + 2][cx - 6] = "#"; grid[cy + 2][cx - 5] = "#"
        for x in range(cx - 4, cx + 5):
            grid[cy + 2][x] = "E"
        grid[cy + 2][cx + 5] = "#"; grid[cy + 2][cx + 6] = "#"
        
        grid[cy + 2][cx - 1] = "C"; grid[cy + 2][cx] = "D"; grid[cy + 2][cx + 1] = "#"
        grid[cy + 3][cx - 1] = "#"; grid[cy + 3][cx] = "D"; grid[cy + 3][cx + 1] = "#"
        grid[cy + 3][cx - 4] = "#"; grid[cy + 3][cx - 3] = "#"; grid[cy + 3][cx + 3] = "#"; grid[cy + 3][cx + 4] = "#"

    elif tilt == -2:
        grid[cy - 7][cx] = "#"; grid[cy - 7][cx + 1] = "K"; grid[cy - 7][cx + 2] = "#"
        grid[cy - 6][cx - 1] = "#"; grid[cy - 6][cx] = "B"; grid[cy - 6][cx + 1] = "C"; grid[cy - 6][cx + 2] = "D"; grid[cy - 6][cx + 3] = "#"
        
        # Specular A upper left
        grid[cy - 5][cx - 3] = "#"; grid[cy - 5][cx - 2] = "A"; grid[cy - 5][cx - 1] = "B"; grid[cy - 5][cx] = "B"; grid[cy - 5][cx + 1] = "C"; grid[cy - 5][cx + 2] = "D"; grid[cy - 5][cx + 3] = "#"
        grid[cy - 4][cx - 5] = "#"; grid[cy - 4][cx - 4] = "A"; grid[cy - 4][cx - 3] = "B"; grid[cy - 4][cx - 2] = "B"; grid[cy - 4][cx - 1] = "C"; grid[cy - 4][cx] = "C"; grid[cy - 4][cx + 1] = "D"; grid[cy - 4][cx + 2] = "D"; grid[cy - 4][cx + 3] = "#"
        
        grid[cy - 3][cx - 6] = "#"; grid[cy - 3][cx - 5] = "B"; grid[cy - 3][cx - 4] = "B"; grid[cy - 3][cx - 2] = "C"; grid[cy - 3][cx - 1] = "D"; grid[cy - 3][cx] = "D"; grid[cy - 3][cx + 1] = "D"; grid[cy - 3][cx + 2] = "#"
        grid[cy - 3][cx - 3] = "C"
        grid[cy - 2][cx - 7] = "#"; grid[cy - 2][cx - 6] = "B"; grid[cy - 2][cx - 5] = "B"; grid[cy - 2][cx - 4] = "C"; grid[cy - 2][cx - 3] = "C"; grid[cy - 2][cx - 2] = "D"; grid[cy - 2][cx - 1] = "D"; grid[cy - 2][cx] = "D"; grid[cy - 2][cx + 1] = "#"
        
        grid[cy - 1][cx - 7] = "#"; grid[cy - 1][cx - 6] = "B"; grid[cy - 1][cx - 5] = "B"; grid[cy - 1][cx - 4] = "C"; grid[cy - 1][cx - 3] = "C"; grid[cy - 1][cx - 2] = "C"; grid[cy - 1][cx - 1] = "D"; grid[cy - 1][cx] = "D"; grid[cy - 1][cx + 1] = "D"; grid[cy - 1][cx + 2] = "#"
        grid[cy][cx - 7] = "#"; grid[cy][cx - 6] = "B"; grid[cy][cx - 5] = "B"; grid[cy][cx - 4] = "C"; grid[cy][cx - 3] = "C"; grid[cy][cx - 2] = "C"; grid[cy][cx - 1] = "D"; grid[cy][cx] = "D"; grid[cy][cx + 1] = "D"; grid[cy][cx + 2] = "D"; grid[cy][cx + 3] = "#"
        
        grid[cy + 1][cx - 7] = "#"; grid[cy + 1][cx - 6] = "A"; grid[cy + 1][cx - 5] = "B"; grid[cy + 1][cx - 4] = "B"; grid[cy + 1][cx - 3] = "C"; grid[cy + 1][cx - 2] = "C"; grid[cy + 1][cx - 1] = "D"; grid[cy + 1][cx] = "D"; grid[cy + 1][cx + 1] = "D"; grid[cy + 1][cx + 2] = "D"; grid[cy + 1][cx + 3] = "D"; grid[cy + 1][cx + 4] = "#"
        
        grid[cy + 2][cx - 6] = "#"; grid[cy + 2][cx - 5] = "#"
        for x in range(cx - 4, cx + 4):
            grid[cy + 2][x] = "E"
        grid[cy + 2][cx + 2] = "D"; grid[cy + 2][cx + 3] = "#"
        grid[cy + 2][cx + 4] = "#"; grid[cy + 2][cx + 5] = "#"
        grid[cy + 3][cx + 2] = "#"; grid[cy + 3][cx + 3] = "D"; grid[cy + 3][cx + 4] = "#"
        grid[cy + 3][cx - 3] = "#"; grid[cy + 3][cx - 2] = "#"

    elif tilt == -1:
        grid[cy - 7][cx] = "#"; grid[cy - 7][cx + 1] = "K"; grid[cy - 7][cx + 2] = "#"
        grid[cy - 6][cx - 1] = "#"; grid[cy - 6][cx] = "B"; grid[cy - 6][cx + 1] = "C"; grid[cy - 6][cx + 2] = "D"; grid[cy - 6][cx + 3] = "#"
        
        grid[cy - 5][cx - 3] = "#"; grid[cy - 5][cx - 2] = "A"; grid[cy - 5][cx - 1] = "B"; grid[cy - 5][cx] = "B"; grid[cy - 5][cx + 1] = "C"; grid[cy - 5][cx + 2] = "D"; grid[cy - 5][cx + 3] = "#"
        grid[cy - 4][cx - 4] = "#"; grid[cy - 4][cx - 3] = "A"; grid[cy - 4][cx - 2] = "B"; grid[cy - 4][cx - 1] = "B"; grid[cy - 4][cx] = "C"; grid[cy - 4][cx + 1] = "C"; grid[cy - 4][cx + 2] = "D"; grid[cy - 4][cx + 3] = "D"; grid[cy - 4][cx + 4] = "#"
        
        grid[cy - 3][cx - 5] = "#"; grid[cy - 3][cx - 4] = "B"; grid[cy - 3][cx - 3] = "B"; grid[cy - 3][cx - 2] = "C"; grid[cy - 3][cx - 1] = "C"; grid[cy - 3][cx] = "D"; grid[cy - 3][cx + 1] = "D"; grid[cy - 3][cx + 2] = "D"; grid[cy - 3][cx + 3] = "#"
        grid[cy - 2][cx - 5] = "#"; grid[cy - 2][cx - 4] = "B"; grid[cy - 2][cx - 3] = "B"; grid[cy - 2][cx - 2] = "C"; grid[cy - 2][cx - 1] = "C"; grid[cy - 2][cx] = "D"; grid[cy - 2][cx + 1] = "D"; grid[cy - 2][cx + 2] = "D"; grid[cy - 2][cx + 3] = "#"
        
        grid[cy - 1][cx - 6] = "#"; grid[cy - 1][cx - 5] = "B"; grid[cy - 1][cx - 4] = "B"; grid[cy - 1][cx - 3] = "C"; grid[cy - 1][cx - 2] = "C"; grid[cy - 1][cx - 1] = "C"; grid[cy - 1][cx] = "D"; grid[cy - 1][cx + 1] = "D"; grid[cy - 1][cx + 2] = "D"; grid[cy - 1][cx + 3] = "D"; grid[cy - 1][cx + 4] = "#"
        grid[cy][cx - 6] = "#"; grid[cy][cx - 5] = "B"; grid[cy][cx - 4] = "B"; grid[cy][cx - 3] = "C"; grid[cy][cx - 2] = "C"; grid[cy][cx - 1] = "C"; grid[cy][cx] = "D"; grid[cy][cx + 1] = "D"; grid[cy][cx + 2] = "D"; grid[cy][cx + 3] = "D"; grid[cy][cx + 4] = "D"; grid[cy][cx + 5] = "#"
        
        grid[cy + 1][cx - 6] = "#"; grid[cy + 1][cx - 5] = "A"; grid[cy + 1][cx - 4] = "B"; grid[cy + 1][cx - 3] = "B"; grid[cy + 1][cx - 2] = "C"; grid[cy + 1][cx - 1] = "C"; grid[cy + 1][cx] = "D"; grid[cy + 1][cx + 1] = "D"; grid[cy + 1][cx + 2] = "D"; grid[cy + 1][cx + 3] = "D"; grid[cy + 1][cx + 4] = "D"; grid[cy + 1][cx + 5] = "#"
        
        grid[cy + 2][cx - 5] = "#"; grid[cy + 2][cx - 4] = "#"
        for x in range(cx - 3, cx + 4):
            grid[cy + 2][x] = "E"
        grid[cy + 2][cx + 4] = "#"; grid[cy + 2][cx + 5] = "#"
        grid[cy + 2][cx + 1] = "D"; grid[cy + 2][cx + 2] = "#"
        grid[cy + 3][cx + 1] = "#"; grid[cy + 3][cx + 2] = "D"; grid[cy + 3][cx + 3] = "#"
        grid[cy + 3][cx - 2] = "#"

    elif tilt == 2:
        grid[cy - 7][cx - 2] = "#"; grid[cy - 7][cx - 1] = "K"; grid[cy - 7][cx] = "#"
        grid[cy - 6][cx - 3] = "#"; grid[cy - 6][cx - 2] = "B"; grid[cy - 6][cx - 1] = "C"; grid[cy - 6][cx] = "D"; grid[cy - 6][cx + 1] = "#"
        
        # Specular A still upper left
        grid[cy - 5][cx - 3] = "#"; grid[cy - 5][cx - 2] = "A"; grid[cy - 5][cx - 1] = "B"; grid[cy - 5][cx] = "B"; grid[cy - 5][cx + 1] = "C"; grid[cy - 5][cx + 2] = "D"; grid[cy - 5][cx + 3] = "#"
        grid[cy - 4][cx - 3] = "#"; grid[cy - 4][cx - 2] = "A"; grid[cy - 4][cx - 1] = "B"; grid[cy - 4][cx] = "B"; grid[cy - 4][cx + 1] = "C"; grid[cy - 4][cx + 2] = "C"; grid[cy - 4][cx + 3] = "D"; grid[cy - 4][cx + 4] = "D"; grid[cy - 4][cx + 5] = "#"
        
        grid[cy - 3][cx - 2] = "#"; grid[cy - 3][cx - 1] = "B"; grid[cy - 3][cx] = "B"; grid[cy - 3][cx + 1] = "C"; grid[cy - 3][cx + 2] = "C"; grid[cy - 3][cx + 3] = "D"; grid[cy - 3][cx + 4] = "D"; grid[cy - 3][cx + 5] = "D"; grid[cy - 3][cx + 6] = "#"
        grid[cy - 2][cx - 1] = "#"; grid[cy - 2][cx] = "B"; grid[cy - 2][cx + 1] = "B"; grid[cy - 2][cx + 2] = "C"; grid[cy - 2][cx + 3] = "C"; grid[cy - 2][cx + 4] = "D"; grid[cy - 2][cx + 5] = "D"; grid[cy - 2][cx + 6] = "D"; grid[cy - 2][cx + 7] = "#"
        
        grid[cy - 1][cx - 2] = "#"; grid[cy - 1][cx - 1] = "B"; grid[cy - 1][cx] = "B"; grid[cy - 1][cx + 1] = "C"; grid[cy - 1][cx + 2] = "C"; grid[cy - 1][cx + 3] = "C"; grid[cy - 1][cx + 4] = "D"; grid[cy - 1][cx + 5] = "D"; grid[cy - 1][cx + 6] = "D"; grid[cy - 1][cx + 7] = "#"
        grid[cy][cx - 3] = "#"; grid[cy][cx - 2] = "B"; grid[cy][cx - 1] = "B"; grid[cy][cx] = "C"; grid[cy][cx + 1] = "C"; grid[cy][cx + 2] = "C"; grid[cy][cx + 3] = "D"; grid[cy][cx + 4] = "D"; grid[cy][cx + 5] = "D"; grid[cy][cx + 6] = "D"; grid[cy][cx + 7] = "#"
        
        grid[cy + 1][cx - 4] = "#"; grid[cy + 1][cx - 3] = "A"; grid[cy + 1][cx - 2] = "B"; grid[cy + 1][cx - 1] = "B"; grid[cy + 1][cx] = "C"; grid[cy + 1][cx + 1] = "C"; grid[cy + 1][cx + 2] = "D"; grid[cy + 1][cx + 3] = "D"; grid[cy + 1][cx + 4] = "D"; grid[cy + 1][cx + 5] = "D"; grid[cy + 1][cx + 6] = "D"; grid[cy + 1][cx + 7] = "#"
        
        grid[cy + 2][cx - 5] = "#"; grid[cy + 2][cx - 4] = "#"
        for x in range(cx - 3, cx + 5):
            grid[cy + 2][x] = "E"
        grid[cy + 2][cx - 3] = "#"; grid[cy + 2][cx - 2] = "D"
        grid[cy + 2][cx + 5] = "#"; grid[cy + 2][cx + 6] = "#"
        grid[cy + 3][cx - 4] = "#"; grid[cy + 3][cx - 3] = "D"; grid[cy + 3][cx - 2] = "#"
        grid[cy + 3][cx + 2] = "#"; grid[cy + 3][cx + 3] = "#"

    elif tilt == 1:
        grid[cy - 7][cx - 2] = "#"; grid[cy - 7][cx - 1] = "K"; grid[cy - 7][cx] = "#"
        grid[cy - 6][cx - 3] = "#"; grid[cy - 6][cx - 2] = "B"; grid[cy - 6][cx - 1] = "C"; grid[cy - 6][cx] = "D"; grid[cy - 6][cx + 1] = "#"
        
        grid[cy - 5][cx - 3] = "#"; grid[cy - 5][cx - 2] = "A"; grid[cy - 5][cx - 1] = "B"; grid[cy - 5][cx] = "B"; grid[cy - 5][cx + 1] = "C"; grid[cy - 5][cx + 2] = "D"; grid[cy - 5][cx + 3] = "#"
        grid[cy - 4][cx - 4] = "#"; grid[cy - 4][cx - 3] = "A"; grid[cy - 4][cx - 2] = "B"; grid[cy - 4][cx - 1] = "B"; grid[cy - 4][cx] = "C"; grid[cy - 4][cx + 1] = "C"; grid[cy - 4][cx + 2] = "D"; grid[cy - 4][cx + 3] = "D"; grid[cy - 4][cx + 4] = "#"
        
        grid[cy - 3][cx - 3] = "#"; grid[cy - 3][cx - 2] = "B"; grid[cy - 3][cx - 1] = "B"; grid[cy - 3][cx] = "C"; grid[cy - 3][cx + 1] = "C"; grid[cy - 3][cx + 2] = "D"; grid[cy - 3][cx + 3] = "D"; grid[cy - 3][cx + 4] = "D"; grid[cy - 3][cx + 5] = "#"
        grid[cy - 2][cx - 3] = "#"; grid[cy - 2][cx - 2] = "B"; grid[cy - 2][cx - 1] = "B"; grid[cy - 2][cx] = "C"; grid[cy - 2][cx + 1] = "C"; grid[cy - 2][cx + 2] = "D"; grid[cy - 2][cx + 3] = "D"; grid[cy - 2][cx + 4] = "D"; grid[cy - 2][cx + 5] = "#"
        
        grid[cy - 1][cx - 4] = "#"; grid[cy - 1][cx - 3] = "B"; grid[cy - 1][cx - 2] = "B"; grid[cy - 1][cx - 1] = "C"; grid[cy - 1][cx] = "C"; grid[cy - 1][cx + 1] = "C"; grid[cy - 1][cx + 2] = "D"; grid[cy - 1][cx + 3] = "D"; grid[cy - 1][cx + 4] = "D"; grid[cy - 1][cx + 5] = "D"; grid[cy - 1][cx + 6] = "#"
        grid[cy][cx - 5] = "#"; grid[cy][cx - 4] = "B"; grid[cy][cx - 3] = "B"; grid[cy][cx - 2] = "C"; grid[cy][cx - 1] = "C"; grid[cy][cx] = "C"; grid[cy][cx + 1] = "D"; grid[cy][cx + 2] = "D"; grid[cy][cx + 3] = "D"; grid[cy][cx + 4] = "D"; grid[cy][cx + 5] = "D"; grid[cy][cx + 6] = "#"
        
        grid[cy + 1][cx - 5] = "#"; grid[cy + 1][cx - 4] = "A"; grid[cy + 1][cx - 3] = "B"; grid[cy + 1][cx - 2] = "B"; grid[cy + 1][cx - 1] = "C"; grid[cy + 1][cx] = "C"; grid[cy + 1][cx + 1] = "D"; grid[cy + 1][cx + 2] = "D"; grid[cy + 1][cx + 3] = "D"; grid[cy + 1][cx + 4] = "D"; grid[cy + 1][cx + 5] = "D"; grid[cy + 1][cx + 6] = "#"
        
        grid[cy + 2][cx - 5] = "#"; grid[cy + 2][cx - 4] = "#"
        for x in range(cx - 3, cx + 4):
            grid[cy + 2][x] = "E"
        grid[cy + 2][cx + 4] = "#"; grid[cy + 2][cx + 5] = "#"
        grid[cy + 2][cx - 2] = "#"; grid[cy + 2][cx - 1] = "D"
        grid[cy + 3][cx - 3] = "#"; grid[cy + 3][cx - 2] = "D"; grid[cy + 3][cx - 1] = "#"
        grid[cy + 3][cx + 2] = "#"

def draw_dynamic_shadow(grid, f_idx):
    cx_table = [21, 18, 21, 24, 27, 30, 27, 24]
    sx = cx_table[f_idx]
    
    # Shadow co-contraction at extremes:
    span = 5 if f_idx in (1, 5) else 6
    
    # Dynamic bell shadow on stone floor (Y = 41..43)
    for y in (41, 42, 43):
        cur_span = span if y == 42 else span - 1
        for x in range(sx - cur_span, sx + cur_span + 1):
            if 0 <= x < W:
                grid[y][x] = "S"
                
    # Static shadows under wooden posts (Anchored at Y=44..45):
    for y in (44, 45):
        for x in range(4, 12):
            if grid[y][x] == ".": grid[y][x] = "S"
        for x in range(36, 44):
            if grid[y][x] == ".": grid[y][x] = "S"

def outline_check(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "@"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

def build_frame(f_idx):
    grid = empty_grid()
    draw_static_environment(grid)
    draw_bell_and_chain(grid, f_idx)
    draw_dynamic_shadow(grid, f_idx)
    return grid

frames = [build_frame(i) for i in range(8)]

print("\n=== VALIDATION CHECKS ===")
cx_table = [21, 18, 21, 24, 27, 30, 27, 24]
for i, fr in enumerate(frames):
    naked = outline_check(fr)
    # Check shadow center
    shadow_xs = [x for x in range(W) for y in (41, 42, 43) if fr[y][x] == "S" and 12 <= x <= 36]
    mean_sx = sum(shadow_xs) / len(shadow_xs) if shadow_xs else 0
    delta_x = cx_table[i] - 24
    print(f"Frame {i+1}:")
    print(f"  Bell X = {cx_table[i]} (Delta X = {delta_x:+d}px)")
    print(f"  Shadow mean X = {mean_sx:.1f} (Target = {cx_table[i]})")
    print(f"  Naked pixels: {len(naked)}")

# Render images
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE_RGBA:
                img.putpixel((x, y), PALETTE_RGBA[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/bell_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 8, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/bell_sheet.png")

gif_frames[0].save(
    "python/bell_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS = 125ms per frame
    loop=0
)
print("\nGenerated bell_sheet.png and bell_anim.gif successfully!")
