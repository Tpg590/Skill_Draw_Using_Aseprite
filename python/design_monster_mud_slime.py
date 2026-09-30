import os
from PIL import Image

WIDTH = 32
HEIGHT = 48
NUM_FRAMES = 8

# Terraria Gritty Toxic Mud Slime
# Deep dark obsidian outline (#0e140c), Toxic green hue-shifting (#123010 -> #358020 -> #75d428 -> #c5ff40)
PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (14, 18, 12, 140),    # Floor Contact Shadow
    
    # Toxic Mud / Organic Slime Body
    'D': (14, 20, 12, 255),    # Deep Slime Outline / Dark Chasm (#0e140c)
    'B': (28, 55, 20, 255),    # Dark Toxic Green Shadow (#1c3714)
    'M': (55, 115, 32, 255),   # Slime Midtone Olive Green (#377320)
    'G': (110, 195, 42, 255),  # Slime SSS Saturated Peak Green (#6ec32a)
    'H': (180, 245, 60, 255),  # Slime Highlight Lime (#b4f53c)
    'W': (235, 255, 160, 255), # Slime Specular Glint (#ebffa0)
    
    # Monster Nucleus / Eyeball inside slime
    'k': (10, 10, 15, 255),    # Eye Socket Dark
    'R': (220, 40, 50, 255),   # Evil Red Iris (#dc2832)
    'Y': (255, 220, 60, 255),  # Sclera Yellow (#ffdc3c)
    'p': (255, 255, 255, 255), # Eye Glint
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_slime_frame(f):
    grid = create_grid()
    cx = 16
    floor_y = 42
    
    # 8 Frames Dynamics:
    # f = 0: Freefall Stretch (apex fall)
    # f = 1: Ground Impact 1 (Maximum Squash)
    # f = 2: Rebound Bounce 1 (High air)
    # f = 3: Freefall 2
    # f = 4: Ground Impact 2 (Medium Squash)
    # f = 5: Rebound Bounce 2 (Low air hop)
    # f = 6: Settle Land (Breathing In)
    # f = 7: Idle Squat (Breathing Out)
    
    # Parameters for each frame: (base_y, width, height, shadow_rx)
    # Area conservation check: W * H approx 100 - 130
    motion_params = [
        # base_y, half_w, half_h, shadow_rx
        (26, 4, 8, 3),   # f=0: Stretch (W=8, H=16, base_y=26 -> air high, shadow rx=3)
        (42, 9, 3, 10),  # f=1: Impact Squash (W=18, H=6, flat on floor, shadow rx=10)
        (32, 4, 6, 4),   # f=2: Rebound 1 (W=8, H=12, base_y=32 -> 10px above floor, shadow rx=4)
        (38, 4, 7, 5),   # f=3: Fall 2 (W=8, H=14, base_y=38 -> 4px above floor, shadow rx=5)
        (42, 8, 4, 9),   # f=4: Impact Squash 2 (W=16, H=8, floor, shadow rx=9)
        (39, 5, 5, 6),   # f=5: Rebound 2 (W=10, H=10, base_y=39 -> 3px above floor, shadow rx=6)
        (42, 6, 5, 7),   # f=6: Settle / Breathe in (W=12, H=10, floor, shadow rx=7)
        (42, 7, 4, 8)    # f=7: Settle / Breathe out (W=14, H=8, floor, shadow rx=8)
    ]
    
    base_y, hw, hh, s_rx = motion_params[f]
    
    # Surface Shadow Lock: Floor Y = 42..44
    # Smooth ellipse bo cong 2 dau!
    for y in [42, 43]:
        for x in range(cx - s_rx, cx + s_rx + 1):
            grid[y][x] = 'S'
    for x in range(cx - s_rx + 1, cx + s_rx):
        grid[44][x] = 'S'
        grid[41][x] = 'S'

    # Draw Slime Body (Deformed Organic Ellipse)
    # Centered at (cx, base_y - hh)
    center_y = base_y - hh
    
    for dy in range(-hh, hh + 1):
        y = center_y + dy
        if y < 0 or y >= HEIGHT:
            continue
        # Oval width at this vertical slice
        if hh == 0:
            cur_w = hw
        else:
            norm_y = abs(dy) / float(hh)
            cur_w = int(hw * (1.0 - norm_y**2 * 0.7)**0.5 + 0.5)
            
        for dx in range(-cur_w, cur_w + 1):
            x = cx + dx
            if x < 0 or x >= WIDTH:
                continue
                
            # Outline
            if dx in [-cur_w, cur_w] or dy in [-hh, hh]:
                grid[y][x] = 'D'
            elif dx < -cur_w // 2 or dy > hh // 3:
                grid[y][x] = 'B' # Shadow side
            elif dx > cur_w // 3 and dy < -hh // 4:
                grid[y][x] = 'W' if (dx > cur_w // 2 and dy < -hh // 2) else 'H'
            elif dx >= 0 and dy <= 0:
                grid[y][x] = 'G' # SSS Terminator peak
            else:
                grid[y][x] = 'M' # Midtone

    # Monster Evil Eye inside slime
    # Eye position tracked with slime center
    eye_y = center_y
    eye_x = cx
    
    # Eye drawn only if slime is tall enough (>= 6px)
    if hh >= 3:
        # Eye socket
        grid[eye_y - 1][eye_x - 1] = 'D'; grid[eye_y - 1][eye_x] = 'D'; grid[eye_y - 1][eye_x + 1] = 'D'
        grid[eye_y][eye_x - 2] = 'D'; grid[eye_y][eye_x - 1] = 'Y'; grid[eye_y][eye_x] = 'R'; grid[eye_y][eye_x + 1] = 'Y'; grid[eye_y][eye_x + 2] = 'D'
        grid[eye_y + 1][eye_x - 1] = 'D'; grid[eye_y + 1][eye_x] = 'D'; grid[eye_y + 1][eye_x + 1] = 'D'
        # Glint
        grid[eye_y][eye_x] = 'p'
    elif hh == 2: # Squashed eye slit
        grid[eye_y][eye_x - 2] = 'D'; grid[eye_y][eye_x - 1] = 'R'; grid[eye_y][eye_x] = 'p'; grid[eye_y][eye_x + 1] = 'R'; grid[eye_y][eye_x + 2] = 'D'
        
    return grid

def generate_frames():
    return [draw_slime_frame(f) for f in range(NUM_FRAMES)]

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (16, 20, 16, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/slime_f{i+1}.png')
        
    sheet.save('test/slime_preview_dark.png')
    print("Monster mud slime frames generated and saved to test/slime_preview_dark.png")
