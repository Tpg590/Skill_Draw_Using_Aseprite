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

# ----------------- FRAME 1 (Rest) -----------------
# On ground: y = 24..43 (Height 20, Width 28)
# Core: rows 32..35
f1_body = [
    ("######", 6),
    ("##AAAAAA##", 10),
    ("#PPAHAAAAAAAB#", 14),
    ("#PPHAAAAAAAAAABBB#", 18),
    ("#PHAAAAAAAAAAAAABBB#", 20),
    ("#HAAAAAAAAGGGGAAAAAAB#", 22),
    ("#AAAAAAAAAGYYYYGAAAAABB#", 24),
    ("#AAAAAAAAAGYYYYYYGAAAABBB#", 26),
    ("#AAAAAAAAGYYWWYYGAAAABBBB#", 26),
    ("#AAAAAAAAGYYWWYYGAAAABBBB#", 26),
    ("#BBAAAAAGYYYYYYGAAAABBBBBBB#", 28),
    ("#BBBAAAAAGGGGGGAAAABBBBBBCB#", 28),
    ("#BBBBAAAAAAAAAAAAABBBBCCCCC#", 28),
    ("#BBBBBBBBBBBBBCCCCCCCBBCDDB#", 28),
    ("#BBBCCCCCCCCCCCCCCBDDDDDDDB#", 28),
    ("#CCCCCCCCCCCCCCDDDDDDDDDD#", 26),
    ("#CCCCCDDDDDDDDDDDDDDDDDDD#", 26),
    ("#DDDDDDDDDDDDDDDDDDDDDDDD#", 26),
    ("#DDDDDDVVVVVVVVDDDDDDDD#", 24),
    ("######################", 22),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSS", 28),
    ("SSSSSSSSSSSSSSSSSSSSSSSS", 24),
    ("SSSSSSSSSSSSSSSSSS", 18),
]
f1 = ["." * 48] * 24 + [center(s, w) for s, w in f1_body] + ["." * 48]
assert len(f1) == 48

# ----------------- FRAME 2 (Squash) -----------------
# Squashed flat: y = 32..43 (Height 12, Width 36)
# Smooth top curve: 12 -> 20 -> 26 -> 32 -> 36
# Core: compressed flat horizontally at rows 38..39
f2_body = [
    ("############", 12),
    ("##AAAAAAHHAAAAAAAA##", 20),
    ("#PPAAHAAAAAAAAAAAAAAAAABB#", 26),
    ("#PPHAAAAAAAGGGGGGGGAAAAAABBBB#", 30),
    ("#PHAAAAAAGGGYYYYYYYYGGGGAAAABBBBB#", 34),
    ("#HAAAAAAGYYYYWWWWWWYYYYGAAAAABBBBBB#", 36),
    ("#AAAAAAAGYYYYWWWWWWWWYYYYGAAABBBBBB#", 36),
    ("#BBAAAAGYYYYWWWWWWWWWWYYYYGAABBBBBB#", 36),
    ("#BBBAAAGYYYYWWWWWWWWWWYYYYGAACCCCCC#", 36),
    ("#BBBBAAAAGGGYYYYYYYYGGGAACCCCCCCB#", 34),
    ("#BBBBBAAAAAGGGGGGGGAACCCCCCCCCDDB#", 34),
    ("#BBBBBCCCCCCCCCCCCCCCDDDDDDDDDB#", 32),
    ("##############################", 30),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", 38),
    ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", 32),
    ("SSSSSSSSSSSSSSSSSSSSSS", 22),
]
f2 = ["." * 48] * 31 + [center(s, w) for s, w in f2_body] + ["." * 48]
assert len(f2) == 48

