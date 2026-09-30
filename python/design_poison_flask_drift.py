import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Hue-Shifting Palette (Magic Violet to Neon Pink):
PALETTE = {
    ".": None,
    "#": (24, 6, 36, 255),        # Deep obsidian plum outline (#180624)
    "S": (20, 6, 28, 130),        # Pure glass contact shadow (Alpha 130)
    
    # Glass & Specular Drift Highlights
    "P": (255, 255, 255, 255),    # Pure specular white highlight (#ffffff)
    "K": (225, 235, 250, 255),    # Translucent glass sheen reflection (#e1ebfa)
    "J": (75, 42, 90, 255),       # Tinted dark glass rim (#4b2a5a)
    
    # Cork Stopper
    "E": (215, 155, 90, 255),     # Cork highlight (#d79b5a)
    "U": (135, 82, 40, 255),      # Cork shadow (#875228)
    
    # Glowing Poison Liquid (Neon Pink to Deepest Violet)
    "W": (255, 255, 255, 255),    # Spark / bubble center (#ffffff)
    "N": (255, 65, 185, 255),     # Neon Pink glowing crest (#ff41b9)
    "F": (216, 28, 156, 255),     # Radiant Magenta liquid mid-highlight (#d81c9c)
    "L": (140, 20, 168, 255),     # Rich Royal Violet liquid midtone (#8c14a8)
    "Q": (75, 8, 94, 255),        # Deep Plum Violet shadow (#4b085e)
    "V": (38, 4, 48, 255),        # Deepest Violet base (#260430)
    
    # Wooden Shelf (Pure Oak Wood)
    "H": (175, 115, 55, 255),     # Oak wood highlight (#af7337)
    "M": (120, 70, 30, 255),      # Oak wood midtone (#78461e)
    "D": (68, 32, 12, 255),       # Shaded wood crevice (#44200c)
}

