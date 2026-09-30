import math
import os
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    
    # Terraria Heavy Iron Cage & Chain
    "#": (18, 21, 28, 255),    # Dark iron outline (#12151c)
    "I": (220, 230, 238, 255), # Specular iron highlight (#dce5ec)
    "T": (155, 175, 192, 255), # Iron light metal (#9db0c0)
    "M": (94, 110, 126, 255),  # Iron shadow (#5e6e7e)
    "K": (52, 63, 74, 255),    # Iron dark crevice (#343f4a)
    "B": (28, 34, 42, 255),    # Back recessed bars (Z-index behind orb) (#1c222a)
    
    # Glowing Jade Spirit Orb (Terraria Magic / Soul)
    "W": (255, 255, 255, 255), # Soul core pure white (#ffffff)
    "H": (195, 255, 234, 255), # Soul bright mint highlight (#c2ffea)
    "A": (47, 246, 176, 255),  # Brilliant jade green (#2ff6b0)
    "E": (0, 200, 130, 255),   # Deep rich emerald (#00c882)
    "G": (6, 134, 86, 255),    # Jade shadow (#068656)
    "J": (4, 75, 48, 255),     # Aura outer boundary (#044b30)
    "Z": (2, 36, 22, 255),     # Deepest soul mist (#022416)
    
    # Rule 3.6: Front Bar Rim Lighting Over Glowing Orb
    "R": (215, 255, 244, 255), # Front bar rim specular (#d5fff4)
    "S": (78, 234, 184, 255),  # Front bar rim jade glow (#4eeab8)
    "F": (20, 104, 72, 255),   # Front bar rim outline over orb (#146848)
}

