import math
import os
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (22, 10, 30, 130),     # Ground shadow (Alpha 130)
    "#": (18, 12, 24, 255),     # Viền sẫm tối Terraria (#120c18)
    
    # Cape / Cloak - Deep Arcane Purple
    "P1": (166, 92, 216, 255),  # Wave crest bright highlight (#a65cd8)
    "P2": (108, 46, 152, 255),  # Rich royal purple midtone (#6c2e98)
    "P3": (60, 22, 92, 255),    # Wave trough / shadow purple (#3c165c)
    "P4": (34, 12, 54, 255),    # Deep crevice darkest purple (#220c36)

    # Gold Trim & Brooch
    "Y1": (255, 235, 120, 255), # Specular gold highlight (#ffeb78)
    "Y2": (224, 160, 32, 255),  # Warm gold midtone (#e0a020)
    "Y3": (138, 82, 10, 255),   # Shadow bronze gold (#8a520a)

    # Ancient Stone Pedestal & Bust
    "M1": (152, 164, 184, 255), # Stone highlight (#98a4b8)
    "M2": (94, 106, 126, 255),  # Stone midtone (#5e6a7e)
    "M3": (52, 58, 74, 255),    # Stone deep shadow (#343a4a)

    # Void & Arcane Eyes/Runes (OSL Exception)
    "K":  (10, 6, 15, 255),     # Pitch black face void under cowl (#0a060f)
    "E1": (112, 255, 255, 255), # Arcane glow cyan highlight (#70ffff)
    "E2": (38, 160, 196, 255),  # Arcane glow cyan/blue shade (#26a0c4)
}

