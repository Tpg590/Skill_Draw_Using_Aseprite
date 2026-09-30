import os
from PIL import Image

WIDTH = 48
HEIGHT = 48
NUM_FRAMES = 6

PALETTE = {
    '.': (0, 0, 0, 0),         # Transparent
    'S': (25, 20, 35, 130),    # Soft Ground Contact Shadow
    
    # Bronze Cauldron
    'D': (36, 22, 16, 255),    # Deep Cauldron Dark / Outline (#241610)
    'B': (82, 50, 28, 255),    # Bronze Shadow (#52321c)
    'M': (144, 95, 46, 255),   # Bronze Midtone (#905f2e)
    'H': (210, 155, 80, 255),  # Bronze Highlight (#d29b50)
    'P': (52, 135, 115, 255),  # Verdigris Patina (#348773)
    
    # Potion Fluid & Bioluminescence
    'k': (12, 52, 30, 255),    # Deep Liquid Dark (#0c341e)
    'g': (22, 130, 68, 255),   # Potion Mid Green (#168244)
    'G': (48, 220, 110, 255),  # Vibrant Neon Lime Green (#30dc6e)
    'Y': (180, 255, 140, 255), # Potion Specular / Bubble Core (#b4ff8c)
    'W': (245, 255, 230, 255), # Boiling Foam Pop White (#f5ffe6)
    
    # Smoke / Mysterious Mist (Puff clusters, NO slashed lines!)
    'm': (60, 90, 105, 130),   # Mist Dark Base
    'T': (100, 180, 170, 170), # Luminous Teal Vapor
    't': (175, 240, 225, 210), # Light Vapor Highlight
}

def create_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]

def draw_cauldron_base(grid):
    # Base contact shadow on floor: Rounded ellipse
    # Y = 42: width from 13 to 35
    # Y = 43: width from 10 to 37 (widest)
    # Y = 44: width from 15 to 33
    for x in range(13, 35):
        grid[42][x] = 'S'
    for x in range(10, 38):
        grid[43][x] = 'S'
    for x in range(15, 33):
        grid[44][x] = 'S'
        
    # Tripod Legs (Rule 4: TRIPOD LEGS GROUNDING - All 3 legs MUST touch ground!)
    # Left front leg: foot at (11, 42)
    for (x, y) in [(15, 35), (14, 36), (13, 37), (13, 38), (12, 39), (12, 40), (11, 41), (11, 42), (12, 42)]:
        grid[y][x] = 'D'
    for (x, y) in [(14, 37), (13, 39), (13, 40), (12, 41)]:
        grid[y][x] = 'B'
    grid[38][14] = 'M'
    grid[39][14] = 'P' # Patina on leg
    
    # Right front leg: foot at (36, 42)
    for (x, y) in [(32, 35), (33, 36), (34, 37), (34, 38), (35, 39), (35, 40), (36, 41), (36, 42), (35, 42)]:
        grid[y][x] = 'D'
    for (x, y) in [(33, 37), (34, 39), (34, 40), (35, 41)]:
        grid[y][x] = 'B'
    grid[38][33] = 'M'
    grid[39][33] = 'H'

    # Rear center leg: MUST EXTEND DOWNWARD TO TOUCH FLOOR AT Y=41/42!
    for y in range(36, 42):
        grid[y][23] = 'D'
        grid[y][24] = 'D'
    grid[41][23] = 'B'; grid[41][24] = 'D'
    grid[40][23] = 'B'; grid[39][23] = 'B'
    grid[42][23] = 'S'; grid[42][24] = 'S' # Foot contact shadow

    # Cauldron Belly Body
    belly_rows = [
        (24, 10, 37),
        (25, 9, 38),
        (26, 8, 39),
        (27, 8, 39),
        (28, 8, 39),
        (29, 8, 39),
        (30, 9, 38),
        (31, 10, 37),
        (32, 11, 36),
        (33, 13, 34),
        (34, 15, 32),
        (35, 17, 30),
        (36, 19, 28)
    ]
    for y, x0, x1 in belly_rows:
        for x in range(x0, x1 + 1):
            if x == x0 or x == x1 or y == 36:
                grid[y][x] = 'D'
            elif x < x0 + 3 or y > 33:
                grid[y][x] = 'B'
            elif x > x1 - 5 and y < 32:
                grid[y][x] = 'H' if x > x1 - 3 else 'M'
            else:
                grid[y][x] = 'M'
                
    # Patina spots on belly
    grid[26][12] = 'P'; grid[27][12] = 'P'; grid[27][13] = 'P'; grid[28][13] = 'P'
    grid[30][15] = 'P'; grid[31][15] = 'P'; grid[29][32] = 'P'

    # OSL Green Glow on cauldron upper belly
    for x in range(14, 34):
        if grid[24][x] == 'M':
            grid[24][x] = 'g'
        elif grid[24][x] == 'H':
            grid[24][x] = 'G'
            
    # Handles (Quai vạc)
    for (x, y) in [(7, 25), (6, 26), (6, 27), (7, 28), (8, 28)]:
        grid[y][x] = 'D'
    grid[26][7] = 'M'; grid[27][7] = 'B'
    
    for (x, y) in [(40, 25), (41, 26), (41, 27), (40, 28), (39, 28)]:
        grid[y][x] = 'D'
    grid[26][40] = 'H'; grid[27][40] = 'M'

    # Cauldron Rim (Vành miệng vạc 3/4)
    for x in range(12, 36):
        grid[16][x] = 'D'
        grid[23][x] = 'D'
    for (x, y) in [(11, 17), (10, 18), (10, 19), (10, 20), (10, 21), (11, 22),
                  (36, 17), (37, 18), (37, 19), (37, 20), (37, 21), (36, 22)]:
        grid[y][x] = 'D'
        
    for x in range(12, 36):
        grid[17][x] = 'B'
        grid[22][x] = 'H' if x > 28 else ('M' if x > 18 else 'B')
    grid[18][11] = 'B'; grid[19][11] = 'B'; grid[20][11] = 'B'; grid[21][11] = 'B'
    grid[18][36] = 'H'; grid[19][36] = 'H'; grid[20][36] = 'H'; grid[21][36] = 'H'
    
    for x in range(18, 30):
        grid[22][x] = 'G'

