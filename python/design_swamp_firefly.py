import os
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (18, 14, 24, 140),     # Opposing cast shadow (Alpha 140)
    "#": (16, 14, 20, 255),     # Terraria near-black outline (#100e14)
    
    # Ancient Stone Pillar
    "P1": (138, 146, 162, 255), # Chiseled slate highlight (#8a92a2)
    "P2": (82, 88, 102, 255),   # Weathered stone midtone (#525866)
    "P3": (42, 46, 56, 255),    # Deep stone crevice / shadow (#2a2e38)
    
    # Moss on Islet
    "M1": (114, 176, 54, 255),  # Vibrant damp moss highlight (#72b036)
    "M2": (62, 110, 34, 255),   # Deep moss green (#3e6e22)
    
    # Soil & Mud Embankment
    "E1": (66, 43, 28, 255),    # Swamp peat soil (#422b1c)
    "E2": (36, 22, 12, 255),    # Dark mud crevice (#24160c)
    
    # Swamp Water & Ripples
    "W1": (94, 224, 232, 255),  # 1px Hollow ripple crest / glimmer (#5ee0e8)
    "W2": (27, 58, 62, 255),    # Murky swamp water surface (#1b3a3e)
    "W3": (14, 30, 34, 255),    # Deep murky water pool (#0e1e22)
    
    # Magic Firefly & OSL
    "F0": (255, 255, 255, 255), # Firefly white-hot core (#ffffff)
    "F1": (66, 245, 215, 255),  # Magic firefly neon cyan aura (#42f5d7)
    "O1": (80, 212, 184, 255),  # OSL stone highlight (#50d4b8)
    "O2": (40, 122, 108, 255),  # OSL stone midtone (#287a6c)
}

def create_environment_base():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Swamp Water Pool (Oval shape at y=38..44, x=6..41)
    # CẤM sàn kẻ ngang tràn viền: Oval bounded pool!
    # y=38: top water edge
    for x in range(12, 36):
        grid[38][x] = "#"
        
    water_spans = {
        39: (9, 39),
        40: (7, 41),
        41: (7, 41),
        42: (8, 40),
        43: (10, 38),
        44: (14, 34)
    }
    for y, (x1, x2) in water_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            grid[y][x] = "W2" if (y + x) % 4 == 0 else "W3"
            
    # Bottom water boundary outline at y=45
    for x in range(14, 35):
        grid[45][x] = "#"
        
    # 2. Mossy Rocky Islet (Mound centered at x=24, y=32..42)
    # y=32: top mound outline
    for x in range(20, 29):
        grid[32][x] = "#"
        
    # y=33: upper moss surface
    grid[33][17] = "#"
    for x in range(18, 31):
        grid[33][x] = "M1" if x % 2 == 0 else "M2"
    grid[33][31] = "#"
    
    # y=34..37: main islet surface (moss + soil + stone)
    islet_spans = {
        34: (15, 33),
        35: (13, 35),
        36: (12, 36),
        37: (11, 37),
    }
    for y, (x1, x2) in islet_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            if y <= 35:
                grid[y][x] = "M1" if (x + y) % 3 == 0 else ("M2" if (x % 2 == 0) else "P2")
            else:
                grid[y][x] = "E1" if x % 3 == 0 else ("E2" if x % 2 == 0 else "P3")
                
    # y=38..41: lower islet embankment dipping into water
    embank_spans = {
        38: (12, 36),
        39: (13, 35),
        40: (15, 33),
        41: (18, 30),
    }
    for y, (x1, x2) in embank_spans.items():
        grid[y][x1] = "#"
        grid[y][x2] = "#"
        for x in range(x1 + 1, x2):
            grid[y][x] = "E1" if (x + y) % 2 == 0 else "E2"
            
    # Bottom mound rim at y=42
    for x in range(18, 31):
        grid[42][x] = "#"
        
    # Add small water reflections around islet
    for x in (8, 9, 39, 40):
        if grid[41][x] in ("W2", "W3"): grid[41][x] = "W1"
    for x in (11, 12, 36, 37):
        if grid[43][x] in ("W2", "W3"): grid[43][x] = "W1"

    # 3. Ancient Stone Pillar (Fixed structure at x=22..26, y=19..36)
    # y=19: pillar pointed cap
    grid[19][23] = "#"; grid[19][24] = "#"; grid[19][25] = "#"
    
    # y=20: pillar cap
    grid[20][22] = "#"
    grid[20][23] = "P1"; grid[20][24] = "P1"; grid[20][25] = "P2"
    grid[20][26] = "#"
    
    # y=21..35: pillar column body
    for y in range(21, 36):
        grid[y][21] = "#"
        grid[y][22] = "P1"
        grid[y][23] = "P2"
        grid[y][24] = "P2"
        grid[y][25] = "P3"
        grid[y][26] = "P3"
        grid[y][27] = "#"
        
    # Weathered carved runes on pillar at y=25, 29, 33
    grid[25][24] = "#"; grid[29][23] = "#"; grid[33][24] = "#"
    
    # y=36: pillar stepped base collar
    grid[36][20] = "#"
    grid[36][21] = "P1"
    for x in range(22, 27):
        grid[36][x] = "P2"
    grid[36][27] = "P3"
    grid[36][28] = "#"
    
    # y=37: bottom collar outline
    for x in range(20, 29):
        grid[37][x] = "#"

    return grid

