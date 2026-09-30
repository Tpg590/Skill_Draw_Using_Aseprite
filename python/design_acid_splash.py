import os
from PIL import Image

W, H = 32, 32

PALETTE = {
    ".": (0, 0, 0, 0),          # Transparent
    "S": (16, 26, 20, 130),     # Ground contact shadow (Alpha 130)
    "#": (10, 34, 20, 255),     # Viền sẫm xanh thẫm sạch (#0a2214)
    "W": (250, 255, 170, 255),  # Phản quang trắng ngả vàng neon (#faffaa)
    "A": (216, 255, 54, 255),   # Sáng: Vàng chanh neon rực rỡ (#d8ff36)
    "B": (74, 224, 34, 255),    # Nền: Xanh lục độc quang (#4ae022)
    "C": (18, 120, 56, 255),    # Tối: Xanh ngọc lục bảo sâu (#127838)
    
    # Optional stone floor colors if tested
    "F1": (110, 118, 130, 255), # Stone highlight (#6e7682)
    "F2": (68, 74, 84, 255),    # Stone midtone (#444a54)
    "F3": (36, 40, 48, 255),    # Stone crevice (#242830)
}

def create_pure_sprite_frames():
    # 4 frames on transparent background with ground shadow S
    frames = [[["." for _ in range(W)] for _ in range(H)] for _ in range(4)]
    
    # Ground plane is at Y = 26 (y=26..28 for shadow S)
    # -------------------------------------------------------------
    # Frame 1: Fall (Rơi tự do - giọt lệ thuôn dài)
    # -------------------------------------------------------------
    f1 = frames[0]
    # Ground shadow below falling drop: compact ellipse awaiting impact
    for x in range(13, 19): f1[27][x] = "S"
    for x in range(14, 18): f1[28][x] = "S"
    
    # Teardrop: top y=6, bottom y=22 (height 17px)
    # y=6: tip
    f1[6][15] = "#"; f1[6][16] = "#"
    # y=7: tip highlight
    f1[7][14] = "#"; f1[7][15] = "W"; f1[7][16] = "A"; f1[7][17] = "#"
    # y=8..10: narrow stream
    for y in (8, 9, 10):
        f1[y][14] = "#"; f1[y][15] = "A"; f1[y][16] = "B"; f1[y][17] = "#"
    f1[8][15] = "W" # specular glint
    
    # y=11..13: expanding neck
    for y in (11, 12, 13):
        f1[y][13] = "#"; f1[y][14] = "A"; f1[y][15] = "B"; f1[y][16] = "B"; f1[y][17] = "C"; f1[y][18] = "#"
    f1[11][14] = "W"
    
    # y=14..15: body expanding
    for y in (14, 15):
        f1[y][12] = "#"; f1[y][13] = "A"; f1[y][14] = "A"; f1[y][15] = "B"; f1[y][16] = "B"; f1[y][17] = "C"; f1[y][18] = "C"; f1[y][19] = "#"
    f1[14][13] = "W"
    
    # y=16..19: bulbous circular drop bottom (width 10: x=11..20)
    for y in range(16, 20):
        f1[y][11] = "#"
        f1[y][12] = "A"
        f1[y][13] = "A"
        f1[y][14] = "B"
        f1[y][15] = "B"
        f1[y][16] = "B"
        f1[y][17] = "C"
        f1[y][18] = "C"
        f1[y][19] = "C"
        f1[y][20] = "#"
    f1[16][12] = "W"; f1[17][12] = "W"; f1[16][13] = "W"
    
    # y=20: rounding bottom (width 10)
    f1[20][11] = "#"
    for x in range(12, 15): f1[20][x] = "A"
    for x in range(15, 18): f1[20][x] = "B"
    for x in range(18, 20): f1[20][x] = "C"
    f1[20][20] = "#"
    
    # y=21: rounding bottom (width 8: x=12..19)
    f1[21][12] = "#"
    for x in range(13, 16): f1[21][x] = "B"
    for x in range(16, 19): f1[21][x] = "C"
    f1[21][19] = "#"
    
    # y=22: bottom cap (width 6: x=13..18)
    for x in range(13, 19): f1[22][x] = "#"

    # -------------------------------------------------------------
    # Frame 2: Impact (Nén va đập - bẹp dí tẹt dày 2px, rộng 10-12px)
    # -------------------------------------------------------------
    f2 = frames[1]
    # Ground shadow under the pancake
    for x in range(8, 24): f2[26][x] = "S"
    for x in range(10, 22): f2[27][x] = "S"
    
    # Flattened pancake at y=24 and y=25 (dày 2px, rộng 12px: x=10..21)
    # Small upward rebound crest at center (y=23, width 6: x=13..18)
    f2[23][13] = "#"; f2[23][14] = "W"; f2[23][15] = "A"; f2[23][16] = "B"; f2[23][17] = "C"; f2[23][18] = "#"
    
    # y=24: upper layer of squashed puddle (x=10..21, width 12)
    f2[24][10] = "#"
    f2[24][11] = "A"; f2[24][12] = "W"; f2[24][13] = "W"; f2[24][14] = "A"; f2[24][15] = "A"
    f2[24][16] = "B"; f2[24][17] = "B"; f2[24][18] = "C"; f2[24][19] = "C"; f2[24][20] = "C"
    f2[24][21] = "#"
    
    # y=25: lower layer of squashed puddle (x=9..22, width 14 for rounded edge)
    f2[25][9] = "#"
    f2[25][10] = "A"; f2[25][11] = "A"; f2[25][12] = "A"; f2[25][13] = "A"
    f2[25][14] = "B"; f2[25][15] = "B"; f2[25][16] = "B"; f2[25][17] = "B"
    f2[25][18] = "C"; f2[25][19] = "C"; f2[25][20] = "C"; f2[25][21] = "C"
    f2[25][22] = "#"
    
    # Bottom outline at y=26 (x=10..21)
    for x in range(10, 22): f2[26][x] = "#"

    # -------------------------------------------------------------
    # Frame 3: Crown Splash (Vương miện bắn tóe + 2 giọt tách rời)
    # -------------------------------------------------------------
    f3 = frames[2]
    # Ground shadow under crown base
    for x in range(7, 25): f3[26][x] = "S"
    for x in range(9, 23): f3[27][x] = "S"
    
    # 2 Airborne droplets (1px each, flying upward at ballistic arcs)
    # Left droplet at (7, 13) with outline
    f3[12][7] = "#"
    f3[13][6] = "#"; f3[13][7] = "W"; f3[13][8] = "#"
    f3[14][7] = "#"
    
    # Right droplet at (24, 13) with outline
    f3[12][24] = "#"
    f3[13][23] = "#"; f3[13][24] = "A"; f3[13][25] = "#"
    f3[14][24] = "#"
    
    # Crown Spikes:
    # Outer Left Spire Tip at y=16 (x=8)
    f3[16][8] = "#"
    f3[17][7] = "#"; f3[17][8] = "W"; f3[17][9] = "#"
    f3[18][7] = "#"; f3[18][8] = "A"; f3[18][9] = "#"
    
    # Outer Right Spire Tip at y=16 (x=23)
    f3[16][23] = "#"
    f3[17][22] = "#"; f3[17][23] = "A"; f3[17][24] = "#"
    f3[18][22] = "#"; f3[18][23] = "B"; f3[18][24] = "#"
    
    # Intermediate Scallops at y=19..20:
    # y=19:
    f3[19][7] = "#"; f3[19][8] = "W"; f3[19][9] = "A"; f3[19][10] = "#"
    f3[19][12] = "#"; f3[19][13] = "W"; f3[19][14] = "#" # mid-left prong
    f3[19][17] = "#"; f3[19][18] = "A"; f3[19][19] = "#" # mid-right prong
    f3[19][21] = "#"; f3[19][22] = "B"; f3[19][23] = "C"; f3[19][24] = "#"
    
    # y=20:
    f3[20][7] = "#"; f3[20][8] = "A"; f3[20][9] = "A"; f3[20][10] = "B"; f3[20][11] = "#"
    f3[20][12] = "#"; f3[20][13] = "A"; f3[20][14] = "B"; f3[20][15] = "#"
    f3[20][16] = "#"; f3[20][17] = "B"; f3[20][18] = "C"; f3[20][19] = "#"
    f3[20][20] = "#"; f3[20][21] = "B"; f3[20][22] = "C"; f3[20][23] = "C"; f3[20][24] = "#"
    
    # y=21: Center dips down! (lõm ở giữa tại x=15..16)
    f3[21][7] = "#"
    for x in range(8, 12): f3[21][x] = "A"
    f3[21][12] = "B"; f3[21][13] = "B"; f3[21][14] = "#"
    f3[21][15] = "."; f3[21][16] = "#" # central dip crater
    f3[21][17] = "B"; f3[21][18] = "C"; f3[21][19] = "C"
    for x in range(20, 24): f3[21][x] = "C"
    f3[21][24] = "#"
    
    # y=22: Crown bowl connects across
    f3[22][7] = "#"
    for x in range(8, 12): f3[22][x] = "A"
    for x in range(12, 17): f3[22][x] = "B"
    for x in range(17, 24): f3[22][x] = "C"
    f3[22][24] = "#"
    
    # y=23: Crown bowl
    f3[23][8] = "#"
    for x in range(9, 13): f3[23][x] = "A"
    for x in range(13, 18): f3[23][x] = "B"
    for x in range(18, 23): f3[23][x] = "C"
    f3[23][23] = "#"
    
    # y=24: Crown base (width 16: x=8..23)
    f3[24][8] = "#"
    for x in range(9, 13): f3[24][x] = "A"
    for x in range(13, 18): f3[24][x] = "B"
    for x in range(18, 23): f3[24][x] = "C"
    f3[24][23] = "#"
    
    # y=25: Bottom base rim
    for x in range(9, 23): f3[25][x] = "#"

    # -------------------------------------------------------------
    # Frame 4: Ripple & Dissipate (Gợn sóng mỏng lan rộng dạng ellipse 3/4)
    # -------------------------------------------------------------
    f4 = frames[3]
    # 2 landing splash dots (droplets landed on the floor plane)
    f4[23][5] = "#"; f4[24][5] = "A"; f4[25][5] = "#"
    f4[23][26] = "#"; f4[24][26] = "C"; f4[25][26] = "#"
    
    # Main ripple ellipse (Top-Down 3/4, width 20, height 5)
    # y=23: top arc of ellipse (x=10..21)
    for x in range(10, 22): f4[23][x] = "#"
    
    # y=24: upper inner ellipse ring
    f4[24][7] = "#"; f4[24][8] = "#"; f4[24][9] = "W"
    for x in range(10, 14): f4[24][x] = "A"
    for x in range(14, 18): f4[24][x] = "B"
    for x in range(18, 22): f4[24][x] = "C"
    f4[24][22] = "C"; f4[24][23] = "#"; f4[24][24] = "#"
    
    # y=25: widest part of ellipse (x=6..25, width 20)
    # Rim outer edges are thick, center is hollow thin liquid film
    f4[25][6] = "#"
    f4[25][7] = "W"; f4[25][8] = "A"; f4[25][9] = "A"; f4[25][10] = "#"
    # Hollow center with thin water tint or transparent
    f4[25][11] = "S"; f4[25][12] = "S"; f4[25][13] = "S"; f4[25][14] = "S"
    f4[25][15] = "S"; f4[25][16] = "S"; f4[25][17] = "S"; f4[25][18] = "S"
    f4[25][19] = "S"; f4[25][20] = "#"
    f4[25][21] = "B"; f4[25][22] = "C"; f4[25][23] = "C"; f4[25][24] = "C"
    f4[25][25] = "#"
    
    # y=26: lower inner ellipse ring (x=7..24)
    f4[26][7] = "#"; f4[26][8] = "#"; f4[26][9] = "A"
    for x in range(10, 15): f4[26][x] = "B"
    for x in range(15, 21): f4[26][x] = "C"
    f4[26][21] = "C"; f4[26][22] = "C"; f4[26][23] = "#"; f4[26][24] = "#"
    
    # y=27: bottom arc of ellipse
    for x in range(10, 22): f4[27][x] = "#"
    
    # Soft shadow rim at y=28
    for x in range(12, 20): f4[28][x] = "S"

    return frames

pure_frames = create_pure_sprite_frames()

# Render pure frames
gif_frames = []
for idx, fr in enumerate(pure_frames):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            code = fr[y][x]
            if code in PALETTE:
                img.putpixel((x, y), PALETTE[code])
    img.resize((W * 8, H * 8), Image.NEAREST).save(f"python/acid_f{idx+1}.png")
    gif_frames.append(img.resize((W * 8, H * 8), Image.NEAREST))

w, h = gif_frames[0].size
sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
for i, gf in enumerate(gif_frames):
    sheet.paste(gf, (w * i, 0))
sheet.save("python/acid_sheet_pure.png")

gif_frames[0].save(
    "python/acid_anim_pure.gif",
    save_all=True,
    append_images=gif_frames[1:],
    duration=125, # 8 FPS = 125ms
    loop=0
)

print("Generated acid_sheet_pure.png and acid_anim_pure.gif")
