import os
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

# Stardew Valley Vintage Steampunk Palette (Warm, Soft Outline, NO #000000!)
PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (55, 35, 30, 110),    # Soft Ground Contact Shadow (Soft Earthy Umber)
    
    # Warm Antique Brass / Copper Body
    'D': (44, 27, 24, 255),    # Soft Walnut Dark Outline (#2c1b18 - NO #000000!)
    'B': (105, 58, 38, 255),   # Warm Shadow Bronze (#693a26)
    'M': (175, 108, 62, 255),  # Warm Brass Midtone (#af6c3e)
    'H': (228, 168, 105, 255), # Warm Brass Highlight (#e4a869)
    'A': (250, 222, 175, 255), # Warm Pale Brass Specular (#fadeaf)
    
    # Metal Belly Plate & Seams (Warm Pewter)
    'p': (80, 72, 85, 255),    # Dark Pewter (#504855)
    'P': (135, 125, 145, 255), # Mid Pewter (#877d91)
    
    # Cute Glowing Cyan Eyes
    'k': (20, 35, 45, 255),    # Eye Ring Dark
    'q': (45, 135, 165, 255),  # Cyan Eye Mid
    'Q': (85, 215, 245, 255),  # Bright Cyan Eye Glow (#55d7f5)
    'w': (235, 255, 255, 255), # Eye Sparkle Glint
    
    # Jet Thruster Flame
    'F': (245, 95, 35, 255),   # Orange Flame
    'f': (255, 215, 75, 255),  # Bright Yellow Flame Core
    
    # Warm Steam Wisps (Creamy Soft Puffs, NO slashed lines!)
    'm': (160, 155, 170, 130), # Soft Steam Base Mist
    'T': (215, 215, 228, 170), # Soft White Steam Body
    't': (250, 250, 255, 210), # Bright Steam Puff Highlight
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_bot_frame(f):
    grid = create_grid()
    cx = 24
    
    # HOVER BOBBING DYNAMIC (Kinematics Rule 1.3):
    # Smooth hovering oscillation:
    # f = 0: cy = 20
    # f = 1: cy = 19 (floating up)
    # f = 2: cy = 18 (Apex peak)
    # f = 3: cy = 19 (settling down)
    # f = 4: cy = 21 (inertia drop low)
    # f = 5: cy = 20 (recovering)
    cy_list = [20, 19, 18, 19, 21, 20]
    cy = cy_list[f]
    
    # AERIAL ELLIPSE SHADOW (Spatial Perspective Rule 3.3):
    # Flattened smooth ellipse (tapering at 2 ends)
    # Scales inversely with height:
    # At cy = 18 (Apex): rx = 5, shadow narrow
    # At cy = 21 (Low): rx = 8, shadow wide
    rx_list = [7, 6, 5, 6, 8, 7]
    rx = rx_list[f]
    
    for x in range(cx - rx + 2, cx + rx - 1):
        grid[41][x] = 'S'
    for x in range(cx - rx, cx + rx + 1):
        grid[42][x] = 'S'
    for x in range(cx - rx + 1, cx + rx):
        grid[43][x] = 'S'
    for x in range(cx - rx + 2, cx + rx - 1):
        grid[44][x] = 'S'

    # Jet Thruster Plume at base of spherical body (cy + 10)
    # Flickering flame particles
    if f % 2 == 0:
        grid[cy + 10][cx] = 'F'; grid[cy + 11][cx] = 'f'; grid[cy + 12][cx] = 'F'
        grid[cy + 11][cx - 1] = 'F'; grid[cy + 11][cx + 1] = 'F'
    else:
        grid[cy + 10][cx] = 'f'; grid[cy + 11][cx] = 'F'
        grid[cy + 10][cx - 1] = 'F'; grid[cy + 10][cx + 1] = 'F'

    # Spherical Brass Hull (radius ~9px)
    hull_rows = [
        (-8, -4, 4),
        (-7, -6, 6),
        (-6, -7, 7),
        (-5, -8, 8),
        (-4, -9, 9),
        (-3, -9, 9),
        (-2, -9, 9),
        (-1, -9, 9),
        (0, -9, 9),
        (1, -9, 9),
        (2, -9, 9),
        (3, -9, 9),
        (4, -8, 8),
        (5, -8, 8),
        (6, -7, 7),
        (7, -6, 6),
        (8, -4, 4),
        (9, -2, 2)
    ]
    
    for dy, dx0, dx1 in hull_rows:
        y = cy + dy
        for dx in range(dx0, dx1 + 1):
            x = cx + dx
            if dx == dx0 or dx == dx1 or dy in [-8, 9]:
                grid[y][x] = 'D'
            elif dx < -4 or dy > 3:
                grid[y][x] = 'B'
            elif dx > 3 and dy < -3:
                grid[y][x] = 'A' if (dx > 5 and dy < -4) else 'H'
            elif dx > 1:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'
                
    # Belly Faceplate (Pewter plate, diameter ~12px)
    for dy in range(-4, 4):
        for dx in range(-5, 6):
            if dx**2 + dy**2 <= 20:
                grid[cy + dy][cx + dx] = 'P' if dy > 0 else 'p'
                
    # Two Cute Glowing Eyes on faceplate
    # Left eye at cx - 3, Right eye at cx + 3
    for ex in [cx - 3, cx + 3]:
        # Eye circle 3x3
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                grid[cy + dy][ex + dx] = 'q'
        grid[cy][ex] = 'Q'
        grid[cy - 1][ex + 1] = 'w' # Eye glint sparkle
        
    # Small Smiling Mouth / Sensor vent
    grid[cy + 2][cx - 1] = 'D'; grid[cy + 2][cx] = 'D'; grid[cy + 2][cx + 1] = 'D'
    
    # 2 Floating Side Fins / Little Arms (Wobbling with bobbing)
    arm_dy = -1 if f in [1, 2] else (1 if f in [4, 5] else 0)
    # Left winglet
    grid[cy + arm_dy][cx - 10] = 'D'; grid[cy + arm_dy][cx - 11] = 'M'; grid[cy + arm_dy - 1][cx - 12] = 'H'
    # Right winglet
    grid[cy + arm_dy][cx + 10] = 'D'; grid[cy + arm_dy][cx + 11] = 'M'; grid[cy + arm_dy - 1][cx + 12] = 'A'

    # Top Chimney / Exhaust Pipe (at cx - 1, Y from cy - 9 up to cy - 13)
    # Brass chimney pipe with rim
    chimney_x = cx
    for y in range(cy - 12, cy - 8):
        grid[y][chimney_x - 2] = 'D'; grid[y][chimney_x - 1] = 'B'; grid[y][chimney_x] = 'M'; grid[y][chimney_x + 1] = 'D'
    # Rim top
    grid[cy - 13][chimney_x - 2] = 'D'; grid[cy - 13][chimney_x - 1] = 'H'; grid[cy - 13][chimney_x] = 'A'; grid[cy - 13][chimney_x + 1] = 'D'

    # ========================================================
    # STEAM WISPS VS SLASHED LINES (Rule 2.3 in Fluid/Gas)
    # Puffs of warm steam: Circular billowing puffs & sinuous clusters!
    # TUYỆT ĐỐI CẤM gạch chéo (/ /)!
    # ========================================================
    
    def set_steam_pixel(gx, gy, color):
        if 0 <= gy < HEIGHT and 0 <= gx < WIDTH:
            grid[gy][gx] = color

    chim_top = cy - 14
    
    if f == 0:
        # Initial small puff emerging from chimney
        for (dx, dy) in [(-1, 0), (0, 0), (1, 0), (0, -1), (-1, -1)]:
            set_steam_pixel(chimney_x + dx, chim_top + dy, 'T')
        set_steam_pixel(chimney_x, chim_top - 1, 't')
        set_steam_pixel(chimney_x + 3, chim_top - 6, 'm')
        set_steam_pixel(chimney_x + 4, chim_top - 7, 'm')
        
    elif f == 1:
        # Puff rises and billows into circular puff (radius 2px)
        puff_y = chim_top - 2
        for (dx, dy) in [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
                        (-1, -1), (0, -1), (1, -1), (0, -2)]:
            set_steam_pixel(chimney_x + dx, puff_y + dy, 'T')
        set_steam_pixel(chimney_x, puff_y - 1, 't')
        set_steam_pixel(chimney_x + 1, puff_y, 't')
        set_steam_pixel(chimney_x, chim_top, 'm')

    elif f == 2:
        # Puff billows larger (3x3 cloud) and drifts slightly right
        puff_y = chim_top - 4
        px = chimney_x + 1
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx**2 + dy**2 <= 5:
                    set_steam_pixel(px + dx, puff_y + dy, 'T')
        set_steam_pixel(px, puff_y - 1, 't')
        set_steam_pixel(px + 1, puff_y - 1, 't')
        set_steam_pixel(chimney_x, chim_top, 'T')
        set_steam_pixel(chimney_x - 1, chim_top, 'm')

    elif f == 3:
        # Large puff at apex, expanding in volume (expansion)
        puff_y = chim_top - 6
        px = chimney_x + 2
        for dy in range(-2, 3):
            for dx in range(-3, 4):
                if dx**2 + (dy*1.2)**2 <= 6:
                    set_steam_pixel(px + dx, puff_y + dy, 'T')
        set_steam_pixel(px, puff_y - 1, 't')
        set_steam_pixel(px + 1, puff_y, 't')
        set_steam_pixel(chimney_x, chim_top - 2, 'T')
        set_steam_pixel(chimney_x - 1, chim_top - 2, 'T')
        set_steam_pixel(chimney_x, chim_top - 3, 't')

    elif f == 4:
        # Apex puff dissipating into separate soft wisps
        puff_y = chim_top - 8
        px = chimney_x + 3
        for (dx, dy) in [(-1, 0), (0, 0), (1, 0), (0, -1), (1, -1), (-2, 0)]:
            set_steam_pixel(px + dx, puff_y + dy, 'T')
        set_steam_pixel(px, puff_y - 1, 't')
        set_steam_pixel(px - 2, puff_y + 1, 'm')
        set_steam_pixel(px + 2, puff_y - 2, 'm')
        set_steam_pixel(chimney_x, chim_top - 3, 'T')
        set_steam_pixel(chimney_x + 1, chim_top - 4, 't')
        set_steam_pixel(chimney_x, chim_top - 4, 'T')

    elif f == 5:
        # Apex puff fading out into 1px particles
        set_steam_pixel(chimney_x + 4, chim_top - 9, 'm')
        set_steam_pixel(chimney_x + 5, chim_top - 10, 'm')
        set_steam_pixel(chimney_x + 2, chim_top - 8, 'm')
        # Second puff expands, connecting seamlessly to Frame 0
        puff_y = chim_top - 4
        px = chimney_x + 1
        for (dx, dy) in [(-1, 0), (0, 0), (1, 0), (0, -1), (1, -1)]:
            set_steam_pixel(px + dx, puff_y + dy, 'T')
        set_steam_pixel(px, puff_y - 1, 't')

    return grid

def generate_frames():
    return [draw_bot_frame(f) for f in range(NUM_FRAMES)]

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (35, 30, 38, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/hover_bot_f{i+1}.png')
        
    sheet.save('test/hover_bot_preview_dark.png')
    print("Vintage steampunk hover bot frames generated and saved to test/hover_bot_preview_dark.png")
