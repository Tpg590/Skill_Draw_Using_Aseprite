import os
import math
from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (18, 14, 24, 140),     # Soft cast shadow (Alpha 140)
    "#": (16, 14, 20, 255),     # Viền sẫm tối Terraria (#100e14)
    
    # Stone Floor Slabs
    "F1": (124, 132, 148, 255), # Stone slab highlight (#7c8494)
    "F2": (74, 80, 94, 255),    # Stone slab midtone (#4a505e)
    "F3": (38, 42, 52, 255),    # Stone slab crevice / shadow (#262a34)
    
    # Cold Iron Stand
    "I1": (154, 160, 176, 255), # Cold iron highlight (#9aa0b0)
    "I2": (84, 90, 104, 255),   # Cold iron midtone (#545a68)
    "I3": (42, 46, 56, 255),    # Cold iron shadow (#2a2e38)

    # Dynamic OSL on Iron (lit by golden lantern)
    "O1": (224, 180, 80, 255),  # Iron highlight lit by gold light (#e0b450)
    "O2": (138, 100, 40, 255),  # Iron midtone lit by warm light (#8a6428)

    # Oil Lantern & Golden Flame (OSL light source)
    "L1": (255, 252, 160, 255), # Blinding white-gold flame core (#ffea90)
    "L2": (252, 168, 32, 255),  # Rich golden-amber lantern glow (#fca820)
    "L3": (208, 90, 16, 255),   # Deep orange flame / heated bronze (#d05a10)
    "G1": (180, 220, 230, 255), # Lantern glass specular highlight (#b4dce6)
}

def draw_stone_floor(grid):
    # Stone Floor Slabs at y=43..45
    # y=43: top surface of stone slabs with highlight edges and cracks
    for x in range(3, 45):
        grid[43][x] = "#"
        
    for x in range(3, 45):
        grid[44][x] = "F2"
        grid[45][x] = "F3"
        
    # Stone slab vertical mortar grooves at x=15, 29
    grid[44][15] = "F3"
    grid[45][15] = "#"
    grid[44][29] = "F3"
    grid[45][29] = "#"
    
    # Stone slab highlights
    for x in (4, 5, 6, 16, 17, 18, 30, 31, 32):
        grid[44][x] = "F1"
        
    # Chisel notches
    grid[44][9] = "F3"
    grid[44][22] = "F3"
    grid[44][38] = "F3"
    
    # Bottom border
    for x in range(3, 45):
        grid[46][x] = "#"

def draw_iron_stand_base_and_arm(grid):
    # Fixed Iron Stand Base (y=40..42, x=20..28)
    # y=42: bolted flange base
    grid[42][19] = "#"
    grid[42][20] = "I1"
    grid[42][21] = "I2"
    for x in range(22, 27):
        grid[42][x] = "I2"
    grid[42][27] = "I3"
    grid[42][28] = "#"

    # y=41: base stepped moulding
    grid[41][20] = "#"
    grid[41][21] = "I1"
    for x in range(22, 26):
        grid[41][x] = "I2"
    grid[41][26] = "I3"
    grid[41][27] = "#"

    # y=40: collar
    grid[40][21] = "#"
    grid[40][22] = "I1"
    grid[40][23] = "I2"
    grid[40][24] = "I2"
    grid[40][25] = "I3"
    grid[40][26] = "#"

    # Top Arm & Pivot Hook (y=6..11)
    # The iron pole reaches y=9.
    # From y=9, an arched decorative gallows bracket curves out:
    # Top arch: y=6..8
    grid[6][23] = "#"
    grid[6][24] = "#"
    grid[6][25] = "#"
    
    grid[7][21] = "#"
    grid[7][22] = "I1"
    grid[7][23] = "I2"
    grid[7][24] = "I2"
    grid[7][25] = "I3"
    grid[7][26] = "#"
    
    grid[8][20] = "#"
    grid[8][21] = "I1"
    grid[8][27] = "#"
    
    # Support strut brace
    grid[9][21] = "#"
    grid[9][22] = "I1"
    grid[9][26] = "#"
    
    # Top finial on pole
    grid[5][24] = "#"

    # Pivot Hook at (X=24, Y=10): FIXED PIVOT POINT across all frames!
    grid[10][23] = "#"
    grid[10][24] = "I1" # Hook link eyelet
    grid[10][25] = "#"

