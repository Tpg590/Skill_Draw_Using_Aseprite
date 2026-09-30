import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette (Neon Pink-Violet Poison Flask):
PALETTE = {
    ".": None,
    "#": (26, 4, 38, 255),       # Deep plum obsidian outline (#1a0426)
    "S": (20, 6, 28, 130),       # Soft ground shadow (Alpha 130)
    
    # Glass & Highlights
    "P": (255, 255, 255, 255),   # Specular pure white highlight (#ffffff)
    "K": (220, 230, 245, 255),   # Translucent glass reflection sheen (#dce6f5)
    "J": (68, 40, 80, 255),      # Glass rim / subtle reflection (#442850)
    
    # Cork Stopper
    "E": (215, 155, 90, 255),    # Cork highlight (#d79b5a)
    "U": (135, 82, 40, 255),     # Cork shadow (#875228)
    
    # Poison Liquid (Hue-shifting Neon Pink to Deep Violet)
    "W": (255, 255, 255, 255),   # Bubble spark center (#ffffff)
    "N": (255, 65, 185, 255),    # Neon Pink glowing crest (#ff41b9)
    "F": (216, 28, 156, 255),    # Radiant Magenta liquid mid-highlight (#d81c9c)
    "L": (140, 20, 168, 255),    # Rich Royal Violet liquid midtone (#8c14a8)
    "Q": (75, 8, 94, 255),       # Deep Plum Violet shadow (#4b085e)
    "V": (38, 4, 48, 255),       # Deepest Violet base (#260430)
    
    # Wooden Shelf & OSL Light bleed
    "H": (180, 120, 60, 255),    # Oak wood highlight (#b4783c)
    "M": (122, 72, 32, 255),     # Oak wood midtone (#7a4820)
    "D": (72, 36, 14, 255),      # Shaded wood crevice (#48240e)
    "O": (195, 50, 150, 255),    # Direct OSL neon magenta bleed onto wood (#c33296)
    "T": (130, 30, 95, 255),     # OSL soft transition on wood (#821e5f)
}

