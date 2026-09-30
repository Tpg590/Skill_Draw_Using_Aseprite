import math
import os
from PIL import Image

W, H = 48, 48
cx, cy = 24.0, 20.0 # Center of helm wheel

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "S": (32, 20, 36, 130),    # Soft ground shadow (Alpha 130)
    
    # Oak Wood (Helm Rim, Spokes, Handles, Pedestal)
    "#": (58, 28, 16, 255),    # Soft dark wood outline (#3a1c10)
    "T": (225, 165, 95, 255),  # Oak highlight (#e1a55f)
    "U": (175, 115, 55, 255),  # Oak midtone (#af7337)
    "M": (120, 70, 32, 255),   # Oak shadow (#784620)
    "D": (75, 38, 18, 255),    # Oak dark crevice (#4b2612)
    
    # Bronze Band & Hub (Aged nautical brass)
    "P": (255, 248, 215, 255), # Specular ivory-white highlight (#fff8d7)
    "A": (245, 190, 70, 255),  # Bright golden shine (#f5be46)
    "B": (195, 130, 38, 255),  # Bronze base (#c38226)
    "C": (130, 75, 20, 255),   # Bronze shadow (#824b14)
    "Z": (75, 38, 12, 255),    # Bronze deep shade (#4b260c)
    
    # Indicator Marker (King Spoke cord wrap)
    "R": (235, 45, 35, 255),   # Vivid crimson marker wrap (#eb2d23)
    "W": (255, 255, 255, 255), # Pure white cord accent (#ffffff)
    "K": (245, 215, 165, 255), # Nautical rope cream (#f5d7a5)
}

