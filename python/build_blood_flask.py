import os
from PIL import Image

PALETTE = {
    ".": None,
    "#": (26, 8, 20, 255),        # Viền tối sẫm (Near-black outline with deep wine tint)
    "S": (24, 8, 18, 130),        # Bóng tiếp đất (Ground contact shadow, Alpha 130)

    # Thủy tinh & Phản quang (Glass & Specular Highlights)
    "P": (255, 255, 255, 255),    # Vệt highlight trắng tinh khiết (Specular white highlight)
    "K": (208, 230, 236, 255),    # Viền kính trong suốt (Pale glass reflection)
    "J": (52, 70, 84, 255),       # Thành kính tối (Dark glass rim)

    # Nút chai bần (Cork stopper)
    "E": (180, 130, 80, 255),     # Nút bần sáng
    "U": (120, 80, 45, 255),      # Nút bần tối

    # Chất lỏng ma thuật đỏ phát sáng & Bọt khí (Glowing Blood/Crimson Liquid)
    "W": (255, 255, 255, 255),    # Tâm bọt khí & tia sáng cực mạnh (White hot sparks/bubble center)
    "Y": (255, 214, 90, 255),     # Vòng hào quang sáng vàng/cam rực rỡ
    "R": (255, 55, 75, 255),      # Màu đỏ neon phát sáng rực rỡ (Glowing neon red)
    "B": (196, 20, 56, 255),      # Màu đỏ thẫm ruby chính (Rich crimson liquid midtone)
    "Q": (110, 8, 36, 255),       # Vùng tối sâu chất lỏng (Deep wine liquid shadow)

    # Hắt sáng OSL lên rễ cây (Color bleed onto withered roots)
    "H": (240, 150, 75, 255),     # Điểm sáng thớ gỗ rễ đón OSL (Bright amber OSL ridge)
    "O": (216, 88, 40, 255),      # Gỗ rễ hắt sáng đỏ/cam rực (OSL highlight on roots)
    "T": (140, 44, 26, 255),      # Gỗ rễ chuyển tiếp ấm (OSL midtone on roots)

    # Rễ cây héo úa vặn xoắn (Withered roots normal tones)
    "M": (74, 34, 24, 255),       # Màu vỏ rễ chính (Withered dark root bark)
    "D": (40, 14, 16, 255),       # Rãnh xoắn sâu & vùng tối rễ (Deep root crevice & shadow)
    "V": (28, 8, 12, 255),        # Khe nứt sâu giữa các rễ (Deepest root fissure)
}

os.makedirs("test", exist_ok=True)

def row(s):
    assert len(s) == 48, f"Row length {len(s)} != 48: '{s}'"
    for ch in s:
        assert ch in PALETTE, f"Invalid character '{ch}' in '{s}'"
    return s

# ---------------- FRAME 1: Rest / Initial Bubble Rise ----------------
# Glass bulb has curved shape, floating specular streak P/K crossing empty space into liquid,
# liquid surface is a 3D ellipse, bottom of glass sphere is closed and resting in roots,
# roots are organic curved claws and braided corkscrew boughs with OSL red/orange glow!
f1 = [
    # 0..5: Empty air
    row("." * 48),
    row("." * 48),
    row("." * 48),
    row("." * 48),
    row("." * 48),
    row("." * 48),
    # 6..8: Cork stopper in bottle neck
    row("......................####......................"),
    row("......................#EEU#....................."),
    row("......................#EEU#....................."),
    # 9..10: Flared glass bottle lip
    row("....................########...................."),
    row("....................#PPKKKJ#...................."),
    # 11..13: Neck
    row(".....................#PKKJ#....................."),
    row(".....................#P..J#....................."),
    row(".....................#P..J#....................."),
    # 14..18: Flask shoulder expanding smoothly into sphere
    row("...................#PK....KJ#..................."),
    row(".................#PK........KJ#................."),
    row("...............#PK............KJ#..............."),
    row("..............#PK..............KJ#.............."),
    row(".............#PK................KJ#............."),
    # 19..20: Empty sphere interior above liquid with floating curved specular highlight P!
    row("............#PK...PP.............KJ#............"),
    row("............#K...PP...............J#............"),
    # 21..23: Liquid Surface Ellipse (Meniscus) - Quy tắc 3.2.2
    # Row 21: Back rim of liquid ellipse curving up; Highlight P crosses right into liquid!
    row("............#K..PPQQBBBBBBBBBBQQ...J#..........."),
    # Row 22: Front rim of liquid ellipse curving down, meniscus shine
    row("............#K.PPQBBBRRYYYYYYRRBBQ.J#..........."),
    # Row 23: Liquid body begins; Highlight P continues
    row("............#K.PQBRRYWWYYYYWWYRRBQ.J#..........."),
    # 24..30: Deep liquid body, glowing core, bubbles, and organic claw roots rising up sides
    row("............#K.PBRYYRRRRRRRRRRYYRB.J#..........."),
    row("............#K.PBYRRRRRRRRRRRRRRYB.J#..........."),
    row("............#K.KBYRRRRRRRRRRYRRRYB.J#..........."), # Bubble 2 (Y) at x=28
    row("............#K..BRRRRRRRRRRWRRRB..J#............"), # Bubble 2 center (W) at x=28
    row("............#K..QBRRRRRRRRYRRRB...J#............"),
    row(".........#..#K...QBRRWYRRRRRRBQ...J#..#........."), # Bubble 1 at x=19, Root claw tips!
    row("........#O#..#....QBRRYRRRRRBQ....#..#D#........"), # Root claws clasping glass flanks
    # 31..34: Bottom of spherical glass resting into roots; Strong OSL color bleed onto roots
    row("........#OO#.#....QBBRRRRRRRBQ....#.#MD#........"),
    row("........#HOO##....QQBBBBBBBBQQ....##OMD#........"), # Glass bottom rim curves closed into roots!
    row("........#THOM#.....##########.....#TOMD#........"),
    row(".........#THOM#..#OOOOOOOOOOOO#..#TOMD#........."), # Direct red-orange OSL color bleed O
    # 35..38: Organic curved withered roots braiding under the flask base (NO 45 DEGREE LINES!)
    row("..........#THOM##OTTTTTTTTTTTTO##TOMD#.........."),
    row("...........#THOMHOTTTTTTTTTTTTOHTOMD#...........") ,
    row("............#THOMDOTTTTTTTTTTTHOMMD#............"),
    row(".............#THOMDOTTTTTTTTTHOMMD#............."),
    # 39..42: Roots curving outward and downward with varying thickness
    row("............#THOMD#VMMTTTTMMV#DOMMD#............"),
    row("...........#THOMD#..VMMMMMMV..#DOMMD#..........."),
    row("..........#THMMD#...VMMMMMMV...#DOMMD#.........."),
    row(".........#TMMMD#....VMMMMMMV....#DOMMD#........."),
    # 43..44: Roots anchoring into ground (gốc to 4 px)
    row("........#MMMDD#.....VMMMMMMV.....#DDMMM#........"),
    row("........#MMMD#......#MMMMMM#......#DMMM#........"),
    # 45..46: Ground contact shadow S (Alpha 130)
    row(".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......."),
    row("..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS.........."),
    # 47
    row("." * 48),
]

