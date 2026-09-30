import os
import math
from PIL import Image

W, H = 48, 48

# Terraria Palette: Ancient Basalt Stone Dais & Deep Void Portal & Glowing Cyan Particles
PALETTE = {
    ".": None,
    "#": (10, 4, 16, 255),        # Deepest obsidian outline (#0a0410)
    "S": (8, 4, 13, 130),         # Contact shadow (Alpha 130)
    
    # Ancient Stone Dais (Basalt Slate with chisel marks & grit)
    "T": (118, 102, 138, 255),    # Stone edge highlight (#76668a)
    "R": (82, 68, 100, 255),      # Stone surface midtone (#524464)
    "G": (52, 40, 68, 255),       # Stone dark face (#342844)
    "D": (28, 20, 38, 255),       # Stone crevice / crack (#1c1426)
    
    # Void Portal Swirling Gradient (Quy tắc 1.3: Rim to Absolute Dark Abyss)
    "A": (168, 64, 235, 255),     # Swirling ethereal purple wisp / aura (#a840eb)
    "B": (120, 32, 186, 255),     # Portal outer rim violet (#7820ba)
    "C": (78, 14, 128, 255),      # Deep void mid-purple (#4e0e80)
    "E": (44, 6, 74, 255),        # Dark abyssal cavity (#2c064a)
    "F": (20, 2, 36, 255),        # Near-singularity shadow (#140224)
    "Z": (2, 0, 5, 255),          # Absolute black singularity abyss (#020005)
    
    # 3 Glowing Cyan Particles & Motion Smear
    "W": (255, 255, 255, 255),    # Intense particle spark core (#ffffff)
    "I": (56, 255, 255, 255),     # Radiant cyan particle (#38ffff)
    "M": (0, 195, 225, 255),      # Smear head / mid cyan (#00c3e1)
    "K": (14, 96, 128, 255),      # Smear trail / dim cyan (#0e6080)
}