def draw_fluid_base(grid):
    fluid_rows = [
        (18, 13, 34),
        (19, 12, 35),
        (20, 12, 35),
        (21, 13, 34)
    ]
    for y, x0, x1 in fluid_rows:
        for x in range(x0, x1 + 1):
            if y == 18:
                grid[y][x] = 'k' if x < 26 else 'g'
            elif y == 21:
                grid[y][x] = 'g' if x < 20 else 'G'
            else:
                grid[y][x] = 'g' if x < 18 else ('G' if x < 30 else 'Y')

def generate_frames():
    frames = []
    
    for f in range(NUM_FRAMES):
        grid = create_grid()
        draw_cauldron_base(grid)
        draw_fluid_base(grid)
        
        # Steam & Boiling: Strictly follow STEAM WISPS VS SLASHED LINES!
        # NO diagonal lines (/ /)! Use organic clusters, billowing puffs, sinuous particles!
        
        if f == 0:
            # Frame 1: Small bubbles forming
            grid[19][16] = 'Y'; grid[19][17] = 'W'
            grid[20][28] = 'Y'; grid[20][29] = 'G'
            grid[19][23] = 'Y'
            # Puffs emerging from surface
            # Left puff cluster (curving sinuous puff)
            for (x, y) in [(18, 15), (17, 15), (18, 14), (19, 14), (17, 13)]:
                grid[y][x] = 'T'
            grid[14][18] = 't'
            # Right puff
            for (x, y) in [(28, 15), (29, 15), (28, 14), (29, 14)]:
                grid[y][x] = 'm'
            grid[13][29] = 'T'
                
        elif f == 1:
            # Frame 2: Bubble expands, bubble 2 pops into white foam
            grid[18][16] = 'W'; grid[18][17] = 'Y'; grid[19][16] = 'Y'; grid[19][17] = 'G'
            grid[20][28] = 'W'; grid[20][29] = 'W'; grid[19][29] = 'Y'
            grid[20][22] = 'Y'; grid[20][23] = 'W'
            # Left puff rises and billows into circular cluster (NO slashed lines!)
            for (x, y) in [(17, 12), (18, 12), (19, 12), (16, 11), (17, 11), (18, 11), (19, 11), (20, 11), (17, 10), (18, 10), (19, 10)]:
                grid[y][x] = 'T'
            grid[11][18] = 't'; grid[10][18] = 't'
            # Right puff curls
            for (x, y) in [(29, 13), (30, 13), (29, 12), (30, 12), (31, 12), (30, 11)]:
                grid[y][x] = 'm'
            grid[12][30] = 'T'

        elif f == 2:
            # Frame 3: Bubble bursts! Droplet pinch-off flying up 1px
            grid[18][16] = 'W'; grid[18][17] = 'G'
            grid[15][16] = 'Y' # airborne droplet
            grid[14][16] = 'W' # splash glint
            grid[19][24] = 'W'; grid[19][25] = 'Y'; grid[20][24] = 'Y'; grid[20][25] = 'G'
            # Sinuous swirling cloud: circular puff expanding at Y=8..10
            for (x, y) in [(18, 9), (19, 9), (20, 9), (17, 8), (18, 8), (19, 8), (20, 8), (21, 8), (18, 7), (19, 7), (20, 7)]:
                grid[y][x] = 'T'
            grid[8][19] = 't'; grid[8][20] = 't'
            # Fissuring mist trail
            grid[12][17] = 'm'; grid[13][18] = 'm'
            for (x, y) in [(28, 10), (29, 10), (28, 9), (29, 9), (30, 9)]:
                grid[y][x] = 'T'

        elif f == 3:
            # Frame 4: Droplet falls back, central bubble at peak diameter (3x2)
            grid[16][17] = 'G'
            grid[18][24] = 'W'; grid[18][25] = 'W'
            grid[19][23] = 'Y'; grid[19][24] = 'Y'; grid[19][25] = 'G'; grid[19][26] = 'k'
            grid[20][24] = 'G'; grid[20][25] = 'G'
            grid[19][32] = 'Y'; grid[19][33] = 'W'
            # Cloud reaches apex: large billowing puff at Y=5..7
            for (x, y) in [(20, 7), (21, 7), (22, 7), (19, 6), (20, 6), (21, 6), (22, 6), (23, 6), (20, 5), (21, 5), (22, 5)]:
                grid[y][x] = 'T'
            grid[6][21] = 't'; grid[5][21] = 't'
            # Dispersing 1px wisps
            grid[9][16] = 'm'; grid[8][26] = 'm'; grid[7][27] = 'T'

        elif f == 4:
            # Frame 5: Central bubble pops into ring of foam
            grid[18][23] = 'W'; grid[18][24] = 'k'; grid[18][25] = 'W'; grid[18][26] = 'W'
            grid[19][23] = 'Y'; grid[19][26] = 'Y'
            grid[14][24] = 'Y' # splash droplet
            grid[19][32] = 'W'; grid[19][33] = 'Y'
            # Dissipating cloud: thinning into separate 1px floating wisps
            for (x, y) in [(21, 5), (22, 5), (21, 4), (22, 4), (23, 4)]:
                grid[y][x] = 'T'
            grid[4][22] = 't'
            grid[6][18] = 'm'; grid[5][25] = 'm'; grid[6][26] = 'm'
            
        elif f == 5:
            # Frame 6: Settle / transition back to Frame 1
            grid[18][24] = 'g'; grid[18][25] = 'G'
            grid[19][18] = 'Y'; grid[20][27] = 'G'
            # Very faint dissipated particles
            grid[3][22] = 'm'; grid[4][23] = 'm'
            grid[16][18] = 'T'; grid[16][28] = 'm'
            
        frames.append(grid)
        
    return frames

if __name__ == '__main__':
    frames = generate_frames()
    os.makedirs('test', exist_ok=True)
    
    sheet = Image.new('RGBA', (WIDTH * NUM_FRAMES, HEIGHT), (20, 18, 28, 255))
    for i, frame in enumerate(frames):
        img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                img.putpixel((x, y), PALETTE[frame[y][x]])
        sheet.paste(img, (i * WIDTH, 0), img)
        img.save(f'test/cauldron_f{i+1}.png')
        
    sheet.save('test/cauldron_preview_dark.png')
    print("Cauldron updated with grounded rear leg and organic billowing smoke wisps!")
