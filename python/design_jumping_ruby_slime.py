import os
import math
from PIL import Image

W, H = 32, 32

# Stardew Valley Style Palette:
PALETTE = {
    ".": None,
    "S": (16, 32, 24, 130),       # Ground contact shadow (Alpha 130)
    "#": (14, 42, 32, 255),       # Soft dark pine/jade outline (#0e2a20 - NO #000000!)
    
    # Translucent Jade Jelly Body
    "P": (230, 255, 245, 255),   # Specular gloss highlight (#e6fff5)
    "A": (120, 245, 195, 255),   # Bright mint/jade highlight (#78f5c3)
    "B": (40, 186, 133, 255),    # Warm vibrant emerald midtone (#28ba85)
    "C": (22, 120, 88, 255),     # Deep teal-jade body shadow (#167858)
    "D": (15, 74, 54, 255),      # Deepest underside jade shadow (#0f4a36)
    
    # Red Ruby Crystal Core
    "W": (255, 255, 255, 255),   # Pure crystal white sparkle (#ffffff)
    "R": (255, 110, 130, 255),   # Bright ruby facet highlight (#ff6e82)
    "K": (225, 35, 60, 255),     # Vibrant ruby red midtone (#e1233c)
    "M": (140, 18, 36, 255),     # Deep ruby wine shadow (#8c1224)
    "Z": (75, 8, 20, 255),       # Ruby facet dark seam (#4b0814)
}

