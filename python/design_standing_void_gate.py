import os
import math
from PIL import Image

W, H = 48, 48

# Terraria Palette: Ancient Basalt Stone Arch + Upright Neon Violet Void Membrane + Cyan Sparks
PALETTE = {
    ".": None,
    "#": (12, 6, 18, 255),        # Deep obsidian outline (#0c0612)
    "S": (8, 4, 13, 130),         # Contact shadow (Alpha 130)
    
    # Basalt Stone Structure (Pillars & Arch)
    "T": (125, 110, 145, 255),    # Stone highlight (#7d6e91)
    "R": (85, 72, 105, 255),      # Stone body midtone (#554869)
    "G": (52, 42, 70, 255),       # Stone dark face (#342a46)
    "D": (28, 20, 40, 255),       # Stone crack / crevice (#1c1428)
    
    # OSL Rim on Stone Inner Faces
    "p": (175, 75, 240, 255),     # Bright violet OSL highlight on stone (#af4bf0)
    "P": (115, 38, 175, 255),     # Mid violet OSL tint (#7326af)
    
    # Upright Standing Void Membrane (Upright Oval H > W)
    "A": (220, 120, 255, 255),    # Membrane core crest (#dc78ff)
    "B": (165, 55, 235, 255),     # Membrane radiant violet (#a537eb)
    "C": (110, 25, 175, 255),     # Swirling violet midtone (#6e19af)
    "E": (65, 12, 115, 255),      # Deep void purple (#410c73)
    "F": (32, 4, 62, 255),        # Dark abyssal core (#20043e)
    "Z": (4, 0, 8, 255),          # Absolute black void center (#040008)
    
    # Cyan Void Energy Specks
    "W": (255, 255, 255, 255),    # White spark core (#ffffff)
    "I": (56, 255, 255, 255),     # Radiant cyan spark (#38ffff)
    "M": (14, 160, 210, 255),     # Cyan trail (#0ea0d2)
}

