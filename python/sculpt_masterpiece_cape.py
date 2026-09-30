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

def build_masterpiece_frame(frame_idx):
    grid = get_flawless_base()
    
    # Traveling wave shift across 4 frames:
    # 5.0 px per frame
    shift = frame_idx * 5.0
    
    # We construct the cloth using continuous traveling waveforms:
    # Main cape trunk: x = 18 to 38
    # Upper streamer: x = 36 to 44
    # Lower streamer: x = 36 to 42
    
    cloth = {} # (x, y) -> (role, sin_val, y_center)
    
    # 1. Main trunk + wave
    for x in range(18, 39):
        t_norm = (x - 18) / 26.0
        amp = 3.6 * (t_norm ** 0.85)
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 18.2 - 1.0 * t_norm
        y_center = y_mean - amp * sin_val
        thick = 5.2 - 0.5 * t_norm
        
        y_top = int(round(y_center - thick / 2.0))
        y_bot = int(round(y_center + thick / 2.0))
        
        # Shoulder anchor
        if x == 18:
            y_top = 16
            y_bot = 21
        elif x == 19:
            y_top = max(15, min(17, y_top))
            y_bot = max(20, min(22, y_bot))
            
        for y in range(y_top, y_bot + 1):
            if 0 <= y < H:
                cloth[(x, y)] = ("MAIN", sin_val, y_center, y_top, y_bot)

    # 2. Upper Streamer (x = 36 to 44)
    # Flaps with the traveling wave, offset slightly upward
    for x in range(36, 45):
        t_norm = (x - 18) / 26.0
        amp = 4.0 * (t_norm ** 0.85)
        # Upper streamer phase
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 17.0 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val - 1.2 # Lifted up
        
        # Streamer thickness tapers gently: 4px -> 3px -> 2px at tip (x=44)
        if x <= 39:
            s_thick = 3.6
        elif x <= 42:
            s_thick = 3.0
        elif x == 43:
            s_thick = 2.4
        else: # x == 44
            s_thick = 2.0
            
        y_top = int(round(y_center - s_thick / 2.0))
        y_bot = int(round(y_center + s_thick / 2.0))
        
        for y in range(y_top, y_bot + 1):
            if 0 <= y < H:
                cloth[(x, y)] = ("UPPER", sin_val, y_center, y_top, y_bot)

    # 3. Lower Streamer (x = 36 to 42)
    # Flaps with the traveling wave, offset slightly downward, ends at x=42
    for x in range(36, 43):
        t_norm = (x - 18) / 26.0
        amp = 3.6 * (t_norm ** 0.85)
        # Lower streamer phase (slight lag creates organic fluid flutter)
        phase = 2.0 * math.pi * ((x - 18 - shift - 1.5) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 19.4 - 0.8 * t_norm
        y_center = y_mean - amp * sin_val + 1.2 # Lower
        
        if x <= 39:
            s_thick = 3.4
        elif x <= 41:
            s_thick = 2.8
        else: # x == 42
            s_thick = 2.0
            
        y_top = int(round(y_center - s_thick / 2.0))
        y_bot = int(round(y_center + s_thick / 2.0))
        
        for y in range(y_top, y_bot + 1):
            if 0 <= y < H:
                # Carve notch: only add if not colliding with upper streamer
                cloth[(x, y)] = ("LOWER", sin_val, y_center, y_top, y_bot)

    # Carve a clear organic notch between the two streamers at x=38..41
    # Find the midpoint between upper and lower streamers
    for x in range(38, 42):
        col_ys = [y for (cx, y) in cloth if cx == x]
        if len(col_ys) >= 6:
            mid_y = int(round(sum(col_ys) / len(col_ys)))
            if (x, mid_y) in cloth:
                del cloth[(x, mid_y)]
            if len(col_ys) >= 7 and (x, mid_y + 1) in cloth:
                del cloth[(x, mid_y + 1)]

    # 4. Outlining pass: Every cloth pixel adjacent to transparency becomes '#'
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
            # Interior Shading
            sin_val, y_center = data[1], data[2]
            
            # Check proximity to top edge (gold trim)
            is_top_trim = ((x, y - 1) in rendered_cape and rendered_cape[(x, y - 1)] == "#") or ((x, y - 1) not in cloth)
            is_bot_trim = ((x, y + 1) in rendered_cape and rendered_cape[(x, y + 1)] == "#") or ((x, y + 1) not in cloth)
            
            if is_top_trim:
                if sin_val > 0.2:
                    rendered_cape[(x, y)] = "Y1"
                elif sin_val > -0.3:
                    rendered_cape[(x, y)] = "Y2"
                else:
                    rendered_cape[(x, y)] = "Y3"
            elif is_bot_trim:
                if sin_val < -0.3:
                    rendered_cape[(x, y)] = "Y2"
                else:
                    rendered_cape[(x, y)] = "Y3"
            else:
                # Purple core
                if sin_val > 0.35:
                    rendered_cape[(x, y)] = "P1"
                elif sin_val > -0.05:
                    rendered_cape[(x, y)] = "P2"
                elif sin_val > -0.5:
                    rendered_cape[(x, y)] = "P3"
                else:
                    rendered_cape[(x, y)] = "P4" if y > y_center else "P3"

    # Apply onto grid
    for (x, y), code in rendered_cape.items():
        if x >= 18:
            grid[y][x] = code

    # Ensure shoulder seal at x=18
    for y in range(15, 23):
        if grid[y][18] != "." and grid[y][17] == ".":
            grid[y][17] = "#"

    return grid

frames = [build_masterpiece_frame(i) for i in range(4)]

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
    print(f"Masterpiece Frame {i+1} naked pixels: {len(n)}")

# Verify wave peak progression
print("\n--- TRAVELING WAVE METRICS ---")
for i, fr in enumerate(frames):
    p1_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P1"]
    p4_xs = [x for x in range(18, 45) for y in range(H) if fr[y][x] == "P4"]
    # Top edge of wave
    top_ys = {x: min(y for y in range(H) if fr[y][x] not in (".", "S")) for x in range(19, 45) if any(fr[y][x] not in (".", "S") for y in range(H))}
    min_y = min(top_ys.values())
    crest_xs = [x for x, y in top_ys.items() if y == min_y]
    
    p1_mean = sum(p1_xs)/len(p1_xs) if p1_xs else 0
    p4_mean = sum(p4_xs)/len(p4_xs) if p4_xs else 0
    print(f"Frame {i+1}: Crest Apex X={crest_xs} (y_min={min_y}), Highlight P1 Mean X={p1_mean:.1f} | Crevice P4 Mean X={p4_mean:.1f}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/master_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/master_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/master_sheet.png")

print("\nSaved master_sheet.png and master_anim.gif")