def apply_dynamic_osl_column(grid, frame_idx):
    # Column runs from y=11 to y=39
    # Width: x=22 (outline/left), x=23 (left face), x=24 (center face), x=25 (right face), x=26 (outline/right)
    # Frame 1: Lamp on Left (X=19) -> Left face lit by gold OSL (O1, L2), Right face is cold iron shadow (I3)
    # Frame 2: Lamp at Center (X=24) -> Symmetrical direct warm OSL
    # Frame 3: Lamp on Right (X=29) -> Right face lit by gold OSL (O1, L2), Left face is cold iron shadow (I3)
    # Frame 4: Lamp at Center (X=24) -> Symmetrical direct warm OSL
    
    for y in range(11, 40):
        grid[y][22] = "#"
        grid[y][26] = "#"
        
        if frame_idx == 0:
            # Frame 1: Lamp on Left (x=19, y=24)
            # Distance in y to lantern
            dist_y = abs(y - 24)
            if dist_y <= 6:
                grid[y][23] = "O1" # Bright gold OSL
                grid[y][24] = "O2" # Warm amber OSL
                grid[y][25] = "I3" # Shadow
            elif dist_y <= 12:
                grid[y][23] = "O2"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
                
        elif frame_idx == 2:
            # Frame 3: Lamp on Right (x=29, y=24)
            dist_y = abs(y - 24)
            if dist_y <= 6:
                grid[y][23] = "I3" # Shadow
                grid[y][24] = "O2" # Warm amber OSL
                grid[y][25] = "O1" # Bright gold OSL
            elif dist_y <= 12:
                grid[y][23] = "I3"
                grid[y][24] = "I2"
                grid[y][25] = "O2"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"
                
        else:
            # Frame 2 & 4: Lamp in Center (x=24, y=25)
            dist_y = abs(y - 25)
            if dist_y <= 5:
                # Behind the lantern
                grid[y][23] = "O1"
                grid[y][24] = "O1"
                grid[y][25] = "O1"
            elif dist_y <= 11:
                grid[y][23] = "O2"
                grid[y][24] = "O1"
                grid[y][25] = "O2"
            else:
                grid[y][23] = "I1"
                grid[y][24] = "I2"
                grid[y][25] = "I3"

def apply_opposing_cast_shadow(grid, frame_idx):
    # Requirement 2: Bóng đổ nghịch chiều trên sàn (Opposing Cast Shadow)
    # Frame 1: Đèn lệch TRÁI -> Bóng đổ của cột trụ đứng BẮT BUỘC ngả dài xiên sang bên PHẢI (x=24 to x=38)
    # Frame 2 & 4: Đèn CHÍNH GIỮA -> Bóng đổ của cột trụ thu ngắn lại ngay chân đế (x=21 to x=27)
    # Frame 3: Đèn lệch PHẢI -> Bóng đổ của cột trụ BẮT BUỘC ngả dài xiên sang bên TRÁI (x=24 to x=10)
    
    if frame_idx == 0:
        # Frame 1: Cast shadow to RIGHT
        for x in range(23, 39):
            grid[44][x] = "S"
        for x in range(24, 38):
            grid[45][x] = "S"
        for x in range(26, 36):
            grid[46][x] = "S"
            
    elif frame_idx == 2:
        # Frame 3: Cast shadow to LEFT
        for x in range(9, 26):
            grid[44][x] = "S"
        for x in range(10, 25):
            grid[45][x] = "S"
        for x in range(12, 23):
            grid[46][x] = "S"
            
    else:
        # Frame 2 & 4: Compact centered shadow at base
        for x in range(20, 28):
            grid[44][x] = "S"
        for x in range(19, 29):
            grid[45][x] = "S"
        for x in range(21, 27):
            grid[46][x] = "S"

