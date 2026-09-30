import os
import math
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

# Terraria style palette: 1-character tokens for perfect 1:1 pixel mapping
PALETTE = {
    '.': (0, 0, 0, 0),             # Transparent
    'K': (20, 14, 10, 255),        # Deep dark outline (Terraria dark tone)
    'k': (42, 28, 16, 255),        # Dark border / seam line / shadow crevice
    
    # Brass/Bronze chassis
    'H': (255, 245, 175, 255),    # Extreme specular highlight (B0)
    'A': (248, 205, 75, 255),     # High brass specular highlight (B1)
    'B': (208, 150, 40, 255),     # Main polished brass tone (B2)
    'b': (155, 98, 22, 255),      # Medium shaded brass / bronze (B3)
    'D': (95, 54, 12, 255),       # Dark shadow bronze (B4)
    
    # Iron / Steel pipes and trims
    'L': (185, 195, 205, 255),    # Light iron (I1)
    'I': (115, 125, 138, 255),    # Mid iron / trim (I2)
    'i': (65, 72, 82, 255),       # Dark iron (I3)
    
    # Pressure Gauge
    'G': (248, 244, 232, 255),    # Gauge dial face (ivory white G1)
    'g': (188, 182, 168, 255),    # Gauge inner shadow (G2)
    'X': (210, 45, 30, 255),      # Gauge red danger zone (G3)
    'N': (35, 12, 8, 255),        # Gauge needle (dark sharp indicator GN)
    
    # Rivets
    'R': (255, 242, 165, 255),    # Gleaming brass rivet
    
    # Jet thruster flame & thermal glow
    'W': (255, 255, 200, 255),    # Incandescent white-yellow core (F1)
    'O': (255, 160, 25, 255),     # Bright orange flame (F2)
    'F': (220, 55, 12, 255),      # Deep red-orange flame (F3)
    'f': (140, 28, 10, 255),      # Dark flame tip / ember (F4)
    
    # Steam puffs (Organic billowing wisps)
    'S': (248, 248, 252, 240),    # Pure white steam highlight (S1)
    's': (210, 215, 225, 210),    # Midtone steam (S2)
    'w': (165, 172, 185, 160),    # Outer dissipating steam edge (S3)
    
    # Ground shadow (Locked at ground plane Y=43..44)
    'P': (22, 14, 10, 160),       # Dense core shadow (SH1)
    'p': (22, 14, 10, 80),        # Soft outer edge shadow (SH2)
}

def create_empty_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def safe_set(grid, x, y, char):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = char

