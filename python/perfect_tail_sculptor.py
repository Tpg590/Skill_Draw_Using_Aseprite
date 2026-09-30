import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (22, 10, 30, 130),     # Soft contact ground shadow (Alpha 130)
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

from perfect_cape_animation import get_flawless_base

def build_artisan_frame_clean(frame_idx):
    grid = get_flawless_base()
    shift = frame_idx * 5.0
    
    cloth = {}
    
    # In Frame 2 (idx=1), trailing tail ends cleanly at x=42
    # In Frame 1, 3, 4, reaches x=43
    max_x = 42 if frame_idx == 1 else 43
    
    for x in range(18, max_x + 1):
        t_norm = (x - 18) / 25.0
        amp = 0.6 + 3.2 * (t_norm ** 0.85)
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 18.2 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        
        if x <= 36:
            thick = 5.2 - 0.4 * t_norm
        elif x <= 40:
            thick = 4.6
        elif x <= 42:
            thick = 3.8
        else:
            thick = 3.2
            
        y_top = int(round(y_center - thick / 2.0))
        y_bot = int(round(y_center + thick / 2.0))
        
        if x == 18:
            y_top = 16
            y_bot = 21
        elif x == 19:
            y_top = max(15, min(17, y_top))
            y_bot = max(20, min(22, y_bot))
            
        yc_round = int(round(y_center))
        
        for y in range(y_top, y_bot + 1):
            if y < 0 or y >= H:
                continue
                
            # Notch at x=39..41
            if x in (39, 40, 41) and y == yc_round:
                continue
                
            # In Frame 2, lower streamer ends at x=41, upper streamer ends at x=42 with 2px tip
            if frame_idx == 1:
                if x >= 42 and y >= yc_round:
                    continue
            else:
                # Other frames:
                if x == 42 and y > yc_round + 1:
                    continue
                if x == 43 and y >= yc_round:
                    continue
                    
            cloth[(x, y)] = (x, y, sin_val, y_center, y_top, y_bot)

    # Post-process cloth: eliminate any 1-pixel isolated spikes
    # A cloth pixel must have at least 2 neighbors in cloth (cardinal or diagonal)
    for (x, y) in list(cloth.keys()):
        if x >= 40:
            neighbors = sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx != 0 or dy != 0) and (x + dx, y + dy) in cloth)
            if neighbors <= 1:
                del cloth[(x, y)]

    # Outlining pass
    rendered_cape = {}
    for (x, y), data in cloth.items():
        is_edge = False
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in cloth:
                is_edge = True
                break
        if is_edge:
            rendered_cape[(x, y)] = "#"
        else:
            sin_val, y_center = data[2], data[3]
            is_adj_top = ((x, y - 1) in rendered_cape and rendered_cape[(x, y - 1)] == "#") or ((x, y - 1) not in cloth)
            is_adj_bot = ((x, y + 1) in rendered_cape and rendered_cape[(x, y + 1)] == "#") or ((x, y + 1) not in cloth)
            
            if is_adj_top:
                if sin_val > 0.2:
                    rendered_cape[(x, y)] = "Y1"
                elif sin_val > -0.3:
                    rendered_cape[(x, y)] = "Y2"
                else:
                    rendered_cape[(x, y)] = "Y3"
            elif is_adj_bot:
                if sin_val < -0.3:
                    rendered_cape[(x, y)] = "Y2"
                else:
                    rendered_cape[(x, y)] = "Y3"
            else:
                if sin_val > 0.35:
                    rendered_cape[(x, y)] = "P1"
                elif sin_val > -0.05:
                    rendered_cape[(x, y)] = "P2"
                elif sin_val > -0.5:
                    rendered_cape[(x, y)] = "P3"
                else:
                    rendered_cape[(x, y)] = "P4" if y > y_center else "P3"

    for (x, y), code in rendered_cape.items():
        if x >= 18:
            grid[y][x] = code
            
    # Seamless shoulder connection at x=18
    for y in range(15, 23):
        if grid[y][18] != "." and grid[y][17] == ".":
            grid[y][17] = "#"

    return grid

clean_frames = [build_artisan_frame_clean(i) for i in range(4)]

# Check naked pixels
def check_outline_completeness(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, code, nx, ny))
    return naked

for i, fr in enumerate(clean_frames):
    n = check_outline_completeness(fr)
    print(f"Clean Frame {i+1} naked pixels: {len(n)}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(clean_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/clean_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/clean_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/clean_sheet.png")

print("\nSaved clean_sheet.png and clean_anim.gif")
