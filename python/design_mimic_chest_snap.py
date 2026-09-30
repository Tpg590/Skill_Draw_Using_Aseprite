import os
import math
from PIL import Image

W, H = 48, 48

# Stardew Valley Palette: Warm Oak Wood, Brass Fittings, Soft Walnut Outline (NO #000000!)
PALETTE = {
    ".": None,
    "#": (54, 22, 8, 255),        # Soft dark walnut outline (#361608 - strictly NO #000000!)
    "S": (36, 16, 12, 130),       # Soft earthy contact shadow (Alpha 130)
    
    # Oak Wood Planks
    "H": (224, 148, 70, 255),     # Golden oak wood highlight (#e09446)
    "M": (170, 98, 38, 255),      # Warm chestnut wood midtone (#aa6226)
    "D": (110, 52, 18, 255),      # Dark walnut wood shadow (#6e3412)
    
    # Metal Bands & Golden Latch (Khóa vàng chói)
    "Y": (255, 220, 96, 255),     # Shiny gold/brass highlight (#ffdc60)
    "B": (196, 150, 40, 255),     # Gold/brass midtone (#c49628)
    "K": (110, 74, 16, 255),      # Gold/brass dark shadow (#6e4a10)
    
    # Mimic Throat, Gums & Eyes
    "X": (48, 8, 28, 255),        # Deep dark gullet shadow (#30081c)
    "G": (148, 28, 56, 255),      # Gums & tongue midtone (#941c38)
    "T": (255, 244, 220, 255),    # Sharp ivory teeth (#fff4dc)
    "E": (255, 28, 48, 255),      # Glowing predatory eyes (#ff1c30)
    "e": (255, 140, 40, 255),     # Eye pupil glow (#ff8c28)
    
    # Viscous Saliva Filaments & Splatter
    "P": (255, 168, 208, 255),    # Saliva highlight / surface tension (#ffa8d0)
    "p": (216, 80, 140, 255),     # Viscous mucus midtone (#d8508c)
}

