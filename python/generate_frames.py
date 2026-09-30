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

def center(s, target_w):
    assert len(s) == target_w, f"String '{s}' length {len(s)} != target_w {target_w}"
    margin = (48 - target_w) // 2
    res = "." * margin + s + "." * (48 - margin - target_w)
    assert len(res) == 48, f"Result length {len(res)} != 48"
    return res

# ----------------- FRAME 1 -----------------
# 24 empty rows: 0..23
f1_body = [
    ("######", 6),
    ("##AAAAAA##", 10),
    ("#PPAHAAAAAAAB#", 14),
    ("#PPHAAAAAAAAAABBB#", 18),
    ("#PHAAAAAAAAAAAAAABBB#", 20),
    ("#HAAAAAAAGGGGAAAAAAB#", 22),
    ("#AAAAAAAGYYYYGAAAAABB#", 24),
    ("#AAAAAAAGYYYYYYGAAAABB#", 26),
    ("#AAAAAAGYYWWYYGAAAABBB#", 26),
    ("#AAAAAAGYYWWYYGAAAABBB#", 26),
    ("#BAAAAAGYYYYYYGAAAABBBBB#", 28),
    ("#BBAAAAAGGGGGGAAAABBBBCB#", 28),
    ("#BBBAAAAAAAAAAAAABBBCCCC#", 28),
    ("#BBBBBBBBBBBBBCCCCCBBCDB#", 28),
    ("#BBBCCCCCCCCCCCCBDDDDDDB#", 28),
    ("#CCCCCCCCCCCCDDDDDDDD#", 26),
    ("#CCCCCDDDDDDDDDDDDDDD#", 26),
    ("#DDDDDDDDDDDDDDDDDDDD#", 26),
    ("#DDDDDVVVVVVVVDDDDDD#", 24),
    ("######################", 22),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSS", 28),
    ("SSSSSSSSSSSSSSSSSSSSSSSS", 24),
    ("SSSSSSSSSSSSSSSSSS", 18),
]
f1 = ["." * 48] * 24 + [center(s, w) for s, w in f1_body] + ["." * 48]
assert len(f1) == 48, f"f1 has {len(f1)} rows"

# ----------------- FRAME 2 -----------------
# 31 empty rows: 0..30
f2_body = [
    ("############", 12),
    ("##AAAAAAHHAAAAAAAA##", 20),
    ("#PPAAHAAAAAAAAAAAAAAAABB#", 26),
    ("#PPHAAAAAAAAAAAAAAAAAAAABBBB#", 30),
    ("#PHAAAAAAAGGGGGGGGGGAAAAAABBBB#", 34),
    ("#HAAAAAAGGGYYYYYYYYGGGGAAAABBBBB#", 36),
    ("#AAAAAAGYYYYWWWWWWYYYYGAAAABBBBB#", 36),
    ("#BAAAAGYYYYWWWWWWWWYYYYGAABBBBBB#", 36),
    ("#BBAAAGYYYYWWWWWWWWYYYYGAACCCCCC#", 36),
    ("#BBBAAAAGGGYYYYYYYYGGGAACCCCCCCB#", 34),
    ("#BBBBAAAAAGGGGGGGGAACCCCCCCCCDDB#", 34),
    ("#BBBBBCCCCCCCCCCCCCCCDDDDDDDDDB#", 32),
    ("##############################", 30),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", 38),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", 32),
    ("SSSSSSSSSSSSSSSSSSSSSS", 22),
]
f2 = ["." * 48] * 31 + [center(s, w) for s, w in f2_body] + ["." * 48]
assert len(f2) == 48, f"f2 has {len(f2)} rows"

