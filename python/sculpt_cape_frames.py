import math
import os
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

def get_static_base():
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
        grid[y][9] = "M1" # Left highlight edge
        for x in range(10, 15):
            grid[y][x] = "M2"
        for x in range(15, 18):
            grid[y][x] = "M3" # Right shadow edge

    # Shadow cast by capital under overhang (y=29..30)
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

    # 6. Bust Socle / Mounting Plinth (y=24..25, x=8..17)
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
    hood_map = {
        7:  (12, ["#", "#", "#", "#"]),
        8:  (11, ["#", "P1", "P1", "#", "#"]),
        9:  (10, ["#", "P1", "P1", "P2", "P3", "#"]),
        10: (9,  ["#", "P1", "P1", "P2", "P2", "P3", "#", "#"]),
        11: (9,  ["#", "Y1", "Y2", "Y1", "Y2", "Y3", "P3", "#"]),
        12: (8,  ["#", "P1", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        13: (8,  ["#", "P1", "#", "K", "E1", "E2", "#", "P3", "P3", "#"]),
        14: (8,  ["#", "P2", "#", "K", "K", "K", "K", "K", "#", "P3", "#"]),
        15: (9,  ["#", "P2", "#", "K", "K", "K", "#", "P3", "#"]),
        16: (9,  ["#", "#", "P2", "P3", "P3", "#", "#"]),
    }
    for y, (start_x, tokens) in hood_map.items():
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    return grid

# Now define sculpt_frame with precise math + edge outline pass
def sculpt_frame(frame_idx):
    grid = get_static_base()
    
    # Mathematical Traveling Wave
    # lambda = 20.0
    shift = frame_idx * 5.0
    
    # Map of cape pixels before outlining:
    # (x, y) -> raw token
    cloth = {}
    
    for x in range(18, 45):
        t_norm = (x - 18) / 26.0
        # Amplitude increases away from shoulder
        amp = 3.8 * (t_norm ** 0.85)
        
        # Traveling wave phase
        # Frame 0: crest at x=23, trough at x=33
        # Frame 1: crest at x=28, trough at x=38
        # Frame 2: crest at x=33, trough at x=43
        # Frame 3: crest at x=38, trough at x=28
        phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        y_mean = 18.0 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        
        # Cloth thickness
        thick = 5.2 - 1.0 * (t_norm ** 1.3)
        y_top = int(round(y_center - thick / 2.0))
        y_bot = int(round(y_center + thick / 2.0))
        
        # Shoulder anchoring at x=18
        if x == 18:
            y_top = 16
            y_bot = 21
        elif x == 19:
            y_top = max(15, min(17, y_top))
            y_bot = max(20, min(22, y_bot))

        # Tattered tail splitting (x >= 40):
        # We produce two organic streamers with a notch in between
        for y in range(y_top, y_bot + 1):
            if y < 0 or y >= H:
                continue
                
            # Notch logic
            if x >= 40:
                yc_round = int(round(y_center))
                # Notch cutout in center
                if y == yc_round and x in (40, 41, 42):
                    continue
                # Lower shred ends at x=42
                if x >= 43 and y > yc_round:
                    continue
                # Upper shred tapers to a fine tip at x=44
                if x == 44 and y > y_top + 1:
                    continue

            # Assign color roles:
            # Top row gets gold trim
            if y == y_top:
                trim_color = "Y1" if sin_val > 0.2 else ("Y2" if sin_val > -0.3 else "Y3")
                cloth[(x, y)] = ("TRIM_TOP", trim_color)
            elif y == y_bot:
                trim_color = "Y2" if sin_val < -0.3 else "Y3"
                cloth[(x, y)] = ("TRIM_BOT", trim_color)
            else:
                # Purple interior
                if sin_val > 0.35:
                    cloth[(x, y)] = ("BODY", "P1")
                elif sin_val > -0.05:
                    cloth[(x, y)] = ("BODY", "P2")
                elif sin_val > -0.5:
                    cloth[(x, y)] = ("BODY", "P3")
                else:
                    cloth[(x, y)] = ("BODY", "P4" if y > y_center else "P3")

    # Now, generate proper Terraria outer outline for cloth:
    # Any cloth pixel that touches empty space (or diagonal corner) gets outline '#'
    # But wait: if we turn the outer pixels into '#', we must keep gold trim inside!
    # Better approach:
    # Expand cloth boundary by 1px for '#' outline, OR assign outer layer as '#' and second layer as gold trim!
    # Let's inspect: for each (x, y) in cloth:
    # Does it have a neighbor in cloth?
    final_cape = {}
    for (x, y), (role, col) in cloth.items():
        # Check 4-connectivity to outside of cloth
        is_boundary = False
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in cloth:
                is_boundary = True
                break
        if is_boundary:
            final_cape[(x, y)] = "#"
        else:
            # Check if adjacent to top boundary -> TRIM_TOP
            adj_top = False
            adj_bot = False
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in cloth and cloth[(nx, ny)][0] == "TRIM_TOP":
                    adj_top = True
                if (nx, ny) in cloth and cloth[(nx, ny)][0] == "TRIM_BOT":
                    adj_bot = True
            if adj_top:
                phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
                sv = math.sin(phase)
                final_cape[(x, y)] = "Y1" if sv > 0.2 else ("Y2" if sv > -0.3 else "Y3")
            elif adj_bot:
                phase = 2.0 * math.pi * ((x - 18 - shift) / 20.0) + (0.05 * math.pi)
                sv = math.sin(phase)
                final_cape[(x, y)] = "Y2" if sv < -0.3 else "Y3"
            else:
                final_cape[(x, y)] = col

    # Apply final_cape onto grid (avoid overwriting bust at x < 18)
    for (x, y), code in final_cape.items():
        if x >= 18:
            grid[y][x] = code

    # Ensure clean connection at shoulder seam (x=18):
    # Close any small gaps
    if grid[16][18] == "#" and grid[16][17] == ".":
        grid[16][17] = "#"
        
    return grid

frames = [sculpt_frame(i) for i in range(4)]

# Verify outline completeness: no colored pixel touches '.' without '#'
def check_outline_completeness(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#"):
                # Check 4 neighbors
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, code, nx, ny))
    return naked

for i, fr in enumerate(frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels touching transparent: {len(n)}")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/sculpt_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/sculpt_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)

# Comparison sheet
w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/sculpt_sheet.png")

print("Saved sculpt_sheet.png and sculpt_anim.gif")