PALETTE_HEX = {
    ".": None,
    "S": "#102018",
    "#": "#0e2a20",
    "P": "#e6fff5",
    "A": "#78f5c3",
    "B": "#28ba85",
    "C": "#167858",
    "D": "#0f4a36",
    "W": "#ffffff",
    "R": "#ff6e82",
    "K": "#e1233c",
    "M": "#8c1224",
    "Z": "#4b0814",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_shadow(grid, cx, w_half):
    for y in (27, 28):
        cur_w = w_half if y == 27 else max(2, w_half - 2)
        for x in range(cx - cur_w, cx + cur_w + 1):
            set_p(grid, x, y, "S")

# FRAME 1: IDLE / REST
def build_f1():
    g = empty_grid()
    draw_shadow(g, 16, 7)
    
    profile = {
        13: (13, 18), # W=6
        14: (11, 20), # W=10
        15: (10, 21), # W=12
        16: (9, 22),  # W=14
        17: (9, 22),  # W=14
        18: (8, 23),  # W=16
        19: (8, 23),  # W=16
        20: (8, 23),  # W=16
        21: (8, 23),  # W=16
        22: (8, 23),  # W=16
        23: (8, 23),  # W=16
        24: (9, 22),  # W=14
        25: (10, 21), # W=12
        26: (12, 19), # W=8
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y <= 15:
                set_p(g, x, y, "A")
            elif y <= 21:
                set_p(g, x, y, "B")
            elif y <= 24:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 12, 15, "P")
    set_p(g, 13, 15, "P")
    set_p(g, 11, 16, "P")
    set_p(g, 12, 16, "P")
    set_p(g, 11, 17, "A")
    
    ruby = [
        (15, 18, "Z"), (16, 18, "Z"),
        (14, 19, "Z"), (15, 19, "W"), (16, 19, "R"), (17, 19, "Z"),
        (14, 20, "Z"), (15, 20, "R"), (16, 20, "K"), (17, 20, "Z"),
        (15, 21, "Z"), (16, 21, "M"),
        (15, 22, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

# FRAME 2: SQUASH NÉN ĐÀ (BẢO TOÀN THỂ TÍCH)
def build_f2():
    g = empty_grid()
    draw_shadow(g, 16, 11)
    
    # H=8 (Y=19..26), W=22 (X=5..26)
    profile = {
        19: (9, 22),  # W=14
        20: (7, 24),  # W=18
        21: (6, 25),  # W=20
        22: (5, 26),  # W=22
        23: (5, 26),  # W=22
        24: (5, 26),  # W=22
        25: (6, 25),  # W=20
        26: (7, 24),  # W=18
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y == 19:
                set_p(g, x, y, "A")
            elif y <= 22:
                set_p(g, x, y, "B")
            elif y <= 24:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 8, 20, "P")
    set_p(g, 9, 20, "P")
    set_p(g, 10, 20, "A")
    set_p(g, 7, 21, "P")
    set_p(g, 8, 21, "A")
    
    ruby = [
        (14, 22, "Z"), (15, 22, "W"), (16, 22, "R"), (17, 22, "Z"),
        (13, 23, "Z"), (14, 23, "R"), (15, 23, "K"), (16, 23, "K"), (17, 23, "M"), (18, 23, "Z"),
        (14, 24, "Z"), (15, 24, "M"), (16, 24, "M"), (17, 24, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

# FRAME 3: LAUNCH & STRETCH
def build_f3():
    g = empty_grid()
    draw_shadow(g, 16, 4)
    
    profile = {
        6:  (14, 17), # W=4
        7:  (13, 18), # W=6
        8:  (12, 19), # W=8
        9:  (11, 20), # W=10
        10: (11, 20),
        11: (11, 20),
        12: (11, 21), # W=11
        13: (11, 21),
        14: (11, 21),
        15: (11, 21),
        16: (11, 21),
        17: (11, 21),
        18: (11, 21),
        19: (11, 20),
        20: (12, 20),
        21: (12, 19),
        22: (12, 19),
        23: (13, 18),
        24: (13, 18),
        25: (14, 17),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y <= 10:
                set_p(g, x, y, "A")
            elif y <= 18:
                set_p(g, x, y, "B")
            elif y <= 22:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 13, 8, "P")
    set_p(g, 14, 8, "P")
    set_p(g, 13, 9, "P")
    set_p(g, 12, 10, "P")
    set_p(g, 12, 11, "A")
    set_p(g, 12, 12, "A")
    
    ruby = [
        (15, 13, "Z"), (16, 13, "Z"),
        (15, 14, "W"), (16, 14, "R"),
        (14, 15, "Z"), (15, 15, "R"), (16, 15, "K"), (17, 15, "Z"),
        (14, 16, "Z"), (15, 16, "K"), (16, 16, "M"), (17, 16, "Z"),
        (15, 17, "M"), (16, 17, "M"),
        (15, 18, "Z"), (16, 18, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

# FRAME 4: APEX
def build_f4():
    g = empty_grid()
    draw_shadow(g, 16, 3)
    
    profile = {
        3:  (12, 19), # W=8
        4:  (11, 20), # W=10
        5:  (10, 21), # W=12
        6:  (9, 22),  # W=14
        7:  (9, 22),
        8:  (9, 22),
        9:  (9, 22),
        10: (9, 22),
        11: (9, 22),
        12: (10, 21),
        13: (10, 21),
        14: (11, 20),
        15: (11, 20),
        16: (12, 19),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y <= 6:
                set_p(g, x, y, "A")
            elif y <= 11:
                set_p(g, x, y, "B")
            elif y <= 14:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 12, 5, "P")
    set_p(g, 13, 5, "P")
    set_p(g, 11, 6, "P")
    set_p(g, 12, 6, "A")
    set_p(g, 11, 7, "A")
    
    ruby = [
        (15, 8, "Z"), (16, 8, "Z"),
        (14, 9, "Z"), (15, 9, "W"), (16, 9, "R"), (17, 9, "Z"),
        (14, 10, "Z"), (15, 10, "R"), (16, 10, "K"), (17, 10, "Z"),
        (15, 11, "Z"), (16, 11, "M"),
        (15, 12, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

# FRAME 5: IMPACT SQUASH (BẢO TOÀN THỂ TÍCH)
def build_f5():
    g = empty_grid()
    draw_shadow(g, 16, 12)
    
    # H=7 (Y=20..26), W=24 (X=4..27)
    profile = {
        20: (8, 23),  # W=16
        21: (6, 25),  # W=20
        22: (4, 27),  # W=24
        23: (4, 27),  # W=24
        24: (4, 27),  # W=24
        25: (5, 26),  # W=22
        26: (6, 25),  # W=20
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y == 20:
                set_p(g, x, y, "A")
            elif y <= 22:
                set_p(g, x, y, "B")
            elif y <= 24:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 7, 21, "P")
    set_p(g, 8, 21, "P")
    set_p(g, 9, 21, "A")
    set_p(g, 6, 22, "P")
    set_p(g, 7, 22, "A")
    
    ruby = [
        (13, 23, "Z"), (14, 23, "W"), (15, 23, "R"), (16, 23, "R"), (17, 23, "K"), (18, 23, "Z"),
        (12, 24, "Z"), (13, 24, "R"), (14, 24, "K"), (15, 24, "K"), (16, 24, "M"), (17, 24, "M"), (18, 24, "Z"),
        (14, 25, "Z"), (15, 25, "M"), (16, 25, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

# FRAME 6: RECOVERY
def build_f6():
    g = empty_grid()
    draw_shadow(g, 16, 7)
    
    profile = {
        11: (13, 18), # W=6
        12: (11, 20), # W=10
        13: (10, 21), # W=12
        14: (9, 22),  # W=14
        15: (9, 22),
        16: (9, 23),  # W=15
        17: (9, 23),
        18: (9, 23),
        19: (9, 23),
        20: (9, 23),
        21: (9, 22),
        22: (10, 22),
        23: (10, 21),
        24: (11, 20),
        25: (13, 18),
    }
    for y, (x1, x2) in profile.items():
        set_p(g, x1, y, "#")
        set_p(g, x2, y, "#")
        for x in range(x1 + 1, x2):
            if y <= 13:
                set_p(g, x, y, "A")
            elif y <= 19:
                set_p(g, x, y, "B")
            elif y <= 22:
                set_p(g, x, y, "C")
            else:
                set_p(g, x, y, "D")
                
    set_p(g, 12, 13, "P")
    set_p(g, 13, 13, "P")
    set_p(g, 11, 14, "P")
    set_p(g, 12, 14, "A")
    set_p(g, 11, 15, "A")
    
    ruby = [
        (15, 17, "Z"), (16, 17, "Z"),
        (14, 18, "Z"), (15, 18, "W"), (16, 18, "R"), (17, 18, "Z"),
        (14, 19, "Z"), (15, 19, "R"), (16, 19, "K"), (17, 19, "Z"),
        (15, 20, "Z"), (16, 20, "M"),
        (15, 21, "Z"),
    ]
    for x, y, c in ruby:
        set_p(g, x, y, c)
        
    return g

frames = [build_f1(), build_f2(), build_f3(), build_f4(), build_f5(), build_f6()]

print("--- VALIDATION CHECKS ---")
for i, f in enumerate(frames):
    total_solid = 0
    ruby_count = 0
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            if c not in (".", "S"):
                total_solid += 1
            if c in ("W", "R", "K", "M", "Z"):
                ruby_count += 1
                for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
                    nx, ny = x + dx, y + dy
                    assert 0 <= nx < W and 0 <= ny < H, f"Ruby pixel at edge ({x},{y})"
                    assert f[ny][nx] != ".", f"Ruby pixel ({x},{y}) touches transparent background in frame {i+1}!"
                    
    print(f"Frame {i+1}: Total solid pixels = {total_solid}, Ruby pixels = {ruby_count}")

os.makedirs("test", exist_ok=True)
images = []
for idx, f in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            val = PALETTE.get(c)
            if val:
                img.putpixel((x, y), val)
    img.save(f"test/slime_f{idx+1}.png")
    images.append(img)

images[0].save(
    "test/slime_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=125,
    loop=0,
    disposal=2
)

print("Balanced volume slime test frames generated successfully.")
