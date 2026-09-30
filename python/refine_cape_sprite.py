import math
import os
from PIL import Image

W, H = 48, 48

# Terraria Palette
# High contrast, deep near-black outline, specular highlights, rich purple cloth, glowing magic runes
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

    # Ancient Stone Pedestal & Bust Mount
    "M1": (152, 164, 184, 255), # Stone highlight (#98a4b8)
    "M2": (94, 106, 126, 255),  # Stone midtone (#5e6a7e)
    "M3": (52, 58, 74, 255),    # Stone deep shadow (#343a4a)

    # Void & Arcane Eyes/Runes (OSL Exception)
    "K":  (10, 6, 15, 255),     # Pitch black face void under cowl (#0a060f)
    "E1": (112, 255, 255, 255), # Arcane glow cyan highlight (#70ffff)
    "E2": (38, 160, 196, 255),  # Arcane glow cyan/blue shade (#26a0c4)
}

def create_master_pedestal_and_bust():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Contact Ground Shadow S (y=44..47, centered under pedestal base x=5..21)
    # Smooth ellipse
    for x in range(5, 22):
        grid[44][x] = "S"
    for x in range(4, 23):
        grid[45][x] = "S"
    for x in range(6, 21):
        grid[46][x] = "S"
    for x in range(9, 18):
        grid[47][x] = "S"

    # 2. Pedestal Plinth Base (y=40..43, width x=5..21)
    # y=43: bottom row outline and contact shadow
    for x in range(5, 22):
        grid[43][x] = "#"
    grid[43][6] = "M3"
    grid[43][7] = "M3"
    grid[43][19] = "M3"
    grid[43][20] = "M3"

    # y=42: plinth body with stone texture and notch
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

    # y=41: plinth top bevel with specular highlight on left
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

    # y=40: plinth step top
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
    # Glowing cyan arcane rune with carved recess
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
    # Left shoulder draping, chest, golden brooch with cyan gem
    # The right shoulder/collar at x=17..18 seamlessly anchors the cape!
    bust_rows = {
        17: (8, ["#", "P1", "P2", "P2", "P3", "P3", "P3", "#"]),
        18: (7, ["#", "Y1", "P1", "P2", "Y2", "Y1", "P2", "P3", "P3"]),
        19: (7, ["#", "Y1", "P1", "Y2", "E1", "Y1", "Y2", "P3", "P3", "P3"]),
        20: (7, ["#", "Y2", "P1", "Y2", "E1", "Y2", "Y3", "P3", "P4", "P4"]),
        21: (7, ["#", "P2", "P2", "P1", "Y3", "Y2", "P3", "P3", "P4", "#"]),
        22: (8, ["#", "P2", "P2", "P3", "P3", "P3", "P4", "P4", "#"]),
        23: (8, ["#", "#", "P3", "P3", "P3", "P4", "P4", "#", "#"])
    }
    for y, (start_x, tokens) in bust_rows.items():
        for idx, tok in enumerate(tokens):
            if tok != ".":
                grid[y][start_x + idx] = tok

    # 8. Head & Mysterious Cowl Hood (y=7..16)
    # Terraria mystic wizard/cultist hood: void face K, glowing eyes E1/E2
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

