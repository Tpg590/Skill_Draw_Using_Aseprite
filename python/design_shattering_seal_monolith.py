import os
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (22, 18, 30, 130),    # Floor Contact Shadow
    
    # Ancient Stone Monolith (Rough Matte Slate Purple)
    'D': (28, 24, 40, 255),    # Stone Deep Shadow / Fissure Chasm (#1c1828)
    'B': (48, 42, 64, 255),    # Stone Dark Midtone (#302a40)
    'M': (76, 70, 98, 255),    # Stone Midtone (#4c4662)
    'H': (116, 110, 145, 255), # Stone Highlight (#746e91)
    'R': (42, 65, 55, 255),    # Ancient Moss Patina (#2a4137)
    
    # Void Purple Energy Leak & OSL
    'v': (75, 10, 100, 255),   # Deep Purple Core Void (#4b0a64)
    'V': (160, 25, 210, 255),  # Vivid Purple Neon Energy (#a019d2)
    'L': (225, 75, 255, 255),  # Radiant Magenta-Violet Glow (#e14bff)
    'Y': (250, 180, 255, 255), # White-Violet Energy Core (#fab4ff)
    'W': (255, 255, 255, 255), # Pure White Glint (#ffffff)
    
    # Stone OSL Tint (Illuminated by Purple Energy)
    'o': (115, 60, 125, 255),  # OSL Dark Purple Stone Tint (#733c7d)
    'O': (175, 105, 185, 255), # OSL Bright Purple Stone Tint (#af69b9)
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_monolith_frame(f):
    grid = create_grid()
    
    # Quiver shift (Rung lắc địa chấn):
    dx_shifts = [0, 1, -1, 0, 1, 0]
    sx = dx_shifts[f]
    
    # Clean Rounded Base Pedestal Shadow (NO side ears! Smooth curved oval):
    # Y = 41: width 20 (X in [14, 33])
    # Y = 42: width 24 (X in [12, 35])
    # Y = 43: width 18 (X in [15, 32])
    for x in range(14, 34):
        grid[41][x] = 'S'
    for x in range(12, 36):
        grid[42][x] = 'S'
    for x in range(15, 33):
        grid[43][x] = 'S'

    # Stone Base Pedestal (Clean stepped oval, no ugly sticking ears!)
    # Top step: Y = 37..38, X = 16..31
    # Bottom step: Y = 39..40, X = 14..33
    for y in [39, 40]:
        for x in range(14 + sx, 34 + sx):
            if x == 14 + sx or x == 33 + sx or y == 40:
                grid[y][x] = 'D'
            elif x < 17 + sx:
                grid[y][x] = 'B'
            elif x > 30 + sx:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'
                
    for y in [37, 38]:
        for x in range(16 + sx, 32 + sx):
            if x == 16 + sx or x == 31 + sx:
                grid[y][x] = 'D'
            elif x < 18 + sx:
                grid[y][x] = 'B'
            elif x > 29 + sx:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'
                
    grid[39][16 + sx] = 'R'; grid[40][17 + sx] = 'R'; grid[39][30 + sx] = 'R'

    # Tapered Obelisk Monolith Body
    for y in range(8, 37):
        progress = (y - 8) / 29.0
        half_w = int(0.5 + progress * 5.5)
        x_left = 24 + sx - half_w
        x_right = 24 + sx + half_w
        x_mid = 24 + sx
        
        for x in range(x_left, x_right + 1):
            if x == x_left or x == x_right or y == 8:
                grid[y][x] = 'D'
            elif x < x_mid:
                grid[y][x] = 'B' if x < x_left + 2 else 'M'
            elif x == x_mid:
                grid[y][x] = 'H' if y > 12 else 'D'
            else:
                grid[y][x] = 'H' if x > x_right - 2 else 'M'

    # Carved Glyphs
    for gy in [13, 17, 21]:
        grid[gy][22 + sx] = 'D'
        grid[gy][26 + sx] = 'D'

    # ========================================================
    # RULE 4: FRACTURE PERSISTENCE IN LOOPS & BRANCHING CRACKS
    # ========================================================
    # The fissure pattern MUST follow sharp branching lightning / bird-foot lines (<60 deg).
    # NEVER wrap around the trunk like a Christmas tree ribbon!
    # Main vertical cleavage: runs from (23, 19) down to (26, 35).
    # Branch 1 (Sharp angle ~35 deg): splits at (24, 25) heading down-left to (21, 31).
    # Branch 2 (Radial ground fissure): splits through pedestal to ground at (26, 36) -> (28, 41).
    
    # Fissure geometry coordinates (Fixed for all frames! Only energy pulse changes):
    main_fault = [
        (19, 23), (20, 23), (21, 24), (22, 24), (23, 24),
        (24, 25), (25, 25), (26, 25), (27, 26), (28, 26),
        (29, 26), (30, 26), (31, 27), (32, 27), (33, 27),
        (34, 26), (35, 26)
    ]
    branch_left = [
        (25, 24), (26, 23), (27, 23), (28, 22), (29, 21), (30, 21)
    ]
    ground_radial = [
        (36, 26), (37, 27), (38, 27), (39, 28), (40, 28), (41, 29)
    ]
    
    # Permanent Fissures: Rendered across all frames!
    # Even in dormant frames, the fracture channel exists (permanence)!
    
    if f == 0:
        # Frame 1: Dormant persistent fracture. Dark chasm lines with faint resting purple in deep core.
        for y, x in main_fault:
            grid[y][x + sx] = 'D'
        for y, x in branch_left:
            grid[y][x + sx] = 'D'
        for y, x in ground_radial:
            grid[y][x + sx] = 'D'
        # Tiny residual ember in core
        grid[25][25 + sx] = 'v'; grid[26][25 + sx] = 'v'
        
    elif f == 1:
        # Frame 2: Seismic Quiver. Fissure glows purple from deep within
        for y, x in main_fault:
            grid[y][x + sx] = 'v'
        for y, x in branch_left:
            grid[y][x + sx] = 'v'
        for y, x in ground_radial:
            grid[y][x + sx] = 'D'
        # Core glowing neon
        grid[24][25 + sx] = 'V'; grid[25][25 + sx] = 'V'; grid[26][25 + sx] = 'V'
        grid[25][24 + sx] = 'V'; grid[26][23 + sx] = 'V'
        # Faint OSL on stone rim
        grid[25][26 + sx] = 'o'; grid[26][26 + sx] = 'o'
        
    elif f == 2:
        # Frame 3: Fracture Burst! Energy surges, channel widens, OSL blooms
        for y, x in main_fault:
            grid[y][x + sx] = 'V'
            grid[y][x + 1 + sx] = 'L'
        for y, x in branch_left:
            grid[y][x + sx] = 'V'
        for y, x in ground_radial:
            grid[y][x + sx] = 'V'
        # Blinding magenta-white core
        grid[24][25 + sx] = 'Y'; grid[25][25 + sx] = 'Y'; grid[26][25 + sx] = 'Y'
        grid[25][24 + sx] = 'L'; grid[26][23 + sx] = 'L'
        # OSL rock illumination
        for y, x in [(23, 25), (24, 27), (25, 27), (26, 27), (27, 28), (28, 28), (26, 22), (27, 22)]:
            grid[y][x + sx] = 'O'
            
    elif f == 3:
        # Frame 4: Apex Eruption! Core blinding White-Violet, sparks ejecting, maximum OSL
        for y, x in main_fault:
            grid[y][x + sx] = 'L'
            grid[y][x + 1 + sx] = 'Y'
        for y, x in branch_left:
            grid[y][x + sx] = 'L'
            grid[y][x + 1 + sx] = 'V'
        for y, x in ground_radial:
            grid[y][x + sx] = 'L'
        # Pure white peak energy in heart of fissure
        grid[24][25 + sx] = 'W'; grid[25][25 + sx] = 'W'; grid[26][25 + sx] = 'W'
        grid[25][26 + sx] = 'Y'; grid[26][26 + sx] = 'Y'
        # Ejected floating spark particles (1px)
        grid[17][20 + sx] = 'Y'; grid[16][19 + sx] = 'L'
        grid[22][29 + sx] = 'W'
        grid[29][18 + sx] = 'Y'
        # Massive OSL
        for y, x in [(22, 25), (23, 26), (24, 27), (25, 27), (26, 27), (27, 28), (28, 28), (25, 22), (26, 21), (27, 21)]:
            grid[y][x + sx] = 'O'
            
    elif f == 4:
        # Frame 5: Aftershock. Energy subsides, BUT FRACTURE REMAINS 100% VISIBLE!
        for y, x in main_fault:
            grid[y][x + sx] = 'V'
        for y, x in branch_left:
            grid[y][x + sx] = 'v'
        for y, x in ground_radial:
            grid[y][x + sx] = 'D'
        # Core still glowing magenta
        grid[24][25 + sx] = 'L'; grid[25][25 + sx] = 'L'; grid[26][25 + sx] = 'L'
        # Residual floating sparks
        grid[15][19 + sx] = 'V'
        # Fading OSL
        for y, x in [(24, 26), (25, 26), (26, 26)]:
            grid[y][x + sx] = 'o'
            
    elif f == 5:
        # Frame 6: Cooldown. Fracture lines fully preserved (never magically healed!), core dim purple
        for y, x in main_fault:
            grid[y][x + sx] = 'D'
        for y, x in branch_left:
            grid[y][x + sx] = 'D'
        for y, x in ground_radial:
            grid[y][x + sx] = 'D'
        # Dim pulsing purple inside crack
        grid[24][25 + sx] = 'v'; grid[25][25 + sx] = 'v'; grid[26][25 + sx] = 'v'
        grid[27][26 + sx] = 'v'; grid[28][26 + sx] = 'v'
        
    return grid

def generate_frames():
    return [draw_monolith_frame(f) for f in range(NUM_FRAMES)]

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (16, 14, 22, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/monolith_f{i+1}.png')
        
    sheet.save('test/monolith_preview_dark.png')
    print("Monolith updated with permanent sharp branching fractures and rounded pedestal shadow!")
