import math
import os
from PIL import Image

W, H = 64, 64
cx, cy = 32.0, 32.0

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "#": (14, 10, 12, 255),    # Near-black outline (#0e0a0c)
    
    # Dungeon Stone Wall
    "K": (135, 142, 152, 255), # Stone brick light/highlight (#878e98)
    "G": (85, 92, 102, 255),   # Stone brick base gray (#555c66)
    "N": (48, 54, 62, 255),    # Stone mortar / crack shadow (#30363e)
    
    # Iron Brackets & Rivets
    "I": (175, 185, 195, 255), # Iron highlight (#afb9c3)
    "F": (100, 110, 122, 255), # Iron dark steel (#646e7a)
    "L": (45, 50, 58, 255),    # Iron shadow (#2d323a)
    
    # Bronze Gear Wheel (Aged Rusted Bronze)
    "P": (255, 252, 235, 255), # Specular highlight (1-2px ivory white, #fffceb)
    "A": (245, 185, 75, 255),  # Bronze bright golden shine (#f5b94b)
    "B": (195, 125, 42, 255),  # Bronze main body (#c37d2a)
    "C": (130, 72, 24, 255),   # Bronze dark shadow (#824818)
    "Z": (75, 38, 16, 255),    # Bronze deep crevice shade (#4b2610)
    
    # Verdigris Patina Rust
    "X": (105, 180, 155, 255), # Light turquoise verdigris (#69b49b)
    "V": (45, 110, 95, 255),   # Dark oxidized green (#2d6e5f)
    
    # Center Axle & Screws
    "E": (220, 225, 235, 255), # Bolt steel shine (#dce1eb)
    "S": (16, 12, 18, 130),    # Drop shadow on stone wall (Alpha 130)
}

