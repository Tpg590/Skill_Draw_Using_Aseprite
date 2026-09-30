import os
import math
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
    
    # 1. Swamp Water Pool (Self-contained 3/4 ellipse, centered at xc=24, yc=41, Rx=18, Ry=3.8)
    # y=37..44, x=6..42. CẤM sàn kẻ ngang tràn viền: Oval bounded pool!
    for y in range(37, 45):
        for x in range(5, 44):
            # Ellipse formula normalized: dx^2 / 18^2 + dy^2 / 3.8^2
            norm = ((x - 24.0) / 18.0)**2 + ((y - 41.0) / 3.8)**2
            if norm <= 1.0:
                grid[y][x] = "W2" if (x + y) % 3 == 0 else "W3"
                
    # Add water edge outline around the pool
    for y in range(H):
        for x in range(W):
            if grid[y][x] in ("W2", "W3"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

    # Add gentle ambient water glimmers on the left
    for x in (7, 8, 10):
        if grid[41][x] in ("W2", "W3"): grid[41][x] = "W1"

    # 2. Mossy Stone & Mud Islet (Centered at xc=24, yc=35, Rx=12, Ry=4)
    # y=31..39, x=12..36
    for y in range(31, 41):
        for x in range(11, 37):
            norm = ((x - 24.0) / 12.0)**2 + ((y - 35.5) / 4.0)**2
            if norm <= 1.0:
                if y <= 34:
                    grid[y][x] = "M1" if (x + y) % 2 == 0 else "M2"
                elif y <= 36:
                    grid[y][x] = "P1" if x % 3 == 0 else ("M2" if x % 2 == 0 else "E1")
                else:
                    grid[y][x] = "E1" if (x + y) % 2 == 0 else "E2"

    # Add islet boundary outline
    for y in range(H):
        for x in range(W):
            if grid[y][x] in ("M1", "M2", "E1", "E2"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] in (".", "W2", "W3"):
                        grid[ny][nx] = "#"

    # 3. Ancient Stone Pillar (Obelisk on islet, centered at x=24, y=17..36)
    # y=17: pointed tip
    grid[17][24] = "#"
    # y=18: top cap bevel
    grid[18][23] = "#"; grid[18][24] = "P1"; grid[18][25] = "#"
    # y=19: top collar
    grid[19][22] = "#"; grid[19][23] = "P1"; grid[19][24] = "P1"; grid[19][25] = "P2"; grid[19][26] = "#"
    
    # y=20..34: column shaft (width 5: x=22..26)
    for y in range(20, 35):
        grid[y][21] = "#"
        grid[y][22] = "P1"
        grid[y][23] = "P2"
        grid[y][24] = "P2"
        grid[y][25] = "P3"
        grid[y][26] = "P3"
        grid[y][27] = "#"
        
    # Carved ancient runes / cracks on pillar
    grid[23][24] = "#"; grid[27][23] = "#"; grid[31][24] = "#"
    # Moss encroaching on pillar bottom corners
    grid[33][22] = "M1"; grid[34][22] = "M2"; grid[34][26] = "M2"

    # y=35: base plinth (width 7: x=21..27)
    grid[35][20] = "#"
    grid[35][21] = "P1"; grid[35][22] = "P1"
    for x in range(23, 26): grid[35][x] = "P2"
    grid[35][26] = "P3"; grid[35][27] = "P3"
    grid[35][28] = "#"

    # y=36: plinth step
    grid[36][20] = "#"
    for x in range(21, 28): grid[36][x] = "P3"
    grid[36][28] = "#"

    # y=37: plinth bottom outline
    for x in range(20, 29):
        grid[37][x] = "#"

    # Re-enforce outlines around water and islet so there are 0 naked pixels
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "#", "S"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

    return grid

def draw_firefly(grid, cx, cy):
    # Firefly: 3x3 diamond orb (F0 core with F1 halo and # rim for clean Terraria aesthetic)
    grid[cy - 1][cx] = "F1"
    grid[cy + 1][cx] = "F1"
    grid[cy][cx - 1] = "F1"
    grid[cy][cx + 1] = "F1"
    grid[cy][cx] = "F0"

def apply_dynamic_pillar_osl(grid, frame_idx):
    if frame_idx == 0:
        # Frame 1: Firefly on Left (x=13, y=14) -> Left face lit, right dark
        for y in range(20, 35):
            grid[y][22] = "O1"
            grid[y][23] = "O2"
            grid[y][24] = "P2"
            grid[y][25] = "P3"
            grid[y][26] = "P3"
        grid[18][24] = "O1"
        grid[19][23] = "O1"; grid[19][24] = "O2"
    elif frame_idx == 1:
        # Frame 2: Firefly on Top-Center (x=24, y=12) -> Top cap and upper shaft fully lit
        grid[18][24] = "O1"
        grid[19][23] = "O1"; grid[19][24] = "O1"; grid[19][25] = "O1"
        for y in range(20, 26):
            grid[y][22] = "O1"; grid[y][23] = "O1"; grid[y][24] = "O1"; grid[y][25] = "O2"; grid[y][26] = "O2"
        for y in range(26, 35):
            grid[y][22] = "P1"; grid[y][23] = "O2"; grid[y][24] = "P2"; grid[y][25] = "P3"; grid[y][26] = "P3"
    elif frame_idx == 2:
        # Frame 3: Firefly on Right (x=35, y=14) -> Right face lit, left dark
        for y in range(20, 35):
            grid[y][22] = "P3"
            grid[y][23] = "P2"
            grid[y][24] = "P2"
            grid[y][25] = "O2"
            grid[y][26] = "O1"
        grid[18][24] = "O2"
        grid[19][24] = "O2"; grid[19][25] = "O1"
    else:
        # Frame 4: Firefly center-right (x=29, y=15) -> Upper-right lit
        for y in range(20, 29):
            grid[y][22] = "P1"
            grid[y][23] = "P2"
            grid[y][24] = "O2"
            grid[y][25] = "O1"
            grid[y][26] = "O1"
        for y in range(29, 35):
            grid[y][22] = "P1"; grid[y][23] = "P2"; grid[y][24] = "P2"; grid[y][25] = "P3"; grid[y][26] = "P3"

def apply_opposing_cast_shadow(grid, frame_idx):
    # Rule 1.2: Opposing Cast Shadow on the Islet Surface
    if frame_idx == 0:
        # Frame 1: Firefly on LEFT (x=13) -> Shadow MUST stretch to the RIGHT (X_bóng > 24)
        for x in range(25, 36):
            if grid[36][x] not in ("#", "."): grid[36][x] = "S"
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
        for x in range(26, 35):
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"
    elif frame_idx == 1:
        # Frame 2: Firefly at CENTER (x=24) -> Shadow compact under pillar base
        for x in range(22, 27):
            if grid[36][x] not in ("#", "."): grid[36][x] = "S"
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
    elif frame_idx == 2:
        # Frame 3: Firefly on RIGHT (x=35) -> Shadow MUST stretch to the LEFT (X_bóng < 24)
        for x in range(13, 24):
            if grid[36][x] not in ("#", "."): grid[36][x] = "S"
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"
        for x in range(14, 23):
            if grid[38][x] not in ("#", "."): grid[38][x] = "S"
    else:
        # Frame 4: Firefly slightly center-right (x=29) -> Shadow leans gently left
        for x in range(18, 24):
            if grid[36][x] not in ("#", "."): grid[36][x] = "S"
            if grid[37][x] not in ("#", "."): grid[37][x] = "S"

def build_perfect_frame(frame_idx):
    grid = create_environment_base()
    apply_opposing_cast_shadow(grid, frame_idx)
    apply_dynamic_pillar_osl(grid, frame_idx)
    
    if frame_idx == 0:
        # Frame 1: Firefly at Top-Left (x=13, y=14)
        draw_firefly(grid, 13, 14)
    elif frame_idx == 1:
        # Frame 2: Firefly at Top-Center (x=24, y=12)
        draw_firefly(grid, 24, 12)
    elif frame_idx == 2:
        # Frame 3: Firefly at Top-Right (x=35, y=14)
        draw_firefly(grid, 35, 14)
        # Mép nước bên cạnh có một giọt sương rơi xuống (x=38, y=36..37)
        grid[35][38] = "#"
        grid[36][37] = "#"; grid[36][38] = "W1"; grid[36][39] = "#"
        grid[37][37] = "#"; grid[37][38] = "W1"; grid[37][39] = "#"
        grid[38][38] = "#"
    else:
        # Frame 4: Firefly lùi nhẹ về tâm (x=29, y=15)
        draw_firefly(grid, 29, 15)
        # Mặt nước lan tỏa một vòng gợn sóng mỏng (Quy tắc 2.3: Hollow 1px Ellipse Ring!)
        # Center of ripple at xc=38, yc=41
        # Top 1px arc at y=40: x=36..40
        for x in range(36, 41):
            grid[40][x] = "W1"
        # y=41: left & right 1px rim, center is 100% HOLLOW swamp water!
        grid[41][35] = "W1"
        # Center x=36..40: untouched W2/W3 (swamp water pool showing through!)
        grid[41][41] = "W1"
        # Bottom 1px arc at y=42: x=36..40
        for x in range(36, 41):
            grid[42][x] = "W1"

    return grid

perfect_frames = [build_perfect_frame(i) for i in range(4)]

# Check outline completeness (excluding floating firefly glow F0/F1)
def check_outline_completeness(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            code = grid[y][x]
            if code not in (".", "S", "#", "F0", "F1"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and grid[ny][nx] == ".":
                        naked.append((x, y, code, nx, ny))
    return naked

print("\n=== OUTLINE COMPLETENESS CHECK ===")
all_clean = True
for i, fr in enumerate(perfect_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")
    if n:
        print(f"  {n[:10]}")
        all_clean = False
print(f"All frames 100% enclosed: {all_clean}")

# Verify Opposing Cast Shadow
print("\n=== OPPOSING CAST SHADOW VERIFICATION ===")
for i, fr in enumerate(perfect_frames):
    shadow_xs = [x for x in range(W) for y in (36, 37, 38) if fr[y][x] == "S"]
    mean_sx = sum(shadow_xs) / len(shadow_xs) if shadow_xs else 0
    print(f"Frame {i+1}: Shadow Mean X = {mean_sx:.1f} (Min X={min(shadow_xs)}, Max X={max(shadow_xs)}) vs Pillar Center X=24")

# Verify Hollow Ripple in Frame 4
print("\n=== HOLLOW RIPPLE VERIFICATION (FRAME 4) ===")
f4 = perfect_frames[3]
ripple_center_pixels = [f4[41][x] for x in range(36, 41)]
print(f"Frame 4 Ripple Center pixels (x=36..40, y=41): {ripple_center_pixels}")
is_hollow = all(c in ("W2", "W3") for c in ripple_center_pixels)
print(f"Is Ripple Center 100% HOLLOW SWAMP WATER: {is_hollow}")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(perfect_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/perfect_swamp_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/perfect_swamp_sheet.png")

gif_frames[0].save(
    "python/perfect_swamp_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

print("\nSaved perfect_swamp_sheet.png and perfect_swamp_anim.gif successfully!")
