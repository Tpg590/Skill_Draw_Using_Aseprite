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

def build_artisan_frame(frame_idx):
    grid = get_flawless_base()
    
    # Traveling wave shift:
    # 5.0 px per frame
    shift = frame_idx * 5.0
    
    # We will build the cape from x=18 to x=43 (or 44)
    # Using a continuous traveling wave with proper aerodynamic cloth damping at the tail
    cloth = {}
    
    # Max x for each frame:
    # In Frame 1 and 4 (lifted), upper streamer reaches x=43
    # In Frame 2 and 3 (trailing/downturned), reaches x=42 or 43
    max_x = 43
    
    for x in range(18, max_x + 1):
        t_norm = (x - 18) / 25.0
        
        # Envelope:
        # Smooth flex starting from shoulder (amp at x=18 is 0.6 for gentle drape)
        amp = 0.6 + 3.2 * (t_norm ** 0.85)
        
        # Traveling wave phase
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        # Mean Y height
        y_mean = 18.2 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        
        # Cloth thickness: tapers naturally towards the tip
        if x <= 36:
            thick = 5.2 - 0.4 * t_norm
        elif x <= 40:
            thick = 4.6
        elif x <= 42:
            thick = 3.8
        else: # x == 43
            thick = 3.0
            
        y_top = int(round(y_center - thick / 2.0))
        y_bot = int(round(y_center + thick / 2.0))
        
        # Shoulder anchoring
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
                
            # Organic tattering:
            # At x=39..41, carve an organic notch
            if x in (39, 40, 41) and y == yc_round:
                continue
            # At x >= 42, lower shred tapers off
            if x == 42 and y > yc_round:
                # Keep 1 pixel of lower shred tip
                if y > yc_round + 1:
                    continue
            if x == 43 and y >= yc_round:
                # Lower shred already ended, only upper streamer reaches x=43
                continue
                
            cloth[(x, y)] = (x, y, sin_val, y_center, y_top, y_bot)

    # Outlining pass:
    # Outer layer of cloth becomes '#'
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
            # Interior pixel
            sin_val, y_center = data[2], data[3]
            
            # Distance to upper/lower boundaries
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

    # Make sure tip at x=max_x has proper core pixel if it's 3px tall:
    # If a column at max_x has 3 pixels: top '#', center 'Y1'/'P1', bottom '#'
    col_max = [y for (cx, y) in cloth if cx == max_x]
    if len(col_max) >= 3:
        top_m = min(col_max)
        bot_m = max(col_max)
        rendered_cape[(max_x, top_m)] = "#"
        rendered_cape[(max_x, bot_m)] = "#"
        mid_m = (top_m + bot_m) // 2
        # Middle pixel is bright glint/gold
        rendered_cape[(max_x, mid_m)] = "Y1" if cloth[(max_x, mid_m)][2] > 0 else "Y2"

    for (x, y), code in rendered_cape.items():
        if x >= 18:
            grid[y][x] = code
            
    # Seamless shoulder connection at x=18
    for y in range(15, 23):
        if grid[y][18] != "." and grid[y][17] == ".":
            grid[y][17] = "#"

    return grid

artisan_frames = [build_artisan_frame(i) for i in range(4)]

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

print("\n--- OUTLINE COMPLETENESS CHECK ---")
for i, fr in enumerate(artisan_frames):
    n = check_outline_completeness(fr)
    print(f"Artisan Frame {i+1} naked pixels: {len(n)}")

print("\n--- TRAVELING WAVE METRICS ---")
for i, fr in enumerate(artisan_frames):
    p1_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P1"]
    p4_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P4"]
    
    top_ys = {x: min(y for y in range(H) if fr[y][x] not in (".", "S")) for x in range(19, 44) if any(fr[y][x] not in (".", "S") for y in range(H))}
    min_y = min(top_ys.values())
    crest_xs = [x for x, y in top_ys.items() if y == min_y]
    
    bot_ys = {x: max(y for y in range(H) if fr[y][x] not in (".", "S")) for x in range(19, 44) if any(fr[y][x] not in (".", "S") for y in range(H))}
    max_y = max(bot_ys.values())
    trough_xs = [x for x, y in bot_ys.items() if y == max_y]
    
    p1_mean = sum(p1_xs)/len(p1_xs) if p1_xs else 0
    p4_mean = sum(p4_xs)/len(p4_xs) if p4_xs else 0
    print(f"Frame {i+1}: Crest Top X={crest_xs} (y_min={min_y}), Trough Bot X={trough_xs} (y_max={max_y}) | Highlight P1 Mean X={p1_mean:.1f}, Crevice P4 Mean X={p4_mean:.1f}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(artisan_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/artisan_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/artisan_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/artisan_sheet.png")

print("\nSaved artisan_sheet.png and artisan_anim.gif")