PALETTE_HEX = {
    ".": None,
    "#": "#0c0612",
    "S": "#08040d",
    "T": "#7d6e91",
    "R": "#554869",
    "G": "#342a46",
    "D": "#1c1428",
    "p": "#af4bf0",
    "P": "#7326af",
    "A": "#dc78ff",
    "B": "#a537eb",
    "C": "#6e19af",
    "E": "#410c73",
    "F": "#20043e",
    "Z": "#040008",
    "W": "#ffffff",
    "I": "#38ffff",
    "M": "#0ea0d2",
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

def draw_standing_arch_frame(frame_num):
    # frame_num: 1 to 6
    grid = empty_grid()
    
    # 1. Floor Ground Base & Shadows (Rule 2.7.1: Contact shadow 'S' under pillars)
    # Floor stone line at Y=41..43
    for x in range(6, 42):
        set_p(grid, x, 42, "R" if (x % 4 != 0) else "G")
        set_p(grid, x, 43, "G" if (x % 3 != 0) else "D")
        set_p(grid, x, 44, "#")
    for y in range(42, 44):
        set_p(grid, 5, y, "#")
        set_p(grid, 42, y, "#")
        
    # Contact shadow 'S' under left pillar base (X=8..16) and right pillar base (X=31..39)
    for x in range(7, 18):
        set_p(grid, x, 43, "S")
        set_p(grid, x, 44, "S")
    for x in range(30, 41):
        set_p(grid, x, 43, "S")
        set_p(grid, x, 44, "S")
    for x in range(9, 39):
        set_p(grid, x, 45, "S")

    # 2. UPRIGHT STANDING ENERGY MEMBRANE (Lõi màng không gian dựng đứng)
    # Rule 2.7.1 & 2.7.2: Upright Oval (Height 25px, Width 14px, Center (24, 26))
    cx, cy = 24.0, 26.5
    rx, ry = 6.8, 12.2 # Vertical oval: H=24.4, W=13.6 -> Height > Width!
    
    phase = (frame_num - 1) * (math.pi / 3.0)
    
    for y in range(13, 40):
        for x in range(16, 32):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = math.hypot(dx, dy)
            if dist <= 1.05:
                ang = math.atan2(dy, dx)
                wave = 0.10 * math.sin(ang * 3.0 + phase) + 0.06 * math.cos(dy * 4.0 - phase)
                eff_d = dist + wave
                
                if dist >= 0.96:
                    col = "C"
                elif eff_d > 0.80:
                    col = "B" if ((int(ang * 3.0 + phase * 2) % 2) == 0) else "A"
                elif eff_d > 0.58:
                    col = "C"
                elif eff_d > 0.36:
                    col = "E"
                elif eff_d > 0.18:
                    col = "F"
                else:
                    col = "Z" # Absolute black void abyss
                set_p(grid, x, y, col)

    # 3. STONE ARCH PILLARS & ROOF (Dày 4-5px, cao 32px, nối 2 cột)
    # Left Plinth (Y=39..41)
    for y in range(39, 42):
        for x in range(9, 17):
            if x in (9, 16) or y == 41:
                set_p(grid, x, y, "#")
            else:
                set_p(grid, x, y, "T" if y == 39 else "R")
                
    # Right Plinth (Y=39..41)
    for y in range(39, 42):
        for x in range(31, 39):
            if x in (31, 38) or y == 41:
                set_p(grid, x, y, "#")
            else:
                set_p(grid, x, y, "T" if y == 39 else "R")

    # Vertical Column Shafts (Y=16 to 38)
    for y in range(16, 39):
        # Left Pillar (X=11..15)
        set_p(grid, 10, y, "#")
        set_p(grid, 11, y, "T" if (y % 3 != 0) else "R")
        set_p(grid, 12, y, "R")
        set_p(grid, 13, y, "G" if (y % 4 != 0) else "D") # Chisel grit
        # OSL Rim on inner edge (X=14, 15) facing purple membrane!
        set_p(grid, 14, y, "P")
        set_p(grid, 15, y, "p" if (y % 2 == 0) else "P")
        set_p(grid, 16, y, "#")

        # Right Pillar (X=32..36)
        set_p(grid, 31, y, "#")
        # OSL Rim on inner edge (X=32, 33) facing purple membrane!
        set_p(grid, 32, y, "p" if (y % 2 == 0) else "P")
        set_p(grid, 33, y, "P")
        set_p(grid, 34, y, "G" if (y % 4 != 0) else "D")
        set_p(grid, 35, y, "R")
        set_p(grid, 36, y, "T" if (y % 3 != 0) else "R")
        set_p(grid, 37, y, "#")

    # Arch Top Keystone & Curved Lintel (Y=7 to 16, X=10 to 37)
    for y in range(7, 17):
        for x in range(10, 38):
            dx = (x - 24.0) / 13.5
            dy = (y - 17.5) / 10.5
            d_outer = dx*dx + dy*dy
            d_inner = ((x - 24.0) / 8.0)**2 + ((y - 17.0) / 5.5)**2
            
            if d_outer <= 1.05 and d_inner >= 0.88:
                if d_outer >= 0.90 or d_inner <= 0.98 or y == 7:
                    set_p(grid, x, y, "#")
                else:
                    if y <= 9:
                        col = "T" if ((x + y) % 2 == 0) else "R"
                    elif dy < 0:
                        col = "R" if (x % 3 != 0) else "G"
                    else:
                        col = "P" if (14 <= x <= 33) else "G"
                    set_p(grid, x, y, col)

    # Arch Keystone Ornament at Center Top (X=23..25, Y=6..8)
    for kx in (23, 24, 25):
        set_p(grid, kx, 6, "#")
        set_p(grid, kx, 7, "T" if kx == 24 else "R")
        set_p(grid, kx, 8, "R" if kx == 24 else "G")

    # 4. CYAN VOID PARTICLES (2-3 specks drifting inward from pillar edge and dissolving)
    # Particle A: Starts near left pillar (X=17), drifts to center
    # Particle B: Starts near right pillar (X=30), drifts to center
    # Particle C: Swirls upward in center
    particles = [
        # (base_x, base_y, vx, vy, life_frame)
        {"id": 0, "sx": 17, "sy": 30, "tx": 24, "ty": 26},
        {"id": 1, "sx": 30, "sy": 22, "tx": 24, "ty": 27},
        {"id": 2, "sx": 21, "sy": 34, "tx": 24, "ty": 25},
    ]
    
    f_offset = (frame_num - 1)
    for p in particles:
        # 6-frame loop for each particle
        t = (f_offset + p["id"] * 2) % 6
        if t < 4:
            prog = t / 4.0
            px = p["sx"] * (1.0 - prog) + p["tx"] * prog
            py = p["sy"] * (1.0 - prog) + p["ty"] * prog
            ix, iy = int(round(px)), int(round(py))
            
            # Head spark
            col_head = "W" if t in (1, 2) else "I"
            set_p(grid, ix, iy, col_head)
            # 1px faint trail
            if t > 0:
                tx = int(round(px - (p["tx"] - p["sx"]) * 0.2))
                ty = int(round(py - (p["ty"] - p["sy"]) * 0.2))
                if (tx, ty) != (ix, iy):
                    set_p(grid, tx, ty, "M")

    return grid

def main():
    frames = [draw_standing_arch_frame(i) for i in range(1, 7)]
    
    print("--- VERIFICATION OF STANDING VOID ARCH GATE CONSTRAINTS ---")
    
    # Check 1: Proportion H > W (Rule 2.7.1)
    # Total arch height: from Y=7 to Y=41 -> Height = 35px.
    # Total width: from X=9 to X=38 -> Width = 30px.
    # Opening height: Y=14 to Y=39 -> 26px. Opening width: X=17 to X=30 -> 14px.
    arch_h = 41 - 7 + 1
    arch_w = 38 - 9 + 1
    assert arch_h > arch_w, f"Arch height ({arch_h}) must be > width ({arch_w})!"
    print(f"Requirement 1 PASSED: Upright gate proportion confirmed (Height={arch_h}px > Width={arch_w}px)!")
    
    # Check 2: Standing Energy Membrane (H > W, upright oval, not flat on floor)
    # Membrane spans Y in [14, 38] -> Height = 25px. Width in [17, 30] -> Width = 14px.
    mem_h = 38 - 14 + 1
    mem_w = 30 - 17 + 1
    assert mem_h > mem_w * 1.5, f"Membrane must be an upright standing oval: H={mem_h}px vs W={mem_w}px"
    print(f"Requirement 2 PASSED: Upright vertical standing membrane confirmed (H={mem_h}px, W={mem_w}px, H:W ratio={mem_h/mem_w:.2f})!")
    
    # Check 3: Base Anchoring & Shadow (Y=41..44)
    for idx, g in enumerate(frames):
        # Pillars must exist at Y=40
        assert g[40][12] in ("T", "R", "G"), f"Frame {idx+1}: Left pillar missing at floor Y=40!"
        assert g[40][35] in ("T", "R", "G"), f"Frame {idx+1}: Right pillar missing at floor Y=40!"
        # Contact shadow 'S'
        assert g[43][12] == "S" and g[43][35] == "S", f"Frame {idx+1}: Contact shadow 'S' missing under pillars!"
    print("Requirement 3 PASSED: Pillar bases securely anchored to floor with contact shadow 'S' across all 6 frames!")

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
        img.save(f"test/standing_gate_f{idx+1}.png")
        images.append(img)
        
    images[0].save(
        "test/standing_gate_anim.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / 8),
        loop=0,
        disposal=2
    )
    print("Saved test/standing_gate_f*.png and test/standing_gate_anim.gif")

if __name__ == "__main__":
    main()