def generate_gear_frame(angle_deg, frame_idx):
    # Base stone wall background
    # Rounded rectangular stone mount from 5 to 58
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Generate Wall
    for y in range(H):
        for x in range(W):
            dx = abs(x + 0.5 - 32.0)
            dy = abs(y + 0.5 - 32.0)
            corner_d = (dx - 22) + (dy - 22)
            if dx <= 28 and dy <= 28 and corner_d <= 14:
                if dx >= 27 or dy >= 27 or corner_d >= 13:
                    grid[y][x] = "#"
                else:
                    is_mortar = False
                    if y in (17, 32, 47):
                        is_mortar = True
                    elif y < 17 and x in (20, 44):
                        is_mortar = True
                    elif 17 < y < 32 and x in (12, 52):
                        is_mortar = True
                    elif 32 < y < 47 and x in (22, 42):
                        is_mortar = True
                    elif y > 47 and x in (14, 34, 50):
                        is_mortar = True
                        
                    if is_mortar:
                        grid[y][x] = "N"
                    else:
                        if (y in (18, 33, 48) or x in (21, 45, 13, 53, 23, 43)) and not is_mortar:
                            grid[y][x] = "K"
                        else:
                            grid[y][x] = "G"
                            
    # Iron corner brackets with hex bolts
    corners = [(9, 9), (54, 9), (9, 54), (54, 54)]
    for cx_c, cy_c in corners:
        for by in range(cy_c - 3, cy_c + 4):
            for bx in range(cx_c - 3, cx_c + 4):
                if 0 <= bx < W and 0 <= by < H:
                    bd = math.hypot(bx - cx_c, by - cy_c)
                    if bd <= 3.2:
                        grid[by][bx] = "F"
                    if bd <= 1.5:
                        grid[by][bx] = "E"
                    elif bd > 3.0 and bd <= 3.8:
                        grid[by][bx] = "#"

    # Wall-mounted ratchet clicker / pawl mounted at top-right (around x=48..53, y=14..22)
    # The pawl clicks as teeth rotate past
    # Frame 1: Pawl resting at y=17..20
    # Frame 2: Pawl lifted by 1h30 tooth to y=15..18
    # Frame 3: Pawl dropping back to y=17..20
    # Frame 4: Pawl resting at y=17..20
    pawl_y_offset = -2 if frame_idx == 1 else 0
    # Pawl mount pivot at (50, 14)
    for py in range(13, 17):
        for px in range(48, 53):
            grid[py][px] = "#" if (px in (48, 52) or py in (13, 16)) else "F"
    grid[14][50] = "E" # Pivot bolt
    
    # Pawl lever arm reaching towards gear rim
    for py in range(16, 22):
        for px in range(44, 49):
            d_arm = abs((px - 46) + (py - 18 - pawl_y_offset))
            if d_arm <= 1:
                grid[py + pawl_y_offset][px] = "I" if px == 45 else "F"

    # 2. Drop Shadow of Gear onto Wall (offset down-right: dx=+2, dy=+2)
    # Gear silhouette check function
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    r_hub = 8.5
    r_in = 13.5
    r_out = 19.5
    r_tip = 26.5
    half_tooth_w = 4.2
    half_spoke_w = 2.6
    
    def is_gear(gx, gy):
        d = math.hypot(gx, gy)
        if d > r_tip + 0.8:
            return False, 0
        # Hub
        if d <= r_hub:
            return True, d
        # Rim
        if r_in <= d <= r_out:
            return True, d
            
        # Rotate point by -angle to align with reference coordinate system
        rx = gx * cos_a + gy * sin_a
        ry = -gx * sin_a + gy * cos_a
        
        # Spokes (connecting hub to rim)
        if d < r_in:
            if abs(rx) <= half_spoke_w or abs(ry) <= half_spoke_w:
                return True, d
                
        # Teeth (projecting from rim to r_tip)
        if r_out <= d <= r_tip:
            # 4 teeth along rx and ry axes
            if (abs(rx) <= half_tooth_w and (ry > r_out - 1 or ry < -r_out + 1)) or \
               (abs(ry) <= half_tooth_w and (rx > r_out - 1 or rx < -r_out + 1)):
                return True, d
                
        return False, 0

    # Draw drop shadow S
    for y in range(H):
        for x in range(W):
            # Check if this pixel is covered by gear shadow (offset by -2, -2)
            gx = (x + 0.5 - cx) - 2.0
            gy = (y + 0.5 - cy) - 2.0
            in_gear_shadow, _ = is_gear(gx, gy)
            if in_gear_shadow and grid[y][x] not in (".", "#"):
                grid[y][x] = "S"

    # 3. Gear Outline & Solid Body
    # We first determine the gear mask
    gear_mask = [[False for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            gx = x + 0.5 - cx
            gy = y + 0.5 - cy
            in_g, _ = is_gear(gx, gy)
            gear_mask[y][x] = in_g

    # Determine outlines (pixels in gear_mask that border non-gear pixels)
    outline_mask = [[False for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if gear_mask[y][x]:
                # Check 4 neighbors
                is_edge = False
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                    if not (0 <= nx < W and 0 <= ny < H) or not gear_mask[ny][nx]:
                        is_edge = True
                        break
                if is_edge:
                    outline_mask[y][x] = True

    # Shading computation with STATIC LIGHT SOURCE AT TOP-LEFT (-1, -1)
    light_x, light_y = -0.707, -0.707
    
    for y in range(H):
        for x in range(W):
            if not gear_mask[y][x]:
                continue
                
            if outline_mask[y][x]:
                grid[y][x] = "#"
                continue
                
            gx = x + 0.5 - cx
            gy = y + 0.5 - cy
            d = math.hypot(gx, gy)
            
            # Central Bolt / Axle
            if d <= 4.2:
                if d <= 1.8:
                    grid[y][x] = "E"
                elif gx < 0 and gy < 0:
                    grid[y][x] = "I"
                elif gx > 0 and gy > 0:
                    grid[y][x] = "L"
                else:
                    grid[y][x] = "F"
                continue
                
            # Axle Hub Ring (between 4.2 and 8.0)
            if d <= r_hub:
                # Top-left gets light, bottom-right gets shadow
                norm_dot = (gx * light_x + gy * light_y) / (d + 0.001)
                if norm_dot > 0.4:
                    grid[y][x] = "A" if norm_dot > 0.75 else "B"
                elif norm_dot < -0.3:
                    grid[y][x] = "Z" if norm_dot < -0.6 else "C"
                else:
                    grid[y][x] = "B"
                continue

            # ROTATING DETAILS (Rust patina & spoke scratches)
            # Local coordinates in rotating frame of reference
            rx = gx * cos_a + gy * sin_a
            ry = -gx * sin_a + gy * cos_a
            
            # Check for a signature verdigris patina patch that rotates with the gear!
            # Patina patch near Tooth 1 (rx around 0, ry < -15)
            # and another smaller patch near Tooth 3 (rx > 15, ry around 0)
            is_patina = False
            if (abs(rx - 1.5) <= 2.2 and -22 <= ry <= -16) or \
               (15 <= rx <= 20 and abs(ry - 2.0) <= 2.0):
                is_patina = True
                
            # STATIC SPECULAR HIGHLIGHT & SHADING
            # Normal vector on gear surfaces:
            # On circular rim: normal is radial (gx/d, gy/d)
            # Light vector is (-0.707, -0.707) -> Angle is 135 deg (10h30)
            norm_dot = (gx * light_x + gy * light_y) / (d + 0.001)
            
            # Angle in degrees (0 is right, 90 is bottom, 180 is left, 270 is top)
            # 10h30 is at dx < 0, dy < 0, around angle = 225 deg (or -135 deg)
            angle_p = math.degrees(math.atan2(gy, gx)) # -180 to +180
            # 10h30 corresponds to -135 degrees!
            dist_to_highlight_angle = abs((angle_p - (-135) + 180) % 360 - 180)
            
            # STATIC SPECULAR REFLECTION on circular rim
            if r_in < d < r_out:
                if dist_to_highlight_angle < 18 and d > 16.0:
                    grid[y][x] = "P" # Specular 1-2px ivory white!
                elif dist_to_highlight_angle < 35:
                    grid[y][x] = "A" # Golden shine
                elif norm_dot > 0.2:
                    grid[y][x] = "B"
                elif norm_dot < -0.4:
                    grid[y][x] = "Z"
                else:
                    grid[y][x] = "C"
                    
                # Patina override on rim if present
                if is_patina:
                    grid[y][x] = "X" if dist_to_highlight_angle < 45 else "V"
                continue
                
            # Spokes
            if d <= r_in:
                if norm_dot > 0.3:
                    grid[y][x] = "A" if norm_dot > 0.7 else "B"
                elif norm_dot < -0.3:
                    grid[y][x] = "Z" if norm_dot < -0.6 else "C"
                else:
                    grid[y][x] = "B"
                continue
                
            # Teeth (d >= r_out)
            # STATIC LIGHTING on teeth:
            # Teeth facing top-left receive highlight!
            if dist_to_highlight_angle < 22 and d > 22.0:
                grid[y][x] = "P" if dist_to_highlight_angle < 12 else "A"
            elif norm_dot > 0.35:
                grid[y][x] = "A" if norm_dot > 0.75 else "B"
            elif norm_dot < -0.3:
                grid[y][x] = "Z" if norm_dot < -0.6 else "C"
            else:
                grid[y][x] = "B"
                
            if is_patina:
                grid[y][x] = "X" if norm_dot > 0 else "V"
                
    return grid

# Test generation of 4 frames:
# Frame 1: 0 deg (+)
# Frame 2: 45 deg (x)
# Frame 3: 90 deg (+) with rotated patina
# Frame 4: 135 deg (x) with rotated patina
frames_grid = [
    generate_gear_frame(0, 0),
    generate_gear_frame(45, 1),
    generate_gear_frame(90, 2),
    generate_gear_frame(135, 3),
]

sheet_img = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
pil_frames = []

for f_idx, f_data in enumerate(frames_grid):
    f_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = f_img.load()
    for y in range(H):
        for x in range(W):
            pix[x, y] = PALETTE.get(f_data[y][x], (0, 0, 0, 0))
    sheet_img.paste(f_img, (f_idx * W, 0))
    pil_frames.append(f_img)

os.makedirs("test", exist_ok=True)
sheet_img.save("test/test_gear_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_gear_sheet_4x.png")

print("Generated test/test_gear_sheet_4x.png successfully!")
