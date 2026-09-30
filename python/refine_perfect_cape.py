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

def build_refined_frame(frame_idx):
    grid = get_flawless_base()
    
    # 4-frame traveling wave shift
    # Frame 0: shift = 0.0 -> crest at x=23, trough at x=33
    # Frame 1: shift = 5.0 -> crest at x=28, trough at x=38
    # Frame 2: shift = 10.0 -> crest at x=33, trough at x=43
    # Frame 3: shift = 15.0 -> crest at x=38, trough at x=28
    shift = frame_idx * 5.0
    
    col_bounds = {}
    
    for x in range(18, 45):
        t_norm = (x - 18) / 26.0
        # Gentle amplitude growth starting with slight flex at shoulder
        amp = 0.8 + 3.0 * (t_norm ** 0.9)
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 18.0 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        thick = 5.4 - 0.6 * t_norm
        
        y_top = int(round(y_center - thick / 2.0))
        y_bot = int(round(y_center + thick / 2.0))
        
        # Shoulder anchoring
        if x == 18:
            y_top = 16
            y_bot = 21
        elif x == 19:
            y_top = max(15, min(17, y_top))
            y_bot = max(20, min(22, y_bot))
            
        col_bounds[x] = (y_top, y_bot, y_center, sin_val)
        
    cloth_pixels = {}
    
    for x in range(18, 45):
        y_top, y_bot, y_center, sin_val = col_bounds[x]
        
        # Tail tattering at x >= 40:
        is_tail = (x >= 40)
        yc_round = int(round(y_center))
        
        for y in range(y_top, y_bot + 1):
            if y < 0 or y >= H:
                continue
                
            # Organic notch cutout at x=40..42
            if is_tail:
                if y == yc_round and x in (40, 41):
                    continue
                # Lower shred ends at x=42
                if x >= 43 and y >= yc_round:
                    continue
                # Upper shred extends to x=44 with a healthy 3-pixel rounded tip (no thin 1px spike!)
                if x == 44 and y > y_top + 2:
                    continue
                    
            cloth_pixels[(x, y)] = (x, y, sin_val, y_center, y_top, y_bot)

    # Enclose with Terraria outline '#'
    frame_cape = {}
    for (x, y), data in cloth_pixels.items():
        is_edge = False
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in cloth_pixels:
                is_edge = True
                break
        if is_edge:
            frame_cape[(x, y)] = "#"
        else:
            # Interior pixel
            sin_val, y_center, y_top, y_bot = data[2], data[3], data[4], data[5]
            
            is_adj_top = False
            for dy in (-1, -2):
                if (x, y + dy) not in cloth_pixels:
                    is_adj_top = True
                    break
            is_adj_bot = False
            for dy in (1, 2):
                if (x, y + dy) not in cloth_pixels:
                    is_adj_bot = True
                    break
                    
            if is_adj_top:
                # Top gold trim
                if sin_val > 0.2:
                    frame_cape[(x, y)] = "Y1" # Specular gold on crest
                elif sin_val > -0.3:
                    frame_cape[(x, y)] = "Y2"
                else:
                    frame_cape[(x, y)] = "Y3"
            elif is_adj_bot:
                # Bottom gold trim
                if sin_val < -0.3:
                    frame_cape[(x, y)] = "Y2"
                else:
                    frame_cape[(x, y)] = "Y3"
            else:
                # Purple cloth interior
                if sin_val > 0.35:
                    frame_cape[(x, y)] = "P1" # Orchid highlight on crest
                elif sin_val > -0.05:
                    frame_cape[(x, y)] = "P2" # Royal purple body
                elif sin_val > -0.5:
                    frame_cape[(x, y)] = "P3" # Shadow purple in trough
                else:
                    frame_cape[(x, y)] = "P4" if y > y_center else "P3" # Crevice shadow

    # Apply onto grid
    for (x, y), code in frame_cape.items():
        if x >= 18:
            grid[y][x] = code
            
    # Seamless shoulder connection at x=18
    for y in range(15, 23):
        if grid[y][18] != "." and grid[y][17] == ".":
            grid[y][17] = "#"

    return grid

frames = [build_refined_frame(i) for i in range(4)]

# Verify outline completeness
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
for i, fr in enumerate(frames):
    n = check_outline_completeness(fr)
    print(f"Refined Frame {i+1} naked pixels: {len(n)}")

# Verify wave peak progression
print("\n--- TRAVELING WAVE METRICS ---")
for i, fr in enumerate(frames):
    p1_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P1"]
    p4_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P4"]
    
    # Top edge of wave
    top_ys = {x: min(y for y in range(H) if fr[y][x] not in (".", "S")) for x in range(19, 45) if any(fr[y][x] not in (".", "S") for y in range(H))}
    min_y = min(top_ys.values())
    crest_xs = [x for x, y in top_ys.items() if y == min_y]
    
    # Bottom edge of wave
    bot_ys = {x: max(y for y in range(H) if fr[y][x] not in (".", "S")) for x in range(19, 45) if any(fr[y][x] not in (".", "S") for y in range(H))}
    max_y = max(bot_ys.values())
    trough_xs = [x for x, y in bot_ys.items() if y == max_y]
    
    p1_mean = sum(p1_xs)/len(p1_xs) if p1_xs else 0
    p4_mean = sum(p4_xs)/len(p4_xs) if p4_xs else 0
    print(f"Frame {i+1}: Crest Top X={crest_xs} (y_min={min_y}), Trough Bot X={trough_xs} (y_max={max_y}) | Highlight P1 Mean X={p1_mean:.1f}, Crevice P4 Mean X={p4_mean:.1f}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/refined_v2_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/refined_v2_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/refined_v2_sheet.png")

print("\nSaved refined_v2_sheet.png and refined_v2_anim.gif")