def draw_boiler_chassis(grid, cx, cy):
    # Boiler body: Width ~ 24px, Height ~ 18px (from cy-8 to cy+9)
    # Cylindrical rounded barrel drum in Top-Down 3/4
    
    # 1. Fill the barrel body with cylindrical brass gradient
    for dy in range(-7, 9):
        y = cy + dy
        if dy in (-7, 8):
            half_w = 7
        elif dy in (-6, 7):
            half_w = 9
        elif dy in (-5, 6):
            half_w = 10
        else:
            half_w = 11
            
        for dx in range(-half_w, half_w + 1):
            x = cx + dx
            if dx < -8:
                c = 'D'
            elif dx < -4:
                c = 'b'
            elif dx < -1:
                c = 'B'
            elif dx <= 1:
                c = 'A' if dy < 2 else 'B'
            elif dx < 6:
                c = 'B'
            elif dx < 9:
                c = 'b'
            else:
                c = 'D'
                
            # Specular glint on top left shoulder
            if dy in (-5, -4) and dx in (-1, 0):
                c = 'H'
                
            # Bottom shadow
            if dy >= 6:
                if c == 'A': c = 'B'
                elif c == 'B': c = 'b'
                else: c = 'D'
            # Top curvature shadow/highlight
            elif dy <= -6:
                if c == 'D': c = 'b'
                elif c == 'b': c = 'B'
                
            safe_set(grid, x, y, c)
            
    # 2. Outline (K)
    for dx in range(-6, 7):
        safe_set(grid, cx + dx, cy - 8, 'K')
    safe_set(grid, cx - 7, cy - 7, 'K')
    safe_set(grid, cx + 7, cy - 7, 'K')
    safe_set(grid, cx - 8, cy - 7, 'K')
    safe_set(grid, cx + 8, cy - 7, 'K')
    safe_set(grid, cx - 9, cy - 6, 'K')
    safe_set(grid, cx + 9, cy - 6, 'K')
    safe_set(grid, cx - 10, cy - 5, 'K')
    safe_set(grid, cx + 10, cy - 5, 'K')
    
    # Sides
    for dy in range(-4, 6):
        safe_set(grid, cx - 12, cy + dy, 'K')
        safe_set(grid, cx + 12, cy + dy, 'K')
        
    # Bottom arc
    safe_set(grid, cx - 11, cy + 6, 'K')
    safe_set(grid, cx + 11, cy + 6, 'K')
    safe_set(grid, cx - 10, cy + 7, 'K')
    safe_set(grid, cx + 10, cy + 7, 'K')
    safe_set(grid, cx - 9, cy + 8, 'K')
    safe_set(grid, cx + 9, cy + 8, 'K')
    safe_set(grid, cx - 8, cy + 8, 'K')
    safe_set(grid, cx + 8, cy + 8, 'K')
    for dx in range(-7, 8):
        safe_set(grid, cx + dx, cy + 9, 'K')

    # 3. Seam lines (Mechanical plate seams - Pixel Art Rule 3.9)
    for dx in range(-10, 11):
        if not (-5 <= dx <= 5):
            safe_set(grid, cx + dx, cy + 2, 'k')
            
    for dy in range(-6, 8):
        if dy != 2:
            safe_set(grid, cx - 7, cy + dy, 'k')
            safe_set(grid, cx + 7, cy + dy, 'k')

    # 4. Rivets (Brass gleaming rivets 1px)
    rivets = [
        (cx - 9, cy - 5), (cx - 9, cy + 4),
        (cx + 9, cy - 5), (cx + 9, cy + 4),
        (cx - 5, cy - 6), (cx + 5, cy - 6),
        (cx - 5, cy + 6), (cx + 5, cy + 6),
        (cx - 1, cy - 7), (cx + 1, cy - 7),
    ]
    for rx, ry in rivets:
        safe_set(grid, rx, ry, 'R')

    # 5. Side Steam Winglet Thrusters / Piston brackets
    for ldy in (-2, -1, 0, 1):
        safe_set(grid, cx - 13, cy + ldy, 'I')
        safe_set(grid, cx - 14, cy + ldy, 'i')
    safe_set(grid, cx - 13, cy - 3, 'K')
    safe_set(grid, cx - 13, cy + 2, 'K')
    safe_set(grid, cx - 15, cy - 1, 'K')
    safe_set(grid, cx - 15, cy, 'K')
    safe_set(grid, cx - 14, cy - 2, 'K')
    safe_set(grid, cx - 14, cy + 1, 'K')
    safe_set(grid, cx - 14, cy - 1, 'R')

    for rdy in (-2, -1, 0, 1):
        safe_set(grid, cx + 13, cy + rdy, 'I')
        safe_set(grid, cx + 14, cy + rdy, 'i')
    safe_set(grid, cx + 13, cy - 3, 'K')
    safe_set(grid, cx + 13, cy + 2, 'K')
    safe_set(grid, cx + 15, cy - 1, 'K')
    safe_set(grid, cx + 15, cy, 'K')
    safe_set(grid, cx + 14, cy - 2, 'K')
    safe_set(grid, cx + 14, cy + 1, 'K')
    safe_set(grid, cx + 14, cy - 1, 'R')

    # 6. Chimney on top (Boiler stack)
    for sy in range(cy - 12, cy - 7):
        safe_set(grid, cx - 3, sy, 'K')
        safe_set(grid, cx - 2, sy, 'I')
        safe_set(grid, cx - 1, sy, 'L')
        safe_set(grid, cx, sy, 'I')
        safe_set(grid, cx + 1, sy, 'i')
        safe_set(grid, cx + 2, sy, 'K')
    # Chimney lip / overhang
    lip_y = cy - 13
    safe_set(grid, cx - 4, lip_y, 'K')
    safe_set(grid, cx - 3, lip_y, 'B')
    safe_set(grid, cx - 2, lip_y, 'A')
    safe_set(grid, cx - 1, lip_y, 'H')
    safe_set(grid, cx, lip_y, 'A')
    safe_set(grid, cx + 1, lip_y, 'B')
    safe_set(grid, cx + 2, lip_y, 'b')
    safe_set(grid, cx + 3, lip_y, 'K')
    for ox in range(-3, 3):
        safe_set(grid, cx + ox, lip_y - 1, 'K')

    # 7. Bottom thruster nozzle with thermal OSL glow
    noz_top = cy + 9
    for ny in range(noz_top, noz_top + 3):
        w = 2 if ny == noz_top else (3 if ny == noz_top + 1 else 2)
        safe_set(grid, cx - w - 1, ny, 'K')
        for nx in range(-w, w + 1):
            c = 'L' if nx == -1 else ('I' if nx <= 1 else 'i')
            safe_set(grid, cx + nx, ny, c)
        safe_set(grid, cx + w + 1, ny, 'K')
    # Nozzle mouth
    safe_set(grid, cx - 3, noz_top + 3, 'K')
    safe_set(grid, cx - 2, noz_top + 3, 'k')
    safe_set(grid, cx - 1, noz_top + 3, 'F')
    safe_set(grid, cx, noz_top + 3, 'O')
    safe_set(grid, cx + 1, noz_top + 3, 'F')
    safe_set(grid, cx + 2, noz_top + 3, 'k')
    safe_set(grid, cx + 3, noz_top + 3, 'K')

