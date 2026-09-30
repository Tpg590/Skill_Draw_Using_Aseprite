import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (14, 24, 36, 130),     # Soft aquatic shadow (Alpha 130)
    "#": (10, 18, 28, 255),     # Clean dark navy-teal outline (#0a121c)
    
    # Real Wooden Rowboat (Rich warm oak with golden highlights)
    "A": (232, 164, 76, 255),   # Golden oak highlight (#e8a44c)
    "B": (164, 94, 38, 255),    # Warm oak midtone (#a45e26)
    "C": (84, 40, 14, 255),     # Deep oak shadow / interior floor (#54280e)
    "D": (48, 22, 10, 255),     # Deepest interior crevice (#30160a)
    
    # Storm Lantern (Golden radiant flame & OSL)
    "L1": (255, 248, 176, 255), # White-gold flame core (#fff8b0)
    "L2": (246, 166, 35, 255),  # Radiant golden-amber glow (#f6a623)
    "L3": (184, 84, 18, 255),   # Deep orange metal cage (#b85412)
    
    # Reflected Boat in Water (Teal-tinted & desaturated)
    "R1": (82, 134, 134, 255),  # Reflected wood highlight (Teal-oak #528686)
    "R2": (42, 82, 88, 255),    # Reflected wood body (Dark teal #2a5258)
    "R3": (20, 46, 52, 255),    # Deep aquatic under-crevice (#142e34)
    "RL1": (170, 230, 195, 255),# Reflected lantern core shimmer (#aae6c3)
    "RL2": (105, 185, 155, 255),# Reflected golden-teal lantern glow (#69b99b)
    
    # Water Surface Ripples (Gợn sóng hồ)
    "W1": (56, 107, 128, 255),  # Water ripple crest highlight (#386b80)
    "W2": (26, 56, 72, 255),    # Deep lake water tone (#1a3848)
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_boat_pro(grid, yw):
    # Keel is at yw, real boat extends from yw - 10 to yw (height = 11px)
    
    # 1. Stern (left transom & stern sheer line)
    grid[yw - 6][7] = "#"; grid[yw - 6][8] = "#"
    grid[yw - 5][6] = "#"; grid[yw - 5][7] = "A"; grid[yw - 5][8] = "B"; grid[yw - 5][9] = "#"
    grid[yw - 4][7] = "#"; grid[yw - 4][8] = "B"; grid[yw - 4][9] = "C"; grid[yw - 4][10] = "#"
    grid[yw - 3][8] = "#"; grid[yw - 3][9] = "C"; grid[yw - 3][10] = "#"
    grid[yw - 2][9] = "#"; grid[yw - 2][10] = "#"
    grid[yw - 1][10] = "#"; grid[yw - 1][11] = "#"
    
    # 2. Far Gunwale (mạn thuyền xa):
    for x in range(9, 35):
        grid[yw - 7][x] = "#"
        grid[yw - 6][x] = "C" # inner shadow wall
        
    # Interior floorboards & shadows (lòng thuyền, vệt ván ngang):
    for x in range(10, 34):
        grid[yw - 5][x] = "D" if (x // 4) % 2 == 0 else "C"
        
    # Stern bench (ghế lái): X=8..12
    for x in range(8, 13):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"
        
    # Midships rowing seat bench (ghế chèo giữa): X=19..25
    for x in range(19, 26):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"
        grid[yw - 4][x] = "C" # shadow under bench
        
    # Bow seat bench (ghế mũi): X=30..33
    for x in range(30, 34):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"

    # 3. Near Gunwale & Hull Planking (mạn thuyền gần):
    # Top railing of near gunwale (bright sun highlight along sheer line)
    for x in range(7, 36):
        grid[yw - 5][x] = "#"
        grid[yw - 4][x] = "A"
        
    # Upper clinker plank: vệt ngang 4 ký tự (A A A A B B B B A A A A...)
    for x in range(9, 36):
        grid[yw - 3][x] = "A" if (x // 4) % 2 == 0 else "B"
        
    # Middle clinker plank: vệt ngang 4 ký tự (B B B B C C C C B B B B...)
    for x in range(10, 35):
        grid[yw - 2][x] = "B" if (x // 4) % 2 == 1 else "C"
        
    # Lower clinker plank & keel curve: vệt gỗ tối C xen kẽ B
    for x in range(11, 34):
        grid[yw - 1][x] = "C" if (x // 5) % 2 == 0 else "B"
        
    # Keel touching water line
    for x in range(12, 33):
        grid[yw][x] = "#"

    # 4. Bow / Prow (mũi thuyền vươn cao sang phải):
    grid[yw - 5][35] = "A"; grid[yw - 5][36] = "#"
    grid[yw - 4][35] = "A"; grid[yw - 4][36] = "B"; grid[yw - 4][37] = "#"
    grid[yw - 3][35] = "B"; grid[yw - 3][36] = "C"; grid[yw - 3][37] = "#"
    grid[yw - 2][34] = "C"; grid[yw - 2][35] = "#"
    grid[yw - 1][33] = "C"; grid[yw - 1][34] = "#"

    # Graceful stem post curving up
    grid[yw - 6][36] = "A"; grid[yw - 6][37] = "#"
    grid[yw - 7][37] = "A"; grid[yw - 7][38] = "#"
    grid[yw - 8][38] = "A"; grid[yw - 8][39] = "#"
    grid[yw - 9][39] = "#"; grid[yw - 9][40] = "#"
    
    # Curved iron davit bracket extending right to hang lantern
    grid[yw - 10][40] = "#"; grid[yw - 10][41] = "#"; grid[yw - 10][42] = "#"
    grid[yw - 9][42] = "#" # hook
    
    # 5. Golden Storm Lantern hanging at X=42:
    lx, ly = 42, yw - 7
    # Cap / chimney roof
    grid[ly - 1][lx - 1] = "#"; grid[ly - 1][lx] = "L3"; grid[ly - 1][lx + 1] = "#"
    # Glass globe with radiant golden core
    grid[ly][lx - 1] = "L3"; grid[ly][lx] = "L1"; grid[ly][lx + 1] = "L3"
    grid[ly + 1][lx - 1] = "L3"; grid[ly + 1][lx] = "L2"; grid[ly + 1][lx + 1] = "L3"
    # Brass base
    grid[ly + 2][lx - 1] = "#"; grid[ly + 2][lx] = "L3"; grid[ly + 2][lx + 1] = "#"

    # OSL Golden Glow onto Prow Stem Post & Deck
    grid[yw - 8][38] = "L2"
    grid[yw - 7][37] = "L2"
    grid[yw - 6][36] = "L3"

def outline_boat_pro(grid, yw):
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def check_naked_pro(grid, yw):
    naked = []
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        naked.append((x, y, c, nx, ny))
    return naked

def draw_inverted_reflection_pro(grid, yw, f_phase):
    # Real boat height = 11 px (from yw - 10 to yw).
    # Reflected height must be strictly 60% - 70% of real boat height:
    # 11 * 0.60 = 6.6 px, 11 * 0.70 = 7.7 px
    # Therefore, reflected height MUST be exactly 7 pixels (depth d = 1..7)!
    # Ratio = 7 / 11 = 63.64% (Strictly within [60%, 70%]!).
    
    # Zigzag wave distortion shifts (+/- 1px) for depths 1..7:
    shifts = [int(round(math.sin(d * 1.35 - f_phase * 1.57))) for d in range(1, 8)]
    
    # Inverted geometry:
    # d = 1 (Y = yw + 1): Keel contact reflection
    s1 = shifts[0]
    for x in range(11 + s1, 34 + s1):
        if 0 <= x < W: grid[yw + 1][x] = "R3"
    # Water ripples flanking keel
    if 0 <= 9 + s1 < W: grid[yw + 1][9 + s1] = "W1"
    if 0 <= 10 + s1 < W: grid[yw + 1][10 + s1] = "W2"
    if 0 <= 34 + s1 < W: grid[yw + 1][34 + s1] = "W2"
    if 0 <= 35 + s1 < W: grid[yw + 1][35 + s1] = "W1"

    # d = 2 (Y = yw + 2): Inverted lower planking (vệt 4 ký tự)
    s2 = shifts[1]
    for x in range(10 + s2, 35 + s2):
        if 0 <= x < W:
            grid[yw + 2][x] = "R2" if (x // 4) % 2 == 0 else "R3"
    if 0 <= 8 + s2 < W: grid[yw + 2][8 + s2] = "W1"
    if 0 <= 36 + s2 < W: grid[yw + 2][36 + s2] = "W1"

    # d = 3 (Y = yw + 3): Inverted mid planking & near sheer (vệt 4 ký tự)
    s3 = shifts[2]
    for x in range(9 + s3, 36 + s3):
        if 0 <= x < W:
            grid[yw + 3][x] = "R1" if (x // 4) % 2 == 1 else "R2"
    if 0 <= 37 + s3 < W: grid[yw + 3][37 + s3] = "R3"

    # d = 4 (Y = yw + 4): Inverted gunwales & interior shadow
    s4 = shifts[3]
    for x in range(8 + s4, 35 + s4):
        if 0 <= x < W:
            grid[yw + 4][x] = "R2" if (x // 3) % 2 == 0 else "R3"
    # Stem post curving down-right
    for x in range(35 + s4, 38 + s4):
        if 0 <= x < W: grid[yw + 4][x] = "R1"
    if 0 <= 38 + s4 < W: grid[yw + 4][38 + s4] = "R3"

    # d = 5 (Y = yw + 5): Inverted stern transom tip & prow stem post
    s5 = shifts[4]
    # Left stern tip
    for x in range(8 + s5, 14 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Mid water break
    for x in range(20 + s5, 27 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Prow stem post
    for x in range(36 + s5, 39 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R2"
    # Lantern top reflection
    for x in range(41 + s5, 44 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "RL2"

    # d = 6 (Y = yw + 6): Inverted stem tip & radiant lantern flame core
    s6 = shifts[5]
    # Center water ripple
    if 0 <= 22 + s6 < W: grid[yw + 6][22 + s6] = "W2"
    if 0 <= 23 + s6 < W: grid[yw + 6][23 + s6] = "R3"
    # Stem post tip
    if 0 <= 38 + s6 < W: grid[yw + 6][38 + s6] = "R3"
    # Lantern flame upside down (RL1 is bright white-teal core, RL2 is golden-teal rim)
    if 0 <= 40 + s6 < W: grid[yw + 6][40 + s6] = "RL2"
    if 0 <= 41 + s6 < W: grid[yw + 6][41 + s6] = "RL1"
    if 0 <= 42 + s6 < W: grid[yw + 6][42 + s6] = "RL1"
    if 0 <= 43 + s6 < W: grid[yw + 6][43 + s6] = "RL2"

    # d = 7 (Y = yw + 7): Inverted lantern base & hook shimmer (deepest point of reflection)
    s7 = shifts[6]
    if 0 <= 41 + s7 < W: grid[yw + 7][41 + s7] = "RL2"
    if 0 <= 42 + s7 < W: grid[yw + 7][42 + s7] = "RL2"
    if 0 <= 43 + s7 < W: grid[yw + 7][43 + s7] = "W1"

def draw_water_pro(grid, yw, f_phase):
    # Surrounding lake ripples (W1, W2) in soft oval bounds
    # Ripple ring 1
    y1 = yw + 4
    if y1 < H:
        for x in (5, 6, 7):
            if grid[y1][x] == ".": grid[y1][x] = "W1" if x == 6 else "W2"
        for x in (42, 43, 44):
            if grid[y1][x] == ".": grid[y1][x] = "W2" if x == 44 else "W1"
            
    # Ripple ring 2
    y2 = yw + 7
    if y2 < H:
        for x in (7, 8):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
        for x in (44, 45):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
            
    # Soft aquatic shadow S anchored at the bottom of the canvas (Y = 39 to 45)
    # Smooth ellipse: narrow -> wide -> narrow
    ellipse_spans = {
        39: 11,
        40: 14,
        41: 16,
        42: 16,
        43: 14,
        44: 10,
        45: 6,
    }
    for y, span in ellipse_spans.items():
        for x in range(24 - span, 24 + span):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def build_pro_frame(f_idx):
    grid = empty_grid()
    # Harmonic bobbing offset:
    # F1: 0 (yw = 29)
    # F2: +1 (yw = 30, dip)
    # F3: 0 (yw = 29)
    # F4: -1 (yw = 28, rise)
    bob_offsets = [0, 1, 0, -1]
    yw = 29 + bob_offsets[f_idx]
    
    # 1. Boat
    draw_boat_pro(grid, yw)
    outline_boat_pro(grid, yw)
    
    # 2. Reflection
    draw_inverted_reflection_pro(grid, yw, f_idx)
    
    # 3. Water effects
    draw_water_pro(grid, yw, f_idx)
    
    return grid, yw

frames_data = [build_pro_frame(i) for i in range(4)]

print("\n=== PRO VERIFICATION CHECKS ===")
for i, (g, yw) in enumerate(frames_data):
    naked = check_naked_pro(g, yw)
    boat_ys = [y for x in range(W) for y in range(0, yw + 1) if g[y][x] not in (".", "S")]
    refl_ys = [y for x in range(W) for y in range(yw + 1, H) if g[y][x] in ("R1", "R2", "R3", "RL1", "RL2")]
    
    boat_h = yw - min(boat_ys) + 1 if boat_ys else 0
    refl_h = max(refl_ys) - yw if refl_ys else 0
    ratio = (refl_h / boat_h) * 100 if boat_h else 0
    
    print(f"Frame {i+1}:")
    print(f"  Naked pixels on real boat: {len(naked)}")
    print(f"  Real Boat Y range: [{min(boat_ys)}, {yw}], Height = {boat_h}px")
    print(f"  Reflected Y range: [{yw + 1}, {max(refl_ys)}], Height = {refl_h}px")
    print(f"  Compression Ratio: {ratio:.2f}% (Target: 60% - 70%)")

# Render images
gif_frames = []
for idx, (g, yw) in enumerate(frames_data):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = g[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/boat_pro_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/boat_pro_sheet.png")

gif_frames[0].save(
    "python/boat_pro_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS
    loop=0
)
print("\nGenerated boat_pro_sheet.png and boat_pro_anim.gif successfully!")
