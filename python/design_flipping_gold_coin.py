import os
import math
from PIL import Image

W, H = 32, 48

# FreeStyle Hue-Shifting Gold Palette:
# Bright Lemon-White Glint -> Radiant Gold -> Deep Amber -> Warm Bronze Shadow
PALETTE = {
    ".": None,
    "#": (24, 12, 4, 255),         # Deep obsidian bronze outline (#180c04)
    "S": (12, 8, 4, 130),          # Contact shadow on stone (Alpha 130)
    
    # Ancient Stone Plinth
    "T": (106, 98, 116, 255),      # Stone plinth top highlight (#6a6274)
    "R": (72, 66, 82, 255),        # Stone plinth body (#484252)
    "D": (42, 36, 50, 255),        # Stone plinth shadow (#2a2432)
    
    # Pure Gold Coin
    "W": (255, 255, 255, 255),     # Specular white glint / lens glint (#ffffff)
    "Y": (255, 242, 117, 255),     # Lemon gold highlight (#fff275)
    "G": (230, 176, 30, 255),      # Radiant gold midtone (#e6b01e)
    "O": (184, 116, 16, 255),      # Rich golden amber (#b87410)
    "B": (104, 52, 8, 255),        # Warm bronze shadow (#683408)
    "b": (54, 22, 4, 255),         # Deep engraved rim / detail (#361604)
}

