import math
import os
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "S": (30, 20, 32, 130),    # Soft ground shadow (Alpha 130)
    
    # Wooden Flagpole & Finial
    "#": (54, 26, 14, 255),    # Soft dark wood outline (#361a0e)
    "T": (215, 155, 85, 255),  # Mast wood highlight (#d79b55)
    "U": (160, 105, 50, 255),  # Mast wood midtone (#a06932)
    "M": (105, 60, 26, 255),   # Mast wood shadow (#693c1a)
    
    # Gold Finial & Flag Golden Trim
    "Y": (255, 240, 160, 255), # Pure gold highlight (#fff0a0)
    "G": (255, 210, 60, 255),  # Golden trim bright (#ffd23c)
    "O": (215, 150, 30, 255),  # Golden trim midtone (#d7961e)
    "J": (145, 90, 15, 255),   # Golden trim shadow / trough (#915a0f)
    
    # Flag Cloth (Crimson Red with Crease Shading)
    "F": (58, 12, 20, 255),    # Flag soft dark outline (#3a0c14)
    "A": (255, 105, 65, 255),  # Wave crest highlight (bright coral/cam) (#ff6941)
    "B": (230, 45, 40, 255),   # Wave crest bright red (#e62d28)
    "R": (185, 25, 35, 255),   # Flag base rich crimson (#b91923)
    "C": (130, 15, 28, 255),   # Wave trough deep red shadow (#820f1c)
    "Z": (75, 10, 20, 255),    # Crevice darkest crimson/wine (#4b0a14)
    
    # Grass & Earthen Mound
    "E": (115, 175, 55, 255),  # Grass bright highlight (#73af37)
    "P": (75, 135, 35, 255),   # Grass base green (#4b8723)
    "N": (45, 85, 25, 255),    # Grass shadow green (#2d5519)
    "D": (115, 70, 38, 255),   # Earth soil brown (#734626)
    "V": (68, 38, 20, 255),    # Earth deep soil (#442614)
}