def create_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Ground Contact Shadow S (Elliptical, grounded at bottom y=43..47)
    for x in range(4, 23):
        grid[44][x] = "S"
    for x in range(5, 22):
        grid[45][x] = "S"
    for x in range(7, 20):
        grid[46][x] = "S"
    for x in range(10, 17):
        grid[47][x] = "S"

    # 2. Pedestal Plinth Base (y=40..43, width x=5..21)
    for x in range(5, 22):
        grid[43][x] = "#"
    grid[43][6] = "M3"
    grid[43][7] = "M3"
    grid[43][19] = "M3"
    grid[43][20] = "M3"

    grid[42][5] = "#"
    grid[42][6] = "M1"
    grid[42][7] = "M2"
    for x in range(8, 16):
        grid[42][x] = "M2"
    grid[42][16] = "M3"
    grid[42][17] = "M2"
    for x in range(18, 21):
        grid[42][x] = "M3"
    grid[42][21] = "#"

    grid[41][5] = "#"
    grid[41][6] = "M1"
    grid[41][7] = "M1"
    for x in range(8, 14):
        grid[41][x] = "M1" if x % 3 == 0 else "M2"
    for x in range(14, 19):
        grid[41][x] = "M2" if x % 2 == 0 else "M3"
    grid[41][19] = "M3"
    grid[41][20] = "M3"
    grid[41][21] = "#"

    grid[40][6] = "#"
    for x in range(7, 12):
        grid[40][x] = "M1"
    for x in range(12, 17):
        grid[40][x] = "M2"
    for x in range(17, 20):
        grid[40][x] = "M3"
    grid[40][20] = "#"

    # 3. Pedestal Sub-base step (y=38..39, width x=6..20)
    grid[39][6] = "#"
    grid[39][7] = "M1"
    for x in range(8, 14):
        grid[39][x] = "M2"
    for x in range(14, 20):
        grid[39][x] = "M3"
    grid[39][20] = "#"

    grid[38][7] = "#"
    for x in range(8, 12):
        grid[38][x] = "M1"
    for x in range(12, 16):
        grid[38][x] = "M2"
    for x in range(16, 19):
        grid[38][x] = "M3"
    grid[38][19] = "#"

    # 4. Pillar Shaft (y=29..37, width x=8..18)
    for y in range(29, 38):
        grid[y][8] = "#"
        grid[y][18] = "#"
        grid[y][9] = "M1"
        for x in range(10, 15):
            grid[y][x] = "M2"
        for x in range(15, 18):
            grid[y][x] = "M3"

    grid[29][9] = "M2"
    for x in range(10, 18):
        grid[29][x] = "M3"
    grid[30][15] = "M3"
    grid[30][16] = "M3"
    grid[30][17] = "M3"

    # Carved Arcane Rune (y=32..36, x=12..14)
    grid[31][13] = "M3"
    grid[32][13] = "E1"
    grid[33][11] = "M3"
    grid[33][12] = "E2"
    grid[33][13] = "E1"
    grid[33][14] = "E2"
    grid[33][15] = "M3"
    grid[34][13] = "E1"
    grid[35][12] = "E2"
    grid[35][14] = "E2"
    grid[36][13] = "E1"
    grid[37][13] = "M3"

    # 5. Pedestal Capital (y=26..28, width x=7..19)
    grid[28][7] = "#"
    grid[28][8] = "M2"
    for x in range(9, 19):
        grid[28][x] = "M3"
    grid[28][19] = "#"

    grid[27][7] = "#"
    grid[27][8] = "M1"
    for x in range(9, 14):
        grid[27][x] = "M2"
    for x in range(14, 19):
        grid[27][x] = "M3"
    grid[27][19] = "#"

    grid[26][7] = "#"
    for x in range(8, 13):
        grid[26][x] = "M1"
    for x in range(13, 17):
        grid[26][x] = "M2"
    for x in range(17, 19):
        grid[26][x] = "M3"
    grid[26][19] = "#"

    # 6. Bust Plinth Socle (y=24..25, x=8..17)
    grid[25][8] = "#"
    grid[25][9] = "M1"
    for x in range(10, 14):
        grid[25][x] = "M2"
    for x in range(14, 17):
        grid[25][x] = "M3"
    grid[25][17] = "#"

    grid[24][9] = "#"
    grid[24][10] = "M1"
    for x in range(11, 14):
        grid[24][x] = "M2"
    for x in range(14, 16):
        grid[24][x] = "M3"
    grid[24][16] = "#"

    # 7. Bust Torso & Brooch (y=17..23)
    bust_rows = {
        17: (8, ["#", "P1", "P2", "P2", "P3", "P3", "P4", "#"]),
        18: (7, ["#", "Y1", "P1", "P2", "Y2", "Y1", "P2", "P3", "P3", "#"]),
        19: (7, ["#", "Y1", "P1", "Y2", "E1", "Y1", "Y2", "P3", "P3", "#"]),
        20: (7, ["#", "Y2", "P1", "Y2", "E1", "Y2", "Y3", "P3", "P4", "#"]),
        21: (7, ["#", "P2", "P2", "P1", "Y3", "Y2", "P3", "P3", "P4", "#"]),
        22: (8, ["#", "P2", "P2", "P3", "P3", "P3", "P4", "P4", "#"]),
        23: (8, ["#", "#", "P3", "P3", "P3", "P4", "P4", "#", "#"])
    }
    for y, (start_x, tokens) in bust_rows.items():
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    # 8. Head & Hood (y=7..16)
    hood_map = {
        7:  (12, ["#", "#", "#", "#"]),
        8:  (11, ["#", "P1", "P1", "#", "#"]),
        9:  (10, ["#", "P1", "P1", "P2", "P3", "#"]),
        10: (9,  ["#", "P1", "P1", "P2", "P2", "P3", "#", "#"]),
        11: (9,  ["#", "Y1", "Y2", "Y1", "Y2", "Y3", "P3", "#"]),
        12: (8,  ["#", "P1", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        13: (8,  ["#", "P1", "#", "K", "E1", "E2", "#", "P3", "#"]),
        14: (8,  ["#", "P2", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        15: (9,  ["#", "P2", "#", "K", "K", "K", "#", "P3", "#"]),
        16: (9,  ["#", "#", "P2", "P3", "P3", "#", "#"]),
    }
    for y, (start_x, tokens) in hood_map.items():
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    return grid

def generate_cape_frames():
    frames = []
    
    # 4 frames
    # Wavelength lambda = 20.0
    # shift = t * (20.0 / 4) = t * 5.0
    # Phase: phi(x, t) = 2*pi*(x - 18 - 5.0*t) / 20.0 + phi0
    # With phi0 = 0.1 * pi:
    # Frame 1 (t=0): Crest at 22, Trough at 32, Crest at 42
    # Frame 2 (t=1): Crest at 27, Trough at 37
    # Frame 3 (t=2): Crest at 32, Trough at 42, Crest entering at 22
    # Frame 4 (t=3): Crest at 37, Trough entering at 27
    
    for frame_idx in range(4):
        grid = create_base()
        shift = frame_idx * 5.0
        
        # We build the cape columns from x=18 to x=44
        # Calculate Y_center and amplitude for each x
        for x in range(18, 45):
            t_norm = (x - 18) / 26.0 # 0.0 at x=18, 1.0 at x=44
            
            # Amplitude grows from shoulder to tail
            # At shoulder (x=18), amplitude is very small for smooth attachment
            amp = 3.6 * (t_norm ** 0.8)
            
            # Sine wave angle
            # Note: in canvas, smaller y is HIGHER (crest), larger y is LOWER (trough)
            # So y_wave = - amp * sin(phase)
            phase = 2 * math.pi * ((x - 18 - shift) / 20.0) + (0.1 * math.pi)
            sin_val = math.sin(phase)
            cos_val = math.cos(phase)
            
            # Mean vertical position: slight lift towards the back
            y_base = 18.5 - 1.0 * t_norm
            y_center = y_base - amp * sin_val
            
            # Thickness of cape:
            # At shoulder (x=18): thickness = 5 px (from y=17 to y=21)
            # Along body: thickness = 5 to 6 px
            # At tattered tail (x >= 38): split or notched
            half_thick = 2.6 - 0.3 * (1.0 - t_norm)
            
            # Tail tattering logic (x >= 37):
            # Shred A (upper) and Shred B (lower)
            is_tail = (x >= 37)
            
            y_top_f = y_center - half_thick
            y_bot_f = y_center + half_thick
            
            y_top = int(round(y_top_f))
            y_bot = int(round(y_bot_f))
            
            # For tattered tail:
            if x >= 42:
                # Top shred extends further on some frames, lower on others
                # Let top shred end at x=44, bottom shred end at x=42
                if x > 43:
                    # Only upper tip remains
                    y_bot = y_top + 1
                elif x == 43:
                    # Upper tip and notch
                    pass
            
            # Shading factor based on slope and height
            # Upward slope / crest => Highlight P1, gold Y1
            # Downward slope / trough => Shadow P3, P4, bronze Y3
            for y in range(y_top, y_bot + 1):
                if y < 0 or y >= H:
                    continue
                
                # Check boundary for outline
                is_edge_top = (y == y_top)
                is_edge_bot = (y == y_bot)
                is_tail_tip = (x == 44) or (x == 43 and y > y_top + 2)
                
                if is_edge_top or is_edge_bot or is_tail_tip:
                    # Outline or Gold trim
                    # Terraria outline on outer edge
                    grid[y][x] = "#"
                else:
                    # Interior cloth
                    # Check if next to top or bottom edge -> Gold Trim
                    if y == y_top + 1:
                        # Top gold trim
                        if sin_val > 0.2: # Near crest
                            grid[y][x] = "Y1"
                        elif sin_val > -0.3:
                            grid[y][x] = "Y2"
                        else: # Trough
                            grid[y][x] = "Y3"
                    elif y == y_bot - 1:
                        # Bottom gold trim
                        if sin_val < -0.2: # Bottom facing light / curve
                            grid[y][x] = "Y2"
                        else:
                            grid[y][x] = "Y3"
                    else:
                        # Body of purple cape
                        # Traveling wave shading:
                        # Crest apex (sin_val > 0.4) -> P1
                        # Slope (sin_val between -0.2 and 0.4) -> P2
                        # Trough (sin_val < -0.2) -> P3
                        # Deep trough fold (sin_val < -0.6 and lower half) -> P4
                        if sin_val > 0.35:
                            grid[y][x] = "P1"
                        elif sin_val > -0.25:
                            grid[y][x] = "P2"
                        elif sin_val > -0.65:
                            grid[y][x] = "P3"
                        else:
                            grid[y][x] = "P4" if y > y_center else "P3"

        # Apply organic notch to tail (x=38..42) to make it organic tattered shreds
        for tx in range(38, 43):
            # Center of the cut
            t_norm = (tx - 18) / 26.0
            amp = 3.6 * (t_norm ** 0.8)
            phase = 2 * math.pi * ((tx - 18 - shift) / 20.0) + (0.1 * math.pi)
            sin_val = math.sin(phase)
            yc = int(round(18.5 - 1.0 * t_norm - amp * sin_val))
            
            # If tx >= 40, carve a notch in the middle of the tail
            if tx >= 40:
                grid[yc][tx] = "."
                # Ensure outline around the notch
                if grid[yc - 1][tx] not in (".", "S", "#"):
                    grid[yc - 1][tx] = "#"
                if grid[yc + 1][tx] not in (".", "S", "#"):
                    grid[yc + 1][tx] = "#"
                    
        frames.append(grid)
        
    return frames

frames = generate_cape_frames()
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/test_frame_{idx+1}.png")

# Also save GIF
gif_frames = []
for fr in frames:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/test_animation.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS = 125ms
    loop=0
)
print("Saved test_frame_1..4.png and test_animation.gif")