# Frame 2: Bubble 1 rises, Bubble 2 rises, Bubble 3 appears at bottom
f2 = list(f1)
f2[24] = row("............#K.PBRYYRRRRRRRRRRYYRB.J#...........")
f2[25] = row("............#K.PBYRRRRRRRRRRYRRRYB.J#...........") # Bubble 2 rising to y=25
f2[26] = row("............#K.KBYRRRWYRRRRRWRRRRB.J#...........") # Bubble 1 at y=26 (x=17), Bubble 2 at y=26
f2[27] = row("............#K..BRRRYRRRRRRRRRRB..J#............")
f2[28] = row("............#K..QBRRRRRRRRRRRRB...J#............")
f2[29] = row(".........#..#K...QBRRRRRRRRRRBQ...J#..#.........")
f2[30] = row("........#O#..#....QBRRWWYRRRBQ....#..#D#........") # Bubble 3 (x=24) at bottom

# Frame 3: Bubble 1 reaches surface, Bubble 2 pops on surface rim!
f3 = list(f1)
f3[21] = row("............#K..PPQQBBBBBBBBWWQQ...J#...........") # Bubble 2 popping on surface (flash W)
f3[22] = row("............#K.PPQBBBRRYYYYYYPPBBQ.J#...........") # Surface spark P
f3[23] = row("............#K.PQBRWYWWYYYYWWYRRBQ.J#...........") # Bubble 1 at surface rim (W)
f3[24] = row("............#K.PBRYYRRRRRRRRRRYYRB.J#...........")
f3[25] = row("............#K.PBYRRRRRRRRRRRRRRYB.J#...........")
f3[26] = row("............#K.KBYRRRRRRWYRRRRRRYB.J#...........") # Bubble 3 rising to y=26 (x=24)
f3[27] = row("............#K..BRRRRRRYRRRRRRRB..J#............")
f3[28] = row("............#K..QBRRRRRRRRRRRRB...J#............")
f3[29] = row(".........#..#K...QBRRRRRRRRRRBQ...J#..#.........")
f3[30] = row("........#O#..#....QBRRRRRRRRBQ....#..#D#........")

# Frame 4: Bubble 3 reaches surface, surface ripple settles, core recharges
f4 = list(f1)
f4[21] = row("............#K..PPQQBBBBBBBBBBQQ...J#...........")
f4[22] = row("............#K.PPQBBBRRYYYWYYRRBBQ.J#...........") # Bubble 3 at surface
f4[23] = row("............#K.PQBRRYWWYYYYWWYRRBQ.J#...........")
f4[24] = row("............#K.PBRYYRRRRRRRRRRYYRB.J#...........")
f4[25] = row("............#K.PBYRRRRRRRRRRRRRRYB.J#...........")
f4[26] = row("............#K.KBYRRRRRRRRRRRRRRYB.J#...........")
f4[27] = row("............#K..BRRRRRRRRRRRRRRB..J#............")
f4[28] = row("............#K..QBRRRRRYRRRRRRB...J#............")
f4[29] = row(".........#..#K...QBRRRWWYRRRRBQ...J#..#.........") # New core recharge
f4[30] = row("........#O#..#....QBRRYRRRRRBQ....#..#D#........")

frames = [f1, f2, f3, f4]
print("All 4 frames defined successfully!")

# Render test images into test/ directory
imgs = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    for y, r_str in enumerate(fr):
        for x, ch in enumerate(r_str):
            col = PALETTE.get(ch)
            if col:
                img.putpixel((x, y), col)
    imgs.append(img)
    img.save(f"test/test_flask_frame_{idx+1}.png")

# Save animated GIF in test/
imgs[0].save("test/test_flask_anim.gif", save_all=True, append_images=imgs[1:], duration=125, loop=0)

# Save sheet in test/
sheet = Image.new("RGBA", (48 * 4, 48), (0, 0, 0, 0))
for i, im in enumerate(imgs):
    sheet.paste(im, (i * 48, 0))
sheet.save("test/test_flask_sheet.png")

# Also 4x zoom in test/
sheet4x = sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST)
sheet4x.save("test/test_flask_sheet_4x.png")

print("Generated test previews in test/ directory!")