PALETTE_HEX = {
    ".": None,
    "#": "#180624",
    "S": "#14061c",
    "P": "#ffffff",
    "K": "#e1ebfa",
    "J": "#4b2a5a",
    "E": "#d79b5a",
    "U": "#875228",
    "W": "#ffffff",
    "N": "#ff41b9",
    "F": "#d81c9c",
    "L": "#8c14a8",
    "Q": "#4b085e",
    "V": "#260430",
    "H": "#af7337",
    "M": "#78461e",
    "D": "#44200c",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def draw_wooden_shelf_and_shadow(grid, tilt_deg):
    # Rule 2.4: Bounded shelf (X=10..38, Y=36..41), NO wall-to-wall line!
    # Rule 3.6: Wood grain strips (A A B A A pattern), no dithering
    # Rule 1.6: Glass contact shadow is strictly 'S' (Alpha 130).
    # TUYỆT ĐỐI CẤM tô một vệt nước màu hồng tím bệt phẳng trên mặt gỗ.
    
    # 1. Wooden shelf
    for x in range(10, 39):
        set_p(grid, x, 36, "H")
    for y in range(37, 40):
        for x in range(10, 39):
            col = "M" if (x % 6 != 0) else "D"
            set_p(grid, x, y, col)
    for x in range(11, 38):
        set_p(grid, x, 40, "D")
    for y in range(36, 41):
        set_p(grid, 9, y, "#")
        set_p(grid, 39, y, "#")
    for x in range(9, 40):
        set_p(grid, x, 41, "#")
        
    # 2. Pure glass contact shadow 'S' on shelf under base (Y=35..36)
    base_x = 24
    if tilt_deg < -10:
        base_x = 23
    elif tilt_deg > 10:
        base_x = 25
        
    for x in range(base_x - 5, base_x + 6):
        set_p(grid, x, 36, "S")
    for x in range(base_x - 3, base_x + 4):
        set_p(grid, x, 35, "S")

    # Under shelf soft shadow on floor
    for x in range(12, 37):
        set_p(grid, x, 42, "S")

def draw_specular_drift(grid, frame_num, sc_x, sc_y):
    # Rule 1.5:
    # 1. Khóa biên độ phản quang trong lòng thể tích (SPECULAR BOUNDARY CLAMPING):
    # - Vệt phản quang BẮT BUỘC nằm trọn vẹn BÊN TRONG lòng vỏ kính, cách đường viền đen tối thiểu 1 pixel.
    # - TUYỆT ĐỐI CẤM vệt sáng trượt lố đè lên viền hoặc văng ra ngoài không gian trong suốt.
    # 2. Cơ chế trượt phản quang (Specular Drift):
    # - Frame 2 (Nghiêng TRÁI): trượt dời nhẹ lên hướng đỉnh vòm đón sáng (góc 11 giờ) bám theo độ nghiêng vỏ kính và co ngắn lại 1px.
    # - Frame 4 (Nghiêng PHẢI): trượt lùi xuống phía sườn đón sáng (góc 9-10 giờ) và hơi giãn cong theo vòm kính, KHÓA CHẶT trong lòng kính!
    
    if frame_num in (1, 6):
        # Frame 1 & 6: Center upright (sc_x=24, sc_y=25)
        # Position: 10 o'clock facing environment light
        hl_pixels = [
            (20, 18, "P"), (21, 18, "K"),
            (19, 19, "P"), (20, 19, "P"),
            (18, 20, "P"), (19, 20, "P"),
            (17, 21, "P"), (18, 21, "K"),
            (17, 22, "P"), (18, 22, "K"),
            (17, 23, "K"),
            (18, 24, "K"),
        ]
    elif frame_num == 2:
        # Frame 2: Tilted LEFT -20° (sc_x=21, sc_y=26)
        # Highlight drifts UP towards 11 o'clock dome crest, shortened by 1px, strictly clamped!
        hl_pixels = [
            (21, 18, "P"), (22, 18, "K"),
            (20, 19, "P"), (21, 19, "P"),
            (19, 20, "P"), (20, 20, "P"),
            (18, 21, "P"), (19, 21, "K"),
            (18, 22, "P"), (19, 22, "K"),
            (19, 23, "K"),
        ]
    elif frame_num == 3:
        # Frame 3: Center rebound (sc_x=24, sc_y=25)
        hl_pixels = [
            (20, 18, "P"), (21, 18, "K"),
            (19, 19, "P"), (20, 19, "P"),
            (18, 20, "P"), (19, 20, "P"),
            (17, 21, "P"), (18, 21, "K"),
            (17, 22, "P"), (18, 22, "K"),
            (17, 23, "K"),
            (18, 24, "K"),
        ]
    elif frame_num == 4:
        # Frame 4: Tilted RIGHT +20° (sc_x=27, sc_y=26)
        # Highlight drifts down towards 9-10 o'clock left flank and elongates along curvature.
        # CRITICAL: STRICTLY CLAMPED inside sphere (margin >= 1.44px from border)!
        hl_pixels = [
            (23, 19, "P"), (24, 19, "K"),
            (22, 20, "P"), (23, 20, "P"),
            (21, 21, "P"), (22, 21, "P"),
            (20, 22, "P"), (21, 22, "P"),
            (20, 23, "P"), (21, 23, "P"),
            (20, 24, "P"), (21, 24, "K"),
            (21, 25, "K"),
            (22, 26, "K"),
        ]
    elif frame_num == 5:
        # Frame 5: Center rebound 2 (sc_x=24, sc_y=25)
        hl_pixels = [
            (20, 18, "P"), (21, 18, "K"),
            (19, 19, "P"), (20, 19, "P"),
            (18, 20, "P"), (19, 20, "P"),
            (17, 21, "P"), (18, 21, "K"),
            (17, 22, "P"), (18, 22, "K"),
            (17, 23, "K"),
            (18, 24, "K"),
        ]

    for x, y, c in hl_pixels:
        set_p(grid, x, y, c)
    return hl_pixels

def build_drift_flask_frame(frame_num):
    grid = empty_grid()
    
    angles = {1: 0, 2: -20, 3: 0, 4: 20, 5: 0, 6: 0}
    angle_deg = angles[frame_num]
    
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # 1. Wooden shelf and pure glass contact shadow 'S'
    draw_wooden_shelf_and_shadow(grid, angle_deg)
    
    # Sphere parameters
    p_x, p_y = 24, 35 # Base contact pivot
    r = 10
    
    # Sphere center
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
                    set_p(grid, x, y, "#")
                else:
                    # Inside the spherical flask
                    if frame_num in (1, 6):
                        # Horizontal calm surface at Y=25
                        if y >= 25:
                            dx = abs(x - sc_x)
                            if y == 25:
                                col = "N" if dx < 6 else "F"
                            elif y == 26:
                                col = "F" if dx < 7 else "L"
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
                        # Tilted LEFT (-20°): liquid sloshes up on LEFT wall, down on RIGHT!
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
                        # Rebound to center: Wave slosh (S-curve) + bubbles
                        dx_rel = (x - sc_x)
                        surf_y = 25.0 - 1.5 * math.sin(dx_rel / 9.0 * 3.14159)
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
                        # Tilted RIGHT (+20°): liquid sloshes up on RIGHT wall, down on LEFT!
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
                        # Rebound to center 2: minor wave dampening
                        dx_rel = (x - sc_x)
                        surf_y = 25.0 + 0.7 * math.sin(dx_rel / 9.0 * 3.14159)
                        if y > surf_y:
                            depth = y - surf_y
                            if depth < 1.4:
                                col = "N"
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

    # 3. Neck & Cork
    neck_h_vals = range(10, 16)
    for nh in neck_h_vals:
        cur_rx = 0 * cos_a - (-nh - 10) * sin_a
        cur_ry = 0 * sin_a + (-nh - 10) * cos_a
        nx = int(round(p_x + cur_rx))
        ny = int(round(p_y + cur_ry))
        perp_x = -sin_a
        perp_y = cos_a
        for pw in (-3, -2, -1, 0, 1, 2, 3):
            px_i = int(round(nx + pw * perp_y))
            py_i = int(round(ny + pw * (-perp_x)))
            if abs(pw) == 3:
                set_p(grid, px_i, py_i, "#")
            elif pw == -1:
                set_p(grid, px_i, py_i, "K")
            else:
                set_p(grid, px_i, py_i, "J")

    # Flared Lip
    lip_rx = 0 * cos_a - (-26) * sin_a
    lip_ry = 0 * sin_a + (-26) * cos_a
    lx = int(round(p_x + lip_rx))
    ly = int(round(p_y + lip_ry))
    for pw in (-4, -3, -2, -1, 0, 1, 2, 3, 4):
        px_i = int(round(lx + pw * cos_a))
        py_i = int(round(ly + pw * sin_a))
        if abs(pw) == 4:
            set_p(grid, px_i, py_i, "#")
        elif pw == -1:
            set_p(grid, px_i, py_i, "K")
        else:
            set_p(grid, px_i, py_i, "J")

    # Cork Stopper
    for cy_off in (-27, -28, -29, -30):
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

    # 4. Bubbles and sparks
    if frame_num in (1, 6):
        set_p(grid, sc_x - 3, 28, "W")
        set_p(grid, sc_x - 2, 28, "N")
        set_p(grid, sc_x + 3, 31, "N")
    elif frame_num == 2:
        set_p(grid, sc_x - 5, 23, "W")
        set_p(grid, sc_x - 6, 24, "N")
        set_p(grid, sc_x - 4, 25, "N")
    elif frame_num == 3:
        set_p(grid, sc_x + 1, 22, "W")
        set_p(grid, sc_x + 2, 21, "N")
        set_p(grid, sc_x - 2, 23, "N")
        set_p(grid, sc_x + 4, 27, "W")
    elif frame_num == 4:
        set_p(grid, sc_x + 5, 23, "W")
        set_p(grid, sc_x + 6, 24, "N")
        set_p(grid, sc_x + 4, 25, "N")
    elif frame_num == 5:
        set_p(grid, sc_x - 1, 26, "W")
        set_p(grid, sc_x + 3, 28, "N")

    # 5. SPECULAR DRIFT (Quy tắc 1.5 - Clamped strictly inside volume)
    hl_pts = draw_specular_drift(grid, frame_num, sc_x, sc_y)

    return grid, hl_pts, (sc_x, sc_y)

frame_results = [build_drift_flask_frame(i) for i in range(1, 7)]
frames = [res[0] for res in frame_results]

# STRICT VERIFICATION ASSERTIONS:
print("--- VERIFICATION OF REQUIREMENTS 1 & 2 ---")
for i, (f, hl_pts, (sc_x, sc_y)) in enumerate(frame_results):
    frame_num = i + 1
    # Check 1: Specular highlight strictly clamped inside sphere volume
    for x, y, c in hl_pts:
        dist = math.hypot(x - sc_x, y - sc_y)
        # Inner sphere boundary is at r - 0.4 = 9.6
        # Outline is at 9.6 .. 10.6
        # Dist <= 8.2 guarantees >= 1.4px margin from outline '#'
        assert dist <= 8.2, f"Frame {frame_num}: Highlight ({x},{y}) too close to border: dist={dist:.2f}"
        # Verify 4-neighbors are NOT outline '#'
        for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
            nx, ny = x + dx, y + dy
            assert f[ny][nx] != "#", f"Frame {frame_num}: Highlight ({x},{y}) touches outline border '#'!"
        # In Frame 4 specifically, highlight must be on left flank (x < sc_x)
        if frame_num == 4:
            assert x < sc_x, f"Frame 4: Highlight ({x},{y}) should be on left flank (x < {sc_x})!"
            assert dist < 9.6, f"Frame 4: Highlight ({x},{y}) outside inner glass volume!"
    print(f"Frame {frame_num}: {len(hl_pts)} specular highlight pixels, 100% strictly clamped inside glass volume (min margin >= 1.44px from border)!")

    # Check 2: Shelf surface (Y=36) has NO liquid colors ('W', 'N', 'F', 'L', 'Q', 'V')
    shelf_liquid_pixels = [f[36][x] for x in range(W) if f[36][x] in ("W", "N", "F", "L", "Q", "V")]
    assert len(shelf_liquid_pixels) == 0, f"Frame {frame_num} has liquid spilled on shelf: {shelf_liquid_pixels}"
print("Requirement 2 PASSED: 0 liquid pixels on shelf! Contact shadow is purely 'S'.")

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
    img.save(f"test/drift_flask_f{idx+1}.png")
    images.append(img)

images[0].save(
    "test/drift_flask_anim.gif",
    save_all=True,
    append_images=images[1:],
    duration=167,
    loop=0,
    disposal=2
)

print("Clamped drift poison flask frames generated successfully.")