# Now design the swinging lantern for each frame
def draw_lantern_frame_1(grid):
    # Frame 1: Swung Left (-25 deg)
    # Pivot Hook at (24, 10)
    # Chain links:
    # (24, 10) -> (23, 12) -> (22, 14) -> (21, 16) -> (20, 18)
    chain = [(23, 11), (23, 12), (22, 13), (22, 14), (21, 15), (21, 16), (20, 17), (20, 18)]
    for cx, cy in chain:
        grid[cy][cx] = "I1" if cx % 2 == 0 else "I2"
        grid[cy][cx - 1] = "#"
        grid[cy][cx + 1] = "#"
        
    # Lantern Cap / Roof (slanted CCW): center at (19, 19..20)
    cap = [
        (19, 19, ["#", "I1", "#"]),
        (18, 20, ["#", "I1", "I2", "I3", "#"]),
        (17, 21, ["#", "I1", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in cap:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Glass chamber with burning golden oil flame: y = 22..25, x = 16..22
    glass_body = [
        (17, 22, ["#", "G1", "L2", "L1", "G1", "#"]),
        (16, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (16, 24, ["#", "G1", "L3", "L2", "L1", "G1", "#"]), # Flame core at x=19, y=24
        (17, 25, ["#", "L3", "L3", "L2", "L3", "#"]),
    ]
    for start_x, y, row in glass_body:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    # Lantern Brass Base & Vent: y = 26..27
    base = [
        (17, 26, ["#", "I1", "I2", "I2", "I3", "#"]),
        (18, 27, ["#", "I2", "I3", "#"]),
    ]
    for start_x, y, row in base:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Floating ember particle drifting up-left (Rule 4.6)
    grid[17][15] = "L2"
    grid[15][13] = "L1"

def draw_lantern_frame_2(grid):
    # Frame 2: Center (0 deg, swinging right)
    # Pivot Hook at (24, 10)
    # Vertical Chain:
    chain = [(24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18), (24, 19)]
    for cx, cy in chain:
        grid[cy][cx] = "I1" if cy % 2 == 0 else "I2"
        grid[cy][cx - 1] = "#"
        grid[cy][cx + 1] = "#"
        
    # Lantern Cap: center at (24, 20..21)
    cap = [
        (23, 20, ["#", "I1", "I2", "#"]),
        (22, 21, ["#", "I1", "I2", "I2", "I3", "#"]),
        (21, 22, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in cap:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Glass Chamber & Flame: y = 23..26, x = 21..27
    glass_body = [
        (21, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (20, 24, ["#", "G1", "L2", "L1", "L1", "L2", "G1", "#"]),
        (20, 25, ["#", "G1", "L3", "L2", "L1", "L2", "G1", "#"]), # Flame core at x=24, y=25
        (21, 26, ["#", "L3", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_body:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    # Lantern Base: y = 27..28
    base = [
        (21, 27, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
        (22, 28, ["#", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in base:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Floating ember particle drifting up-left due to rightward motion
    grid[19][22] = "L2"
    grid[17][20] = "L1"

def draw_lantern_frame_3(grid):
    # Frame 3: Swung Right (+25 deg)
    # Pivot Hook at (24, 10)
    # Chain links:
    # (24, 10) -> (25, 12) -> (26, 14) -> (27, 16) -> (28, 18)
    chain = [(25, 11), (25, 12), (26, 13), (26, 14), (27, 15), (27, 16), (28, 17), (28, 18)]
    for cx, cy in chain:
        grid[cy][cx] = "I1" if cx % 2 == 0 else "I2"
        grid[cy][cx - 1] = "#"
        grid[cy][cx + 1] = "#"
        
    # Lantern Cap / Roof (slanted CW): center at (29, 19..20)
    cap = [
        (28, 19, ["#", "I1", "#"]),
        (27, 20, ["#", "I1", "I2", "I3", "#"]),
        (26, 21, ["#", "I1", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in cap:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Glass chamber with burning golden oil flame: y = 22..25, x = 26..32
    glass_body = [
        (26, 22, ["#", "G1", "L1", "L2", "G1", "#"]),
        (25, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (25, 24, ["#", "G1", "L1", "L2", "L3", "G1", "#"]), # Flame core at x=29, y=24
        (26, 25, ["#", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_body:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    # Lantern Brass Base & Vent: y = 26..27
    base = [
        (26, 26, ["#", "I1", "I2", "I2", "I3", "#"]),
        (27, 27, ["#", "I2", "I3", "#"]),
    ]
    for start_x, y, row in base:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Floating ember particle drifting up-right (Rule 4.6)
    grid[17][33] = "L2"
    grid[15][35] = "L1"

def draw_lantern_frame_4(grid):
    # Frame 4: Center (0 deg, swinging left)
    # Similar to Frame 2, but flame trails right and embers trail right
    chain = [(24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (24, 16), (24, 17), (24, 18), (24, 19)]
    for cx, cy in chain:
        grid[cy][cx] = "I1" if cy % 2 == 0 else "I2"
        grid[cy][cx - 1] = "#"
        grid[cy][cx + 1] = "#"
        
    cap = [
        (23, 20, ["#", "I1", "I2", "#"]),
        (22, 21, ["#", "I1", "I2", "I2", "I3", "#"]),
        (21, 22, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in cap:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    glass_body = [
        (21, 23, ["#", "G1", "L2", "L1", "L2", "G1", "#"]),
        (20, 24, ["#", "G1", "L2", "L2", "L1", "L1", "G1", "#"]), # Flame leans slightly right
        (20, 25, ["#", "G1", "L3", "L2", "L2", "L1", "G1", "#"]),
        (21, 26, ["#", "L3", "L3", "L2", "L3", "L3", "#"]),
    ]
    for start_x, y, row in glass_body:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok

    base = [
        (21, 27, ["#", "I1", "I2", "I2", "I2", "I3", "#"]),
        (22, 28, ["#", "I2", "I2", "I3", "#"]),
    ]
    for start_x, y, row in base:
        for idx, tok in enumerate(row):
            grid[y][start_x + idx] = tok
            
    # Floating ember particle drifting up-right due to leftward motion
    grid[19][26] = "L2"
    grid[17][28] = "L1"

def build_lantern_frame(frame_idx):
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Floor & Opposing Cast Shadow
    apply_opposing_cast_shadow(grid, frame_idx)
    draw_stone_floor(grid)
    
    # 2. Iron Stand Base & Top Arm
    draw_iron_stand_base_and_arm(grid)
    
    # 3. Dynamic OSL Column
    apply_dynamic_osl_column(grid, frame_idx)
    
    # 4. Swinging Lantern
    if frame_idx == 0:
        draw_lantern_frame_1(grid)
    elif frame_idx == 1:
        draw_lantern_frame_2(grid)
    elif frame_idx == 2:
        draw_lantern_frame_3(grid)
    else:
        draw_lantern_frame_4(grid)
        
    return grid

test_frames = [build_lantern_frame(i) for i in range(4)]

# Check naked pixels
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

for i, fr in enumerate(test_frames):
    n = check_outline_completeness(fr)
    print(f"Frame {i+1} naked pixels: {len(n)}")

# Render PNGs and GIF
gif_frames = []
for idx, fr in enumerate(test_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 6, H * 6), Image.NEAREST).save(f"python/lantern_f{idx+1}.png")
    gif_frames.append(img.resize((W * 6, H * 6), Image.NEAREST))

gif_frames[0].save(
    "python/lantern_anim.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=166, # 6 FPS = 166.6ms
    loop=0
)

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/lantern_sheet.png")

print("Saved lantern_sheet.png and lantern_anim.gif")
