import os
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (20, 20, 32, 130),    # Floor Contact Shadow
    
    # Chrome Metallic Body
    'D': (18, 20, 32, 255),    # Metal Dark Shadow / Seam Line (#121420)
    'B': (48, 54, 76, 255),    # Metal Deep Steel (#30364c)
    'M': (110, 122, 150, 255), # Metal Midtone Steel (#6e7a96)
    'H': (190, 205, 230, 255), # Metal Bright Specular (#becde6)
    'W': (255, 255, 255, 255), # Pure White Glint (#ffffff)
    
    # Brass / Copper Mechanical Trim
    'c': (140, 75, 30, 255),   # Copper Dark
    'C': (220, 150, 60, 255),  # Copper Bright Accent
    
    # Glowing Cyan Lens & Iris
    'k': (8, 30, 45, 255),     # Deep Eye Socket / Aperture Dark
    'q': (10, 100, 140, 255),  # Cyan Lens Rim Dark
    'Q': (0, 210, 255, 255),   # Cyan Neon Iris Glowing (#00d2ff)
    'I': (150, 245, 255, 255), # Bright Cyan Pupil Core (#96f5ff)
    'P': (255, 60, 90, 255),   # Red Tracking Target Dot (#ff3c5a)
    'R': (0, 210, 255, 80),    # Scan Beam Cone Light
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_drone_frame(f):
    grid = create_grid()
    
    # HOVER BOBBING DYNAMIC (Rule 3 in Kinematics):
    # Prominent Z-axis oscillation between frames
    # f = 0: cy = 19
    # f = 1: cy = 18 (rising)
    # f = 2: cy = 17 (Apex peak height)
    # f = 3: cy = 18 (gliding down)
    # f = 4: cy = 21 (Blink + inertia drop low)
    # f = 5: cy = 20 (recovering)
    cy_list = [19, 18, 17, 18, 21, 20]
    cy = cy_list[f]
    cx = 24
    
    # AERIAL ELLIPSE SHADOW (Rule 3 in Spatial Perspective):
    # NEVER a flat rectangle bar [_____]!
    # MUST be a smooth flattened ellipse (ratio Y/X approx 0.3 - 0.4, tapering at ends)
    # Width scales inversely with height:
    # At cy = 17 (Apex): radius_x = 6, height = 3 (Y = 42..44)
    # At cy = 21 (Low): radius_x = 8, height = 4 (Y = 41..44)
    rx_list = [7, 6, 5, 6, 8, 7]
    rx = rx_list[f]
    
    # Draw curved oval shadow
    # Top arc
    for x in range(cx - rx + 2, cx + rx - 1):
        grid[41][x] = 'S'
    # Middle widest
    for x in range(cx - rx, cx + rx + 1):
        grid[42][x] = 'S'
    for x in range(cx - rx + 1, cx + rx):
        grid[43][x] = 'S'
    # Bottom arc
    for x in range(cx - rx + 2, cx + rx - 1):
        grid[44][x] = 'S'

    # Outer Spherical Hull (radius ~10px)
    hull_rows = [
        (-9, -4, 4),
        (-8, -6, 6),
        (-7, -7, 7),
        (-6, -8, 8),
        (-5, -9, 9),
        (-4, -9, 9),
        (-3, -10, 10),
        (-2, -10, 10),
        (-1, -10, 10),
        (0, -10, 10),
        (1, -10, 10),
        (2, -10, 10),
        (3, -10, 10),
        (4, -9, 9),
        (5, -9, 9),
        (6, -8, 8),
        (7, -7, 7),
        (8, -6, 6),
        (9, -4, 4)
    ]
    
    for dy, dx0, dx1 in hull_rows:
        y = cy + dy
        for dx in range(dx0, dx1 + 1):
            x = cx + dx
            if dx == dx0 or dx == dx1 or dy in [-9, 9]:
                grid[y][x] = 'D'
            elif dx < -5 or dy > 4:
                grid[y][x] = 'B'
            elif dx > 4 and dy < -3:
                grid[y][x] = 'W' if (dx > 6 and dy < -5) else 'H'
            elif dx > 2:
                grid[y][x] = 'H'
            else:
                grid[y][x] = 'M'
                
    # Panel grooves
    for dx in range(-7, 8):
        grid[cy - 6][cx + dx] = 'D'
        grid[cy + 6][cx + dx] = 'D'
        
    # Brass Rivets
    grid[cy - 6][cx - 6] = 'C'; grid[cy - 6][cx + 6] = 'C'
    grid[cy + 6][cx - 6] = 'C'; grid[cy + 6][cx + 6] = 'C'
    
    # Antenna & Thrusters
    grid[cy - 10][cx] = 'D'; grid[cy - 11][cx] = 'D'; grid[cy - 12][cx] = 'C'; grid[cy - 13][cx] = 'W'
    grid[cy][cx - 11] = 'D'; grid[cy - 1][cx - 12] = 'C'; grid[cy + 1][cx - 12] = 'c'
    grid[cy][cx + 11] = 'D'; grid[cy - 1][cx + 12] = 'C'; grid[cy + 1][cx + 12] = 'c'

    # Aperture
    aperture_rows = [
        (-4, -2, 2),
        (-3, -4, 4),
        (-2, -5, 5),
        (-1, -5, 5),
        (0, -5, 5),
        (1, -5, 5),
        (2, -5, 5),
        (3, -4, 4),
        (4, -2, 2)
    ]
    
    if f == 4:
        # Blink shutter closure
        for dy, dx0, dx1 in aperture_rows:
            y = cy + dy
            for dx in range(dx0, dx1 + 1):
                x = cx + dx
                if dy == 0:
                    grid[y][x] = 'D'
                elif dy < 0:
                    grid[y][x] = 'M' if dy > -3 else 'B'
                else:
                    grid[y][x] = 'B' if dy < 3 else 'D'
        grid[cy][cx - 1] = 'P'; grid[cy][cx] = 'P'; grid[cy][cx + 1] = 'P'
        return grid
        
    for dy, dx0, dx1 in aperture_rows:
        y = cy + dy
        for dx in range(dx0, dx1 + 1):
            x = cx + dx
            if dx == dx0 or dx == dx1 or dy in [-4, 4]:
                grid[y][x] = 'k'
            else:
                grid[y][x] = 'q'
                
    if f == 0:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                grid[cy + dy][cx + dx] = 'Q'
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                grid[cy + dy][cx + dx] = 'I'
        grid[cy][cx] = 'P'
        grid[cy - 2][cx + 2] = 'W'
        
    elif f == 1:
        for dy in range(-2, 3):
            for dx in range(-4, 0):
                grid[cy + dy][cx + dx] = 'Q'
        for dy in range(-1, 2):
            for dx in range(-3, -1):
                grid[cy + dy][cx + dx] = 'I'
        grid[cy][cx - 2] = 'P'
        grid[cy - 2][cx - 1] = 'W'
        
    elif f == 2:
        for dy in range(-2, 3):
            for dx in range(0, 4):
                grid[cy + dy][cx + dx] = 'Q'
        for dy in range(-1, 2):
            for dx in range(1, 3):
                grid[cy + dy][cx + dx] = 'I'
        grid[cy][cx + 2] = 'P'
        grid[cy - 2][cx + 3] = 'W'
        
    elif f == 3:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                grid[cy + dy][cx + dx] = 'Q'
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                grid[cy + dy][cx + dx] = 'I'
        grid[cy][cx] = 'P'; grid[cy - 1][cx] = 'P'; grid[cy + 1][cx] = 'P'; grid[cy][cx - 1] = 'P'; grid[cy][cx + 1] = 'P'
        grid[cy - 2][cx + 2] = 'W'
        grid[cy + 6][cx] = 'Q'
        grid[cy + 7][cx - 1] = 'Q'; grid[cy + 7][cx] = 'I'; grid[cy + 7][cx + 1] = 'Q'

    elif f == 5:
        for dy in range(-1, 2):
            for dx in range(-3, 4):
                grid[cy + dy][cx + dx] = 'Q'
        grid[cy][cx - 1] = 'I'; grid[cy][cx] = 'P'; grid[cy][cx + 1] = 'I'
        grid[cy - 1][cx + 1] = 'W'
        
    return grid

def generate_frames():
    return [draw_drone_frame(f) for f in range(NUM_FRAMES)]

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (16, 16, 24, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/mecha_eye_f{i+1}.png')
        
    sheet.save('test/mecha_eye_preview_dark.png')
    print("Mecha eyeball updated with rounded aerial ellipse shadow and dynamic hover bobbing!")