PALETTE_HEX = {
    ".": None,
    "#": "#361608",
    "S": "#24100c",
    "H": "#e09446",
    "M": "#aa6226",
    "D": "#6e3412",
    "Y": "#ffdc60",
    "B": "#c49628",
    "K": "#6e4a10",
    "X": "#30081c",
    "G": "#941c38",
    "T": "#fff4dc",
    "E": "#ff1c30",
    "e": "#ff8c28",
    "P": "#ffa8d0",
    "p": "#d8508c",
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

def draw_chest_base(grid, x_left, x_right, y_top, y_bot, is_squash=False):
    # Rule 3: BASE ANCHORING - y_bot is strictly 39 across all frames!
    for y in range(y_top, y_bot + 1):
        for x in range(x_left, x_right + 1):
            if x in (x_left, x_right) or y == y_bot:
                set_p(grid, x, y, "#")
            else:
                # 2 Iron/brass vertical bands at x_left+3, x_right-3
                if x in (x_left + 3, x_right - 3):
                    col = "Y" if y == y_top else ("B" if y < y_bot - 1 else "K")
                elif y == y_bot - 1:
                    col = "D"
                elif y == y_top:
                    col = "H" if not is_squash else "M"
                else:
                    col = "M" if (x % 3 != 0) else "D"
                set_p(grid, x, y, col)

def draw_shadow(grid, cx, base_w, y_floor=40):
    half_w = base_w // 2 + 2
    for x in range(cx - half_w, cx + half_w + 1):
        set_p(grid, x, y_floor, "S")
    for x in range(cx - half_w + 2, cx + half_w - 1):
        set_p(grid, x, y_floor + 1, "S")

def draw_golden_lock(grid, center_x, center_y):
    # Rule 4.7: Attached Prop Continuity - Shiny Golden Latch (3x3 with keyhole)
    # Must exist in ALL frames!
    set_p(grid, center_x - 1, center_y - 1, "Y")
    set_p(grid, center_x,     center_y - 1, "Y")
    set_p(grid, center_x + 1, center_y - 1, "Y")
    set_p(grid, center_x - 1, center_y,     "B")
    set_p(grid, center_x,     center_y,     "K") # Keyhole / lock core
    set_p(grid, center_x + 1, center_y,     "B")
    set_p(grid, center_x,     center_y + 1, "B")

def build_mimic_frame(frame_num):
    grid = empty_grid()
    cx = 24
    
    # -------------------------------------------------------------
    # FRAME 1: IDLE (Closed normal chest, golden latch in center)
    # -------------------------------------------------------------
    if frame_num == 1:
        draw_shadow(grid, cx, 22, y_floor=40)
        draw_chest_base(grid, 13, 35, 31, 39)
        # Lid: X=12..36 (Overhang Rule 3.3), Y=24..30
        for y in range(24, 31):
            for x in range(12, 37):
                if x in (12, 36) or y in (24, 30):
                    set_p(grid, x, y, "#")
                else:
                    if x in (15, 33):
                        set_p(grid, x, y, "Y" if y == 25 else "B")
                    elif y == 25:
                        set_p(grid, x, y, "H")
                    elif y == 29:
                        set_p(grid, x, y, "D")
                    else:
                        set_p(grid, x, y, "M" if (x % 3 != 0) else "D")
        # Rule 4.7: Golden Latch at front edge
        draw_golden_lock(grid, 24, 30)

    # -------------------------------------------------------------
    # FRAME 2: CRACK OPEN (Lid lifts slightly, latch moves up with lid)
    # -------------------------------------------------------------
    elif frame_num == 2:
        draw_shadow(grid, cx, 22, y_floor=40)
        draw_chest_base(grid, 13, 35, 31, 39)
        
        # Dark maw slit: Y=28..30
        for y in range(28, 31):
            for x in range(14, 35):
                set_p(grid, x, y, "X")
                
        # Sharp teeth peeking
        for tx in (16, 19, 22, 26, 29, 32):
            set_p(grid, tx, 30, "T")
        for tx in (17, 21, 27, 31):
            set_p(grid, tx, 28, "T")
            
        # Glowing red eyes
        set_p(grid, 20, 29, "E")
        set_p(grid, 28, 29, "E")
        
        # Lid tilted up: Y=22..27
        for y in range(22, 28):
            for x in range(12, 37):
                if x in (12, 36) or y in (22, 27):
                    set_p(grid, x, y, "#")
                else:
                    if x in (15, 33):
                        set_p(grid, x, y, "Y" if y == 23 else "B")
                    elif y == 23:
                        set_p(grid, x, y, "H")
                    else:
                        set_p(grid, x, y, "M" if (x % 3 != 0) else "D")
                        
        # Rule 4.7: Golden Latch moves up with lid
        draw_golden_lock(grid, 24, 27)

    # -------------------------------------------------------------
    # FRAME 3: FULL GAPE (Rule 4.6: Hinge Rotation, Lid compressed to 6-7px, Latch on front edge)
    # -------------------------------------------------------------
    elif frame_num == 3:
        draw_shadow(grid, cx, 22, y_floor=40)
        draw_chest_base(grid, 13, 35, 31, 39)
        
        # Deep open gullet (Y=20..30, X=14..34)
        for y in range(20, 31):
            for x in range(14, 35):
                col = "G" if y >= 28 else "X"
                set_p(grid, x, y, col)
                
        # Menacing red & amber eyes
        set_p(grid, 19, 24, "E")
        set_p(grid, 20, 24, "e")
        set_p(grid, 27, 24, "e")
        set_p(grid, 28, 24, "E")
        
        # Lower Jaw Teeth
        lower_teeth = [
            (14, 29), (16, 28), (17, 29), (19, 28), (21, 29),
            (23, 28), (25, 29), (27, 28), (29, 29), (31, 28), (33, 29)
        ]
        for tx, ty in lower_teeth:
            set_p(grid, tx, ty, "T")
            
        # Rule 4.6: HINGE ROTATION - Lid tilted far back around rear hinge!
        # Lid vertical height is foreshortened to 6px (Y=16..21)
        for y in range(16, 22):
            for x in range(12, 37):
                if x in (12, 36) or y in (16, 21):
                    set_p(grid, x, y, "#")
                else:
                    if x in (15, 33):
                        set_p(grid, x, y, "Y" if y == 17 else "B")
                    elif y == 17:
                        set_p(grid, x, y, "H")
                    else:
                        set_p(grid, x, y, "M" if (x % 2 == 0) else "D")
                        
        # Upper Jaw Fangs hanging down from lid
        upper_teeth = [
            (14, 21), (16, 22), (18, 21), (22, 22),
            (26, 22), (30, 21), (32, 22), (34, 21)
        ]
        for tx, ty in upper_teeth:
            set_p(grid, tx, ty, "T")

        # Rule 4.7: GOLDEN LATCH PRESERVATION ON FRONT RIM OF TILTED LID!
        draw_golden_lock(grid, 24, 20)

        # 2 VISCOUS SALIVA FILAMENTS (Pinched thin to 1px in the middle)
        left_saliva = [
            (18, 22, "P"), (18, 23, "P"),
            (17, 24, "p"), (17, 25, "P"), # 1px pinched middle
            (17, 26, "P"),
            (17, 27, "p"), (17, 28, "P")
        ]
        for sx, sy, col in left_saliva:
            set_p(grid, sx, sy, col)
            
        right_saliva = [
            (30, 22, "P"), (30, 23, "P"),
            (31, 24, "p"), (31, 25, "P"), # 1px pinched middle
            (31, 26, "P"),
            (31, 27, "p"), (31, 28, "P")
        ]
        for sx, sy, col in right_saliva:
            set_p(grid, sx, sy, col)

    # -------------------------------------------------------------
    # FRAME 4: SNAP DOWN (Lid slams down, golden latch rushes down, saliva snaps)
    # -------------------------------------------------------------
    elif frame_num == 4:
        draw_shadow(grid, cx, 22, y_floor=40)
        draw_chest_base(grid, 13, 35, 31, 39)
        
        # Lid slammed down with Motion Smear (Y=25..31)
        for y in range(25, 31):
            for x in range(12, 37):
                if x in (12, 36) or y in (25, 30):
                    set_p(grid, x, y, "#")
                else:
                    if x in (15, 33):
                        set_p(grid, x, y, "Y")
                    elif y == 26:
                        set_p(grid, x, y, "H")
                    else:
                        set_p(grid, x, y, "M")
                        
        # Smear wind streaks above
        set_p(grid, 13, 23, "H")
        set_p(grid, 14, 22, "M")
        set_p(grid, 35, 23, "H")
        set_p(grid, 34, 22, "M")
        
        # Rule 4.7: Golden Latch slamming down
        draw_golden_lock(grid, 24, 30)
        
        # Snapped saliva droplets flying
        set_p(grid, 10, 26, "P")
        set_p(grid, 11, 28, "p")
        set_p(grid, 12, 31, "P")
        set_p(grid, 37, 26, "P")
        set_p(grid, 38, 28, "p")
        set_p(grid, 36, 31, "P")

    # -------------------------------------------------------------
    # FRAME 5: IMPACT SQUASH (Chest squashes 1-2px, latch squashes)
    # -------------------------------------------------------------
    elif frame_num == 5:
        draw_shadow(grid, cx, 26, y_floor=40)
        # Squashed Base (Y=32..39, X=12..36)
        draw_chest_base(grid, 12, 36, 32, 39, is_squash=True)
        # Squashed Lid (Y=26..32, X=11..37)
        for y in range(26, 33):
            for x in range(11, 38):
                if x in (11, 37) or y in (26, 32):
                    set_p(grid, x, y, "#")
                else:
                    if x in (14, 34):
                        set_p(grid, x, y, "Y" if y == 27 else "B")
                    elif y == 27:
                        set_p(grid, x, y, "H")
                    else:
                        set_p(grid, x, y, "M" if (x % 2 == 0) else "D")
                        
        # Rule 4.7: Golden Latch in squashed position
        draw_golden_lock(grid, 24, 32)
        set_p(grid, 10, 39, "p")
        set_p(grid, 38, 39, "p")

    # -------------------------------------------------------------
    # FRAME 6: RECOVERY (Restores to Frame 1 shape)
    # -------------------------------------------------------------
    elif frame_num == 6:
        draw_shadow(grid, cx, 22, y_floor=40)
        draw_chest_base(grid, 13, 35, 31, 39)
        for y in range(24, 31):
            for x in range(12, 37):
                if x in (12, 36) or y in (24, 30):
                    set_p(grid, x, y, "#")
                else:
                    if x in (15, 33):
                        set_p(grid, x, y, "Y" if y == 25 else "B")
                    elif y == 25:
                        set_p(grid, x, y, "H")
                    elif y == 29:
                        set_p(grid, x, y, "D")
                    else:
                        set_p(grid, x, y, "M" if (x % 3 != 0) else "D")
        # Rule 4.7: Golden Latch restored
        draw_golden_lock(grid, 24, 30)

    return grid

def main():
    frames = [build_mimic_frame(i) for i in range(1, 7)]
    
    print("--- VERIFICATION OF MIMIC CHEST SNAP CONSTRAINTS ---")
    
    # Check 1: Base Anchoring (Y=39 is strictly bottom across all frames)
    for idx, g in enumerate(frames):
        assert g[39][24] in ("#", "D", "K", "B", "Y"), f"Frame {idx+1}: Chest base missing at floor Y=39!"
        assert g[40][24] == "S", f"Frame {idx+1}: Contact shadow missing at Y=40!"
    print("Requirement 1 PASSED: Chest base firmly anchored to Y=39 with contact shadow 'S' at Y=40 across all frames!")
    
    # Check 2: Rule 4.7 - Golden Latch Preservation across ALL 6 FRAMES!
    for idx, g in enumerate(frames):
        # Must find yellow 'Y' around x=24 for the lock
        lock_y_pixels = [y for y in range(15, 35) if g[y][24] == "Y" or g[y][23] == "Y" or g[y][25] == "Y"]
        assert len(lock_y_pixels) > 0, f"Frame {idx+1}: Golden latch 'Y' missing!"
        print(f"Frame {idx+1}: Golden latch confirmed present at Y in {lock_y_pixels}!")
    print("Requirement 2 PASSED: Rule 4.7 (Attached Prop Continuity) strictly obeyed! Golden latch present across all 6 frames!")

    # Check 3: Rule 4.6 - Hinge Rotation in Frame 3 (Lid height foreshortened to 6-7px)
    f3 = frames[2]
    lid_y_span = [y for y in range(10, 25) if any(f3[y][x] == "#" for x in (12, 36))]
    lid_h = max(lid_y_span) - min(lid_y_span) + 1
    assert 5 <= lid_h <= 7, f"Frame 3: Lid height ({lid_h}px) must be foreshortened to 5-7px (Hinge Rotation)!"
    print(f"Requirement 3 PASSED: Rule 4.6 (Hinge Rotation) verified! Open lid height foreshortened to {lid_h}px!")

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
        img.save(f"test/mimic_chest_f{idx+1}.png")
        images.append(img)
        
    images[0].save(
        "test/mimic_chest_anim.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / 8),
        loop=0,
        disposal=2
    )
    print("Saved test/mimic_chest_f*.png and test/mimic_chest_anim.gif")

if __name__ == "__main__":
    main()