def draw_firefly(grid, cx, cy):
    # Firefly: white core with cyan glow halo
    # Halo diamond
    grid[cy - 1][cx] = "F1"
    grid[cy + 1][cx] = "F1"
    grid[cy][cx - 1] = "F1"
    grid[cy][cx + 1] = "F1"
    # White-hot core
    grid[cy][cx] = "F0"

def apply_dynamic_pillar_osl(grid, frame_idx):
    if frame_idx == 0:
        # Frame 1: Firefly on Left (x=14, y=15) -> Left face lit, right dark
        for y in range(20, 36):
            grid[y][22] = "O1"
            grid[y][23] = "O2"
            grid[y][24] = "P2"
            grid[y][25] = "P3"
            grid[y][26] = "P3"
        grid[20][23] = "O1"; grid[20][24] = "O2"
    elif frame_idx == 1:
        # Frame 2: Firefly on Center (x=24, y=13) -> Top cap and crown fully lit
        grid[20][23] = "O1"; grid[20][24] = "O1"; grid[20][25] = "O1"
        for y in range(21, 26):
            grid[y][22] = "O1"; grid[y][23] = "O1"; grid[y][24] = "O1"; grid[y][25] = "O2"; grid[y][26] = "O2"
        for y in range(26, 36):
            grid[y][22] = "P1"; grid[y][23] = "O2"; grid[y][24] = "P2"; grid[y][25] = "P3"; grid[y][26] = "P3"
    elif frame_idx == 2:
        # Frame 3: Firefly on Right (x=34, y=15) -> Right face lit, left dark
        for y in range(20, 36):
            grid[y][22] = "P3"
            grid[y][23] = "P2"
            grid[y][24] = "P2"
            grid[y][25] = "O2"
            grid[y][26] = "O1"
        grid[20][24] = "O2"; grid[20][25] = "O1"
    else:
        # Frame 4: Firefly slightly center-right (x=28, y=16) -> Upper-right lit
        for y in range(20, 30):
            grid[y][22] = "P1"
            grid[y][23] = "P2"
            grid[y][24] = "O2"
            grid[y][25] = "O1"
            grid[y][26] = "O1"
        for y in range(30, 36):
            grid[y][22] = "P1"; grid[y][23] = "P2"; grid[y][24] = "P2"; grid[y][25] = "P3"; grid[y][26] = "P3"

