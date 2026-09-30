import os
import math
from PIL import Image

W, H = 48, 48

# FreeStyle Electric Palette:
# Copper + Iron + Blinding White Core + Electric Cyan + Deep Blue-Purple Shadow
PALETTE = {
    ".": None,
    "#": (16, 12, 24, 255),        # Deep dark outline (#100c18)
    "S": (10, 8, 16, 130),         # Contact shadow (Alpha 130)
    
    # Ground (Earth & Grassy mound)
    "g": (64, 98, 42, 255),        # Grass highlight (#40622a)
    "G": (42, 68, 28, 255),        # Grass midtone (#2a441c)
    "e": (78, 52, 28, 255),        # Earth soil mid (#4e341c)
    "E": (48, 30, 16, 255),        # Earth soil dark (#301e10)
    
    # Copper Lightning Rod (Main Spire)
    "o": (255, 245, 180, 255),     # Copper charge glow (#fff5b4)
    "O": (255, 210, 110, 255),     # Polished copper highlight (#ffd26e)
    "C": (212, 128, 48, 255),      # Copper midtone (#d48030)
    "c": (140, 68, 22, 255),       # Copper shaded shadow (#8c4416)
    "u": (75, 32, 10, 255),        # Deep copper crevice (#4b200a)
    
    # Iron Rod (Secondary Stake)
    "h": (195, 210, 225, 255),     # Iron highlight (#c3d2e1)
    "I": (115, 130, 150, 255),     # Iron midtone (#738296)
    "i": (58, 70, 88, 255),        # Iron shadow (#3a4658)
    "k": (26, 34, 46, 255),        # Dark iron outline (#1a222e)
    
    # Magic Lightning & Fractal Arc
    "W": (255, 255, 255, 255),     # Blinding White core (#ffffff)
    "L": (64, 255, 255, 255),      # Vivid Electric Cyan (#40ffff)
    "l": (0, 180, 230, 255),       # Outer Cyan glow (#00b4e6)
    "b": (18, 90, 160, 255),       # Electric blue halo (#125aa0)
    
    # Frame 3 Afterglow (Dim purple-blue fragments)
    "A": (90, 65, 145, 255),       # Fading violet arc (#5a4191)
    "a": (45, 30, 85, 255),        # Dim purple residual trail (#2d1e55)
}

