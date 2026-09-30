import os
import math
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 8

# Terraria style palette: 1-character tokens for perfect 1:1 pixel mapping
PALETTE = {
    '.': (0, 0, 0, 0),             # Transparent
    'K': (6, 20, 6, 255),          # Deep dark outline (Terraria dark tone)
    'k': (14, 42, 14, 255),        # Dark crevice / inner edge
    
    # Translucent Toxic Acid Slime Body (with SSS Terminator peak 'B')
    'H': (235, 255, 175, 255),     # Specular highlight glint
    'A': (170, 255, 55, 255),      # Light translucent lime
    'B': (82, 240, 24, 255),       # SSS Saturation Peak: Neon toxic green!
    'C': (46, 168, 20, 255),       # Midtone toxic green
    'D': (25, 100, 12, 255),       # Deep shaded murky green
    'd': (13, 56, 6, 255),         # Darkest bottom slime shadow
    
    # Internal air bubbles
    'b': (150, 255, 110, 240),     # Glowing internal air bubble
    
    # Demon Eye in Core
    'W': (255, 255, 255, 255),     # Eye specular reflection
    'Y': (255, 215, 0, 255),       # Yellow demon iris
    'R': (255, 32, 32, 255),       # Fiery red pupil/sclera
    'r': (150, 10, 10, 255),       # Deep crimson eye shadow
    
    # Acid spit droplet & splatter
    'S': (230, 255, 90, 255),      # Droplet core highlight (hot acid)
    's': (80, 230, 24, 255),       # Droplet neon body
    'v': (180, 255, 140, 210),     # Acid sizzle vapor
    
    # Contact ground shadow (Locked on ground plane)
    'P': (8, 18, 6, 170),          # Dense contact shadow
    'p': (8, 18, 6, 85),           # Soft outer edge shadow
}

def create_empty_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def safe_set(grid, x, y, char):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = char

def draw_slime_body(grid, cx, cy, rx, ry):
    for dy in range(-ry, ry + 1):
        y = cy + dy
        norm_y = dy / ry
        
        # Organic slime droplet shape: narrower top, bulbous bottom
        if norm_y < 0:
            w_factor = math.sqrt(max(0, 1 - norm_y * norm_y)) * (0.85 + 0.15 * (1 + norm_y))
        else:
            w_factor = math.sqrt(max(0, 1 - norm_y * norm_y * 0.95))
            
        cur_rx = int(round(rx * w_factor))
        if cur_rx < 1:
            cur_rx = 1
            
        for dx in range(-cur_rx, cur_rx + 1):
            x = cx + dx
            norm_x = (dx + rx * 0.25) / rx
            dist_light = math.sqrt(norm_x * norm_x + (norm_y + 0.3) * (norm_y + 0.3))
            
            # SSS Shading:
            if dist_light < 0.35 and norm_y < 0.1:
                c = 'H' if (dist_light < 0.18 and norm_y < -0.1) else 'A'
            elif dist_light < 0.65:
                c = 'A'
            elif dist_light < 0.95:
                c = 'B'
            elif dist_light < 1.3:
                c = 'C'
            elif dy >= ry - 2:
                c = 'd'
            else:
                c = 'D'
                
            safe_set(grid, x, y, c)
            
    # Outline tracing
    border_pts = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] != '.':
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1), 
                               (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)):
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                        if grid[ny][nx] == '.':
                            border_pts.append((nx, ny))
                            
    for bx, by in set(border_pts):
        safe_set(grid, bx, by, 'K')

