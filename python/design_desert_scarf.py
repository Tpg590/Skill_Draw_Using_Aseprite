import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (44, 30, 24, 130),     # Soft ground shadow (Alpha 130)
    "#": (52, 28, 16, 255),     # Soft dark wood/sand outline (#341c10)
    
    # Sand Dune / Mound
    "D1": (240, 200, 128, 255), # Desert sand bright highlight (#f0c880)
    "D2": (212, 155, 76, 255),  # Golden desert sand base (#d49b4c)
    "D3": (158, 104, 46, 255),  # Desert sand shadow (#9e682e)
    
    # Weathered Wooden Post
    "W1": (196, 147, 90, 255),  # Wood highlight (#c4935a)
    "W2": (140, 88, 40, 255),   # Wood grain midtone (#8c5828)
    "W3": (86, 46, 18, 255),    # Wood deep shadow/crack (#562e12)
    "M1": (216, 200, 176, 255), # Weathered iron nail/plate highlight (#d8c8b0)
    "M2": (112, 96, 84, 255),   # Weathered iron shadow (#706054)

    # Silk Scarf - Turmeric Gold Yellow with Warm Orange Trim
    "C":  (74, 24, 8, 255),     # Soft dark cloth outline (#4a1808)
    "K1": (255, 242, 117, 255), # Saffron silk crest glint (#fff275)
    "K2": (240, 184, 36, 255),  # Golden turmeric silk midtone (#f0b824)
    "K3": (184, 122, 20, 255),  # Amber turmeric silk shadow (#b87a14)
    "O1": (240, 106, 24, 255),  # Warm glowing orange trim crest (#f06a18)
    "O2": (166, 62, 12, 255),   # Terracotta orange trim shadow (#a63e0c)
}

from design_perfect_scarf import get_clean_static_base

def build_desert_scarf_frame(frame_idx):
    grid = get_clean_static_base()
    
    # Wavelength: 24.0 px, shift: 6.0 px per frame
    shift = frame_idx * 6.0
    wavelength = 24.0
    
    cloth = {} # (x, y) -> data
    
    # Calculate y_center for each x from 14 to 44
    y_centers = {}
    sin_vals = {}
    
    for x in range(14, 45):
        # 1. Gravity Sag at x = 14..18:
        # Dips by 1.8 pixels at x = 16..17
        if x <= 18:
            t_sag = (x - 14) / 4.0
            sag = 1.8 * math.sin(t_sag * math.pi)
        else:
            sag = 0.0
            
        # 2. Traveling Wave
        # phase: at x=22, f=0 => phase = 2*pi*(6)/24 = pi/2 (Crest at x=22)
        phase = 2.0 * math.pi * ((x - 16 - shift) / wavelength)
        sin_val = math.sin(phase)
        sin_vals[x] = sin_val
        
        # Amplitude envelope: 0 at x=16, growing to 3.2 at x=36..44
        if x <= 16:
            amp = 0.0
        elif x <= 36:
            amp = 3.2 * (((x - 16) / 20.0) ** 0.85)
        else:
            amp = 3.2
            
        y_mean = 14.5 + sag - 0.8 * ((x - 14) / 30.0)
        y_c = y_mean - amp * sin_val
        y_centers[x] = y_c
        
    # Requirement 3: Tail must stream horizontally to the right
    # At x = 42, 43, 44, clamp y_center to horizontal direction
    # (dy/dx = 0)
    y_tail = y_centers[41]
    for tx in (42, 43, 44):
        y_centers[tx] = y_tail
        sin_vals[tx] = sin_vals[41]

    # Generate cloth pixels with 2-3px interior thickness (Requirement 2)
    for x in range(14, 45):
        y_c = y_centers[x]
        sin_val = sin_vals[x]
        
        # Stable thickness: interior 2-3px, total thickness with outlines 4-5px
        if x <= 42:
            thick = 4.0 # interior 2px
        elif x == 43:
            thick = 3.4
        else: # x == 44
            thick = 2.6 # clean horizontal tip
            
        y_top = int(round(y_c - thick / 2.0))
        y_bot = int(round(y_c + thick / 2.0))
        
        if x == 14:
            y_top = 13
            y_bot = 16
        elif x == 15:
            y_top = 14
            y_bot = 17
            
        # Ensure interior is at least 2 pixels tall for vibrant turmeric silk
        if y_bot - y_top < 3 and x < 44:
            y_bot = y_top + 3
            
        for y in range(y_top, y_bot + 1):
            if 0 <= y < H:
                cloth[(x, y)] = (x, y, sin_val, y_c, y_top, y_bot)

    # Outlining & Shading Pass
    rendered_scarf = {}
    for (x, y), data in cloth.items():
        is_edge = False
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in cloth:
                is_edge = True
                break
        if is_edge:
            rendered_scarf[(x, y)] = "C" # Soft dark cloth outline
        else:
            sin_val, y_c, y_top, y_bot = data[2], data[3], data[4], data[5]
            
            # Check if adjacent to top/bottom edge for orange trim
            is_adj_top = ((x, y - 1) not in cloth) or (rendered_scarf.get((x, y - 1)) == "C")
            is_adj_bot = ((x, y + 1) not in cloth) or (rendered_scarf.get((x, y + 1)) == "C")
            
            # Interior layout:
            # Top row interior: Orange Trim O1 / O2
            # Middle row interior: Golden Turmeric Silk K1 / K2 / K3
            # Bottom row interior: Orange Trim O2 / O1
            if is_adj_top and not is_adj_bot:
                rendered_scarf[(x, y)] = "O1" if sin_val > 0.1 else "O2"
            elif is_adj_bot and not is_adj_top:
                rendered_scarf[(x, y)] = "O2" if sin_val < -0.1 else "O1"
            else:
                # Golden Turmeric body
                if sin_val > 0.3:
                    rendered_scarf[(x, y)] = "K1" # Glint on wave crest
                elif sin_val > -0.2:
                    rendered_scarf[(x, y)] = "K2" # Rich saffron base
                else:
                    rendered_scarf[(x, y)] = "K3" # Deep amber shadow in trough

    # Apply onto grid
    for (x, y), code in rendered_scarf.items():
        if x >= 15:
            grid[y][x] = code
        elif x == 14 and grid[y][x] == ".":
            grid[y][x] = code

    # Seal wrap connection at x=14..15
    if grid[14][15] != "." and grid[14][14] == ".":
        grid[14][14] = "C"

    return grid