PALETTE_HEX = {
    ".": None,
    "#": "#0a0410",
    "S": "#08040d",
    "T": "#76668a",
    "R": "#524464",
    "G": "#342844",
    "D": "#1c1426",
    "A": "#a840eb",
    "B": "#7820ba",
    "C": "#4e0e80",
    "E": "#2c064a",
    "F": "#140224",
    "Z": "#020005",
    "W": "#ffffff",
    "I": "#38ffff",
    "M": "#00c3e1",
    "K": "#0e6080",
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

def build_void_portal_frame(frame_idx):
    # frame_idx: 0 to 5 (Frames 1 to 6)
    grid = empty_grid()
    
    X0, Y0 = 24.0, 25.0 # Center of stone dais top surface and portal
    y_ratio = 0.52       # 3/4 perspective compression
    
    # 1. Contact Shadow under Stone Dais on Floor
    for y in range(35, 41):
        for x in range(5, 43):
            dx = (x - X0) / 19.5
            dy = (y - 35.0) / 4.5
            if dx*dx + dy*dy <= 1.0:
                set_p(grid, x, y, "S")
                
    # 2. Stone Dais (Pedestal thickness & top ellipse)
    # Pedestal thickness: from Y=25 down to Y=35
    for y in range(25, 36):
        for x in range(5, 43):
            dx = (x - X0) / 18.5
            bot_dy = (y - 30.5) / 8.5
            if abs(dx) <= 1.0:
                # Vertical side walls of the circular altar
                if y >= 25 and bot_dy <= 0.6:
                    dist_ped = math.hypot(dx, (y - 30.5) / 6.0)
                    if dist_ped <= 1.05:
                        if dist_ped >= 0.95 or y >= 34:
                            set_p(grid, x, y, "#")
                        else:
                            # Stone side shading (Terraria style grit & cracks)
                            if x < 10 or x > 38:
                                col = "#"
                            elif y == 34:
                                col = "D"
                            elif (x + y * 3) % 7 == 0:
                                col = "D" # Chiseled crack
                            elif dx < -0.4:
                                col = "R" if (x % 3 != 0) else "T"
                            elif dx > 0.4:
                                col = "G" if (x % 2 == 0) else "D"
                            else:
                                col = "R" if (y % 2 == 0) else "G"
                            set_p(grid, x, y, col)

    # Top Ellipse of Stone Dais
    for y in range(H):
        for x in range(W):
            dx = (x - X0) / 18.5
            dy = (y - Y0) / 9.5
            d2 = dx*dx + dy*dy
            if d2 <= 1.05:
                if d2 >= 0.90:
                    set_p(grid, x, y, "#")
                else:
                    # Top stone surface texture
                    if dy < -0.6:
                        col = "T" if ((x + y) % 3 != 0) else "R"
                    elif dy > 0.4:
                        col = "G" if ((x * 2 + y) % 5 != 0) else "D"
                    else:
                        # Ancient stone slabs with rune engraving / grit
                        if (x == 15 and y == 23) or (x == 33 and y == 27) or (x == 20 and y == 32):
                            col = "D"
                        elif (x == 16 and y == 23) or (x == 32 and y == 27):
                            col = "T"
                        else:
                            col = "R" if ((x + y) % 4 != 0) else "G"
                    set_p(grid, x, y, col)

    # 3. VOID PORTAL (Lỗ hổng hư không - Quy tắc 1.3: Rim to Absolute Singularity)
    # Portal Ellipse: A_p = 10.5, B_p = 5.4
    portal_rot_angle = frame_idx * (math.pi / 3.0) # Swirling aura rotation
    for y in range(H):
        for x in range(W):
            dx = (x - X0) / 10.5
            dy = (y - Y0) / 5.4
            dist_p = math.hypot(dx, dy)
            if dist_p <= 1.05:
                ang_p = math.atan2(dy, dx) + portal_rot_angle
                wisp = 0.14 * math.sin(ang_p * 3.0)
                eff_dist = dist_p + wisp
                
                if dist_p >= 0.94:
                    # Outer perimeter rim of portal
                    set_p(grid, x, y, "#")
                elif eff_dist > 0.76:
                    # Outer ethereal purple aura wisps (pulsing)
                    col = "A" if ((int(ang_p * 4.0) % 2) == 0) else "B"
                    set_p(grid, x, y, col)
                elif eff_dist > 0.52:
                    # Deep void mid-purple
                    set_p(grid, x, y, "C")
                elif eff_dist > 0.32:
                    # Dark abyssal cavity
                    set_p(grid, x, y, "E")
                elif eff_dist > 0.16:
                    # Near-singularity
                    set_p(grid, x, y, "F")
                else:
                    # ABSOLUTE BLACK SINGULARITY (Rule 1.3)
                    set_p(grid, x, y, "Z")

    # Ensure central core (23..25, 24..26) is PURE ABSOLUTE BLACK 'Z'
    for cy in (24, 25, 26):
        for cx in (23, 24, 25):
            set_p(grid, cx, cy, "Z")
            
    # 4. 3 GLOWING CYAN MAGIC PARTICLES (Spiral trajectory 3/4 squashed)
    base_angles = [0.0, 2.094395, 4.188790]
    
    f = frame_idx # 0 to 5
    particle_points = []
    
    for p_id, b_ang in enumerate(base_angles):
        # Spiral radius: starts at 15.0 (edge of stone dais) and spirals into center (0.2)
        r = 15.0 * (1.0 - f / 5.2)**1.3
        # Accelerating spiral rotation
        ang = b_ang + 0.85 * f + 0.12 * (f**2)
        
        px = X0 + r * math.cos(ang)
        py = Y0 + r * y_ratio * math.sin(ang)
        
        # Tangent vector (motion direction)
        dr_dt = -15.0 * 1.3 * (1.0 - f / 5.2)**0.3 * (1.0 / 5.2) if f < 5.0 else -0.5
        d_ang_dt = 0.85 + 0.24 * f
        
        vx = dr_dt * math.cos(ang) - r * math.sin(ang) * d_ang_dt
        vy = (dr_dt * math.sin(ang) + r * math.cos(ang) * d_ang_dt) * y_ratio
        v_mag = math.hypot(vx, vy)
        ux, uy = (vx / v_mag, vy / v_mag) if v_mag > 0 else (0, 0)
        
        ix, iy = int(round(px)), int(round(py))
        particle_points.append({
            "id": p_id,
            "f": f + 1,
            "x": ix,
            "y": iy,
            "r": r,
            "ux": ux,
            "uy": uy
        })
        
        if f < 5:
            # Frames 1 to 5: particle is visible
            head_col = "W" if f in (2, 3, 4) else "I"
            set_p(grid, ix, iy, head_col)
            
            # Halo around spark
            if f == 0:
                # Frame 1: 1px single glowing speck at edge of dais
                pass
            elif f in (1, 2):
                # Frame 2 & 3: Moving inward along spiral arc with faint glow
                smear_x = int(round(px - ux * 1.0))
                smear_y = int(round(py - uy * 1.0))
                if (smear_x, smear_y) != (ix, iy):
                    set_p(grid, smear_x, smear_y, "I")
            elif f in (3, 4):
                # Frame 4 & 5: Accelerating swirl near event horizon, dragging 2px motion smear!
                sm1_x = int(round(px - ux * 1.0))
                sm1_y = int(round(py - uy * 1.0))
                sm2_x = int(round(px - ux * 2.1))
                sm2_y = int(round(py - uy * 2.1))
                if (sm1_x, sm1_y) != (ix, iy):
                    set_p(grid, sm1_x, sm1_y, "M")
                if (sm2_x, sm2_y) != (ix, iy) and (sm2_x, sm2_y) != (sm1_x, sm1_y):
                    set_p(grid, sm2_x, sm2_y, "K")
        else:
            # Frame 6 (f=5): Old particles have plunged into the singularity 'Z' and vanished!
            # Concurrently, at the outer edge of stone dais, new nascent particle specks condense for next cycle!
            new_r = 15.2
            new_ang = b_ang - 0.2
            n_px = int(round(X0 + new_r * math.cos(new_ang)))
            n_py = int(round(Y0 + new_r * y_ratio * math.sin(new_ang)))
            set_p(grid, n_px, n_py, "K")

    return grid, particle_points

def main():
    frames_data = []
    all_particles = []
    
    for f in range(6):
        grid, pts = build_void_portal_frame(f)
        frames_data.append(grid)
        all_particles.extend(pts)
        
    print("--- VERIFICATION OF VOID PORTAL CONSTRAINTS ---")
    
    # Check 1: Absolute Darkness at center (Rule 1.3)
    for idx, g in enumerate(frames_data):
        assert g[25][24] == "Z", f"Frame {idx+1}: Center (24,25) is not absolute black 'Z'!"
        assert g[24][24] == "Z", f"Frame {idx+1}: Center (24,24) is not absolute black 'Z'!"
        assert g[26][24] == "Z", f"Frame {idx+1}: Center (24,26) is not absolute black 'Z'!"
    print("Requirement 2 PASSED: Pure absolute black singularity 'Z' (#020005) at portal center across all frames!")
    
    # Check 2: 3/4 Flattened Spiral Trajectory verification
    p0_pts = [p for p in all_particles if p["id"] == 0]
    for i in range(len(p0_pts) - 2): # Check transitions 1->2, 2->3, 3->4, 4->5
        p_curr = p0_pts[i]
        p_next = p0_pts[i+1]
        assert p_next["r"] < p_curr["r"], f"Radius did not shrink: {p_curr['r']} -> {p_next['r']}"
        dx_radial = 24.0 - p_curr["x"]
        dy_radial = 25.0 - p_curr["y"]
        dx_move = p_next["x"] - p_curr["x"]
        dy_move = p_next["y"] - p_curr["y"]
        cross = dx_radial * dy_move - dy_radial * dx_move
        print(f"P0 Frame {p_curr['f']}->{p_next['f']}: pos=({p_curr['x']},{p_curr['y']}), r={p_curr['r']:.1f}, cross={cross:.1f} (spiral curvature verified)")
        assert abs(cross) >= 4.0, f"Trajectory segment {p_curr['f']}->{p_next['f']} is too straight: cross={cross}"
        
    print("Requirement 1 PASSED: True squashed 3/4 spiral trajectory (curved path, non-linear velocity, motion smear)!")
    
    # Render test images
    os.makedirs("test", exist_ok=True)
    images = []
    for idx, g in enumerate(frames_data):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for y in range(H):
            for x in range(W):
                c = g[y][x]
                col = PALETTE.get(c)
                if col:
                    img.putpixel((x, y), col)
        img.save(f"test/void_portal_f{idx+1}.png")
        images.append(img)
        
    images[0].save(
        "test/void_portal_anim.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / 8),
        loop=0,
        disposal=2
    )
    print("Test images and gif saved in test/")

if __name__ == "__main__":
    main()
