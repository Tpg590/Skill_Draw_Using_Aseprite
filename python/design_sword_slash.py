import math
import os
from PIL import Image

W, H = 48, 48

# Color Palette: FreeStyle (Crisp Hue-shifting, Brilliant Cyan & Steel Knight Sword)
PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    
    # Radiant Energy Arc & Core Highlights
    "W": (255, 255, 255, 255), # Pure white core (radiant energy)
    "H": (205, 250, 255, 255), # Soft cyan-white glow
    "A": (45, 240, 255, 255),  # Electric neon cyan
    "B": (0, 180, 235, 255),   # Rich vibrant cyan
    "C": (0, 115, 175, 255),   # Deep cyan shadow
    "D": (15, 55, 95, 255),    # Outer magical navy outline
    "Z": (6, 25, 48, 255),     # Deepest navy crevice
    
    # Knight Sword Steel Blade
    "L": (230, 242, 250, 255), # Polished steel highlight
    "M": (155, 180, 200, 255), # Steel midtone
    "K": (85, 110, 135, 255),  # Steel shadow
    "X": (40, 58, 78, 255),    # Steel dark outline
    
    # Gilded Gold Crossguard & Pommel
    "Y": (255, 235, 120, 255), # Gold highlight
    "G": (230, 170, 35, 255),  # Rich gold midtone
    "O": (155, 95, 18, 255),   # Gold shadow
    "Q": (75, 42, 10, 255),    # Dark gold outline
    
    # Leather Grip
    "U": (135, 65, 30, 255),   # Leather grip highlight
    "V": (70, 30, 12, 255),    # Dark leather shadow
}