desert_frames = [build_desert_scarf_frame(i) for i in range(4)]

# Verify outline completeness
def check_outline_completeness(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "C"):
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, code, nx, ny))
    return naked

print("\n--- OUTLINE COMPLETENESS CHECK ---")
for i, fr in enumerate(desert_frames):
    n = check_outline_completeness(fr)
    print(f"Desert Frame {i+1} naked pixels: {len(n)}")

# Verify wave peak progression
print("\n--- TRAVELING WAVE METRICS ---")
for i, fr in enumerate(desert_frames):
    k1_xs = [x for x in range(16, 45) for y in range(H) if fr[y][x] == "K1"]
    k3_xs = [x for x in range(16, 45) for y in range(H) if fr[y][x] == "K3"]
    
    # Top edge of wave (excluding post x <= 14)
    top_ys = {x: min(y for y in range(H) if fr[y][x] not in (".", "S", "#")) for x in range(18, 45) if any(fr[y][x] not in (".", "S", "#") for y in range(H))}
    min_y = min(top_ys.values())
    crest_xs = [x for x, y in top_ys.items() if y == min_y]
    
    bot_ys = {x: max(y for y in range(H) if fr[y][x] not in (".", "S", "#")) for x in range(18, 45) if any(fr[y][x] not in (".", "S", "#") for y in range(H))}
    max_y = max(bot_ys.values())
    trough_xs = [x for x, y in bot_ys.items() if y == max_y]
    
    k1_mean = sum(k1_xs)/len(k1_xs) if k1_xs else 0
    k3_mean = sum(k3_xs)/len(k3_xs) if k3_xs else 0
    print(f"Frame {i+1}: Crest Top X={crest_xs} (y_min={min_y}), Trough Bot X={trough_xs} (y_max={max_y}) | Highlight K1 Mean X={k1_mean:.1f}, Shadow K3 Mean X={k3_mean:.1f}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(desert_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/desert_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/desert_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/desert_sheet.png")

print("\nSaved desert_sheet.png and desert_anim.gif")