def set_pixel(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def build_cage_frame(orb_radius, core_offset_y=0.0, particles=[]):
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # ==========================================
    # 1. CHAIN & SUSPENSION (Locked 100% Y/X)
    # ==========================================
    # Vertical Link 1: y = 0..3
    grid[0][23] = "T"; grid[0][24] = "I"
    grid[1][22] = "#"; grid[1][23] = "T"; grid[1][24] = "M"; grid[1][25] = "#"
    grid[2][22] = "#"; grid[2][23] = "M"; grid[2][24] = "K"; grid[2][25] = "#"
    grid[3][23] = "K"; grid[3][24] = "#"
    
    # Horizontal Link 2: y = 3..6
    grid[3][21] = "#"; grid[3][22] = "I"; grid[3][25] = "M"; grid[3][26] = "#"
    grid[4][20] = "#"; grid[4][21] = "T"; grid[4][26] = "K"; grid[4][27] = "#"
    grid[5][21] = "#"; grid[5][22] = "M"; grid[5][25] = "K"; grid[5][26] = "#"
    
    # Vertical Link 3: y = 6..8
    grid[6][23] = "T"; grid[6][24] = "I"
    grid[7][22] = "#"; grid[7][23] = "T"; grid[7][24] = "M"; grid[7][25] = "#"
    grid[8][22] = "#"; grid[8][23] = "M"; grid[8][24] = "K"; grid[8][25] = "#"
    
    # Heavy Hanging Ring: y = 8..11
    grid[9][21] = "#"; grid[9][22] = "T"; grid[9][25] = "M"; grid[9][26] = "#"
    grid[10][21] = "#"; grid[10][22] = "M"; grid[10][25] = "K"; grid[10][26] = "#"
    
    # ==========================================
    # 2. TOP DOME & ROOF (Rule 4.9: 3/4 Ellipse)
    # Center: (23.5, 13.5), Rx=10.5, Ry=4.2
    # ==========================================
    # Top Cap Central Hub: y = 11..12
    for x in range(21, 27):
        grid[11][x] = "#" if x in (21, 26) else ("I" if x in (23, 24) else "T")
        grid[12][x] = "#" if x in (21, 26) else ("M" if x < 24 else "K")
        
    for y in range(12, 16):
        for x in range(13, 35):
            dx = (x - 23.5) / 10.5
            dy = (y - 13.5) / 4.2
            d_sq = dx*dx + dy*dy
            if d_sq <= 1.05:
                if d_sq > 0.82:
                    grid[y][x] = "#"
                elif x < 19:
                    grid[y][x] = "I" if (x % 2 == 0 and y == 13) else "T"
                elif x < 27:
                    grid[y][x] = "T" if y <= 13 else "M"
                else:
                    grid[y][x] = "M" if y <= 13 else "K"

    # ==========================================
    # 3. LAYER 1: BACK BARS (Z-Index Behind Orb)
    # Back Bar 1: x = 16..17, Back Bar 2: x = 30..31
    # ==========================================
    for y in range(15, 39):
        # Back Bar 1 (left side window)
        grid[y][16] = "B"
        grid[y][17] = "#"
        # Back Bar 2 (right side window)
        grid[y][30] = "B"
        grid[y][31] = "#"

    # ==========================================
    # 4. LAYER 2: GLOWING JADE SPIRIT ORB
    # Center: (23.5, 27.0 + core_offset_y)
    # ==========================================
    orb_cx = 23.5
    orb_cy = 27.0 + core_offset_y
    for y in range(17, 37):
        for x in range(14, 34):
            dist = math.hypot(x - orb_cx, y - orb_cy)
            if dist <= orb_radius:
                norm_d = dist / orb_radius
                
                # Spherical ethereal shading
                if norm_d <= 0.28:
                    col = "W" # Brilliant core
                elif norm_d <= 0.50:
                    col = "H" # Bright mint highlight
                elif norm_d <= 0.72:
                    col = "A" # Electric jade green
                elif norm_d <= 0.88:
                    col = "E" # Emerald midtone
                elif norm_d <= 0.96:
                    col = "G" # Deep jade shadow
                else:
                    col = "J" # Outer magical boundary
                    
                # Ethereal glint highlight towards top-left
                if dist <= orb_radius * 0.42 and (x < orb_cx and y < orb_cy):
                    col = "W"
                    
                grid[y][x] = col
                
    # Detached spirit embers (Rule 4.6 Particle Separation)
    for px, py, p_char in particles:
        set_pixel(grid, px, py, p_char)

    # ==========================================
    # 5. LAYER 3: FRONT BARS (Z-Index ON TOP of Orb)
    # Symmetrically spaced with 3px open windows:
    # Corner Left:  13..14
    # Front Bar 1:  18..19
    # Center Bar:   23..24
    # Front Bar 2:  28..29
    # Corner Right: 33..34
    # ==========================================
    for y in range(15, 39):
        # Corner Left Bar (x = 13..14)
        grid[y][13] = "#"
        grid[y][14] = "I" if y % 4 == 0 else "T"
        
        # Corner Right Bar (x = 33..34)
        grid[y][33] = "M" if y % 4 == 0 else "K"
        grid[y][34] = "#"
        
        # FRONT BAR 1 (x = 18..19)
        # Check overlap with spirit orb
        dist_b1 = math.hypot(18.5 - orb_cx, y - orb_cy)
        if dist_b1 <= orb_radius + 0.6:
            # Overlaps glowing orb! Rule 3.6 Rim Lighting:
            # Left edge faces outward: dark rim outline F
            # Right edge faces the glowing orb core: intense rim highlight R/S!
            grid[y][18] = "F"
            grid[y][19] = "R" if dist_b1 <= orb_radius * 0.7 else "S"
        else:
            # Outside orb: regular Terraria iron
            grid[y][18] = "#"
            grid[y][19] = "T" if y % 4 == 0 else "M"
            
        # FRONT BAR 2 (x = 28..29)
        dist_b2 = math.hypot(28.5 - orb_cx, y - orb_cy)
        if dist_b2 <= orb_radius + 0.6:
            # Overlaps glowing orb! Rule 3.6 Rim Lighting:
            # Left edge faces the glowing orb core: intense rim highlight R/S!
            # Right edge faces outward: dark rim outline F
            grid[y][28] = "R" if dist_b2 <= orb_radius * 0.7 else "S"
            grid[y][29] = "F"
        else:
            grid[y][28] = "M" if y % 4 == 0 else "K"
            grid[y][29] = "#"
            
        # CENTER FRONT BAR (x = 23..24)
        # Passes directly through the center of the spirit orb!
        dist_bc = math.hypot(23.5 - orb_cx, y - orb_cy)
        if dist_bc <= orb_radius + 0.6:
            # Rule 3.6: Both edges catch backlight from the surrounding jade soul!
            # Silhouetted iron metal in the bar:
            grid[y][23] = "R" # Specular jade rim on left
            grid[y][24] = "K" # Silhouetted dark iron metal on right!
        else:
            grid[y][23] = "T" if y % 4 == 0 else "M"
            grid[y][24] = "M" if y % 4 == 0 else "K"

    # ==========================================
    # 6. LAYER 4: BOTTOM BASE / TRAY (Rule 4.9: 3/4 Ellipse)
    # Center: (23.5, 38.5), Rx=10.5, Ry=4.5
    # ==========================================
    for y in range(38, 44):
        for x in range(13, 35):
            dx = (x - 23.5) / 10.5
            dy = (y - 38.5) / 4.5
            d_sq = dx*dx + dy*dy
            if d_sq <= 1.08:
                if d_sq > 0.85 or y == 43:
                    grid[y][x] = "#"
                elif y == 38:
                    # Upper lip with rivets
                    grid[y][x] = "I" if x in (15, 19, 23, 27, 31) else "T"
                elif y == 39:
                    grid[y][x] = "T" if x < 22 else ("M" if x < 28 else "K")
                elif y in (40, 41):
                    grid[y][x] = "M" if x < 22 else "K"
                else:
                    grid[y][x] = "K"
                    
    # Bottom spike / teardrop finial (y = 44..46)
    grid[44][23] = "T"; grid[44][24] = "M"
    grid[44][22] = "#"; grid[44][25] = "#"
    grid[45][23] = "M"; grid[45][24] = "K"
    grid[45][22] = "#"; grid[45][25] = "#"
    grid[46][23] = "#"; grid[46][24] = "#"
    
    return grid

# Build 4 frames for the breathing soul animation
# Frame 1: Pulse in / normal state (R = 7.0)
f1_particles = [
    (21, 18, "H"),
    (26, 19, "A")
]
frame1 = build_cage_frame(orb_radius=7.0, core_offset_y=0.0, particles=f1_particles)

# Frame 2: Flare / maximum expansion (R = 7.8, breathing in)
f2_particles = [
    (20, 16, "W"), # Particle separation (Rule 4.6): detached embers rising through bars
    (21, 15, "H"),
    (27, 17, "A"),
    (16, 21, "E")
]
frame2 = build_cage_frame(orb_radius=7.8, core_offset_y=-0.5, particles=f2_particles)

# Frame 3: Contract / pulse out (R = 7.2)
f3_particles = [
    (20, 14, "H"), # Embers floating higher
    (28, 15, "A"),
    (27, 14, "E"),
    (15, 22, "A")
]
frame3 = build_cage_frame(orb_radius=7.2, core_offset_y=0.0, particles=f3_particles)

# Frame 4: Rest / smallest pulse (R = 6.5, breathing out)
f4_particles = [
    (21, 13, "G"), # Dissipating faint wisps
    (27, 13, "J")
]
frame4 = build_cage_frame(orb_radius=6.5, core_offset_y=0.5, particles=f4_particles)

frames = [frame1, frame2, frame3, frame4]

for f_idx, fr in enumerate(frames):
    assert len(fr) == H, f"Frame {f_idx+1} row count is {len(fr)}, expected {H}"
    for r_idx, r in enumerate(fr):
        assert len(r) == W, f"Frame {f_idx+1} row {r_idx} length is {len(r)}, expected {W}"

print("All 4 frames successfully built and validated (48x48)!")

sheet_img = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
pil_frames = []

for f_idx, frame_data in enumerate(frames):
    f_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = f_img.load()
    for y in range(H):
        row = frame_data[y]
        for x in range(W):
            pix[x, y] = PALETTE.get(row[x], (0, 0, 0, 0))
    sheet_img.paste(f_img, (f_idx * W, 0))
    pil_frames.append(f_img)

os.makedirs("test", exist_ok=True)
sheet_img.save("test/test_cage_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_cage_sheet_4x.png")

pil_frames_scaled = [f.resize((W * 4, H * 4), Image.NEAREST) for f in pil_frames]
pil_frames_scaled[0].save(
    "test/test_cage_preview.gif",
    save_all=True,
    append_images=pil_frames_scaled[1:],
    duration=166, # 6 FPS
    loop=0
)

print("Saved test/test_cage_sheet_4x.png and test/test_cage_preview.gif!")
