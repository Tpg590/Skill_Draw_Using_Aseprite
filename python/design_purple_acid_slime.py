import os
import math
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 8

# Terraria style palette: 1-character tokens for perfect 1:1 pixel mapping
PALETTE = {
    '.': (0, 0, 0, 0),             # Transparent
    'K': (18, 6, 26, 255),         # Deep dark outline (Terraria dark tone)
    'k': (30, 10, 42, 255),        # Dark crevice / stone seam
    
    # Translucent Toxic Purple Slime Body (with SSS Terminator peak 'M')
    'H': (248, 224, 255, 255),     # Specular glint highlight
    'A': (212, 128, 255, 255),     # Light translucent lavender
    'M': (255, 34, 170, 255),      # SSS Saturation Peak: Neon Magenta / Hot Pink!
    'C': (160, 24, 184, 255),      # Midtone toxic purple
    'D': (96, 12, 122, 255),       # Deep shaded violet
    'd': (54, 5, 72, 255),         # Murky base violet shadow
    
    # Internal air bubbles
    'b': (224, 160, 255, 230),     # Glowing internal air bubble
    
    # Demon Eye in Core
    'W': (255, 255, 255, 255),     # Eye specular reflection
    'Y': (255, 204, 0, 255),       # Yellow demon iris
    'R': (255, 24, 24, 255),       # Fiery red demon sclera
    'r': (144, 8, 8, 255),         # Deep crimson eye shadow
    'N': (24, 2, 4, 255),          # Pupil slit
    
    # Acid spit droplet & splatter
    'S': (255, 128, 223, 255),     # Acid droplet core highlight
    's': (216, 24, 160, 255),      # Acid droplet neon body
    'v': (232, 160, 240, 200),     # Acid vapor wisp
    
    # Stone Pedestal
    'T': (122, 114, 128, 255),     # Stone pedestal top light surface
    't': (80, 72, 86, 255),        # Stone pedestal front face
    'Q': (48, 42, 54, 255),        # Stone pedestal shadow face
    
    # Contact ground shadow (Locked on ground plane)
    'P': (16, 8, 22, 160),         # Dense contact shadow
    'p': (16, 8, 22, 80),          # Soft outer edge shadow
}

def create_empty_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def safe_set(grid, x, y, char):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = char

def draw_stone_pedestal(grid, cx, pedestal_top_y):
    # Rule: Spatial 3.2 - Pedestal / Platform
    # Flat top surface with rounded ends, depth of 4px
    pw = 19 # half-width 19 -> 39px wide
    
    # 1. Top light surface (Y = pedestal_top_y)
    for dx in range(-pw + 2, pw - 1):
        safe_set(grid, cx + dx, pedestal_top_y, 'T')
    safe_set(grid, cx - pw + 1, pedestal_top_y, 'k')
    safe_set(grid, cx + pw - 1, pedestal_top_y, 'k')
    
    # 2. Front vertical face (Y = pedestal_top_y + 1 to + 3)
    for dy in (1, 2):
        y = pedestal_top_y + dy
        for dx in range(-pw + 1, pw):
            c = 'T' if dy == 1 and dx < -pw + 6 else ('t' if dx < pw - 6 else 'Q')
            safe_set(grid, cx + dx, y, c)
        safe_set(grid, cx - pw, y, 'K')
        safe_set(grid, cx + pw, y, 'K')
        
    # Stone bottom bevel
    y_bot = pedestal_top_y + 3
    for dx in range(-pw + 1, pw):
        safe_set(grid, cx + dx, y_bot, 'Q')
    safe_set(grid, cx - pw + 1, y_bot, 'K')
    safe_set(grid, cx + pw - 1, y_bot, 'K')
    
    # Top & bottom outlines of pedestal
    for dx in range(-pw + 2, pw - 1):
        safe_set(grid, cx + dx, pedestal_top_y - 1, 'k')
        safe_set(grid, cx + dx, y_bot + 1, 'K')
        
    # Ground shadow below pedestal
    for dx in range(-pw + 3, pw - 2):
        safe_set(grid, cx + dx, y_bot + 2, 'P')
    safe_set(grid, cx - pw + 2, y_bot + 2, 'p')
    safe_set(grid, cx + pw - 2, y_bot + 2, 'p')