# ----------------- FRAME 3 (Stretch / Apex) -----------------
# Launched high: y = 8..37 (Height 30, Width 18)
# Slime airborne: 6 empty rows beneath it
# Shadow on ground (rows 44..45) smaller/detached
f3_body = [
    ("####", 4),
    ("##AAAA##", 8),
    ("#PPAHAAABAA#", 12),
    ("#PPHAAAAAABBA#", 14),
    ("#PHAAAAAAAAAAAB#", 16),
    ("#HAAAAAAAAAAAAB#", 16),
    ("#AAAAAAAAAAAAAB#", 16),
    ("#AAAAAGGGGGAAAABB#", 18),
    ("#AAAAGYYYYYGAAAAB#", 18),
    ("#AAAGYYYYYYYGAAAB#", 18),
    ("#AAAGYYWWYYYGAAAB#", 18),
    ("#AAAGYYWWYYYGAAAB#", 18),
    ("#BAAGYYWWYYGAABBB#", 18),
    ("#BAAGYYWWYYGAABBB#", 18),
    ("#BAAGYYYYYYGAABBB#", 18),
    ("#BAAAGGGGGGACBBBB#", 18),
    ("#BBAAAAACCCCBBB#", 16),
    ("#BBBAAAACCCCCBB#", 16),
    ("#BBBBAACCCCCCCB#", 16),
    ("#BBBBCCCCCCCCDB#", 16),
    ("#BBBCCCCCCCCCDB#", 16),
    ("#BBCCCCCCCCCDDB#", 16),
    ("#BCCCCCCBDDDD#", 14),
    ("#CCCCCDDDDDDB#", 14),
    ("#CCCDDDDDDDDB#", 14),
    ("#DDDDDDDDDDDB#", 14),
    ("#DDDDDDDDDD#", 12),
    ("#DDDVVVVDDD#", 12),
    ("#DDVVVVDD#", 10),
    ("######", 6),
]
f3_shadow = [
    ("SSSSSSSSSSSSSS", 14),
    ("SSSSSSSSSS", 10),
]
f3 = ["." * 48] * 8 + [center(s, w) for s, w in f3_body] + ["." * 48] * 6 + [center(s, w) for s, w in f3_shadow] + ["." * 48] * 2
assert len(f3) == 48

# ----------------- FRAME 4 (Fall / Descent) -----------------
# Falling down in mid-air: y = 17..40 (Height 24, Width 26)
# 3 empty rows (rows 41..43) between descending slime and ground!
# Shadow on ground (rows 44..46) expanding back
f4_body = [
    ("########", 8),
    ("##AAAAAAHH##", 12),
    ("#PPAHAAAAAAAAAA#", 16),
    ("#PPHAAAAAAAAAAAABBB#", 20),
    ("#PHAAAAAAAAAAAAAAAABB#", 22),
    ("#HAAAAAAAAGGGGAAAAAAABB#", 24),
    ("#AAAAAAAAAGYYYYGAAAAABB#", 24),
    ("#AAAAAAAAGYYYYYYGAAAABB#", 24),
    ("#AAAAAAAAGYYWWYYGAAAABBBB#", 26),
    ("#BAAAAAAAGYYWWYYGAAAABBBB#", 26),
    ("#BBAAAAAAGYYWWYYGAAACBBBB#", 26),
    ("#BBBAAAAAGYYYYYYGAAACBBBB#", 26),
    ("#BBBBAAAAAGYYYYGAACCCCCCB#", 26),
    ("#BBBBBAAAAGGGGAAACCCCCCCB#", 26),
    ("#BBBBBBBAAAAAAACCCCCCBCBB#", 26),
    ("#BBBBBBBCCCCCCBDDDDDDDB#", 24),
    ("#BBBBBCCCCCCCCBDDDDDDDB#", 24),
    ("#BBCCCCCCCCCCBDDDDDDDDB#", 24),
    ("#CCCCCCCCCCCDDDDDDDDDDB#", 24),
    ("#CCCCCCCCCDDDDDDDDDDD#", 22),
    ("#CCCCCDDDDDDDDDDDDDDD#", 22),
    ("#DDDDDDDDDDDDDDDDDD#", 20),
    ("#DDDDDVVVVVVDDD#", 16),
    ("############", 12),
]
f4_shadow = [
    ("SSSSSSSSSSSSSSSSSSSSSSSS", 24),
    ("SSSSSSSSSSSSSSSSSSSS", 20),
    ("SSSSSSSSSSSSSS", 14),
]
# 17 empty rows (0..16) + 24 body rows (17..40) + 3 air rows (41..43) + 3 shadow rows (44..46) + 1 bottom row (47) = 48
f4 = ["." * 48] * 17 + [center(s, w) for s, w in f4_body] + ["." * 48] * 3 + [center(s, w) for s, w in f4_shadow] + ["." * 48]
assert len(f4) == 48

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

imgs[0].save("test_slime_anim.gif", save_all=True, append_images=imgs[1:], duration=125, loop=0)

sheet = Image.new("RGBA", (48 * 4, 48), (0, 0, 0, 0))
for i, img in enumerate(imgs):
    sheet.paste(img, (i * 48, 0))
sheet.save("test_slime_sheet.png")

# Also 4x zoomed
sheet4x = sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST)
sheet4x.save("test_slime_sheet_4x.png")

print("Refined frames generated successfully!")
