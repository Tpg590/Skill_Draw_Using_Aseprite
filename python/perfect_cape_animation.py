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

def get_flawless_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Ground Contact Shadow S (y=44..47, centered under pedestal base x=5..21)
    for x in range(5, 22):
        grid[44][x] = "S"
    for x in range(4, 23):
        grid[45][x] = "S"
    for x in range(6, 21):
        grid[46][x] = "S"
    for x in range(9, 18):
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
    grid[42][17] = "M2" # notch
    for x in range(18, 21):
        grid[42][x] = "M3"
    grid[42][21] = "#"

    grid[41][5] = "#"
    grid[41][6] = "M1"
    grid[41][7] = "M1"
    grid[41][8] = "M1"
    for x in range(9, 14):
        grid[41][x] = "M2"
    for x in range(14, 18):
        grid[41][x] = "M3"
    grid[41][18] = "M2" # chip
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
    grid[39][8] = "M1"
    for x in range(9, 14):
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

    # 4. Pillar Shaft (y=29..37, width x=8..18, 11px wide -> Overhang rule 3.1.3)
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
    grid[30][14] = "M3"
    grid[30][15] = "M3"
    grid[30][16] = "M3"
    grid[30][17] = "M3"

    # Carved Arcane Rune on Shaft (y=32..36, x=12..14)
    grid[31][13] = "M3"
    grid[32][13] = "E1"
    grid[33][11] = "M3"
    grid[33][12] = "E2"
    grid[33][13] = "E1"
    grid[33][14] = "E2"
    grid[33][15] = "M3"
    grid[34][13] = "E1"
    grid[35][12] = "E2"
    grid[35][13] = "E1"
    grid[35][14] = "E2"
    grid[36][13] = "E1"
    grid[37][13] = "M3"

    # 5. Pedestal Capital (y=26..28, width x=7..19, 13px wide -> overhangs shaft by 1px)
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

    # 6. Bust Socle / Mounting Plinth (y=24..25, x=8..18)
    grid[25][8] = "#"
    grid[25][9] = "M1"
    for x in range(10, 14):
        grid[25][x] = "M2"
    for x in range(14, 17):
        grid[25][x] = "M3"
    grid[25][17] = "#"
    grid[25][18] = "#" # Covers capital ledge at (18, 26)

    grid[24][9] = "#"
    grid[24][10] = "M1"
    for x in range(11, 14):
        grid[24][x] = "M2"
    for x in range(14, 16):
        grid[24][x] = "M3"
    grid[24][16] = "#"

    # 7. Bust Torso, Mantle & Brooch (y=17..23)
    bust_rows = {
        17: (8, ["#", "P1", "P2", "P2", "P3", "P3", "P3", "#"]),
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

    # 8. Head & Mysterious Cowl Hood (y=7..16)
    # Fully enclosed with dark outline '#'
    hood_map = {
        7:  (12, ["#", "#", "#", "#"]),
        8:  (11, ["#", "P1", "P1", "#", "#"]),
        9:  (10, ["#", "P1", "P1", "P2", "P3", "#"]),
        10: (9,  ["#", "P1", "P1", "P2", "P2", "P3", "#", "#"]),
        11: (9,  ["#", "Y1", "Y2", "Y1", "Y2", "Y3", "P3", "#", "#"]), # Closed at x=17
        12: (8,  ["#", "P1", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        13: (8,  ["#", "P1", "#", "K", "E1", "E2", "#", "P3", "P3", "#"]),
        14: (8,  ["#", "P2", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        15: (9,  ["#", "P2", "#", "K", "K", "K", "#", "P3", "#"]),
        16: (9,  ["#", "#", "P2", "P3", "P3", "#", "#", "#"]), # Closed at x=16..17
    }
    for y, (start_x, tokens) in hood_map.items():
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    return grid

def build_perfect_frame(frame_idx):
    grid = get_flawless_base()
    
    # 4-frame traveling wave shift
    # Frame 0: shift = 0.0 -> crest at x=23, trough at x=33
    # Frame 1: shift = 5.0 -> crest at x=28, trough at x=38
    # Frame 2: shift = 10.0 -> crest at x=33, trough at x=43
    # Frame 3: shift = 15.0 -> crest at x=38, trough at x=28
    shift = frame_idx * 5.0
    
    # Step 1: Compute upper and lower envelope for each column x in [18..44]
    # We define:
    # y_center(x) = y_base(x) - amp(x) * sin(phase(x))
    # cloth_thickness(x)
    col_bounds = {}
    
    for x in range(18, 45):
        t_norm = (x - 18) / 26.0
        amp = 3.8 * (t_norm ** 0.85)
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 18.0 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        thick = 5.2 - 0.8 * (t_norm ** 1.2)
        
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
        
    # Step 2: Build cloth pixel map
    # (x, y) -> role, color
    cloth_pixels = {}
    
    for x in range(18, 45):
        y_top, y_bot, y_center, sin_val = col_bounds[x]
        
        # Tail tattering at x >= 40:
        # Shred A (upper) and Shred B (lower)
        is_tail = (x >= 40)
        yc_round = int(round(y_center))
        
        for y in range(y_top, y_bot + 1):
            if y < 0 or y >= H:
                continue
                
            # Notch logic: carve middle out at x=40..42
            if is_tail:
                if y == yc_round and x in (40, 41, 42):
                    continue
                # Lower shred ends at x=42
                if x >= 43 and y > yc_round:
                    continue
                # Upper shred tapers at x=44
                if x == 44 and y > y_top + 1:
                    continue
                    
            cloth_pixels[(x, y)] = (x, y, sin_val, y_center, y_top, y_bot)

    # Step 3: Enclose with Terraria outline '#'
    # Any pixel in cloth_pixels that has a neighbor NOT in cloth_pixels is an outline '#'
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
            
            # Check if adjacent to top outline -> Gold trim
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
                    frame_cape[(x, y)] = "Y1" # Glint on wave crest
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
                    frame_cape[(x, y)] = "P4" if y > y_center else "P3" # Deepest fold crease

    # Step 4: Apply onto grid
    for (x, y), code in frame_cape.items():
        if x >= 18:
            grid[y][x] = code
            
    # Guarantee seamless shoulder seam at x=18
    # If x=18 has an outline pixel, connect it to shoulder outline at x=17
    for y in range(15, 23):
        if grid[y][18] != "." and grid[y][17] == ".":
            grid[y][17] = "#"

    return grid

perfect_frames = [build_perfect_frame(i) for i in range(4)]

# Check outline completeness
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

for i, fr in enumerate(perfect_frames):
    n = check_outline_completeness(fr)
    print(f"Perfect Frame {i+1} naked pixels: {len(n)}")

# Find and print primary crest and trough coordinates
def get_peaks_and_valleys(fr):
    top_ys = {}
    bot_ys = {}
    p1_xs = []
    p4_xs = []
    for x in range(19, 45):
        ys = [y for y in range(H) if fr[y][x] not in (".", "S")]
        if ys:
            top_ys[x] = min(ys)
            bot_ys[x] = max(ys)
        for y in range(H):
            if fr[y][x] == "P1":
                p1_xs.append(x)
            elif fr[y][x] == "P4":
                p4_xs.append(x)
                
    # Highest top point (minimum top_y) in wave zone
    min_top = min(top_ys.values())
    crest_xs = [x for x, y in top_ys.items() if y == min_top]
    
    # Lowest bottom point (maximum bot_y) in wave zone
    max_bot = max(bot_ys.values())
    trough_xs = [x for x, y in bot_ys.items() if y == max_bot]
    
    return crest_xs, trough_xs, p1_xs, p4_xs

print("\n--- WAVE MOTION VERIFICATION ---")
for i, fr in enumerate(perfect_frames):
    c_xs, t_xs, p1s, p4s = get_peaks_and_valleys(fr)
    p1_mean = sum(p1s)/len(p1s) if p1s else 0
    p4_mean = sum(p4s)/len(p4s) if p4s else 0
    print(f"Frame {i+1}: Crest Top Xs={c_xs} (min y), Trough Bot Xs={t_xs} (max y) | P1 Mean X={p1_mean:.1f}, P4 Mean X={p4_mean:.1f}")

# Render GIF and comparison sheet
gif_frames = []
for idx, fr in enumerate(perfect_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/perfect_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_sheet.png")

print("\nSaved perfect_sheet.png and perfect_anim.gif")