def draw_pressure_gauge(grid, cx, cy, needle_phase):
    # Circular pressure gauge in front center:
    ring_outline = [
        (-2, -5), (-1, -5), (0, -5), (1, -5), (2, -5),
        (-3, -4), (3, -4),
        (-4, -3), (4, -3),
        (-5, -2), (5, -2),
        (-5, -1), (5, -1),
        (-5, 0),  (5, 0),
        (-5, 1),  (5, 1),
        (-5, 2),  (5, 2),
        (-4, 3),  (4, 3),
        (-3, 4),  (3, 4),
        (-2, 5), (-1, 5), (0, 5), (1, 5), (2, 5)
    ]
    for ox, oy in ring_outline:
        safe_set(grid, cx + ox, cy + oy, 'K')

    bezel = [
        (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4),
        (-3, -3), (3, -3),
        (-4, -2), (4, -2),
        (-4, -1), (4, -1),
        (-4, 0),  (4, 0),
        (-4, 1),  (4, 1),
        (-4, 2),  (4, 2),
        (-3, 3),  (3, 3),
        (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4)
    ]
    for bx, by in bezel:
        if by < 0 and bx <= 0:
            c = 'H' if bx == -1 and by == -4 else 'A'
        elif by <= 1:
            c = 'B'
        else:
            c = 'D'
        safe_set(grid, cx + bx, cy + by, c)

    dial_points = [
        (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3),
        (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2),
        (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1),
        (-3, 0),  (-2, 0),  (-1, 0),  (0, 0),  (1, 0),  (2, 0),  (3, 0),
        (-3, 1),  (-2, 1),  (-1, 1),  (0, 1),  (1, 1),  (2, 1),  (3, 1),
        (-3, 2),  (-2, 2),  (-1, 2),  (0, 2),  (1, 2),  (2, 2),  (3, 2),
        (-2, 3),  (-1, 3),  (0, 3),   (1, 3),  (2, 3),
    ]
    for px, py in dial_points:
        safe_set(grid, cx + px, cy + py, 'G')
        
    # Red danger zone in upper right arc
    safe_set(grid, cx + 1, cy - 3, 'X')
    safe_set(grid, cx + 2, cy - 3, 'X')
    safe_set(grid, cx + 3, cy - 2, 'X')

    # Inner bezel shadow
    safe_set(grid, cx - 2, cy - 2, 'g')
    safe_set(grid, cx - 1, cy - 3, 'g')
    safe_set(grid, cx, cy - 3, 'g')
    safe_set(grid, cx - 3, cy - 1, 'g')

    # Needle
    safe_set(grid, cx, cy, 'K') # Pivot pin
    
    if needle_phase == 0: # 10 o'clock
        safe_set(grid, cx - 1, cy - 1, 'N')
        safe_set(grid, cx - 2, cy - 2, 'N')
    elif needle_phase == 1: # 11 o'clock
        safe_set(grid, cx - 1, cy - 1, 'N')
        safe_set(grid, cx - 1, cy - 2, 'N')
        safe_set(grid, cx - 1, cy - 3, 'N')
    elif needle_phase == 2: # 12 o'clock
        safe_set(grid, cx, cy - 1, 'N')
        safe_set(grid, cx, cy - 2, 'N')
        safe_set(grid, cx, cy - 3, 'N')
    elif needle_phase == 3: # 12:30 o'clock (touching red zone!)
        safe_set(grid, cx, cy - 1, 'N')
        safe_set(grid, cx + 1, cy - 2, 'N')
        safe_set(grid, cx + 1, cy - 3, 'N')
    elif needle_phase == 4: # 11:30 o'clock
        safe_set(grid, cx, cy - 1, 'N')
        safe_set(grid, cx, cy - 2, 'N')
        safe_set(grid, cx - 1, cy - 3, 'N')
    else: # 10:30 o'clock
        safe_set(grid, cx - 1, cy - 1, 'N')
        safe_set(grid, cx - 1, cy - 2, 'N')
        safe_set(grid, cx - 2, cy - 2, 'N')