PALETTE_HEX = {
    ".": None,
    "#": "#1a0426",
    "S": "#14061c",
    "P": "#ffffff",
    "K": "#dce6f5",
    "J": "#442850",
    "E": "#d79b5a",
    "U": "#875228",
    "W": "#ffffff",
    "N": "#ff41b9",
    "F": "#d81c9c",
    "L": "#8c14a8",
    "Q": "#4b085e",
    "V": "#260430",
    "H": "#b4783c",
    "M": "#7a4820",
    "D": "#48240e",
    "O": "#c33296",
    "T": "#821e5f",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_wooden_shelf(grid):
    # Rule 2.4: Bounded pedestal / shelf (X=10..38, Y=36..41), NO wall-to-wall line!
    # Rule 3.6: Wood grain strips (A A B A A pattern), no dithering
    # Rule 1.1 / 1.2: OSL glow directly beneath glowing poison flask
    
    # Top surface of wooden shelf (Y=36)
    for x in range(10, 39):
        # Default oak top highlight
        set_p(grid, x, 36, "H")
    # Front rim / face of shelf (Y=37..39)
    for y in range(37, 40):
        for x in range(10, 39):
            col = "M" if (x % 6 != 0) else "D" # Vertical seam grooves
            set_p(grid, x, y, col)
    # Bottom bevel / shadow (Y=40)
    for x in range(11, 38):
        set_p(grid, x, 40, "D")
        
    # Left and right shelf end caps
    for y in range(36, 41):
        set_p(grid, 9, y, "#")
        set_p(grid, 39, y, "#")
    for x in range(9, 40):
        set_p(grid, x, 41, "#")
        
    # OSL GLOW on wood directly under flask (X=18..30, Y=36..37)
    for x in range(18, 31):
        set_p(grid, x, 36, "O") # Neon magenta OSL bleed
    for x in range(19, 30):
        set_p(grid, x, 37, "T") # Soft violet OSL midtone
    for x in range(16, 18):
        set_p(grid, x, 36, "T")
    for x in range(31, 33):
        set_p(grid, x, 36, "T")
        
    # Contact shadow under shelf (Y=42)
    for x in range(12, 37):
        set_p(grid, x, 42, "S")

def draw_static_glass_highlight(grid):
    # Quy tắc 1.5 & 2.2:
    # Vệt Highlight cong màu trắng ngà mô tả vỏ kính bên ngoài
    # BẮT BUỘC giữ nguyên vị trí ở góc Trên-Trái (10 giờ) trên thân bình qua mọi frame!
    # Không nghiêng ngả xoay theo bình! Vắt qua cả vùng rỗng lẫn vùng có chất lỏng!
    hl_pixels = [
        # (x, y, char)
        (19, 18, "P"), (20, 18, "K"),
        (18, 19, "P"), (19, 19, "P"), (20, 19, "K"),
        (17, 20, "P"), (18, 20, "P"),
        (16, 21, "P"), (17, 21, "P"),
        (16, 22, "P"), (17, 22, "K"),
        (16, 23, "P"), (17, 23, "K"),
        (17, 24, "K"),
        (18, 25, "K"),
    ]
    for x, y, c in hl_pixels:
        set_p(grid, x, y, c)

def build_flask_frame(frame_num):
    grid = empty_grid()
    
    # 1. Wooden shelf with OSL
    draw_wooden_shelf(grid)
    
    # Glass sphere parameters
    # Frame 1: upright (angle = 0)
    # Frame 2: tilted left -20 deg
    # Frame 3: upright shaking / wave
    # Frame 4: tilted right +20 deg
    # Frame 5: slight tilt left -5 deg damping
    # Frame 6: upright settled
    
    cx, cy = 24, 25
    r = 10
    
    if frame_num == 1:
        angle_deg = 0
    elif frame_num == 2:
        angle_deg = -20
    elif frame_num == 3:
        angle_deg = 0
    elif frame_num == 4:
        angle_deg = 20
    elif frame_num == 5:
        angle_deg = -6
    elif frame_num == 6:
        angle_deg = 0
        
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Bottom contact pivot is at (24, 35)
    p_x, p_y = 24, 35
    
    # Neck and Cork offsets
    # Cork center relative to pivot: dx=0, dy=-27
    cork_rx = 0 * cos_a - (-27) * sin_a
    cork_ry = 0 * sin_a + (-27) * cos_a
    cork_cx = int(round(p_x + cork_rx))
    cork_cy = int(round(p_y + cork_ry))
    
    # Sphere center relative to pivot: dx=0, dy=-10
    sc_rx = 0 * cos_a - (-10) * sin_a
    sc_ry = 0 * sin_a + (-10) * cos_a
    sc_x = int(round(p_x + sc_rx))
    sc_y = int(round(p_y + sc_ry))
    
    # 2. Draw Sphere Outer Shell & Liquid
    for y in range(H):
        for x in range(W):
            dist = math.hypot(x - sc_x, y - sc_y)
            if dist <= r + 0.6:
                if dist >= r - 0.4:
                    # Glass outer shell outline
                    set_p(grid, x, y, "#")
                else:
                    # Inside the spherical bulb!
                    # Determine liquid level based on frame kinematics
                    # Quy tắc khắt khe 1: Độ nghiêng mặt thoáng chất lỏng
                    # TUYỆT ĐỐI CẤM song song với đáy bình.
                    # Khi bình nghiêng trái (Frame 2): nước dạt mạnh ép lên thành TRÁI,
                    # mặt thoáng dốc chéo (trái cao, phải thấp).
                    # Khi bình nghiêng phải (Frame 4): nước dạt mạnh ép lên thành PHẢI,
                    # mặt thoáng dốc ngược lại (phải cao, trái thấp).
                    
                    if frame_num == 1:
                        # Level horizontal surface at Y=25 (with 3D ellipse curvature)
                        # Ellipse: ((x-sc_x)/9)^2 + ((y-25)/2.2)^2
                        dx_rel = (x - sc_x)
                        is_liquid = (y >= 25)
                        meniscus_y = 25 - 0.2 * (1 - (dx_rel/9.5)**2) if abs(dx_rel) <= 9.5 else 25
                        if y > 25:
                            is_liquid = True
                        elif y == 25:
                            is_liquid = True
                        else:
                            is_liquid = False
                            
                        if is_liquid:
                            if y == 25:
                                col = "N" if abs(dx_rel) < 6 else "F"
                            elif y == 26:
                                col = "F" if abs(dx_rel) < 7 else "L"
                            elif y <= 29:
                                col = "L"
                            elif y <= 32:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

                    elif frame_num == 2:
                        # Frame 2: Tilted LEFT. Liquid sloshes up on LEFT wall, down on RIGHT!
                        # Liquid surface equation: y - 25 = 0.55 * (x - sc_x)
                        # Left side (x < sc_x): y_surface < 25 (higher, up to y=20)
                        # Right side (x > sc_x): y_surface > 25 (lower, down to y=29)
                        surf_y = 25.0 + 0.52 * (x - sc_x)
                        if y > surf_y:
                            depth = y - surf_y
                            if depth < 1.4:
                                col = "N" if x < sc_x else "F"
                            elif depth < 3.2:
                                col = "F" if x < sc_x else "L"
                            elif depth < 6.5:
                                col = "L"
                            elif depth < 9.0:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

                    elif frame_num == 3:
                        # Frame 3: Lắc giật về giữa! Sóng sánh nảy bọt, mặt nước hình chữ S
                        # Wave: y_surf = 25 - 1.5 * sin((x - sc_x)/8 * pi)
                        dx_rel = (x - sc_x)
                        surf_y = 25.0 - 1.6 * math.sin(dx_rel / 9.0 * 3.14159)
                        if y > surf_y:
                            depth = y - surf_y
                            if depth < 1.4:
                                col = "N" if (x + y) % 2 == 0 else "F"
                            elif depth < 3.0:
                                col = "F"
                            elif depth < 6.0:
                                col = "L"
                            elif depth < 9.0:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

                    elif frame_num == 4:
                        # Frame 4: Tilted RIGHT. Liquid sloshes up on RIGHT wall, down on LEFT!
                        # Left side (x < sc_x): drops down to Y=29
                        # Right side (x > sc_x): rises up to Y=20
                        surf_y = 25.0 - 0.52 * (x - sc_x)
                        if y > surf_y:
                            depth = y - surf_y
                            if depth < 1.4:
                                col = "N" if x > sc_x else "F"
                            elif depth < 3.2:
                                col = "F" if x > sc_x else "L"
                            elif depth < 6.5:
                                col = "L"
                            elif depth < 9.0:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

                    elif frame_num == 5:
                        # Frame 5: Damping oscillation. Gentle tilt left (-6 deg)
                        surf_y = 25.0 + 0.22 * (x - sc_x)
                        if y > surf_y:
                            depth = y - surf_y
                            if depth < 1.3:
                                col = "N"
                            elif depth < 2.8:
                                col = "F"
                            elif depth < 6.0:
                                col = "L"
                            elif depth < 8.5:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

                    elif frame_num == 6:
                        # Frame 6: Settling back to calm horizontal surface
                        if y >= 25:
                            dx_rel = abs(x - sc_x)
                            if y == 25:
                                col = "N" if dx_rel < 6 else "F"
                            elif y == 26:
                                col = "F" if dx_rel < 7 else "L"
                            elif y <= 29:
                                col = "L"
                            elif y <= 32:
                                col = "Q"
                            else:
                                col = "V"
                            set_p(grid, x, y, col)
                        else:
                            set_p(grid, x, y, ".")

    # 3. Draw Neck & Flared Lip & Cork
    # Calculate neck segment along tilted spine
    neck_h_vals = range(10, 16)
    for nh in neck_h_vals:
        # Distance from pivot: nh from bottom
        dist_from_pivot = -(35 - (25 - 10 + (16 - nh))) # roughly -20..-15
        cur_rx = 0 * cos_a - (-nh - 10) * sin_a
        cur_ry = 0 * sin_a + (-nh - 10) * cos_a
        nx = int(round(p_x + cur_rx))
        ny = int(round(p_y + cur_ry))
        # Neck width = 5px (-2..+2 perpendicular to axis)
        perp_x = -sin_a
        perp_y = cos_a
        for pw in (-3, -2, -1, 0, 1, 2, 3):
            px_i = int(round(nx + pw * perp_y))
            py_i = int(round(ny + pw * (-perp_x)))
            if abs(pw) == 3:
                set_p(grid, px_i, py_i, "#")
            else:
                set_p(grid, px_i, py_i, "K" if pw < 0 else "J")

    # Flared Lip at neck top
    lip_rx = 0 * cos_a - (-26) * sin_a
    lip_ry = 0 * sin_a + (-26) * cos_a
    lx = int(round(p_x + lip_rx))
    ly = int(round(p_y + lip_ry))
    for pw in (-4, -3, -2, -1, 0, 1, 2, 3, 4):
        px_i = int(round(lx + pw * cos_a))
        py_i = int(round(ly + pw * sin_a))
        if abs(pw) == 4:
            set_p(grid, px_i, py_i, "#")
        else:
            set_p(grid, px_i, py_i, "K" if pw <= 0 else "J")

    # Cork Stopper
    cork_y_offsets = (-27, -28, -29, -30)
    for cy_off in cork_y_offsets:
        crx = 0 * cos_a - cy_off * sin_a
        cry = 0 * sin_a + cy_off * cos_a
        c_pt_x = int(round(p_x + crx))
        c_pt_y = int(round(p_y + cry))
        for pw in (-3, -2, -1, 0, 1, 2, 3):
            cx_i = int(round(c_pt_x + pw * cos_a))
            cy_i = int(round(c_pt_y + pw * sin_a))
            if abs(pw) == 3 or cy_off == -30:
                set_p(grid, cx_i, cy_i, "#")
            else:
                set_p(grid, cx_i, cy_i, "E" if pw < 1 else "U")

    # 4. Bubbles and Magic Particles (Quy tắc 3.5: Embers/particles)
    if frame_num == 1:
        set_p(grid, sc_x - 3, 28, "W")
        set_p(grid, sc_x - 2, 28, "N")
        set_p(grid, sc_x + 3, 31, "N")
    elif frame_num == 2:
        # Bubbles pressed against left wall
        set_p(grid, sc_x - 5, 23, "W")
        set_p(grid, sc_x - 6, 24, "N")
        set_p(grid, sc_x - 4, 25, "N")
    elif frame_num == 3:
        # Splash droplets leaping out of liquid!
        set_p(grid, sc_x + 1, 22, "W") # Leaping drop
        set_p(grid, sc_x + 2, 21, "N")
        set_p(grid, sc_x - 2, 23, "N")
        set_p(grid, sc_x + 4, 27, "W")
    elif frame_num == 4:
        # Bubbles pressed against right wall
        set_p(grid, sc_x + 5, 23, "W")
        set_p(grid, sc_x + 6, 24, "N")
        set_p(grid, sc_x + 4, 25, "N")
    elif frame_num == 5:
        set_p(grid, sc_x - 1, 26, "W")
        set_p(grid, sc_x + 3, 29, "N")
    elif frame_num == 6:
        set_p(grid, sc_x - 2, 28, "W")
        set_p(grid, sc_x + 3, 30, "N")

    # 5. STATIC GLASS HIGHLIGHT (Quy tắc 1.5 & 2.2)
    # BẮT BUỘC giữ nguyên vị trí ở góc Trên-Trái (10 giờ) trên thân bình qua mọi frame!
    draw_static_glass_highlight(grid)

    return grid

frames = [build_flask_frame(i) for i in range(1, 7)]

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
    img.save(f"test/flask_f{idx+1}.png")
    images.append(img)

# Save test GIF at 6 FPS (duration = 1000 / 6 = 167ms)
images[0].save(
    "test/flask_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=167,
    loop=0,
    disposal=2
)

print("Poison flask test frames generated successfully.")