def draw_gumdrop_slime_body(grid, cx, cy, rx, ry, is_gumdrop=True):
    # Rule: Fluid & Gas 1.4 - GRAVITY SLUMP & GUMDROP SHAPE (H ~ 75% W, W_base >= 50% W_max)
    # Bottom rests flatly on pedestal, dome on top
    
    for dy in range(-ry, ry + 1):
        y = cy + dy
        norm_y = dy / ry
        
        if is_gumdrop:
            # Gumdrop equation: dome at top, spreads wide at bottom
            if norm_y < 0:
                # Dome top
                w_factor = math.sqrt(max(0, 1 - norm_y * norm_y)) * (0.8 + 0.2 * (1 + norm_y))
            else:
                # Flat slumping base: W stays wide (> 50% max)
                w_factor = 0.95 + 0.05 * (1 - norm_y)
        else:
            # During high stretch: elongated teardrop
            if norm_y < 0:
                w_factor = math.sqrt(max(0, 1 - norm_y * norm_y)) * 0.9
            else:
                w_factor = math.sqrt(max(0, 1 - norm_y * norm_y * 0.8))
                
        cur_rx = int(round(rx * w_factor))
        if cur_rx < 1:
            cur_rx = 1
            
        for dx in range(-cur_rx, cur_rx + 1):
            x = cx + dx
            norm_x = (dx + rx * 0.25) / rx
            dist_light = math.sqrt(norm_x * norm_x + (norm_y + 0.3) * (norm_y + 0.3))
            
            # SSS Shading with Magenta saturation peak:
            if dist_light < 0.35 and norm_y < 0.1:
                c = 'H' if (dist_light < 0.18 and norm_y < -0.1) else 'A'
            elif dist_light < 0.65:
                c = 'A'
            elif dist_light < 0.98:
                # Rule: Material 2.1 - Magenta / Hot Pink SSS Saturation Peak!
                c = 'M'
            elif dist_light < 1.35:
                c = 'C'
            elif dy >= ry - 2:
                c = 'd'
            else:
                c = 'D'
                
            safe_set(grid, x, y, c)
            
    # Trace crisp dark Terraria outline
    border_pts = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] not in ('.', 'T', 't', 'Q', 'P', 'p'):
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1), 
                               (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)):
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                        if grid[ny][nx] == '.' or grid[ny][nx] in ('T', 't', 'Q'):
                            border_pts.append((nx, ny))
                            
    for bx, by in set(border_pts):
        safe_set(grid, bx, by, 'K')