def draw_demon_eye(grid, eye_x, eye_y, eye_state=0):
    if eye_state == 1: # Squint
        eye_shape = [
            (-2, -1, 'r'), (-1, -1, 'r'), (0, -1, 'r'), (1, -1, 'r'), (2, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'Y'), (0, 0,  'Y'), (1, 0,  'R'), (2, 0,  'R'), (3, 0,  'r'),
            (-2, 1,  'r'), (-1, 1,  'R'), (0, 1,  'Y'), (1, 1,  'R'), (2, 1,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y, 'K')
        safe_set(grid, eye_x - 1, eye_y, 'W')
        
    elif eye_state == 2: # Dilated wide
        eye_shape = [
            (-2, -3, 'r'), (-1, -3, 'r'), (0, -3, 'r'), (1, -3, 'r'), (2, -3, 'r'),
            (-3, -2, 'r'), (-2, -2, 'R'), (-1, -2, 'R'), (0, -2, 'R'), (1, -2, 'R'), (2, -2, 'R'), (3, -2, 'r'),
            (-3, -1, 'r'), (-2, -1, 'R'), (-1, -1, 'Y'), (0, -1, 'Y'), (1, -1, 'Y'), (2, -1, 'R'), (3, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'Y'), (0, 0,  'Y'), (1, 0,  'Y'), (2, 0,  'R'), (3, 0,  'r'),
            (-3, 1,  'r'), (-2, 1,  'R'), (-1, 1,  'Y'), (0, 1,  'Y'), (1, 1,  'Y'), (2, 1,  'R'), (3, 1,  'r'),
            (-3, 2,  'r'), (-2, 2,  'R'), (-1, 2,  'R'), (0, 2,  'R'), (1, 2,  'R'), (2, 2,  'R'), (3, 2,  'r'),
            (-2, 3,  'r'), (-1, 3,  'r'), (0, 3,  'r'), (1, 3,  'r'), (2, 3,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y - 1, 'K')
        safe_set(grid, eye_x, eye_y, 'K')
        safe_set(grid, eye_x, eye_y + 1, 'K')
        safe_set(grid, eye_x - 1, eye_y - 1, 'W')
        
    elif eye_state == 3: # Recoil squint
        eye_shape = [
            (-2, -1, 'r'), (-1, -1, 'r'), (0, -1, 'r'), (1, -1, 'r'), (2, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'R'), (0, 0,  'R'), (1, 0,  'R'), (2, 0,  'R'), (3, 0,  'r'),
            (-2, 1,  'r'), (-1, 1,  'r'), (0, 1,  'r'), (1, 1,  'r'), (2, 1,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y, 'K')
        
    else: # Normal open
        eye_shape = [
            (-2, -2, 'r'), (-1, -2, 'r'), (0, -2, 'r'), (1, -2, 'r'), (2, -2, 'r'),
            (-3, -1, 'r'), (-2, -1, 'R'), (-1, -1, 'R'), (0, -1, 'R'), (1, -1, 'R'), (2, -1, 'R'), (3, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'Y'), (0, 0,  'Y'), (1, 0,  'R'), (2, 0,  'R'), (3, 0,  'r'),
            (-3, 1,  'r'), (-2, 1,  'R'), (-1, 1,  'Y'), (0, 1,  'Y'), (1, 1,  'R'), (2, 1,  'R'), (3, 1,  'r'),
            (-2, 2,  'r'), (-1, 2,  'R'), (0, 2,  'R'),  (1, 2,  'R'), (2, 2,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y, 'K')
        safe_set(grid, eye_x, eye_y + 1, 'K')
        safe_set(grid, eye_x - 1, eye_y - 1, 'W')

def draw_internal_bubbles(grid, cx, cy, frame_idx):
    b_offsets = [
        (-7, -4 + (frame_idx % 2)),
        (6, 1 - (frame_idx % 3)),
        (-4, 3 - ((frame_idx + 1) % 2)),
    ]
    for bx, by in b_offsets:
        safe_set(grid, cx + bx, cy + by, 'b')
        safe_set(grid, cx + bx + 1, cy + by, 'A')

def draw_acid_spit_mechanics(grid, cx, mouth_y, stage):
    # Rule: Spatial 2.2 - FORWARD REACH IN TOP-DOWN 3/4 (+Y direction towards viewer)
    # Rule: Fluid & Gas 1.2 - SỨC CĂNG BỀ MẶT & ĐỘ NHỎ GIỌT (DROPLET PINCH-OFF)
    
    if stage == 1:
        # F3: High stretch, mouth opens wide on front belly, NECK PINCHING!
        # Mouth open
        safe_set(grid, cx - 2, mouth_y, 'K')
        safe_set(grid, cx - 1, mouth_y, 'k')
        safe_set(grid, cx, mouth_y, 'd')
        safe_set(grid, cx + 1, mouth_y, 'k')
        safe_set(grid, cx + 2, mouth_y, 'K')
        
        # Neck pinching (eo thắt 1-2px)
        safe_set(grid, cx - 1, mouth_y + 1, 'K')
        safe_set(grid, cx, mouth_y + 1, 's')
        safe_set(grid, cx + 1, mouth_y + 1, 'K')
        
        safe_set(grid, cx - 1, mouth_y + 2, 'K')
        safe_set(grid, cx, mouth_y + 2, 's')
        safe_set(grid, cx + 1, mouth_y + 2, 'K')
        
        # Bulging droplet head (3x3 with highlight)
        safe_set(grid, cx - 2, mouth_y + 3, 'K')
        safe_set(grid, cx - 1, mouth_y + 3, 's')
        safe_set(grid, cx, mouth_y + 3, 'S')
        safe_set(grid, cx + 1, mouth_y + 3, 's')
        safe_set(grid, cx + 2, mouth_y + 3, 'K')
        
        safe_set(grid, cx - 2, mouth_y + 4, 'K')
        safe_set(grid, cx - 1, mouth_y + 4, 's')
        safe_set(grid, cx, mouth_y + 4, 's')
        safe_set(grid, cx + 1, mouth_y + 4, 's')
        safe_set(grid, cx + 2, mouth_y + 4, 'K')
        
        safe_set(grid, cx - 1, mouth_y + 5, 'K')
        safe_set(grid, cx, mouth_y + 5, 'K')
        safe_set(grid, cx + 1, mouth_y + 5, 'K')

    elif stage == 2:
        # F4: Neck snapped! Droplet detached & hurtling forward into foreground (+Y)
        # Mouth puckered shut with snap-back droplet
        safe_set(grid, cx - 1, mouth_y, 'k')
        safe_set(grid, cx, mouth_y, 'd')
        safe_set(grid, cx + 1, mouth_y, 'k')
        safe_set(grid, cx, mouth_y + 2, 's')
        safe_set(grid, cx, mouth_y + 3, 'K')
        
        # Detached flying droplet in foreground air at Y=41..43
        dy = 41
        safe_set(grid, cx - 1, dy, 'K')
        safe_set(grid, cx, dy, 'K')
        safe_set(grid, cx + 1, dy, 'K')
        
        safe_set(grid, cx - 2, dy + 1, 'K')
        safe_set(grid, cx - 1, dy + 1, 's')
        safe_set(grid, cx, dy + 1, 'S')
        safe_set(grid, cx + 1, dy + 1, 's')
        safe_set(grid, cx + 2, dy + 1, 'K')
        
        safe_set(grid, cx - 2, dy + 2, 'K')
        safe_set(grid, cx - 1, dy + 2, 's')
        safe_set(grid, cx, dy + 2, 's')
        safe_set(grid, cx + 1, dy + 2, 's')
        safe_set(grid, cx + 2, dy + 2, 'K')
        
        safe_set(grid, cx - 1, dy + 3, 'K')
        safe_set(grid, cx, dy + 3, 'K')
        safe_set(grid, cx + 1, dy + 3, 'K')

    elif stage == 3:
        # F5: Droplet impacts foreground floor at Y=44 (Splatter Pool!)
        impact_y = 44
        # Splatter puddle
        for dx in range(-4, 5):
            safe_set(grid, cx + dx, impact_y - 1, 'K')
            safe_set(grid, cx + dx, impact_y + 1, 'K')
        safe_set(grid, cx - 5, impact_y, 'K')
        safe_set(grid, cx + 5, impact_y, 'K')
        
        safe_set(grid, cx - 4, impact_y, 's')
        safe_set(grid, cx - 3, impact_y, 's')
        safe_set(grid, cx - 2, impact_y, 'S')
        safe_set(grid, cx - 1, impact_y, 'S')
        safe_set(grid, cx, impact_y, 'S')
        safe_set(grid, cx + 1, impact_y, 'S')
        safe_set(grid, cx + 2, impact_y, 's')
        safe_set(grid, cx + 3, impact_y, 's')
        safe_set(grid, cx + 4, impact_y, 's')
        
        # Splatter beads flying up
        safe_set(grid, cx - 4, impact_y - 2, 'S')
        safe_set(grid, cx + 4, impact_y - 2, 's')
        safe_set(grid, cx - 1, impact_y - 2, 'K')
        safe_set(grid, cx + 1, impact_y - 2, 'K')

    elif stage == 4:
        # F6: Splatter sizzles with toxic vapor
        impact_y = 44
        for dx in range(-3, 4):
            safe_set(grid, cx + dx, impact_y - 1, 'K')
            safe_set(grid, cx + dx, impact_y + 1, 'K')
        safe_set(grid, cx - 4, impact_y, 'K')
        safe_set(grid, cx + 4, impact_y, 'K')
        
        for dx in range(-3, 4):
            safe_set(grid, cx + dx, impact_y, 'S' if abs(dx) <= 1 else 's')
            
        # Vapor wisps
        safe_set(grid, cx - 2, impact_y - 2, 'v')
        safe_set(grid, cx + 2, impact_y - 2, 'v')
        safe_set(grid, cx, impact_y - 3, 'v')

    elif stage == 5:
        # F7: Final faint vapor wisp dissolving
        safe_set(grid, cx - 1, 44, 's')
        safe_set(grid, cx, 44, 's')
        safe_set(grid, cx + 1, 44, 's')
        safe_set(grid, cx, 42, 'v')
        safe_set(grid, cx + 1, 41, 'v')

def draw_ground_shadow(grid, cx, floor_y, cur_rx):
    shadow_half_w = cur_rx + 1
    for dx in range(-shadow_half_w, shadow_half_w + 1):
        if abs(dx) == shadow_half_w:
            c = 'p'
        elif abs(dx) >= shadow_half_w - 2:
            c = 'p'
        else:
            c = 'P'
        safe_set(grid, cx + dx, floor_y, c)
        
    for dx in range(-shadow_half_w + 2, shadow_half_w - 1):
        safe_set(grid, cx + dx, floor_y + 1, 'p')

def generate_frames():
    frames = []
    cx = 24
    floor_y = 40
    
    # 8 Frames Animation Profile:
    # Rule: Volume Conservation (Squash & Stretch)
    # Area W * H ~ constant
    # Baseline: rx = 12 (W=24), ry = 10 (H=20) -> Area ~ 120
    frame_configs = [
        # (rx, ry, spit_stage, eye_dy, eye_state, mouth_rel_y)
        (12, 10, 0,  0, 0, 4),   # F1: Idle breathing
        (17, 6,  0,  2, 1, 3),   # F2: Deep squash intake, eye squints
        (9,  14, 1, -4, 2, 7),   # F3: High stretch, mouth opens wide, neck pinching spit (+Y)
        (10, 12, 2, -2, 3, 5),   # F4: Recoil, droplet pinches off and flies forward (+Y)
        (12, 10, 3,  0, 0, 4),   # F5: Descending, droplet impacts foreground ground
        (15, 8,  4,  1, 1, 4),   # F6: Landing squash overshoot, splash sizzles
        (11, 11, 5, -1, 0, 4),   # F7: Rebound wobble, vapor dissolves
        (12, 10, 0,  0, 0, 4),   # F8: Cooldown settling back to F1
    ]
    
    for f_idx, (rx, ry, spit_stage, eye_dy, eye_state, mouth_rel_y) in enumerate(frame_configs):
        grid = create_empty_grid()
        cy = floor_y - ry
        
        # 1. Contact ground shadow (locked at floor_y + 1)
        draw_ground_shadow(grid, cx, floor_y + 1, rx)
        
        # 2. Translucent Slime Body
        draw_slime_body(grid, cx, cy, rx, ry)
        
        # 3. Internal Air Bubbles (Pixel Art 3.9)
        draw_internal_bubbles(grid, cx, cy, f_idx)
        
        # 4. Demon Eye at core (anchored inside body)
        eye_y = cy + eye_dy
        draw_demon_eye(grid, cx, eye_y, eye_state)
        
        # 5. Acid Spit Mechanics (+Y direction)
        mouth_y = cy + mouth_rel_y
        draw_acid_spit_mechanics(grid, cx, mouth_y, spit_stage)
        
        frames.append(grid)
        
    return frames

def render_preview_sheet(frames, filename="test/acid_slime_clot_preview.png"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sheet_w = WIDTH * NUM_FRAMES
    sheet_h = HEIGHT
    img = Image.new("RGBA", (sheet_w, sheet_h), (25, 20, 30, 255))
    
    for f_idx, grid in enumerate(frames):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                c = grid[y][x]
                if c in PALETTE and c != '.':
                    color = PALETTE[c]
                    img.putpixel((f_idx * WIDTH + x, y), color)
                    
    img.save(filename)
    print(f"Preview saved to {filename}")

if __name__ == '__main__':
    frames = generate_frames()
    render_preview_sheet(frames)