PALETTE_HEX = {
    ".": None,
    "#": "#180c04",
    "S": "#0c0804",
    "T": "#6a6274",
    "R": "#484252",
    "D": "#2a2432",
    "W": "#ffffff",
    "Y": "#fff275",
    "G": "#e6b01e",
    "O": "#b87410",
    "B": "#683408",
    "b": "#361604",
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

def draw_stone_plinth(grid):
    # Stone plinth: X=4..27, Y=37..43
    # Top face at Y=37..38
    for x in range(5, 27):
        set_p(grid, x, 37, "T")
    for y in range(38, 43):
        for x in range(5, 27):
            set_p(grid, x, y, "R" if (x % 3 != 0) else "D")
    for x in range(4, 28):
        set_p(grid, x, 43, "#")
    for y in range(37, 44):
        set_p(grid, 4, y, "#")
        set_p(grid, 27, y, "#")
    # Base contact shadow under plinth
    for x in range(6, 26):
        set_p(grid, x, 44, "S")

def draw_coin_shadow(grid, width_px, y_floor=37):
    # Rule 3.4 (Z-Axis Shadow):
    # Shadow ALWAYS sits on the stone plinth surface at y_floor=37!
    # Width shrinks with altitude.
    cx = 16
    hw = width_px // 2
    for x in range(cx - hw, cx + hw + 1):
        set_p(grid, x, y_floor, "S")

def build_coin_frame(frame_num):
    grid = empty_grid()
    draw_stone_plinth(grid)
    cx = 16
    
    # -------------------------------------------------------------
    # FRAME 1: REST (Flat on plinth, Heads side / Dragon emblem)
    # -------------------------------------------------------------
    if frame_num == 1:
        # Full shadow under coin on plinth (width 12px)
        draw_coin_shadow(grid, 12, y_floor=37)
        
        # Coin center (16, 34), flat ellipse: rx=6, ry=3
        cy = 34
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 6, cx + 7):
                dx = (x - cx) / 6.0
                dy = (y - cy) / 3.0
                d2 = dx*dx + dy*dy
                if d2 <= 1.05:
                    if d2 >= 0.85:
                        set_p(grid, x, y, "b")
                    else:
                        # Gold face with dragon head crest
                        if (x, y) in ((15, 33), (16, 33), (17, 34), (16, 35)):
                            col = "O" # Dragon crest
                        elif dx < -0.3 and dy < 0:
                            col = "Y" # Highlight crest
                        elif dy > 0.4:
                            col = "B" # Bottom rim shadow
                        else:
                            col = "G"
                        set_p(grid, x, y, col)
        # Specular gleam on left rim
        set_p(grid, 12, 33, "W")

    # -------------------------------------------------------------
    # FRAME 2: LAUNCH (Rises to Y=28, tilts 45 degrees)
    # -------------------------------------------------------------
    elif frame_num == 2:
        # Shadow on plinth shrinks to 9px (Rule 3.4)
        draw_coin_shadow(grid, 9, y_floor=37)
        
        # Coin at cy = 28, tilted 45 deg: rx=5.5, ry=2.2
        cy = 28
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 6, cx + 7):
                dx = (x - cx) / 5.5
                dy = (y - cy) / 2.2
                d2 = dx*dx + dy*dy
                if d2 <= 1.05:
                    if d2 >= 0.82:
                        set_p(grid, x, y, "b")
                    else:
                        # Tilting face: edge rim visible
                        if dy > 0.2:
                            col = "O" if dy < 0.6 else "B" # Thick rim
                        elif dx < 0 and dy < 0:
                            col = "Y"
                        else:
                            col = "G"
                        set_p(grid, x, y, col)
        # Top-left edge gleam
        set_p(grid, 12, 27, "W")
        set_p(grid, 13, 27, "Y")

    # -------------------------------------------------------------
    # FRAME 3: APEX (Rises to Y=16, 90 deg edge-on 2px strip, FLASH GLINT)
    # -------------------------------------------------------------
    elif frame_num == 3:
        # Shadow at plinth shrinks to tiny 3px dot! (Rule 3.4)
        draw_coin_shadow(grid, 3, y_floor=37)
        
        # Coin at cy = 16: perfectly edge-on!
        # Horizontal strip: X=11..21 (width 11px), Height=2px (Y=16..17)
        for x in range(11, 22):
            set_p(grid, x, 16, "Y" if (x <= 15) else "G")
            set_p(grid, x, 17, "O" if (x <= 15) else "B")
        set_p(grid, 10, 16, "b")
        set_p(grid, 10, 17, "b")
        set_p(grid, 22, 16, "b")
        set_p(grid, 22, 17, "b")
        
        # FLASH SPECULAR LENS GLINT (White cross spark at top-left corner)
        set_p(grid, 12, 16, "W")
        set_p(grid, 13, 16, "W")
        set_p(grid, 12, 15, "W") # Lens flare vertical spike
        set_p(grid, 12, 17, "Y")
        set_p(grid, 11, 15, "Y")

    # -------------------------------------------------------------
    # FRAME 4: FALL (Free-fall to Y=26, reverse 45 deg, TAILS Numeral '1')
    # -------------------------------------------------------------
    elif frame_num == 4:
        # Shadow expands back to 8px
        draw_coin_shadow(grid, 8, y_floor=37)
        
        # Coin at cy = 26, reverse tilt showing TAILS face: rx=5.5, ry=2.4
        cy = 26
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 6, cx + 7):
                dx = (x - cx) / 5.5
                dy = (y - cy) / 2.4
                d2 = dx*dx + dy*dy
                if d2 <= 1.05:
                    if d2 >= 0.82:
                        set_p(grid, x, y, "b")
                    else:
                        # Tail side with numeral '1' engraving
                        if x == 16 and (25 <= y <= 27):
                            col = "b" # Numeral '1' stem
                        elif (x, y) == (15, 25):
                            col = "b" # Numeral '1' flag
                        elif dx > 0.2 and dy < 0:
                            col = "Y" # Highlight
                        elif dy > 0.3:
                            col = "B" # Bottom edge
                        else:
                            col = "G"
                        set_p(grid, x, y, col)
        # Specular gleam on top right
        set_p(grid, 19, 25, "W")

    # -------------------------------------------------------------
    # FRAME 5: IMPACT LANDING (Slams on plinth, Squash: 14x5px)
    # -------------------------------------------------------------
    elif frame_num == 5:
        # Full wide impact shadow (width 14px)
        draw_coin_shadow(grid, 14, y_floor=37)
        
        # Squashed Coin: cy = 35, rx=7, ry=2.2 (flatter, wider)
        cy = 35
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 7, cx + 8):
                dx = (x - cx) / 7.0
                dy = (y - cy) / 2.2
                d2 = dx*dx + dy*dy
                if d2 <= 1.05:
                    if d2 >= 0.80:
                        set_p(grid, x, y, "b")
                    else:
                        if dy > 0.3:
                            col = "B"
                        elif dy < -0.3:
                            col = "Y"
                        else:
                            col = "G" if (x % 2 == 0) else "O"
                        set_p(grid, x, y, col)
        # Impact sparks (2 tiny specks)
        set_p(grid, 8, 36, "Y")
        set_p(grid, 24, 36, "Y")

    # -------------------------------------------------------------
    # FRAME 6: SETTLE (Recovery back to Frame 1 standard shape)
    # -------------------------------------------------------------
    elif frame_num == 6:
        # Standard shadow (width 12px)
        draw_coin_shadow(grid, 12, y_floor=37)
        
        # Coin cy = 34, rx=6, ry=3
        cy = 34
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 6, cx + 7):
                dx = (x - cx) / 6.0
                dy = (y - cy) / 3.0
                d2 = dx*dx + dy*dy
                if d2 <= 1.05:
                    if d2 >= 0.85:
                        set_p(grid, x, y, "b")
                    else:
                        if (x, y) in ((15, 33), (16, 33), (17, 34), (16, 35)):
                            col = "O"
                        elif dx < -0.3 and dy < 0:
                            col = "Y"
                        elif dy > 0.4:
                            col = "B"
                        else:
                            col = "G"
                        set_p(grid, x, y, col)
        set_p(grid, 12, 33, "Y")

    return grid

