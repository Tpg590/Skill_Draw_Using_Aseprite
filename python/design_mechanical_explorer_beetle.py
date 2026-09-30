import os
import math
from PIL import Image

W, H = 48, 48

# Terraria Mech Style Palette
PALETTE = {
    ".": None,
    "S": (16, 20, 26, 130),     # Ground contact shadow (Alpha 130)
    "#": (14, 16, 22, 255),     # Near-black Terraria outline (#0e1016)
    
    # Heavy Steel Armor Plates (Carapace, Upper/Forearm)
    "P": (235, 245, 255, 255), # Specular highlight / Polished rim (#ebf5ff)
    "A": (175, 192, 212, 255), # Light steel plate (#afd0d4)
    "B": (108, 128, 150, 255), # Mid steel plate (#6c8096)
    "C": (60, 74, 92, 255),    # Dark shaded steel (#3c4a5c)
    "D": (32, 40, 52, 255),    # Deep crevice / shadow (#202834)
    
    # Steampunk Brass / Bronze Gears, Elbow Disc, Rivets
    "J": (255, 228, 110, 255), # Brass bright highlight (#ffe46e)
    "G": (210, 155, 30, 255),  # Polished brass midtone (#d29b1e)
    "K": (135, 90, 14, 255),   # Shaded bronze (#875a0e)
    "Z": (68, 40, 8, 255),     # Deep bronze groove / crevice (#442808)
    
    # Glowing Crimson Optical Sensor / Cockpit Eye
    "E": (255, 60, 85, 255),   # Glowing crimson core (#ff3c55)
    "R": (185, 22, 42, 255),   # Crimson shadow / lens rim (#b9162a)
}

