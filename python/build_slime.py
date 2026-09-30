import os
from PIL import Image

PALETTE = {
    ".": None,
    "#": (24, 5, 41, 255),       # Deep dark plum/purple outline
    "S": (20, 5, 32, 130),       # Contact ground shadow (Alpha 130)
    # Translucent Jelly Body (Cyan to Deep Violet-Purple Hue-Shift)
    "P": (255, 255, 255, 255),   # Specular white gloss
    "H": (178, 255, 255, 255),   # Brilliant cyan specular halo
    "A": (69, 235, 252, 255),    # Vibrant bright cyan (Outer jelly)
    "B": (14, 169, 204, 255),    # Rich mid-cyan (Core jelly)
    "C": (8, 115, 150, 255),     # Deep teal mid-shadow
    "D": (59, 28, 97, 255),      # Hue-shifted deep purple body shadow
    "V": (33, 11, 56, 255),      # Deepest purple underside crevice
    # Inner Glowing Core & OSL Color Bleed
    "W": (255, 255, 255, 255),   # Pure white hot core center
    "Y": (185, 255, 255, 255),   # Neon cyan core halo
    "G": (103, 243, 255, 255),   # OSL color bleed radiating into jelly
}

def row_c(content):
    if not content:
        return "." * 48
    k = len(content)
    assert k % 2 == 0, f"content '{content}' length {k} is not even!"
    margin = 24 - (k // 2)
    line = "." * margin + content + "." * margin
    assert len(line) == 48, f"line length {len(line)} != 48"
    return line

# ---------------- FRAME 1: REST (Nghỉ) ----------------
# Height 20 (rows 24..43), Width 28 (rows 34..38)
f1 = ["." * 48] * 24 + [
    # 24 (len 6)
    row_c("######"),
    # 25 (len 10)
    row_c("##AAAAAA##"),
    # 26 (len 14)
    row_c("#PPAHAAAAAAAB#"),
    # 27 (len 18)
    row_c("#PPHAAAAAAAAAABB#"),
    # 28 (len 20)
    row_c("#PHAAAAAAAAAAAAAABB#"),
    # 29 (len 22)
    row_c("#HAAAAAAAGGGGAAAAABB#"),
    # 30 (len 24)
    row_c("#AAAAAAAGYYYYGAAAABB#"),
    # 31 (len 26)
    row_c("#AAAAAAAGYYYYYYGAAAABB#"),
    # 32 (len 26)
    row_c("#AAAAAAGYYWWYYGAAAABBB#"),
    # 33 (len 26)
    row_c("#AAAAAAGYYWWYYGAAAABBB#"),
    # 34 (len 28)
    row_c("#BAAAAAGYYYYYYGAAAABBBBB#"),
    # 35 (len 28)
    row_c("#BBAAAAAGGGGGGAAAABBBBCB#"),
    # 36 (len 28)
    row_c("#BBBAAAAAAAAAAAAABBBCCCC#"),
    # 37 (len 28)
    row_c("#BBBBBBBBBBBBBCCCCCBBCDB#"),
    # 38 (len 28)
    row_c("#BBBCCCCCCCCCCCCBDDDDDDB#"),
    # 39 (len 26)
    row_c("#CCCCCCCCCCCCDDDDDDDD#"),
    # 40 (len 26)
    row_c("#CCCCCDDDDDDDDDDDDDDD#"),
    # 41 (len 26)
    row_c("#DDDDDDDDDDDDDDDDDDDD#"),
    # 42 (len 24)
    row_c("#DDDDDVVVVVVVVDDDDDD#"),
    # 43 (len 22)
    row_c("######################"),
    # 44 (len 28)
    row_c("SSSSSSSSSSSSSSSSSSSSSSSSSSSS"),
    # 45 (len 24)
    row_c("SSSSSSSSSSSSSSSSSSSSSSSS"),
    # 46 (len 18)
    row_c("SSSSSSSSSSSSSSSSSS"),
    # 47
    "." * 48,
]

# ---------------- FRAME 2: SQUASH (Ép dẹp) ----------------
# Slime flattens hard: Height 13 (rows 31..43), Width 36 (rows 36..39)
f2 = ["." * 48] * 31 + [
    # 31 (len 12)
    row_c("############"),
    # 32 (len 20)
    row_c("##AAAAAAHHAAAAAAAA##"),
    # 33 (len 26)
    row_c("#PPAAHAAAAAAAAAAAAAAAABB#"),
    # 34 (len 30)
    row_c("#PPHAAAAAAAAAAAAAAAAAAAABBBB#"),
    # 35 (len 34)
    row_c("#PHAAAAAAAGGGGGGGGGGAAAAAABBBB#"),
    # 36 (len 36)
    row_c("#HAAAAAAGGGYYYYYYYYGGGGAAAABBBBB#"),
    # 37 (len 36)
    row_c("#AAAAAAGYYYYWWWWWWYYYYGAAAABBBBB#"),
    # 38 (len 36)
    row_c("#BAAAAGYYYYWWWWWWWWYYYYGAABBBBBB#"),
    # 39 (len 36)
    row_c("#BBAAAGYYYYWWWWWWWWYYYYGAACCCCCC#"),
    # 40 (len 34)
    row_c("#BBBAAAAGGGYYYYYYYYGGGAACCCCCCCB#"),
    # 41 (len 34)
    row_c("#BBBBAAAAAGGGGGGGGAACCCCCCCCCDDB#"),
    # 42 (len 32)
    row_c("#BBBBBCCCCCCCCCCCCCCCDDDDDDDDDB#"),
    # 43 (len 30)
    row_c("##############################"),
    # 44 (len 38)
    row_c("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"),
    # 45 (len 32)
    row_c("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"),
    # 46 (len 22)
    row_c("SSSSSSSSSSSSSSSSSSSSSS"),
    # 47
    "." * 48,
]

# ---------------- FRAME 3: STRETCH (Bật cao) ----------------
# Airborne high jump! Height 30 (rows 8..37), Width 18 (rows 15..23)
f3 = ["." * 48] * 8 + [
    # 8 (len 4)
    row_c("####"),
    # 9 (len 8)
    row_c("##AAAA##"),
    # 10 (len 12)
    row_c("#PPAHAAABAA#"),
    # 11 (len 14)
    row_c("#PPHAAAAAABBA#"),
    # 12 (len 16)
    row_c("#PHAAAAAAAAAAAAB#"),
    # 13 (len 16)
    row_c("#HAAAAAAAAAAAAAB#"),
    # 14 (len 16)
    row_c("#AAAAAAAAAAAAAAB#"),
    # 15 (len 18)
    row_c("#AAAAAAGGGGGAAAABB#"),
    # 16 (len 18)
    row_c("#AAAAAGYYYYYGAAAAB#"),
    # 17 (len 18)
    row_c("#AAAAGYYYYYYYGAAAB#"),
    # 18 (len 18)
    row_c("#AAAAGYYWWYYYGAAAB#"),
    # 19 (len 18)
    row_c("#AAAAGYYWWYYYGAAAB#"),
    # 20 (len 18)
    row_c("#BAAAGYYWWYYGAABBB#"),
    # 21 (len 18)
    row_c("#BAAAGYYWWYYGAABBB#"),
    # 22 (len 18)
    row_c("#BBAAGYYYYYYGAABBB#"),
    # 23 (len 18)
    row_c("#BBAAAGGGGGGACBBBB#"),
    # 24 (len 16)
    row_c("#BBBAAAAACCCCBBB#"),
    # 25 (len 16)
    row_c("#BBBBAAAACCCCCBB#"),
    # 26 (len 16)
    row_c("#BBBBBAACCCCCCCB#"),
    # 27 (len 16)
    row_c("#BBBBBCCCCCCCCDB#"),
    # 28 (len 16)
    row_c("#BBBBCCCCCCCCCDB#"),
    # 29 (len 16)
    row_c("#BBBCCCCCCCCCDDB#"),
    # 30 (len 14)
    row_c("#BCCCCCCBDDDDB#"),
    # 31 (len 14)
    row_c("#CCCCCDDDDDDDB#"),
    # 32 (len 14)
    row_c("#CCCDDDDDDDDDB#"),
    # 33 (len 14)
    row_c("#DDDDDDDDDDDDB#"),
    # 34 (len 12)
    row_c("#DDDDDDDDDDDD#"),
    # 35 (len 12)
    row_c("#DDDVVVVVVDDD#"),
    # 36 (len 10)
    row_c("#DDVVVVVVDD#"),
    # 37 (len 6)
    row_c("######"),
    # 38..43 (6 empty rows under airborne slime)
    "." * 48, "." * 48, "." * 48, "." * 48, "." * 48, "." * 48,
    # 44 (len 14)
    row_c("SSSSSSSSSSSSSS"),
    # 45 (len 10)
    row_c("SSSSSSSSSS"),
    # 46..47
    "." * 48, "." * 48,
]

# ---------------- FRAME 4: FALL (Rơi xuống) ----------------
# Descending back toward ground: Height 24 (rows 20..43), Width 26 (rows 28..34)
f4 = ["." * 48] * 20 + [
    # 20 (len 8)
    row_c("########"),
    # 21 (len 12)
    row_c("##AAAAAAHH##"),
    # 22 (len 16)
    row_c("#PPAHAAAAAAAAAA#"),
    # 23 (len 20)
    row_c("#PPHAAAAAAAAAAAAAABB#"),
    # 24 (len 22)
    row_c("#PHAAAAAAAAAAAAAAAABB#"),
    # 25 (len 24)
    row_c("#HAAAAAAAAGGGGAAAAAAABB#"),
    # 26 (len 24)
    row_c("#AAAAAAAAAGYYYYGAAAAABB#"),
    # 27 (len 24)
    row_c("#AAAAAAAAGYYYYYYGAAAABB#"),
    # 28 (len 26)
    row_c("#AAAAAAAAGYYWWYYGAAAABBB#"),
    # 29 (len 26)
    row_c("#BAAAAAAAGYYWWYYGAAAABBB#"),
    # 30 (len 26)
    row_c("#BBAAAAAAGYYWWYYGAAACBBB#"),
    # 31 (len 26)
    row_c("#BBBAAAAAGYYYYYYGAAACBBB#"),
    # 32 (len 26)
    row_c("#BBBBAAAAAGYYYYGAACCCCCB#"),
    # 33 (len 26)
    row_c("#BBBBBAAAAGGGGAAACCCCCCC#"),
    # 34 (len 26)
    row_c("#BBBBBBBAAAAAAACCCCCCBCB#"),
    # 35 (len 24)
    row_c("#BBBBBBBCCCCCCBDDDDDDDB#"),
    # 36 (len 24)
    row_c("#BBBBBCCCCCCCCBDDDDDDDB#"),
    # 37 (len 24)
    row_c("#BBCCCCCCCCCCBDDDDDDDDB#"),
    # 38 (len 24)
    row_c("#CCCCCCCCCCCDDDDDDDDDDB#"),
    # 39 (len 22)
    row_c("#CCCCCCCCCDDDDDDDDDDDD#"),
    # 40 (len 22)
    row_c("#CCCCCDDDDDDDDDDDDDDDD#"),
    # 41 (len 20)
    row_c("#DDDDDDDDDDDDDDDDDDDD#"),
    # 42 (len 16)
    row_c("#DDDDDVVVVVVDDDD#"),
    # 43 (len 12)
    row_c("############"),
    # 44 (len 24)
    row_c("SSSSSSSSSSSSSSSSSSSSSSSS"),
    # 45 (len 20)
    row_c("SSSSSSSSSSSSSSSSSSSS"),
    # 46 (len 14)
    row_c("SSSSSSSSSSSSSS"),
    # 47
    "." * 48,
]

frames = [f1, f2, f3, f4]
for idx, fr in enumerate(frames):
    assert len(fr) == 48, f"Frame {idx+1} has {len(fr)} rows, expected 48!"
    for y, row in enumerate(fr):
        assert len(row) == 48, f"Frame {idx+1}, row {y} has length {len(row)}, expected 48!"

print("All 4 frames strictly validated at 48x48!")

imgs = []
for idx, fr in enumerate(frames):
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    for y, row in enumerate(fr):
        for x, ch in enumerate(row):
            col = PALETTE.get(ch)
            if col:
                img.putpixel((x, y), col)
    imgs.append(img)
    img.save(f"test_frame_{idx+1}.png")

imgs[0].save("test_slime_anim.gif", save_all=True, append_images=imgs[1:], duration=125, loop=0)

sheet = Image.new("RGBA", (48 * 4, 48), (0, 0, 0, 0))
for i, img in enumerate(imgs):
    sheet.paste(img, (i * 48, 0))
sheet.save("test_slime_sheet.png")

print("Generated test_slime_anim.gif and test_slime_sheet.png!")