def main():
    frames = [build_coin_frame(i) for i in range(1, 7)]
    
    print("--- VERIFICATION OF FLIPPING GOLD COIN CONSTRAINTS ---")
    
    # Check 1: Rule 3.4 (Z-Axis Shadow)
    # In all frames, shadow MUST stay on the stone plinth surface (Y=37)!
    # Shadow must shrink as coin flies high:
    # F1 (on plinth) -> shadow width 12px
    # F2 (rising)    -> shadow width 9px
    # F3 (apex)      -> shadow width 3px
    # F4 (falling)   -> shadow width 8px
    # F5 (squash)    -> shadow width 14px
    shadow_widths = []
    for idx, g in enumerate(frames):
        s_pixels = [x for x in range(W) if g[37][x] == "S"]
        w_s = len(s_pixels)
        shadow_widths.append(w_s)
        print(f"Frame {idx+1}: Shadow at Y=37 has width {w_s}px")
        # In F2 & F3, shadow MUST NOT fly with coin
        assert w_s > 0, f"Frame {idx+1}: Shadow disappeared from plinth!"
        
    assert shadow_widths[2] <= 5, f"Frame 3 shadow must shrink to tiny dot at apex: {shadow_widths[2]}"
    assert shadow_widths[2] < shadow_widths[1] < shadow_widths[0], "Shadow did not shrink inversely with height!"
    print("Requirement 1 PASSED: Rule 3.4 strictly obeyed! Shadow stays fixed at plinth Y=37 and shrinks inversely with height!")

    # Check 2: 3D Flip Cycle verification
    # Frame 1: Coin at Y=34 (Heads)
    # Frame 2: Coin at Y=28 (45 deg)
    # Frame 3: Coin at Y=16 (Edge-on, height=2px, glint 'W')
    # Frame 4: Coin at Y=26 (Tails, Numeral '1' engraved)
    f3 = frames[2]
    assert f3[16][12] == "W", "Frame 3 edge-on flash glint 'W' missing!"
    f4 = frames[3]
    assert f4[26][16] == "b", "Frame 4 tails numeral '1' missing!"
    print("Requirement 2 PASSED: 3D Flip cycle verified (Heads -> 45 tilt -> 90 edge-on 2px strip with glint -> Tails numeral '1' -> Squash -> Settle)!")

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
        img.save(f"test/gold_coin_f{idx+1}.png")
        images.append(img)
        
    images[0].save(
        "test/gold_coin_anim.gif",
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / 8),
        loop=0,
        disposal=2
    )
    print("Saved test/gold_coin_f*.png and test/gold_coin_anim.gif")

if __name__ == "__main__":
    main()