def draw_viscous_demon_eye(grid, eye_x, eye_y, eye_state=0):
    # Rule: Kinematics 2.3 - VISCOUS CORE DRAG
    # Demon eye moves with inertia lag inside the slime body
    if eye_state == 1: # Squint during squash
        eye_shape = [
            (-2, -1, 'r'), (-1, -1, 'r'), (0, -1, 'r'), (1, -1, 'r'), (2, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'Y'), (0, 0,  'Y'), (1, 0,  'R'), (2, 0,  'R'), (3, 0,  'r'),
            (-2, 1,  'r'), (-1, 1,  'R'), (0, 1,  'Y'), (1, 1,  'R'), (2, 1,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y, 'N')
        safe_set(grid, eye_x - 1, eye_y, 'W')
        
    elif eye_state == 2: # Dilated wide during spit discharge
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
        safe_set(grid, eye_x, eye_y - 1, 'N')
        safe_set(grid, eye_x, eye_y, 'N')
        safe_set(grid, eye_x, eye_y + 1, 'N')
        safe_set(grid, eye_x - 1, eye_y - 1, 'W')
        
    elif eye_state == 3: # Recoil squint
        eye_shape = [
            (-2, -1, 'r'), (-1, -1, 'r'), (0, -1, 'r'), (1, -1, 'r'), (2, -1, 'r'),
            (-3, 0,  'r'), (-2, 0,  'R'), (-1, 0,  'R'), (0, 0,  'R'), (1, 0,  'R'), (2, 0,  'R'), (3, 0,  'r'),
            (-2, 1,  'r'), (-1, 1,  'r'), (0, 1,  'r'), (1, 1,  'r'), (2, 1,  'r'),
        ]
        for ex, ey, col in eye_shape:
            safe_set(grid, eye_x + ex, eye_y + ey, col)
        safe_set(grid, eye_x, eye_y, 'N')
        
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
        safe_set(grid, eye_x, eye_y, 'N')
        safe_set(grid, eye_x, eye_y + 1, 'N')
        safe_set(grid, eye_x - 1, eye_y - 1, 'W')

def draw_internal_bubbles(grid, cx, cy, frame_idx):
    # Rule: Fluid & Gas 2.1 & Pixel Art 3.9: 2-3 internal bubbles
    b_offsets = [
        (-7, -4 + (frame_idx % 2)),
        (6, 1 - (frame_idx % 3)),
        (-4, 3 - ((frame_idx + 1) % 2)),
    ]
    for bx, by in b_offsets:
        safe_set(grid, cx + bx, cy + by, 'b')
        safe_set(grid, cx + bx + 1, cy + by, 'A')

def draw_acid_spit_mechanics(grid, cx, mouth_y, stage, ped_top_y):
    # Rule: Spatial 2.2 - FORWARD REACH IN TOP-DOWN 3/4 (+Y direction towards viewer)
    # Rule: Spatial 2.2 Clearance - Đạn lướt trên bề mặt sàn bệ đá (Y_spit <= Y_pedestal_bottom)
    # Rule: Fluid & Gas 1.2 - SỨC CĂNG BỀ MẶT & ĐỘ NHỎ GIỌT (DROPLET PINCH-OFF)
    
    if stage == 1:
        # F4: High stretch, mouth opens wide on front belly, NECK PINCHING!
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
        
        # Bulging droplet head
        safe_set(grid, cx - 2, mouth_y + 3, 'K')
        safe_set(grid, cx - 1, mouth_y + 3, 's')
        safe_set(grid, cx, mouth_y + 3, 'S')
        safe_set(grid, cx + 1, mouth_y + 3, 's')
        safe_set(grid, cx + 2, mouth_y + 3, 'K')
        
        safe_set(grid, cx - 1, mouth_y + 4, 'K')
        safe_set(grid, cx, mouth_y + 4, 's')
        safe_set(grid, cx + 1, mouth_y + 4, 'K')
        safe_set(grid, cx, mouth_y + 5, 'K')

    elif stage == 2:
        # F5: Neck snapped! Droplet detached & skimming over stone pedestal (+Y)
        # Mouth puckers shut with snap-back bead
        safe_set(grid, cx - 1, mouth_y, 'k')
        safe_set(grid, cx, mouth_y, 'd')
        safe_set(grid, cx + 1, mouth_y, 'k')
        safe_set(grid, cx, mouth_y + 2, 's')
        
        # Detached flying droplet at ped_top_y - 1 (skimming right above stone surface)
        dy = ped_top_y - 1
        safe_set(grid, cx, dy - 1, 'K')
        safe_set(grid, cx - 1, dy, 'K')
        safe_set(grid, cx, dy, 'S')
        safe_set(grid, cx + 1, dy, 'K')
        safe_set(grid, cx - 1, dy + 1, 'K')
        safe_set(grid, cx, dy + 1, 's')
        safe_set(grid, cx + 1, dy + 1, 'K')
        safe_set(grid, cx, dy + 2, 'K')

    elif stage == 3:
        # F6: Droplet impacts stone pedestal surface at ped_top_y (Splatter Pool!)
        impact_y = ped_top_y
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
        
        # Splash beads kicking up
        safe_set(grid, cx - 4, impact_y - 2, 'S')
        safe_set(grid, cx + 4, impact_y - 2, 's')

    elif stage == 4:
        # F7: Splatter sizzles on pedestal with vapor
        impact_y = ped_top_y
        for dx in range(-3, 4):
            safe_set(grid, cx + dx, impact_y - 1, 'K')
            safe_set(grid, cx + dx, impact_y + 1, 'K')
        safe_set(grid, cx - 4, impact_y, 'K')
        safe_set(grid, cx + 4, impact_y, 'K')
        
        for dx in range(-3, 4):
            safe_set(grid, cx + dx, impact_y, 'S' if abs(dx) <= 1 else 's')
            
        safe_set(grid, cx - 2, impact_y - 2, 'v')
        safe_set(grid, cx + 2, impact_y - 2, 'v')

    elif stage == 5:
        # F8: Faint sizzle dissolving
        safe_set(grid, cx - 1, ped_top_y, 's')
        safe_set(grid, cx, ped_top_y, 's')
        safe_set(grid, cx + 1, ped_top_y, 's')
        safe_set(grid, cx, ped_top_y - 2, 'v')

def draw_contact_shadow(grid, cx, floor_y, cur_rx):
    shadow_half_w = cur_rx + 1
    for dx in range(-shadow_half_w, shadow_half_w + 1):
        if abs(dx) == shadow_half_w:
            c = 'p'
        elif abs(dx) >= shadow_half_w - 2:
            c = 'p'
        else:
            c = 'P'
        safe_set(grid, cx + dx, floor_y, c)

def generate_frames():
    frames = []
    cx = 24
    pedestal_top_y = 38 # Slime sits on pedestal top
    
    # 8 Frames Profile with VISCOUS CORE DRAG:
    # Rule 1: Gumdrop shape idle (H = 75% W): rx = 14 (W=28), ry = 10 (H=21) -> H/W = 75%.
    # Rule 2: Volume conservation (Squash & Stretch): rx * ry ~ 140
    # Rule 3: Viscous core drag: Eye Y lags behind shell motion by exactly 1 frame!
    
    frame_configs = [
        # (rx, ry, is_gumdrop, eye_y, eye_state, spit_stage, mouth_rel_y)
        # F1: Idle Gumdrop. Shell cy = 38 - 10 = 28. Eye at 28 (neutral).
        (14, 10, True,  28, 0, 0, 4),
        
        # F2: Deep Squash! Shell cy = 38 - 6 = 32. Shell squashes to ry=6, rx=18.
        # VISCOUS DRAG: Eye lags behind, only drops to Y=30 (not 32)! Squint.
        (18, 6,  True,  30, 1, 0, 3),
        
        # F3: Shell starts rising! Shell cy = 38 - 12 = 26, ry=12, rx=11.
        # VISCOUS DRAG: Eye hits bottom 1 FRAME LATE at Y=34!
        (11, 12, False, 34, 1, 0, 4),
        
        # F4: Max Stretch! Shell cy = 38 - 14 = 24, ry=14, rx=9.
        # VISCOUS DRAG: Eye pulled upward but lags at Y=27 (apex of shell is 24)! Dilated wide, spit neck pinching.
        (9,  14, False, 27, 2, 1, 6),
        
        # F5: Shell descending! Shell cy = 38 - 11 = 27, ry=11, rx=11.
        # VISCOUS DRAG: Eye reaches its top APEX 1 FRAME LATE at Y=22! Recoil squint. Spit flying forward.
        (11, 11, False, 22, 3, 2, 4),
        
        # F6: Landing Squash Cushion! Shell cy = 38 - 8 = 30, ry=8, rx=15.
        # VISCOUS DRAG: Eye descends to Y=28. Droplet impacts pedestal top!
        (15, 8,  True,  28, 1, 3, 4),
        
        # F7: Rebound Wobble! Shell cy = 38 - 11 = 27, ry=11, rx=13.
        # VISCOUS DRAG: Eye oscillates to Y=29. Splatter sizzles.
        (13, 11, True,  29, 0, 4, 4),
        
        # F8: Cooldown settling to Gumdrop F1! Shell cy = 38 - 10 = 28, ry=10, rx=14.
        # Eye settles to Y=28.
        (14, 10, True,  28, 0, 5, 4),
    ]
    
    for f_idx, (rx, ry, is_gumdrop, eye_y, eye_state, spit_stage, mouth_rel_y) in enumerate(frame_configs):
        grid = create_empty_grid()
        cy = pedestal_top_y - ry
        
        # 1. Stone Pedestal
        draw_stone_pedestal(grid, cx, pedestal_top_y)
        
        # 2. Contact ground shadow on pedestal top
        draw_contact_shadow(grid, cx, pedestal_top_y, rx)
        
        # 3. Gumdrop / Slime Body
        draw_gumdrop_slime_body(grid, cx, cy, rx, ry, is_gumdrop)
        
        # 4. Internal Air Bubbles
        draw_internal_bubbles(grid, cx, cy, f_idx)
        
        # 5. Viscous Drag Demon Eye (Lagging by 1 frame!)
        draw_viscous_demon_eye(grid, cx, eye_y, eye_state)
        
        # 6. Acid Spit Mechanics (+Y direction gliding over pedestal)
        mouth_y = cy + mouth_rel_y
        draw_acid_spit_mechanics(grid, cx, mouth_y, spit_stage, pedestal_top_y)
        
        frames.append(grid)
        
    return frames

def render_preview_sheet(frames, filename="test/purple_acid_slime_preview.png"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sheet_w = WIDTH * NUM_FRAMES
    sheet_h = HEIGHT
    img = Image.new("RGBA", (sheet_w, sheet_h), (20, 16, 26, 255))
    
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