def build_flag_frame(phi_phase):
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Base Earthen Mound (Mô đất nhỏ có cỏ)
    for y in range(39, 41):
        for x in range(6, 19):
            if x in (6, 18) or (y == 39 and x in (6, 7, 17, 18)):
                grid[y][x] = "#"
            elif y == 39:
                grid[y][x] = "E" if x % 2 == 0 else "P"
            else:
                grid[y][x] = "P" if x < 13 else "N"
                
    for y in range(41, 44):
        for x in range(3, 23):
            if x in (3, 22) or (y == 41 and x in (3, 4, 21, 22)):
                grid[y][x] = "#"
            elif y == 41:
                grid[y][x] = "P" if x < 10 else "D"
            elif y == 42:
                grid[y][x] = "D" if x < 14 else "V"
            else:
                grid[y][x] = "V"

    # Soft Elliptical Ground Shadow S (Alpha 130) at y=43..46 (Rule 2.2 & 3.1.4)
    for x in range(3, 23):
        if grid[43][x] == ".":
            grid[43][x] = "S"
    for x in range(4, 22):
        if grid[44][x] == ".":
            grid[44][x] = "S"
    for x in range(6, 20):
        if grid[45][x] == ".":
            grid[45][x] = "S"
    for x in range(9, 17):
        if grid[46][x] == ".":
            grid[46][x] = "S"

    # 2. Wooden Flagpole & Golden Finial (Locked Y/X across all frames!)
    finial = [
        (3, "..##.."),
        (4, ".#YG#."),
        (5, ".#OJ#."),
        (6, "..##.."),
    ]
    for fy, row_str in finial:
        for fx, ch in enumerate(row_str, start=8):
            if ch != ".":
                grid[fy][fx] = ch
                
    for py in range(7, 41):
        grid[py][9] = "#"
        grid[py][10] = "T"
        grid[py][11] = "U"
        grid[py][12] = "#"

    # 3. Wave Propagation Dynamics for Pennant Flag (x=13 to x=42)
    wavelength = 18.0
    flag_pixels = {} # (x, y) -> color
    flag_bounds = {} # x -> (y_top, y_bot, notch_top, notch_bot)
    
    for x in range(13, 43):
        u = (x - 13) / 29.0
        amp = 3.2 * (u ** 0.85)
        wave_arg = 2 * math.pi * (x - 13) / wavelength - phi_phase
        dy = amp * math.sin(wave_arg)
        slope = math.cos(wave_arg)
        
        h_taper = 14.0 - 5.0 * (u ** 0.7)
        cy = 15.0 + 1.5 * u + dy
        
        y_top = int(round(cy - h_taper / 2.0))
        y_bot = int(round(cy + h_taper / 2.0))
        
        notch_depth = 0
        if x >= 34:
            notch_progress = (x - 34) / 8.0
            notch_depth = int(round((h_taper / 2.0 - 1.5) * notch_progress))
            
        notch_top = int(round(cy - notch_depth))
        notch_bot = int(round(cy + notch_depth))
        flag_bounds[x] = (y_top, y_bot, notch_top, notch_bot, slope)
        
        for y in range(y_top, y_bot + 1):
            if x >= 34 and notch_depth > 0:
                if notch_top <= y <= notch_bot:
                    continue
            flag_pixels[(x, y)] = "RAW"

    # Second pass: apply Golden Trim (1px inside the flag edges) and Crease Shading
    for (x, y) in list(flag_pixels.keys()):
        y_top, y_bot, notch_top, notch_bot, slope = flag_bounds[x]
        
        # Check if bordered by empty space outside flag -> Outline F
        is_outline = False
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if (nx, ny) not in flag_pixels and nx != 12:
                is_outline = True
                break
                
        if is_outline:
            flag_pixels[(x, y)] = "F" # Soft dark wine outline
            continue
            
        # Check if immediately adjacent to top/bottom outline -> Golden Trim!
        is_trim = (y in (y_top + 1, y_bot - 1)) or \
                  (x >= 34 and (y == notch_top - 1 or y == notch_bot + 1)) or \
                  (x == 41)
                  
        if is_trim:
            if slope > 0.25:
                trim_color = "Y" if y == y_top + 1 else "G" # Bright sparkling gold
            elif slope < -0.25:
                trim_color = "J" # Shadow antique gold
            else:
                trim_color = "G" if y < (y_top + y_bot) / 2 else "O"
            flag_pixels[(x, y)] = trim_color
        else:
            # Crease Shading inside the crimson cloth
            rel_y = (y - y_top) / max(1, (y_bot - y_top))
            if slope > 0.35:
                cloth_color = "A" if rel_y < 0.45 else "B" # Bright coral / red crest
            elif slope > 0.05:
                cloth_color = "B" if rel_y < 0.55 else "R"
            elif slope < -0.35:
                cloth_color = "C" if rel_y < 0.55 else "Z" # Deep ruby / dark wine trough
            elif slope < -0.05:
                cloth_color = "R" if rel_y < 0.4 else "C"
            else:
                cloth_color = "R"
            flag_pixels[(x, y)] = cloth_color

    for (x, y), color in flag_pixels.items():
        grid[y][x] = color
            
    # Draw attachment eyelets at mast
    grid[8][12] = "Y"
    grid[22][12] = "Y"
    
    return grid

frames = [
    build_flag_frame(0.0),
    build_flag_frame(math.pi / 2.0),
    build_flag_frame(math.pi),
    build_flag_frame(3.0 * math.pi / 2.0),
]

for f_idx, fr in enumerate(frames):
    for r_idx, r in enumerate(fr):
        if len(r) != 48:
            raise ValueError(f"Frame {f_idx+1} row {r_idx} has length {len(r)}, expected 48!")

print("All 4 frames successfully validated (48x48)!")

sheet_img = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
pil_frames = []

for f_idx, frame_data in enumerate(frames):
    f_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = f_img.load()
    for y in range(H):
        row = frame_data[y]
        for x in range(W):
            pix[x, y] = PALETTE.get(row[x], (0, 0, 0, 0))
    sheet_img.paste(f_img, (f_idx * W, 0))
    pil_frames.append(f_img)

os.makedirs("test", exist_ok=True)
sheet_img.save("test/test_flag_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_flag_sheet_4x.png")

print("Generated test/test_flag_sheet_4x.png successfully!")