# ----------------- FRAME 3 -----------------
# 8 empty rows: 0..7
f3_body = [
    ("####", 4),
    ("##AAAA##", 8),
    ("#PPAHAAABAA#", 12),
    ("#PPHAAAAAABBA#", 14),
    ("#PHAAAAAAAAAAAAB#", 16),
    ("#HAAAAAAAAAAAAAB#", 16),
    ("#AAAAAAAAAAAAAAB#", 16),
    ("#AAAAAAGGGGGAAAABB#", 18),
    ("#AAAAAGYYYYYGAAAAB#", 18),
    ("#AAAAGYYYYYYYGAAAB#", 18),
    ("#AAAAGYYWWYYYGAAAB#", 18),
    ("#AAAAGYYWWYYYGAAAB#", 18),
    ("#BAAAGYYWWYYGAABBB#", 18),
    ("#BAAAGYYWWYYGAABBB#", 18),
    ("#BBAAGYYYYYYGAABBB#", 18),
    ("#BBAAAGGGGGGACBBBB#", 18),
    ("#BBBAAAAACCCCBBB#", 16),
    ("#BBBBAAAACCCCCBB#", 16),
    ("#BBBBBAACCCCCCCB#", 16),
    ("#BBBBBCCCCCCCCDB#", 16),
    ("#BBBBCCCCCCCCCDB#", 16),
    ("#BBBCCCCCCCCCDDB#", 16),
    ("#BCCCCCCBDDDDB#", 14),
    ("#CCCCCDDDDDDDB#", 14),
    ("#CCCDDDDDDDDDB#", 14),
    ("#DDDDDDDDDDDDB#", 14),
    ("#DDDDDDDDDDDD#", 12),
    ("#DDDVVVVVVDDD#", 12),
    ("#DDVVVVVVDD#", 10),
    ("######", 6),
]
# 6 rows empty under airborne slime (38..43)
# 2 rows shadow (44..45)
# 2 rows empty (46..47)
f3_shadow = [
    ("SSSSSSSSSSSSSS", 14),
    ("SSSSSSSSSS", 10),
]
f3 = ["." * 48] * 8 + [center(s, w) for s, w in f3_body] + ["." * 48] * 6 + [center(s, w) for s, w in f3_shadow] + ["." * 48] * 2
assert len(f3) == 48, f"f3 has {len(f3)} rows"

# ----------------- FRAME 4 -----------------
# 20 empty rows: 0..19
f4_body = [
    ("########", 8),
    ("##AAAAAAHH##", 12),
    ("#PPAHAAAAAAAAAA#", 16),
    ("#PPHAAAAAAAAAAAAAABB#", 20),
    ("#PHAAAAAAAAAAAAAAAABB#", 22),
    ("#HAAAAAAAAGGGGAAAAAAABB#", 24),
    ("#AAAAAAAAAGYYYYGAAAAABB#", 24),
    ("#AAAAAAAAGYYYYYYGAAAABB#", 24),
    ("#AAAAAAAAGYYWWYYGAAAABBB#", 26),
    ("#BAAAAAAAGYYWWYYGAAAABBB#", 26),
    ("#BBAAAAAAGYYWWYYGAAACBBB#", 26),
    ("#BBBAAAAAGYYYYYYGAAACBBB#", 26),
    ("#BBBBAAAAAGYYYYGAACCCCCB#", 26),
    ("#BBBBBAAAAGGGGAAACCCCCCC#", 26),
    ("#BBBBBBBAAAAAAACCCCCCBCB#", 26),
    ("#BBBBBBBCCCCCCBDDDDDDDB#", 24),
    ("#BBBBBCCCCCCCCBDDDDDDDB#", 24),
    ("#BBCCCCCCCCCCBDDDDDDDDB#", 24),
    ("#CCCCCCCCCCCDDDDDDDDDDB#", 24),
    ("#CCCCCCCCCDDDDDDDDDDDD#", 22),
    ("#CCCCCDDDDDDDDDDDDDDDD#", 22),
    ("#DDDDDDDDDDDDDDDDDDDD#", 20),
    ("#DDDDDVVVVVVDDDD#", 16),
    ("############", 12),
    ("SSSSSSSSSSSSSSSSSSSSSSSS", 24),
    ("SSSSSSSSSSSSSSSSSSSS", 20),
    ("SSSSSSSSSSSSSS", 14),
]
f4 = ["." * 48] * 20 + [center(s, w) for s, w in f4_body] + ["." * 48]
assert len(f4) == 48, f"f4 has {len(f4)} rows"

print("All frame rows successfully created!")

frames = [f1, f2, f3, f4]
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

print("Generated test images, test_slime_anim.gif, and test_slime_sheet.png!")