def apply_opposing_cast_shadow(grid, frame_idx):
    # Rule 1.2: Opposing Cast Shadow
    if frame_idx == 0:
        # Frame 1: Firefly on LEFT (x=14) -> Shadow MUST stretch to the RIGHT (X_bóng > 24)
        for x in range(24, 37):
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"
        for x in range(26, 35):
            if grid[39][x] not in ("#", "."): grid[39][x] = "S"
    elif frame_idx == 1:
        # Frame 2: Firefly at CENTER (x=24) -> Shadow compact under pillar base
        for x in range(21, 28):
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"
    elif frame_idx == 2:
        # Frame 3: Firefly on RIGHT (x=34) -> Shadow MUST stretch to the LEFT (X_bóng < 24)
        for x in range(12, 25):
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"
        for x in range(14, 23):
            if grid[39][x] not in ("#", "."): grid[39][x] = "S"
    else:
        # Frame 4: Firefly slightly center-right (x=28) -> Shadow leans gently left
        for x in range(18, 25):
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"

def build_frame(frame_idx):
    grid = create_environment_base()
    apply_opposing_cast_shadow(grid, frame_idx)
    apply_dynamic_pillar_osl(grid, frame_idx)
    
    if frame_idx == 0:
        # Frame 1: Firefly at Top-Left (x=14, y=15)
        draw_firefly(grid, 14, 15)
    elif frame_idx == 1:
        # Frame 2: Firefly at Top-Center (x=24, y=13)
        draw_firefly(grid, 24, 13)
    elif frame_idx == 2:
        # Frame 3: Firefly at Top-Right (x=34, y=15)
        draw_firefly(grid, 34, 15)
        # Đồng thời mép nước bên cạnh có một giọt sương rơi xuống (x=37, y=38)
        grid[37][37] = "W1" # Dewdrop falling towards water pool
        grid[38][37] = "W1"
    else:
        # Frame 4: Firefly lùi nhẹ về tâm (x=28, y=16)
        draw_firefly(grid, 28, 16)
        # Mặt nước lan tỏa một vòng gợn sóng mỏng (Quy tắc 2.3: Hollow 1px Ellipse Ring!)
        # Water pool at x=34..40, y=40..42
        # Center of ripple at (37, 41)
        # y=40: top 1px arc
        for x in range(35, 40):
            grid[40][x] = "W1"
        # y=41: left & right 1px rim, center is HOLLOW swamp water!
        grid[41][34] = "W1"
        # x=35..39 left untouched as W2/W3 (hollow water, revealing swamp pool!)
        grid[41][40] = "W1"
        # y=42: bottom 1px arc
        for x in range(35, 40):
            grid[42][x] = "W1"

    return grid

test_frames = [build_frame(i) for i in range(4)]

# Verify Opposing Cast Shadow
print("\n=== OPPOSING CAST SHADOW VERIFICATION ===")
for i, fr in enumerate(test_frames):
    shadow_xs = [x for x in range(W) for y in (37, 38, 39) if fr[y][x] == "S"]
    mean_sx = sum(shadow_xs) / len(shadow_xs) if shadow_xs else 0
    print(f"Frame {i+1}: Shadow Mean X = {mean_sx:.1f} (Min X={min(shadow_xs)}, Max X={max(shadow_xs)}) vs Pillar Center X=24")

# Verify Hollow Ripple in Frame 4
print("\n=== HOLLOW RIPPLE VERIFICATION (FRAME 4) ===")
f4 = test_frames[3]
ripple_center_pixels = [f4[41][x] for x in range(35, 40)]
print(f"Frame 4 Ripple Center pixels (x=35..39, y=41): {ripple_center_pixels}")
is_hollow = all(c in ("W2", "W3", ".") for c in ripple_center_pixels)
print(f"Is Ripple Center 100% HOLLOW: {is_hollow}")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(test_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/swamp_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/swamp_sheet.png")

gif_frames[0].save(
    "python/swamp_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

print("\nRendered swamp_sheet.png and swamp_anim.gif successfully!")