def build_helm_frame(angle_deg):
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # 1. Base Pedestal (Ship Deck Mounting Post) behind the wheel
    for y in range(21, 41):
        for x in range(21, 27):
            if x in (21, 26):
                grid[y][x] = "#"
            elif x in (22, 23):
                grid[y][x] = "T" if x == 22 else "U"
            else:
                grid[y][x] = "M"
                
    # Pedestal base steps (y=40..43)
    for y in range(40, 42):
        for x in range(18, 30):
            if x in (18, 29) or (y == 40 and x in (18, 19, 28, 29)):
                grid[y][x] = "#"
            elif x < 23:
                grid[y][x] = "T"
            elif x < 26:
                grid[y][x] = "U"
            else:
                grid[y][x] = "M"
                
    for y in range(42, 44):
        for x in range(15, 33):
            if x in (15, 32) or (y == 42 and x in (15, 16, 31, 32)):
                grid[y][x] = "#"
            elif x < 21:
                grid[y][x] = "T"
            elif x < 27:
                grid[y][x] = "U"
            else:
                grid[y][x] = "M"

    # Soft Elliptical Ground Shadow S (Alpha 130) at y=44..46 (Rule 2.2 & 3.1.4)
    for x in range(13, 35):
        if grid[44][x] == ".":
            grid[44][x] = "S"
    for x in range(15, 33):
        if grid[45][x] == ".":
            grid[45][x] = "S"
    for x in range(18, 30):
        if grid[46][x] == ".":
            grid[46][x] = "S"

    # 2. Wheel Geometry & Masking
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    r_rim_out = 12.6
    r_rim_in = 8.4
    r_bronze = 5.2
    r_axle = 2.4
    r_handle_tip = 18.0
    half_handle_w = 2.0
    
    comp_map = {}
    for y in range(H):
        for x in range(W):
            gx = x + 0.5 - cx
            gy = y + 0.5 - cy
            d = math.hypot(gx, gy)
            
            # Local rotated coordinates
            rx = gx * cos_a + gy * sin_a
            ry = -gx * sin_a + gy * cos_a
            
            if d <= r_axle:
                comp_map[(x, y)] = (gx, gy, "AXLE", d, 0)
                continue
                
            if d <= r_bronze:
                comp_map[(x, y)] = (gx, gy, "BRONZE", d, 0)
                continue
                
            is_rim = (r_rim_in <= d <= r_rim_out)
            is_spoke = False
            handle_id = 0
            
            # Vertical arm (in local coords: ry axis)
            if abs(rx) <= half_handle_w and d <= r_handle_tip:
                is_spoke = True
                handle_id = 1 if ry < 0 else 3
                
            # Horizontal arm (in local coords: rx axis)
            if abs(ry) <= half_handle_w and d <= r_handle_tip:
                is_spoke = True
                handle_id = 2 if rx > 0 else 4
                
            if is_rim or is_spoke:
                comp_type = "HANDLE" if (d > r_rim_out and is_spoke) else \
                            "RIM" if is_rim else "SPOKE"
                comp_map[(x, y)] = (gx, gy, comp_type, d, handle_id)
                
    outline_set = set()
    for (x, y) in comp_map:
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if (nx, ny) not in comp_map:
                outline_set.add((x, y))
                break

    # 3. Ambient Lighting & Specular Highlight at 10 o'clock (-135 deg)
    light_x, light_y = -0.707, -0.707
    
    for (x, y), (gx, gy, comp_type, d, handle_id) in comp_map.items():
        ang = math.degrees(math.atan2(gy, gx))
        diff_10_oclock = abs((ang - (-135) + 180) % 360 - 180)
        norm_dot = (gx * light_x + gy * light_y) / (d + 0.001)
        
        if (x, y) in outline_set:
            grid[y][x] = "#"
            continue
            
        # Center Axle Bolt
        if comp_type == "AXLE":
            if d <= 1.2:
                grid[y][x] = "P"
            elif gx < 0 and gy < 0:
                grid[y][x] = "A"
            else:
                grid[y][x] = "C"
            continue
            
        # Central Bronze Ring
        if comp_type == "BRONZE":
            if diff_10_oclock < 25 and d > 3.2:
                grid[y][x] = "P" # Specular ivory-white!
            elif diff_10_oclock < 55:
                grid[y][x] = "A"
            elif norm_dot > 0.1:
                grid[y][x] = "B"
            elif norm_dot < -0.4:
                grid[y][x] = "Z"
            else:
                grid[y][x] = "C"
            continue
            
        # Wooden Circular Rim
        if comp_type == "RIM":
            if diff_10_oclock < 20 and d > 10.0:
                grid[y][x] = "P" # Specular highlight 1-2px at 10 o'clock!
            elif diff_10_oclock < 45:
                grid[y][x] = "T"
            elif norm_dot > 0.2:
                grid[y][x] = "U"
            elif norm_dot < -0.35:
                grid[y][x] = "D"
            else:
                grid[y][x] = "M"
            continue
            
        # Spokes (connecting bronze to rim)
        if comp_type == "SPOKE":
            if norm_dot > 0.35:
                grid[y][x] = "T"
            elif norm_dot < -0.3:
                grid[y][x] = "M"
            else:
                grid[y][x] = "U"
            continue
            
        # Handles
        if comp_type == "HANDLE":
            # King Spoke (handle_id == 1): DISTINCT ON ALL 4 FRAMES!
            if handle_id == 1:
                if 12.8 <= d < 14.3:
                    grid[y][x] = "R" # Vivid crimson cord band
                    continue
                elif 14.3 <= d <= 15.6:
                    grid[y][x] = "W" # White nautical rope band
                    continue
                elif d > 15.6:
                    grid[y][x] = "A" if norm_dot > 0 else "B" # Golden knob tip
                    continue
                    
            # Normal turned wooden handles
            if norm_dot > 0.4:
                grid[y][x] = "T"
            elif norm_dot < -0.3:
                grid[y][x] = "M"
            else:
                grid[y][x] = "U"
                
    return grid

# Build 4 Frames (Continuous Rotation, King Spoke moves 0 -> 45 -> 90 -> 135 deg)
frames = [
    build_helm_frame(0),   # Frame 1: King Spoke at 12 o'clock (0 deg)
    build_helm_frame(45),  # Frame 2: King Spoke at 1:30 o'clock (45 deg)
    build_helm_frame(90),  # Frame 3: King Spoke at 3 o'clock (90 deg)
    build_helm_frame(135), # Frame 4: King Spoke at 4:30 o'clock (135 deg)
]

# Validation
for f_idx, fr in enumerate(frames):
    for r_idx, r in enumerate(fr):
        if len(r) != 48:
            raise ValueError(f"Frame {f_idx+1} row {r_idx} has length {len(r)}, expected 48!")

print("All 4 frames successfully validated (48x48)!")

# Render test sheet
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
sheet_img.save("test/test_helm_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_helm_sheet_4x.png")

print("Generated test/test_helm_sheet_4x.png successfully!")