def set_pixel(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def render_sword_up_right(grid, hx=17, hy=31, blade_len=20, glowing=True):
    # Pommel (gold diamond) in lower-left
    pom_x, pom_y = hx - 4, hy + 4
    set_pixel(grid, pom_x, pom_y, "Y")
    set_pixel(grid, pom_x, pom_y - 1, "G")
    set_pixel(grid, pom_x + 1, pom_y, "O")
    set_pixel(grid, pom_x, pom_y + 1, "Q")
    set_pixel(grid, pom_x - 1, pom_y, "Q")
    
    # Grip (leather wrapped, from pommel to guard)
    for step in range(1, 4):
        gx = pom_x + step
        gy = pom_y - step
        set_pixel(grid, gx, gy, "U")
        set_pixel(grid, gx, gy + 1, "V")
        
    # Crossguard (perpendicular wings)
    set_pixel(grid, hx, hy, "W" if glowing else "A") # Central power gem
    set_pixel(grid, hx - 1, hy, "G")
    set_pixel(grid, hx, hy + 1, "O")
    set_pixel(grid, hx - 1, hy + 1, "Q")
    
    # Upper-left wing (-1, -1)
    set_pixel(grid, hx - 1, hy - 1, "G")
    set_pixel(grid, hx - 2, hy - 1, "Y")
    set_pixel(grid, hx - 2, hy - 2, "G")
    set_pixel(grid, hx - 3, hy - 2, "Y")
    set_pixel(grid, hx - 3, hy - 3, "Q")
    set_pixel(grid, hx - 2, hy - 3, "Q")
    set_pixel(grid, hx - 1, hy - 2, "O")
    
    # Lower-right wing (+1, +1)
    set_pixel(grid, hx + 1, hy + 1, "O")
    set_pixel(grid, hx + 1, hy + 2, "O")
    set_pixel(grid, hx + 2, hy + 2, "G")
    set_pixel(grid, hx + 2, hy + 3, "O")
    set_pixel(grid, hx + 3, hy + 3, "Q")
    set_pixel(grid, hx + 3, hy + 2, "Q")
    set_pixel(grid, hx + 2, hy + 1, "Q")
    
    # Blade: spine from (hx+1, hy-1) to (hx+blade_len, hy-blade_len)
    for k in range(1, blade_len):
        sx = hx + k
        sy = hy - k
        
        # Upper cutting edge (radiant cyan magic)
        set_pixel(grid, sx, sy - 1, "A" if k < blade_len - 3 else "W")
        set_pixel(grid, sx - 1, sy - 1, "D") # Outline
        
        # Spine (polished steel fuller)
        set_pixel(grid, sx, sy, "L" if k < blade_len - 4 else "H")
        
        # Lower edge (steel shadow & blue reflection)
        set_pixel(grid, sx + 1, sy, "M" if k < blade_len - 3 else "B")
        set_pixel(grid, sx + 1, sy + 1, "X") # Outline
        
    # Needle-sharp tip at (hx + blade_len, hy - blade_len)
    tx = hx + blade_len
    ty = hy - blade_len
    set_pixel(grid, tx - 1, ty, "H")
    set_pixel(grid, tx, ty + 1, "M")
    set_pixel(grid, tx, ty, "W") # Apex glint
    set_pixel(grid, tx - 1, ty - 1, "D")
    set_pixel(grid, tx, ty - 1, "D")
    set_pixel(grid, tx + 1, ty, "D")
    set_pixel(grid, tx + 1, ty - 1, "D")

def render_sword_down_left(grid, hx=30, hy=18, blade_len=20, glowing=True):
    # Pommel (gold diamond) in upper-right
    pom_x, pom_y = hx + 4, hy - 4
    set_pixel(grid, pom_x, pom_y, "Y")
    set_pixel(grid, pom_x, pom_y + 1, "G")
    set_pixel(grid, pom_x - 1, pom_y, "O")
    set_pixel(grid, pom_x, pom_y - 1, "Q")
    set_pixel(grid, pom_x + 1, pom_y, "Q")
    
    # Grip (leather wrapped, from pommel to guard)
    for step in range(1, 4):
        gx = pom_x - step
        gy = pom_y + step
        set_pixel(grid, gx, gy, "U")
        set_pixel(grid, gx + 1, gy, "V")
        
    # Crossguard
    set_pixel(grid, hx, hy, "W" if glowing else "A") # Central power gem
    set_pixel(grid, hx + 1, hy, "G")
    set_pixel(grid, hx, hy - 1, "O")
    set_pixel(grid, hx + 1, hy - 1, "Q")
    
    # Upper-left wing (-1, -1)
    set_pixel(grid, hx - 1, hy - 1, "G")
    set_pixel(grid, hx - 2, hy - 1, "Y")
    set_pixel(grid, hx - 2, hy - 2, "G")
    set_pixel(grid, hx - 3, hy - 2, "Y")
    set_pixel(grid, hx - 3, hy - 3, "Q")
    set_pixel(grid, hx - 2, hy - 3, "Q")
    set_pixel(grid, hx - 1, hy - 2, "O")
    
    # Lower-right wing (+1, +1)
    set_pixel(grid, hx + 1, hy + 1, "O")
    set_pixel(grid, hx + 1, hy + 2, "O")
    set_pixel(grid, hx + 2, hy + 2, "G")
    set_pixel(grid, hx + 2, hy + 3, "O")
    set_pixel(grid, hx + 3, hy + 3, "Q")
    set_pixel(grid, hx + 3, hy + 2, "Q")
    set_pixel(grid, hx + 2, hy + 1, "Q")
    
    # Blade: spine from (hx-1, hy+1) to (hx-blade_len, hy+blade_len)
    for k in range(1, blade_len):
        sx = hx - k
        sy = hy + k
        
        # Cutting edge (upper-left side: sx - 1, sy)
        set_pixel(grid, sx - 1, sy, "A" if k < blade_len - 3 else "W")
        set_pixel(grid, sx - 1, sy - 1, "D") # Outline
        
        # Spine (polished steel fuller)
        set_pixel(grid, sx, sy, "L" if k < blade_len - 4 else "H")
        
        # Back edge (lower-right side: sx, sy + 1)
        set_pixel(grid, sx, sy + 1, "M" if k < blade_len - 3 else "B")
        set_pixel(grid, sx + 1, sy + 1, "X") # Outline
        
    # Needle-sharp tip at (hx - blade_len, hy + blade_len)
    tx = hx - blade_len
    ty = hy + blade_len
    set_pixel(grid, tx, ty - 1, "H")
    set_pixel(grid, tx + 1, ty, "M")
    set_pixel(grid, tx, ty, "W") # Apex glint
    set_pixel(grid, tx - 1, ty, "D")
    set_pixel(grid, tx, ty + 1, "D")
    set_pixel(grid, tx - 1, ty - 1, "D")

# Frame 1: Anticipation (Kiếm giương cao góc Trên-Phải)
def build_frame_1():
    grid = [["." for _ in range(W)] for _ in range(H)]
    render_sword_up_right(grid, hx=17, hy=31, blade_len=21, glowing=True)
    
    # Gathering energy motes / sparks around anticipation sword tip (Rule 4.6)
    tip_x, tip_y = 17 + 21, 31 - 21 # (38, 10)
    sparks = [
        (tip_x + 2, tip_y - 2, "A"),
        (tip_x + 3, tip_y - 1, "W"),
        (tip_x - 2, tip_y - 3, "B"),
        (tip_x + 1, tip_y - 4, "H"),
        (tip_x + 4, tip_y + 1, "C"),
        (tip_x - 4, tip_y - 1, "B"),
    ]
    for px, py, c in sparks:
        set_pixel(grid, px, py, c)
        
    return grid

# Frame 2: Smear Frame / Vung cực đại (Arc Slash VFX)
def build_frame_2():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # Outer curve (cutting boundary)
    P0 = (42.0, 6.0)
    P1 = (13.0, 11.0)
    P2 = (6.0, 42.0)
    
    # Inner curve (trailing boundary)
    Q0 = (42.0, 6.0)
    Q1 = (19.0, 17.0)
    Q2 = (6.0, 42.0)
    
    steps = 1400
    for s in range(steps + 1):
        t = s / steps
        # Outer point
        ox = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
        oy = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
        
        # Inner point
        ix = (1 - t)**2 * Q0[0] + 2 * (1 - t) * t * Q1[0] + t**2 * Q2[0]
        iy = (1 - t)**2 * Q0[1] + 2 * (1 - t) * t * Q1[1] + t**2 * Q2[1]
        
        seg_len = math.hypot(ix - ox, iy - oy)
        sub_steps = max(1, int(math.ceil(seg_len * 4)))
        
        for k in range(sub_steps + 1):
            u = k / sub_steps # 0 is outer curve, 1 is inner curve
            px = int(round(ox + (ix - ox) * u))
            py = int(round(oy + (iy - oy) * u))
            
            if not (0 <= px < W and 0 <= py < H):
                continue
                
            dist_c = abs(u - 0.5) * 2.0
            
            if seg_len < 1.2:
                col = "W" if dist_c < 0.6 else "A"
            else:
                if dist_c <= 0.35:
                    col = "W" # Radiant ivory-white core!
                elif dist_c <= 0.65:
                    col = "H" # Soft cyan-white
                elif dist_c <= 0.85:
                    col = "A" # Electric cyan
                elif dist_c <= 0.96:
                    col = "B" # Vibrant cyan
                else:
                    col = "C" # Deep cyan rim
                    
            grid[py][px] = col
            
    # Add crisp 1px outline D around the boundary
    outline_candidates = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] != ".":
                continue
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    if grid[ny][nx] in ("W", "H", "A", "B", "C"):
                        outline_candidates.append((x, y))
                        break
                        
    for x, y in outline_candidates:
        grid[y][x] = "D"
        
    return grid