def build_frame(frame_idx):
    grid = create_master_pedestal_and_bust()
    
    # Mathematical Traveling Wave parameters:
    # Wavelength lambda = 20.0
    # Phase shift per frame = 5.0
    shift = frame_idx * 5.0
    
    # We will record the crest and trough coordinates
    crest_x = None
    max_height = 999
    
    # Cape spans from x=17 to x=44
    for x in range(17, 45):
        t_norm = (x - 17) / 27.0 # 0.0 at x=17, 1.0 at x=44
        
        # Amplitude increases organically with distance from shoulder
        # At anchor (x=17): amp is 0.0 for seamless attachment
        amp = 3.6 * (t_norm ** 0.85)
        
        # Traveling wave phase:
        # phi0 = 0.05 * pi
        phase = 2.0 * math.pi * ((x - 17 - shift) / 20.0) + (0.05 * math.pi)
        sin_val = math.sin(phase)
        
        # Mean baseline: cape billows back and slightly upward in strong wind
        y_mean = 18.0 - 1.2 * t_norm
        y_center = y_mean - amp * sin_val
        
        # Cape thickness: 5 to 6 px, tapering towards the tail tips
        thick = 5.4 - 1.2 * (t_norm ** 1.5)
        
        y_top_f = y_center - thick / 2.0
        y_bot_f = y_center + thick / 2.0
        
        y_top = int(round(y_top_f))
        y_bot = int(round(y_bot_f))
        
        # Ensure smooth shoulder anchoring at x=17..18
        if x == 17:
            y_top = 17
            y_bot = 21
        elif x == 18:
            y_top = max(16, min(17, y_top))
            y_bot = max(20, min(22, y_bot))
            
        # Tattered tail splitting (x >= 40):
        # We split the cloth into an upper streamer (Tip A) and lower streamer (Tip B)
        # separated by an organic notch
        is_split = (x >= 40)
        
        # Color each pixel in column x
        for y in range(y_top, y_bot + 1):
            if y < 0 or y >= H:
                continue
                
            # Notch cutout for tattered tail
            if is_split:
                notch_center = int(round(y_center))
                if y == notch_center and x in (40, 41, 42):
                    grid[y][x] = "."
                    continue
                # Lower shred ends sooner (at x=42 or 43), upper shred extends to x=44
                if x >= 43 and y > notch_center:
                    continue # Lower shred has ended!
                if x == 44 and y > y_top + 1:
                    continue # Tip A tapers to 1-2px point!
                    
            # Edges get outline '#'
            is_top = (y == y_top)
            is_bot = (y == y_bot)
            is_end = (x == 44) or (x == 43 and y > int(round(y_center)))
            
            # If next to notch:
            is_notch_edge = False
            if is_split and x in (40, 41, 42):
                if y in (int(round(y_center)) - 1, int(round(y_center)) + 1):
                    is_notch_edge = True

            if is_top or is_bot or is_end or is_notch_edge:
                # Outside boundary: Terraria dark outline
                # Avoid overwriting already placed bust pixels at x=17
                if x == 17 and grid[y][x] != ".":
                    pass
                else:
                    grid[y][x] = "#"
            else:
                # Interior:
                # Layer adjacent to top outline: Gold trim
                if y == y_top + 1:
                    if sin_val > 0.2:
                        grid[y][x] = "Y1" # Bright gold highlight on crest
                    elif sin_val > -0.3:
                        grid[y][x] = "Y2" # Base gold
                    else:
                        grid[y][x] = "Y3" # Shadow gold in trough
                # Layer adjacent to bottom outline: Gold trim
                elif y == y_bot - 1:
                    if sin_val < -0.3:
                        grid[y][x] = "Y2"
                    else:
                        grid[y][x] = "Y3"
                else:
                    # Body of Cape:
                    # Crest apex (sin_val > 0.35) -> P1 (orchid highlight)
                    # Crest slope (sin_val 0.0 to 0.35) -> P2 (royal purple)
                    # Trough slope (sin_val -0.4 to 0.0) -> P3 (shadow purple)
                    # Deep trough crease (sin_val < -0.4) -> P4 (darkest crease)
                    if sin_val > 0.35:
                        grid[y][x] = "P1"
                    elif sin_val > 0.0:
                        grid[y][x] = "P2"
                    elif sin_val > -0.45:
                        grid[y][x] = "P3"
                    else:
                        grid[y][x] = "P4" if y > y_center else "P3"

    return grid

# Build all 4 frames and verify crest coordinates
frames = [build_frame(i) for i in range(4)]

def find_primary_crest_and_trough(frame, frame_idx):
    # Scan cape columns x=19..44
    min_y = 999
    crest_x = []
    max_y = -999
    trough_x = []
    
    # Also find P1 highlight center of mass in cape
    p1_xs = []
    p4_xs = []
    
    for x in range(19, 45):
        col_ys = [y for y in range(H) if frame[y][x] not in (".", "S") and frame[y][x] in ("#", "P1", "P2", "P3", "P4", "Y1", "Y2", "Y3")]
        if not col_ys:
            continue
        top_y = min(col_ys)
        bot_y = max(col_ys)
        
        for y in col_ys:
            if frame[y][x] == "P1":
                p1_xs.append(x)
            elif frame[y][x] == "P4":
                p4_xs.append(x)
                
    # Find crest peak
    # Wave peak is where top_y is minimum in the primary wave zone
    return p1_xs, p4_xs

print("Frames built. Checking crests...")
for i in range(4):
    p1s, p4s = find_primary_crest_and_trough(frames[i], i)
    p1_mean = sum(p1s)/len(p1s) if p1s else 0
    p4_mean = sum(p4s)/len(p4s) if p4s else 0
    print(f"Frame {i+1}: P1 highlight Xs={sorted(list(set(p1s)))}, Mean P1 X={p1_mean:.1f}; P4 crevice Xs={sorted(list(set(p4s)))}, Mean P4 X={p4_mean:.1f}")

# Save PNG and GIF for inspection
gif_frames = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/refined_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/refined_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125,
    loop=0
)
print("Saved refined_f1..4.png and refined_anim.gif")