def draw_jet_thrust(grid, cx, noz_bottom_y, flame_type):
    if flame_type == 0: # Standard thrust (4px)
        flame = [
            (0, 0, 'W'), (-1, 0, 'O'), (1, 0, 'O'),
            (0, 1, 'W'), (-1, 1, 'F'), (1, 1, 'F'),
            (0, 2, 'O'),
            (0, 3, 'F'),
            (-1, 4, 'f'), # Ember spark
        ]
    elif flame_type == 1: # Boosted flame when descending / braking (5px)
        flame = [
            (0, 0, 'W'), (-1, 0, 'W'), (1, 0, 'W'), (-2, 0, 'O'), (2, 0, 'O'),
            (0, 1, 'W'), (-1, 1, 'O'), (1, 1, 'O'),
            (0, 2, 'O'), (-1, 2, 'F'), (1, 2, 'F'),
            (0, 3, 'O'),
            (0, 4, 'F'),
            (1, 5, 'f'), # Ember spark
        ]
    else: # Medium / soft thrust (3px)
        flame = [
            (0, 0, 'W'), (-1, 0, 'O'), (1, 0, 'O'),
            (0, 1, 'W'),
            (0, 2, 'O'),
            (0, 3, 'F'),
            (1, 3, 'f'), # Ember spark
        ]
        
    for fx, fy, color in flame:
        safe_set(grid, cx + fx, noz_bottom_y + 1 + fy, color)

