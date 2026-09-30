import os
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

# FreeStyle Cyan-Teal Energy Crystal + Blinding Lightning Core
PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (16, 22, 28, 130),    # Ground Contact Shadow
    
    # Ground Stone Pedestal
    'D': (20, 24, 32, 255),    # Stone Dark Outline / Fissure Chasm (#141820)
    'B': (38, 48, 60, 255),    # Stone Dark Midtone (#26303c)
    'M': (65, 80, 100, 255),   # Stone Midtone (#415064)
    'H': (105, 125, 150, 255), # Stone Highlight (#697d96)
    
    # Crystal Pillar Facets (Hexagonal Prism)
    'c': (12, 45, 58, 255),    # Crystal Deep Dark Shadow (#0c2d3a)
    'C': (20, 80, 102, 255),   # Crystal Dark Facet (#145066)
    'E': (35, 140, 175, 255),  # Crystal Midtone Facet (#238caf)
    'F': (75, 205, 240, 255),  # Crystal Bright Lit Facet (#4bcdb0)
    'A': (170, 242, 255, 255), # Crystal Top Specular Glint (#aaf2ff)
    
    # Fractal Lightning & Glowing Core
    'v': (10, 95, 120, 255),   # Dim Residual Crack Glow
    'Q': (0, 225, 255, 255),   # Electric Cyan Neon Arc (#00e1ff)
    'L': (140, 245, 255, 255), # Radiant Electric Light (#8cf5ff)
    'W': (255, 255, 255, 255), # Blinding White Lightning Core (#ffffff)
    
    # OSL Glow on rock/crystal surface
    'o': (30, 120, 145, 255),  # OSL Mid Cyan Tint
    'O': (80, 215, 245, 255),  # OSL Intense Cyan Flash
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_crystal_frame(f):
    grid = create_grid()
    
    # Quiver shift (Rung lắc khi nứt):
    dx_shifts = [0, 1, -1, 0, 1, 0]
    sx = dx_shifts[f]
    cx = 24 + sx
    
    # Pedestal Shadow: Clean flattened oval at Y = 41..43
    for x in range(14, 34):
        grid[41][x] = 'S'
    for x in range(12, 36):
        grid[42][x] = 'S'
    for x in range(16, 32):
        grid[43][x] = 'S'

    # Stepped Stone Base Pedestal
    for y in [39, 40]:
        for x in range(14 + sx, 34 + sx):
            if x == 14 + sx or x == 33 + sx or y == 40:
                grid[y][x] = 'D'
            elif x < 18 + sx:
                grid[y][x] = 'B'
            elif x > 29 + sx:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'
                
    for y in [37, 38]:
        for x in range(16 + sx, 32 + sx):
            if x == 16 + sx or x == 31 + sx:
                grid[y][x] = 'D'
            elif x < 19 + sx:
                grid[y][x] = 'B'
            elif x > 28 + sx:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'

    # Hexagonal Crystal Pillar Body
    # Top apex tip at (cx, 8)
    # Beveled crystal crown at Y = 9..12
    # Vertical body at Y = 13..36, width 14px (x from cx-6 to cx+7)
    
    # Top Peak Pyramidal Crown
    crown_rows = [
        (8, 0, 0),
        (9, -1, 1),
        (10, -3, 3),
        (11, -5, 5),
        (12, -6, 6)
    ]
    for y, dx0, dx1 in crown_rows:
        for dx in range(dx0, dx1 + 1):
            x = cx + dx
            if dx == dx0 or dx == dx1 or y == 8:
                grid[y][x] = 'c'
            elif dx < 0:
                grid[y][x] = 'C'
            elif dx == 0:
                grid[y][x] = 'A' if y <= 10 else 'E'
            else:
                grid[y][x] = 'F'
                
    # Vertical Pillar Body (Y = 13..36)
    for y in range(13, 37):
        for dx in range(-6, 8):
            x = cx + dx
            if dx == -6 or dx == 7:
                grid[y][x] = 'c' # Dark outline
            elif dx < -1:
                # Left facet (Shadow side)
                grid[y][x] = 'C' if dx < -3 else 'E'
            elif dx in [-1, 0]:
                # Center ridge line
                grid[y][x] = 'F' if y % 4 != 0 else 'E'
            else:
                # Right facet (Lit side)
                grid[y][x] = 'A' if dx > 4 else 'F'

    # ========================================================
    # FRACTURE & LIGHTNING DYNAMICS (PERMANENT FISSURES!)
    # Rule 4: Fracture Persistence in Loops + Sharp Branching
    # ========================================================
    
    # Main vertical cleavage (sharp zigzag 1-2-1):
    main_fissure = [
        (15, -1), (16, -1), (17, 0), (18, 0), (19, 0),
        (20, 1), (21, 1), (22, 1), (23, 2), (24, 2),
        (25, 2), (26, 1), (27, 1), (28, 0), (29, 0),
        (30, -1), (31, -1), (32, -1), (33, 0), (34, 0), (35, 1), (36, 1)
    ]
    # Sharp Branch 1 (angle ~45 deg down-left):
    branch_left = [
        (22, 0), (23, -1), (24, -2), (25, -3), (26, -4), (27, -4)
    ]
    # Sharp Branch 2 (angle ~45 deg down-right):
    branch_right = [
        (27, 2), (28, 3), (29, 4), (30, 5), (31, 5)
    ]
    # Pedestal Ground Crack:
    ground_crack = [
        (37, 1), (38, 2), (39, 2), (40, 3)
    ]

    # Frame 0: Dormant / Rest. Persistent dark fissure lines already etched into crystal.
    if f == 0:
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'c'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'c'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'c'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'D'
        # Tiny residual energy hum in core
        grid[22][cx + 1] = 'v'; grid[23][cx + 2] = 'v'

    # Frame 1: Seismic Quiver. Crack begins to glow electric cyan from deep core.
    elif f == 1:
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'Q'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'v'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'v'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'c'
        # Core bright electric
        grid[21][cx + 1] = 'L'; grid[22][cx + 1] = 'L'; grid[23][cx + 2] = 'L'
        # OSL on crystal edges
        grid[21][cx + 2] = 'o'; grid[22][cx + 2] = 'o'

    # Frame 2: Fracture Burst! Main fissure splits open, bright core white-cyan
    elif f == 2:
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'L'
            grid[y][cx + dx + 1] = 'Q'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'Q'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'Q'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'Q'
        # White electrical surge in core
        for y in range(20, 26):
            grid[y][cx + 1] = 'W'
        # OSL blooms
        for y in range(19, 27):
            grid[y][cx - 1] = 'o'; grid[y][cx + 3] = 'O'

    # Frame 3: LIGHTNING DISCHARGE APEX! Blinding lightning bolt arcs into sky!
    elif f == 3:
        # Fissures fully ionized with blinding core
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'W'
            grid[y][cx + dx + 1] = 'L'
            grid[y][cx + dx - 1] = 'Q'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'L'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'L'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'L'
            
        # FRACTAL LIGHTNING BOLT SHOOTING INTO SKY (from crystal apex (cx, 8)):
        # Main bolt zig-zag: (cx, 8) -> (cx-2, 6) -> (cx-1, 4) -> (cx-4, 2) -> (cx-5, 0)
        bolt_main = [
            (7, 0), (6, -1), (5, -2), (4, -1), (3, -2), (2, -3), (1, -4), (0, -4)
        ]
        for y, dx in bolt_main:
            grid[y][cx + dx] = 'W'
            grid[y][cx + dx + 1] = 'Q'
            if y > 1:
                grid[y][cx + dx - 1] = 'L'
        # Forked branch right: (4, -1) -> (3, 1) -> (2, 3) -> (1, 4)
        fork_right = [
            (3, 1), (2, 2), (2, 3), (1, 4), (0, 5)
        ]
        for y, dx in fork_right:
            grid[y][cx + dx] = 'L'
            grid[y][cx + dx - 1] = 'W'
            
        # Floating electric sparks (particles)
        grid[11][cx - 4] = 'W'; grid[10][cx + 5] = 'L'
        grid[18][cx - 5] = 'Q'; grid[26][cx + 5] = 'W'
        
        # Intense OSL across entire pillar
        for y in range(13, 30):
            grid[y][cx - 2] = 'O'
            grid[y][cx + 3] = 'O'

    # Frame 4: After-strike Ionization. Bolt dissipates into sparks, crack crackles
    elif f == 4:
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'L'
            grid[y][cx + dx + 1] = 'Q'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'Q'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'Q'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'Q'
            
        # Lingering bolt sparks in sky
        grid[3][cx - 2] = 'L'; grid[1][cx - 4] = 'Q'
        grid[2][cx + 3] = 'L'; grid[12][cx - 3] = 'W'
        grid[24][cx + 4] = 'Q'
        
        # Core still hot white
        grid[22][cx + 1] = 'W'; grid[23][cx + 1] = 'W'
        for y in range(21, 26):
            grid[y][cx + 2] = 'o'

    # Frame 5: Persistent Fissure & Cooldown. Fissures remain permanently etched!
    elif f == 5:
        # Fissure channel lines remain completely visible!
        for y, dx in main_fissure:
            grid[y][cx + dx] = 'c'
        for y, dx in branch_left:
            grid[y][cx + dx] = 'c'
        for y, dx in branch_right:
            grid[y][cx + dx] = 'c'
        for y, dx in ground_crack:
            grid[y][cx + dx] = 'D'
            
        # Residual pulsing cyan current in deep crack
        grid[19][cx] = 'v'; grid[20][cx + 1] = 'Q'; grid[21][cx + 1] = 'L'
        grid[22][cx + 1] = 'Q'; grid[23][cx + 2] = 'v'
        grid[25][cx - 2] = 'v'; grid[29][cx + 4] = 'v'
        
    return grid

def generate_frames():
    return [draw_crystal_frame(f) for f in range(NUM_FRAMES)]

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (14, 18, 24, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/crystal_f{i+1}.png')
        
    sheet.save('test/crystal_preview_dark.png')
    print("Energy crystal pillar frames generated and saved to test/crystal_preview_dark.png")