# Frame 3: Impact / Kết thúc đòn (Sword at Bottom-Left, Shattered Particles)
def build_frame_3():
    grid = [["." for _ in range(W)] for _ in range(H)]
    render_sword_down_left(grid, hx=30, hy=18, blade_len=21, glowing=True)
    
    # Dissipating remnants of the slash arc
    ghost_trail = [
        (37, 9, "D"), (34, 11, "C"), (29, 13, "D"),
        (23, 16, "C"), (18, 22, "D"), (13, 28, "C"),
    ]
    for gx, gy, c in ghost_trail:
        set_pixel(grid, gx, gy, c)
        
    # Detached shattered energy sparks / embers (Rule 4.6 Particle Separation)
    # Exploding out from the impact point and shattered arc
    impact_x, impact_y = 30 - 21, 18 + 21 # (9, 39)
    sparks = [
        (impact_x - 3, impact_y + 2, "W"), # Impact burst
        (impact_x - 4, impact_y, "A"),
        (impact_x - 1, impact_y + 4, "H"),
        (impact_x - 5, impact_y - 2, "B"),
        (impact_x + 3, impact_y + 5, "C"),
        # Mid-air floating embers
        (15, 23, "W"), (16, 22, "A"),
        (22, 15, "A"), (24, 14, "B"),
        (31, 10, "C"), (33, 9, "D"),
    ]
    for px, py, c in sparks:
        set_pixel(grid, px, py, c)
        
    return grid

# Frame 4: Recovery / Thu chiêu (Sword lifted slightly, ready stance)
def build_frame_4():
    grid = [["." for _ in range(W)] for _ in range(H)]
    # Sword rebounds/lifts up by ~6 pixels: hilt at (28, 16), blade_len=16
    # Tip at (28 - 16, 16 + 16) = (12, 32)
    render_sword_down_left(grid, hx=28, hy=16, blade_len=16, glowing=False)
    
    # Residual faint fading motes (dimming, floating away)
    fading_motes = [
        (6, 41, "D"),
        (7, 37, "C"),
        (14, 21, "D"),
        (21, 13, "C"),
    ]
    for px, py, c in fading_motes:
        set_pixel(grid, px, py, c)
        
    # Calm cyan runic glow pulse along the fuller
    set_pixel(grid, 20, 24, "H")
    set_pixel(grid, 17, 27, "A")
    set_pixel(grid, 14, 30, "W")
    
    return grid

frames = [
    build_frame_1(),
    build_frame_2(),
    build_frame_3(),
    build_frame_4(),
]

# Validation
for f_idx, fr in enumerate(frames):
    assert len(fr) == H, f"Frame {f_idx+1} row count is {len(fr)}, expected {H}"
    for r_idx, r in enumerate(fr):
        assert len(r) == W, f"Frame {f_idx+1} row {r_idx} length is {len(r)}, expected {W}"

print("All 4 frames successfully built and validated (48x48)!")

# Generate Spritesheet and Preview
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
sheet_img.save("test/test_slash_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_slash_sheet_4x.png")

pil_frames_scaled = [f.resize((W * 4, H * 4), Image.NEAREST) for f in pil_frames]
pil_frames_scaled[0].save(
    "test/test_slash_preview.gif",
    save_all=True,
    append_images=pil_frames_scaled[1:],
    duration=125, # 8 FPS
    loop=0
)

print("Saved test/test_slash_sheet_4x.png and test/test_slash_preview.gif!")