PALETTE_HEX = {
    ".": None,
    "S": "#10141a",
    "#": "#0e1016",
    "P": "#ebf5ff",
    "A": "#afd0d4",
    "B": "#6c8096",
    "C": "#3c4a5c",
    "D": "#202834",
    "J": "#ffe46e",
    "G": "#d29b1e",
    "K": "#875a0e",
    "Z": "#442808",
    "E": "#ff3c55",
    "R": "#b9162a",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_hline(grid, x1, x2, y, char):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        set_p(grid, x, y, char)

def draw_central_shadow(grid, body_dy):
    # Rule 2.4: Bounded oval ground shadow, NOT a continuous line
    # Undercarriage central shadow fixed at Y=35..38
    for y in range(35, 39):
        w_half = 7 if y in (36, 37) else 5
        draw_hline(grid, 24 - w_half, 24 + w_half, y, "S")

def draw_limb(grid, hx, hy, kx, ky, fx, fy, is_grounded):
    # 1. Thigh (Hip to Knee)
    steps_thigh = 8
    for s in range(steps_thigh + 1):
        t = s / steps_thigh
        x = int(round(hx + t * (kx - hx)))
        y = int(round(hy + t * (ky - hy)))
        set_p(grid, x, y, "B")
        set_p(grid, x, y - 1, "A")
        set_p(grid, x, y + 1, "C")
        
    # 2. Knee disc (Brass joint)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if abs(dx) + abs(dy) <= 1:
                set_p(grid, kx + dx, ky + dy, "G")
    set_p(grid, kx, ky, "J")
    set_p(grid, kx, ky + 1, "K")
    
    # 3. Shin (Knee to Foot)
    steps_shin = 10
    for s in range(steps_shin + 1):
        t = s / steps_shin
        x = int(round(kx + t * (fx - kx)))
        y = int(round(ky + t * (fy - ky)))
        set_p(grid, x, y, "B")
        if x < 24:
            set_p(grid, x - 1, y, "A")
            set_p(grid, x + 1, y, "C")
        else:
            set_p(grid, x - 1, y, "C")
            set_p(grid, x + 1, y, "A")
            
    # 4. Foot claw tip
    set_p(grid, fx, fy, "P" if fx < 24 else "A")
    set_p(grid, fx, fy - 1, "B")
    
    # 5. Foot ground contact shadow (Quy tắc 4.4 / 4.7):
    # If grounded, draw contact shadow under móng chân. If lifted, NONE!
    if is_grounded:
        set_p(grid, fx, fy + 1, "S")
        set_p(grid, fx - 1, fy + 1, "S")
        set_p(grid, fx + 1, fy + 1, "S")

def draw_legs(grid, frame_num, dy):
    # Pair A: Front-Left (FL) & Back-Right (BR)
    # Pair B: Front-Right (FR) & Back-Left (BL)
    
    # Back-Left (BL):
    if frame_num == 1:
        # Lifted swinging forward
        draw_limb(grid, 17, 26+dy, 13, 21+dy, 12, 23+dy, is_grounded=False)
    elif frame_num == 2:
        # Landing (dy=1)
        draw_limb(grid, 17, 26+dy, 11, 23, 8, 27, is_grounded=True)
    elif frame_num == 3:
        # Grounded firmly
        draw_limb(grid, 17, 26+dy, 11, 22, 8, 26, is_grounded=True)
    elif frame_num == 4:
        # Grounded supporting
        draw_limb(grid, 17, 26+dy, 11, 22, 8, 26, is_grounded=True)

    # Back-Right (BR):
    if frame_num in (1, 2):
        # Grounded firmly
        fy = 27 if frame_num == 2 else 26
        draw_limb(grid, 31, 26+dy, 36, 22+dy, 40, fy, is_grounded=True)
    elif frame_num == 3:
        # Lifted swinging forward
        draw_limb(grid, 31, 26+dy, 35, 20+dy, 36, 22+dy, is_grounded=False)
    elif frame_num == 4:
        # Landing / touching down
        draw_limb(grid, 31, 26+dy, 36, 22+dy, 40, 26, is_grounded=True)

    # Front-Left (FL):
    if frame_num in (1, 2, 4):
        # Grounded firmly
        fy = 35 if frame_num == 2 else 34
        draw_limb(grid, 18, 23+dy, 14, 28+dy, 9, fy, is_grounded=True)
    elif frame_num == 3:
        # Lifted high swinging forward
        draw_limb(grid, 18, 23+dy, 13, 24+dy, 14, 28+dy, is_grounded=False)

    # Front-Right (FR):
    if frame_num == 1:
        # Lifted high swinging forward
        draw_limb(grid, 30, 23+dy, 34, 24+dy, 34, 28+dy, is_grounded=False)
    elif frame_num in (2, 3, 4):
        # Grounded firmly
        fy = 35 if frame_num == 2 else 34
        draw_limb(grid, 30, 23+dy, 35, 28+dy, 37, fy, is_grounded=True)

def draw_carapace(grid, dy):
    # Main beetle body carapace
    rows = [
        (18+dy, 22, 27),
        (19+dy, 20, 28),
        (20+dy, 18, 30),
        (21+dy, 17, 31),
        (22+dy, 16, 32),
        (23+dy, 16, 32),
        (24+dy, 16, 32),
        (25+dy, 16, 32),
        (26+dy, 16, 32),
        (27+dy, 17, 31),
        (28+dy, 17, 31),
        (29+dy, 18, 30),
        (30+dy, 19, 29),
        (31+dy, 20, 28),
        (32+dy, 22, 26),
    ]
    for y, x1, x2 in rows:
        set_p(grid, x1, y, "#")
        set_p(grid, x2, y, "#")
        for x in range(x1 + 1, x2):
            set_p(grid, x, y, "B")

    # Front Visor & Crimson Optical Sensor (Terraria Mech Eye)
    set_p(grid, 21, 19+dy, "#")
    set_p(grid, 22, 19+dy, "E")
    set_p(grid, 23, 19+dy, "E")
    set_p(grid, 24, 19+dy, "#")
    set_p(grid, 21, 20+dy, "R")
    set_p(grid, 22, 20+dy, "E")
    set_p(grid, 23, 20+dy, "R")
    set_p(grid, 24, 20+dy, "R")

    # Steel Highlights & Rivets
    for x in range(18, 22):
        set_p(grid, x, 21+dy, "P")
    for y in range(22+dy, 26+dy):
        set_p(grid, 17, y, "P")
        set_p(grid, 18, y, "A")
    for x in range(18, 24):
        set_p(grid, x, 22+dy, "A")

    # Brass Rivets
    rivets = [(19, 24+dy), (29, 24+dy), (20, 29+dy), (28, 29+dy), (24, 26+dy)]
    for rx, ry in rivets:
        set_p(grid, rx, ry, "J")
        set_p(grid, rx+1, ry, "G")

    # Central armor divider
    for y in range(23+dy, 31+dy):
        set_p(grid, 24, y, "D")
        set_p(grid, 25, y, "#")

    # Dark underside shading
    for y in range(26+dy, 31+dy):
        set_p(grid, 30, y, "C")
        set_p(grid, 31, y, "D")
    for x in range(20, 29):
        set_p(grid, x, 31+dy, "D")
        set_p(grid, x, 30+dy, "C")

    # Rear exhaust nozzles
    for ex in (19, 28):
        set_p(grid, ex, 32+dy, "#")
        set_p(grid, ex+1, 32+dy, "#")
        set_p(grid, ex, 33+dy, "K")
        set_p(grid, ex+1, 33+dy, "G")
        set_p(grid, ex, 34+dy, "#")
        set_p(grid, ex+1, 34+dy, "#")

def draw_mechanical_claw(grid, frame_num, dy):
    # Mounting shoulder socket at (27, 20+dy)
    sx, sy = 27, 20+dy
    set_p(grid, sx, sy, "J")
    set_p(grid, sx+1, sy, "G")
    set_p(grid, sx, sy+1, "K")
    set_p(grid, sx+1, sy+1, "#")
    
    if frame_num == 1:
        # Frame 1: Càng kẹp co gập hình chữ V sát thân.
        # Upper arm: (27, 19) -> (24, 16)
        for (x, y) in [(27, 19), (26, 18), (25, 17), (24, 16)]:
            set_p(grid, x, y, "B")
            set_p(grid, x, y-1, "A")
            set_p(grid, x, y+1, "#")
        # Circular elbow joint at (23, 15)
        for dx in (-1, 0, 1):
            for dy_k in (-1, 0, 1):
                if abs(dx) + abs(dy_k) <= 1:
                    set_p(grid, 23+dx, 15+dy_k, "G")
        set_p(grid, 23, 15, "J")
        set_p(grid, 23, 16, "K")
        set_p(grid, 22, 15, "#")
        
        # Forearm folded tightly back along upper arm (acute V angle ~ 60 deg)
        for (x, y) in [(24, 14), (25, 13), (26, 13)]:
            set_p(grid, x, y, "B")
            set_p(grid, x, y-1, "P")
            set_p(grid, x, y+1, "#")
            
        # Pincer prongs closed tight
        set_p(grid, 27, 12, "P")
        set_p(grid, 28, 12, "A")
        set_p(grid, 27, 13, "A")
        set_p(grid, 28, 13, "B")
        set_p(grid, 29, 12, "#")

    elif frame_num == 2:
        # Frame 2: Càng kẹp bắt đầu duỗi mở khớp (angle ~ 110 deg).
        # Upper arm: (27, 20) -> (25, 16)
        for (x, y) in [(27, 20), (26, 19), (25, 18), (25, 17), (24, 16)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "A")
            set_p(grid, x+1, y, "#")
            
        # Circular elbow joint at (23, 14)
        for dx in (-1, 0, 1):
            for dy_k in (-1, 0, 1):
                if abs(dx) + abs(dy_k) <= 1:
                    set_p(grid, 23+dx, 14+dy_k, "G")
        set_p(grid, 23, 14, "J")
        set_p(grid, 23, 15, "K")
        set_p(grid, 22, 14, "#")
        
        # Forearm extending forward-right
        for (x, y) in [(24, 13), (25, 12), (25, 11), (26, 10)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "P")
            set_p(grid, x+1, y, "#")
            
        # Pincers beginning to part
        set_p(grid, 25, 9, "P")
        set_p(grid, 24, 8, "A")
        set_p(grid, 27, 9, "A")
        set_p(grid, 28, 8, "B")

    elif frame_num == 3:
        # Frame 3: Càng kẹp vươn dài CỰC ĐẠI về phía trước.
        # CRITICAL RULE 4.8:
        # Hai đốt kim loại BẮT BUỘC duy trì góc tù (150-160 độ) với khớp khuỷu tròn và rãnh phân đoạn rõ rệt ở giữa.
        # TUYỆT ĐỐI CẤM làm biến mất khớp khuỷu!
        
        # 1. Upper arm (Đốt bắp tay) from (27, 19) to (25, 14)
        for (x, y) in [(27, 19), (26, 18), (26, 17), (25, 16), (25, 15)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "A")
            set_p(grid, x+1, y, "#")
            
        # Distinct dividing groove between upper arm and elbow
        set_p(grid, 25, 14, "#")
        set_p(grid, 24, 14, "#")
        
        # 2. Circular Elbow Joint (Khớp khuỷu tròn 3x3 with central brass rivet & ring)
        for dx in (-1, 0, 1):
            for dy_k in (-1, 0, 1):
                if abs(dx) + abs(dy_k) <= 1:
                    set_p(grid, 24+dx, 12+dy_k, "G")
        set_p(grid, 24, 12, "J")      # Specular highlight on brass hinge
        set_p(grid, 24, 13, "K")      # Shaded bronze bottom
        set_p(grid, 23, 12, "#")      # Clear dividing groove
        set_p(grid, 25, 12, "Z")      # Central socket depth
        
        # Distinct dividing groove between elbow and forearm
        set_p(grid, 23, 11, "#")
        set_p(grid, 24, 11, "#")
        
        # 3. Forearm (Đốt cẳng tay) extending at 155-degree obtuse angle to (22, 6)
        for (x, y) in [(23, 10), (23, 9), (22, 8), (22, 7)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "P") # Specular light edge
            set_p(grid, x+1, y, "#") # Outline
            
        # Pincer wrist hub at (22, 6)
        set_p(grid, 22, 6, "J")
        set_p(grid, 21, 6, "G")
        set_p(grid, 23, 6, "#")
        
        # 4. TWO PINCER PRONGS SPREAD WIDE OPEN MENACINGLY (Mở rộng đe dọa):
        # Left/Upper Prong: curves outward-left and hooks forward
        set_p(grid, 20, 5, "P")
        set_p(grid, 20, 6, "#")
        set_p(grid, 19, 4, "P")
        set_p(grid, 18, 4, "A")
        set_p(grid, 17, 3, "P")
        set_p(grid, 18, 3, "B")
        set_p(grid, 18, 2, "P") # Sharp hook tip
        set_p(grid, 19, 3, "#") # Inner sharp tooth
        
        # Right/Lower Prong: curves outward-right and hooks forward
        set_p(grid, 23, 5, "A")
        set_p(grid, 24, 5, "#")
        set_p(grid, 25, 4, "B")
        set_p(grid, 26, 4, "A")
        set_p(grid, 27, 3, "B")
        set_p(grid, 26, 3, "P")
        set_p(grid, 26, 2, "A") # Sharp hook tip
        set_p(grid, 25, 3, "#") # Inner sharp tooth

    elif frame_num == 4:
        # Frame 4: Càng kẹp thu dần về lại vị trí chuẩn bị khép vòng lặp.
        # Upper arm: (27, 19) -> (25, 16)
        for (x, y) in [(27, 19), (26, 18), (25, 17), (25, 16)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "A")
            set_p(grid, x+1, y, "#")
            
        # Circular elbow joint at (24, 14)
        for dx in (-1, 0, 1):
            for dy_k in (-1, 0, 1):
                if abs(dx) + abs(dy_k) <= 1:
                    set_p(grid, 24+dx, 14+dy_k, "G")
        set_p(grid, 24, 14, "J")
        set_p(grid, 24, 15, "K")
        set_p(grid, 23, 14, "#")
        
        # Forearm retracting (angle ~ 115 deg)
        for (x, y) in [(25, 13), (25, 12), (26, 11), (26, 10)]:
            set_p(grid, x, y, "B")
            set_p(grid, x-1, y, "P")
            set_p(grid, x+1, y, "#")
            
        # Pincers closing together
        set_p(grid, 26, 9, "P")
        set_p(grid, 25, 8, "A")
        set_p(grid, 27, 9, "A")
        set_p(grid, 28, 8, "B")

def apply_clean_outlines(grid):
    new_grid = [row[:] for row in grid]
    for y in range(H):
        for x in range(W):
            if grid[y][x] not in (".", "S"):
                for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            new_grid[ny][nx] = "#"
    return new_grid

def build_frame(frame_num):
    grid = empty_grid()
    dy = 1 if frame_num == 2 else 0
    
    # 1. Base central ground shadow
    draw_central_shadow(grid, dy)
    
    # 2. Articulated legs with synchronized grounding contact shadows
    draw_legs(grid, frame_num, dy)
    
    # 3. Main Carapace
    draw_carapace(grid, dy)
    
    # 4. Mechanical Claw
    draw_mechanical_claw(grid, frame_num, dy)
    
    # 5. Apply clean outlines
    final_grid = apply_clean_outlines(grid)
    return final_grid

frames = [build_frame(i) for i in range(1, 5)]

os.makedirs("test", exist_ok=True)
images = []
for idx, f in enumerate(frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            c = f[y][x]
            val = PALETTE.get(c)
            if val:
                img.putpixel((x, y), val)
    img.save(f"test/beetle_f{idx+1}.png")
    images.append(img)

images[0].save(
    "test/beetle_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=167,
    loop=0,
    disposal=2
)

print("Synchronized frames generated in test/ successfully.")