def draw_steam_puff(grid, cx, chim_top_y, frame_idx):
    def p(dx, dy, color):
        x = cx + dx
        y = chim_top_y + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = color

    if frame_idx == 0:
        p(-1, -2, 's'); p(0, -2, 'S'); p(1, -2, 's')
        p(-2, -3, 'w'); p(-1, -3, 'S'); p(0, -3, 'S'); p(1, -3, 's')
        p(-1, -4, 's'); p(0, -4, 's')
        p(3, -5, 'w'); p(4, -5, 's'); p(5, -5, 'w')

    elif frame_idx == 1:
        p(-1, -3, 'w'); p(0, -3, 's'); p(1, -3, 'S'); p(2, -3, 's')
        p(-2, -4, 'w'); p(-1, -4, 'S'); p(0, -4, 'S'); p(1, -4, 'S'); p(2, -4, 's'); p(3, -4, 'w')
        p(-1, -5, 's'); p(0, -5, 'S'); p(1, -5, 'S'); p(2, -5, 's')
        p(0, -6, 'w'); p(1, -6, 's')
        p(5, -6, 'w')

    elif frame_idx == 2:
        p(0, -3, 'w'); p(1, -3, 's')
        p(-1, -4, 'w'); p(0, -4, 'S'); p(1, -4, 'S'); p(2, -4, 'S'); p(3, -4, 's')
        p(-1, -5, 's'); p(0, -5, 'S'); p(1, -5, 'S'); p(2, -5, 'S'); p(3, -5, 's'); p(4, -5, 'w')
        p(0, -6, 'w'); p(1, -6, 's'); p(2, -6, 's'); p(3, -6, 'w')
        p(-1, -2, 'w')

    elif frame_idx == 3:
        p(1, -5, 'w'); p(2, -5, 's'); p(3, -5, 'S'); p(4, -5, 's'); p(5, -5, 'w')
        p(2, -6, 'w'); p(3, -6, 's'); p(4, -6, 'w')
        p(-1, -2, 's'); p(0, -2, 'S'); p(1, -2, 's')
        p(0, -3, 's')

    elif frame_idx == 4:
        p(2, -6, 'w')
        p(4, -6, 's'); p(5, -6, 'w')
        p(6, -5, 'w')
        p(-1, -3, 'w'); p(0, -3, 's'); p(1, -3, 'S'); p(2, -3, 's')
        p(-1, -4, 's'); p(0, -4, 'S'); p(1, -4, 'S'); p(2, -4, 's')
        p(0, -5, 'w')

    elif frame_idx == 5:
        p(5, -6, 'w')
        p(0, -3, 'w'); p(1, -3, 's'); p(2, -3, 'w')
        p(-1, -4, 'w'); p(0, -4, 'S'); p(1, -4, 'S'); p(2, -4, 's'); p(3, -4, 'w')
        p(0, -5, 's'); p(1, -5, 'S'); p(2, -5, 's')
        p(0, -2, 'w')

def draw_ground_shadow(grid, cx, ground_y, hover_dy):
    half_w = 8 - hover_dy // 2
    
    # Row 1 (ground_y): Main shadow body
    for dx in range(-half_w, half_w + 1):
        if abs(dx) == half_w:
            c = 'p'
        elif abs(dx) >= half_w - 2:
            c = 'p'
        else:
            c = 'P'
        safe_set(grid, cx + dx, ground_y, c)
        
    # Row 2 (ground_y + 1): Tapered rounded bottom
    for dx in range(-half_w + 2, half_w - 1):
        safe_set(grid, cx + dx, ground_y + 1, 'p')

def generate_frames():
    frames = []
    cx = 24
    base_cy = 21
    ground_y = 43
    
    hover_dys = [0, -1, -2, -1, 0, 1]
    needle_phases = [0, 1, 2, 3, 4, 5]
    flame_types = [0, 2, 2, 0, 1, 1]
    
    for f_idx in range(NUM_FRAMES):
        grid = create_empty_grid()
        dy = hover_dys[f_idx]
        needle = needle_phases[f_idx]
        flame = flame_types[f_idx]
        cy = base_cy + dy
        
        # 1. Ground contact shadow (permanently locked at ground_y)
        draw_ground_shadow(grid, cx, ground_y, dy)
        
        # 2. Boiler Chassis (Cylindrical barrel, rivets, seam lines, winglets, chimney, nozzle)
        draw_boiler_chassis(grid, cx, cy)
        
        # 3. Pressure Gauge (Front and center, needle rotating)
        draw_pressure_gauge(grid, cx, cy, needle)
        
        # 4. Jet Thruster Flame (Firing below nozzle)
        noz_bottom_y = cy + 12
        draw_jet_thrust(grid, cx, noz_bottom_y, flame)
        
        # 5. Steam Puff (Billowing from chimney top)
        chim_top_y = cy - 13
        draw_steam_puff(grid, cx, chim_top_y, f_idx)
        
        frames.append(grid)
        
    return frames

def render_preview_sheet(frames, filename="test/steampunk_boiler_drone_preview.png"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sheet_w = WIDTH * NUM_FRAMES
    sheet_h = HEIGHT
    img = Image.new("RGBA", (sheet_w, sheet_h), (30, 25, 35, 255))
    
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