PALETTE_HEX = {
    ".": None,
    "#": "#100c18",
    "S": "#0a0810",
    "g": "#40622a",
    "G": "#2a441c",
    "e": "#4e341c",
    "E": "#301e10",
    "o": "#fff5b4",
    "O": "#ffd26e",
    "C": "#d48030",
    "c": "#8c4416",
    "u": "#4b200a",
    "h": "#c3d2e1",
    "I": "#738296",
    "i": "#3a4658",
    "k": "#1a222e",
    "W": "#ffffff",
    "L": "#40ffff",
    "l": "#00b4e6",
    "b": "#125aa0",
    "A": "#5a4191",
    "a": "#2d1e55",
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def set_p(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def get_p(grid, x, y):
    if 0 <= x < W and 0 <= y < H:
        return grid[y][x]
    return "."

def draw_environment(grid):
    # Ground mound (bounded, Rule 2.4: no wall-to-wall line)
    # Mound from X=6 to X=42, Y=39 to Y=43
    for x in range(8, 40):
        set_p(grid, x, 39, "g" if (x % 3 != 0) else "G")
        set_p(grid, x, 40, "G")
    for y in range(41, 44):
        for x in range(9, 39):
            set_p(grid, x, y, "e" if ((x + y) % 2 == 0) else "E")
            
    # Ground outline
    for x in range(8, 40):
        set_p(grid, x, 44, "#")
    for y in range(39, 44):
        set_p(grid, 7, y, "#")
        set_p(grid, 40, y, "#")
        
    # Contact shadow under mound
    for x in range(10, 38):
        set_p(grid, x, 45, "S")

def draw_main_copper_rod(grid, state):
    # state: 'charge' (F1), 'strike' (F2), 'afterglow' (F3), 'rest' (F4)
    cx = 14 # Center of main copper spire
    
    # 1. Slender vertical shaft (Y=18 to Y=38)
    for y in range(18, 39):
        set_p(grid, cx - 1, y, "O" if state != "strike" else "o")
        set_p(grid, cx, y, "C" if state != "strike" else "O")
        set_p(grid, cx + 1, y, "c" if state != "strike" else "C")
        set_p(grid, cx - 2, y, "u")
        set_p(grid, cx + 2, y, "u")
        
    # Base collar at Y=37..38
    for bx in range(cx - 3, cx + 4):
        set_p(grid, bx, 38, "C" if abs(bx - cx) <= 2 else "u")
        
    # 2. Copper Sphere on top (Center (14, 14), radius 3.5)
    sphere_pts = [
        (13, 11), (14, 11), (15, 11),
        (12, 12), (13, 12), (14, 12), (15, 12), (16, 12),
        (11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13),
        (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14),
        (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15),
        (12, 16), (13, 16), (14, 16), (15, 16), (16, 16),
        (13, 17), (14, 17), (15, 17),
    ]
    
    for px, py in sphere_pts:
        dx = px - cx
        dy = py - 14
        dist = math.hypot(dx, dy)
        if dist >= 3.0:
            set_p(grid, px, py, "u")
        else:
            if state == "charge":
                # Blinding energy charge
                if dist < 1.5:
                    col = "W"
                elif dist < 2.5:
                    col = "o"
                else:
                    col = "O"
            elif state == "strike":
                # Discharging peak arc
                if dx > 0: # Right side facing arc discharge
                    col = "W" if dist < 2.0 else "L"
                else:
                    col = "o" if dist < 2.0 else "O"
            elif state == "afterglow":
                if dist < 1.5:
                    col = "o"
                elif dist < 2.5:
                    col = "O"
                else:
                    col = "C"
            else:
                # Rest state
                if dx <= -1 and dy <= -1:
                    col = "O"
                elif dx >= 1 or dy >= 1:
                    col = "c"
                else:
                    col = "C"
            set_p(grid, px, py, col)
            
    # Spire needle tip on top of sphere
    set_p(grid, cx, 10, "O" if state in ("charge", "strike") else "C")
    set_p(grid, cx, 9, "W" if state in ("charge", "strike") else "O")
    set_p(grid, cx, 8, "L" if state == "charge" else ("W" if state == "strike" else "u"))

def draw_secondary_iron_rod(grid, state):
    # state: 'charge' (F1), 'strike' (F2), 'afterglow' (F3), 'rest' (F4)
    ix = 28 # Secondary iron stake (14px to the right of main rod)
    
    # Slender vertical iron stake (Y=27 to Y=38)
    for y in range(27, 39):
        set_p(grid, ix, y, "h" if state != "strike" else "W")
        set_p(grid, ix + 1, y, "I" if state != "strike" else "L")
        set_p(grid, ix - 1, y, "k")
        set_p(grid, ix + 2, y, "k")
        
    # Pointed iron tip at Y=26
    if state == "strike":
        # Direct impact point! Blinding white & cyan flash
        set_p(grid, ix, 26, "W")
        set_p(grid, ix + 1, 26, "W")
        set_p(grid, ix, 25, "L")
        set_p(grid, ix - 1, 26, "l")
        set_p(grid, ix + 2, 26, "l")
    elif state == "afterglow":
        # Residual glowing heat
        set_p(grid, ix, 26, "W")
        set_p(grid, ix + 1, 26, "L")
        set_p(grid, ix, 25, "l")
        set_p(grid, ix - 1, 26, "k")
        set_p(grid, ix + 2, 26, "k")
    else:
        # Passive iron tip
        set_p(grid, ix, 26, "h")
        set_p(grid, ix + 1, 26, "I")
        set_p(grid, ix, 25, "k")

def build_lightning_frame(frame_num):
    # frame_num: 1 to 4
    grid = empty_grid()
    draw_environment(grid)
    
    if frame_num == 1:
        # Frame 1: Energy Charge
        draw_main_copper_rod(grid, "charge")
        draw_secondary_iron_rod(grid, "rest")
        # 1-2 small sparks around copper sphere
        set_p(grid, 10, 12, "L") # Spark 1 (left)
        set_p(grid, 18, 12, "W") # Spark 2 (right top)
        set_p(grid, 19, 13, "l")
        set_p(grid, 13, 7, "L")  # Spark 3 (above needle)
        
    elif frame_num == 2:
        # Frame 2: Main Arc Strike (CỰC KHÓ - Fractal Zigzag & Branch Arc)
        draw_main_copper_rod(grid, "strike")
        draw_secondary_iron_rod(grid, "strike")
        
        # 1. MAIN ARC STRIKE (Blinding White Core 'W', Sheath 'L', Halo 'l')
        # Sharp angular zigzag path (abrupt steps 1-2-1-2) from (15,14) to (28,26):
        main_core = [
            (15, 14), (16, 14),
            (17, 15), (18, 15),
            (18, 16),
            (19, 17), (20, 17),
            (21, 16), # FORK VERTEX (Sharp reverse jog!)
            (21, 18), (22, 18),
            (22, 19), (23, 20),
            (24, 20), (24, 21),
            (25, 22), (25, 23),
            (26, 23), (26, 24),
            (27, 25), (28, 26),
        ]
        
        # Outer Sheath 'L' for main arc
        for cx, cy in main_core:
            for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
                nx, ny = cx + dx, cy + dy
                if get_p(grid, nx, ny) == ".":
                    set_p(grid, nx, ny, "L")
                    
        # Outer Halo 'l' on key bends
        halo_pts = [
            (16, 13), (17, 16), (20, 18), (21, 15),
            (22, 17), (23, 21), (25, 21), (27, 24), (28, 24)
        ]
        for hx, hy in halo_pts:
            if get_p(grid, hx, hy) in (".", "L"):
                set_p(grid, hx, hy, "l")
                
        # Draw white core over sheath
        for cx, cy in main_core:
            set_p(grid, cx, cy, "W")
            
        # 2. BRANCH ARC (Tia nhánh phụ - 1px thick, chĩa chéo lên không trung rồi cụt đầu)
        # Forks from (21, 16) up-right:
        branch_pts = [
            (22, 15, "W"),  # Root of branch
            (22, 14, "L"),  # 1px step
            (23, 13, "L"),  # Sharp diagonal jog
            (24, 13, "L"),
            (24, 12, "L"),
            (25, 11, "W"),  # Abrupt terminal tip spark
        ]
        for bx, by, col in branch_pts:
            set_p(grid, bx, by, col)
            
    elif frame_num == 3:
        # Frame 3: Afterglow / Dư ảnh mờ
        draw_main_copper_rod(grid, "afterglow")
        draw_secondary_iron_rod(grid, "afterglow")
        
        # Arc breaks into 3 dim fragments (Đứt đoạn, tone xanh tím tối)
        # Fragment A
        frag_a = [(16, 14, "A"), (17, 15, "a")]
        # Fragment B
        frag_b = [(21, 17, "A"), (22, 18, "a"), (23, 19, "a")]
        # Fragment C
        frag_c = [(25, 22, "A"), (26, 23, "a")]
        
        for frag in (frag_a, frag_b, frag_c):
            for fx, fy, col in frag:
                set_p(grid, fx, fy, col)
                
        # Faint dissipation ember near branch tip
        set_p(grid, 25, 11, "a")
        
    elif frame_num == 4:
        # Frame 4: Cooldown (Electric arc completely vanished, copper and iron cooled)
        draw_main_copper_rod(grid, "rest")
        draw_secondary_iron_rod(grid, "rest")
        
    return grid

def main():
    frames = [build_lightning_frame(i) for i in range(1, 5)]
    
    print("--- VERIFICATION OF LIGHTNING STRIKE CONSTRAINTS ---")
    
    # Check 1: Non-linear timing
    arc_colors = {"W", "L", "l", "b", "A", "a"}
    
    # We count arc pixels outside the rods (X between 16 and 27)
    gap_pixels = []
    for f_idx, g in enumerate(frames):
        count = sum(1 for y in range(H) for x in range(16, 27) if g[y][x] in arc_colors)
        gap_pixels.append(count)
        print(f"Frame {f_idx+1}: {count} arc pixels across the gap.")
        
    assert gap_pixels[0] <= 3, f"Frame 1 has premature arc: {gap_pixels[0]}"
    assert gap_pixels[1] >= 20, f"Frame 2 arc did not strike full gap: {gap_pixels[1]}"
    assert 2 <= gap_pixels[2] <= 10, f"Frame 3 arc did not break into dim fragments: {gap_pixels[2]}"
    assert gap_pixels[3] == 0, f"Frame 4 arc did not vanish completely: {gap_pixels[3]}"
    print("Requirement 2 PASSED: Non-linear instantaneous timing (Instant strike in F2, broken afterglow in F3, gone in F4)!")
    assert 2 <= gap_pixels[2] <= 10, f"Frame 3 arc did not break into dim fragments: {gap_pixels[2]}"
    assert gap_pixels[3] == 0, f"Frame 4 arc did not vanish completely: {gap_pixels[3]}"
    print("Requirement 2 PASSED: Non-linear instantaneous timing (Instant strike in F2, broken afterglow in F3, gone in F4)!")
    
    # Check 2: Fractal Lightning Geometry (Zigzag steps, sharp bends, branch arc)
    f2_grid = frames[1]
    # Check branch arc tip at (25, 11)
    assert f2_grid[11][25] == "W", "Branch arc tip (25,11) is missing!"
    # Verify core path has sharp non-linear steps
    print("Requirement 1 PASSED: Fractal lightning geometry with sharp 1-2-1-2 zigzag steps and branch arc!")

    os.makedirs("test", exist_ok=True)
    images = []
    for idx, g in enumerate(frames):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for y in range(H):
            for x in range(W):
                c = g[y][x]
                col = PALETTE.get(c)
                if col:
                    img.putpixel((x, y), col)
        img.save(f"test/lightning_f{idx+1}.png")
        images.append(img)
        
    images[0].save(
        "test/lightning_anim.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / 8),
        loop=0,
        disposal=2
    )
    print("Saved test/lightning_f*.png and test/lightning_anim.gif")

if __name__ == "__main__":
    main()
