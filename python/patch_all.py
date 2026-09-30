with open("build_clean_frames.py", "r") as f:
    text = f.read()

text = text.replace('"#CCCCCDDDDDDDB#"', '"#CCCCCDDDDDDB#"')
text = text.replace('"#CCCDDDDDDDDDB#"', '"#CCCDDDDDDDDB#"')
text = text.replace('"#DDDDDDDDDDDDB#"', '"#DDDDDDDDDDDB#"')
text = text.replace('"#DDDVVVVVDDD#"', '"#DDDVVVVDDD#"')
text = text.replace('"#DDVVVVVDD#"', '"#DDVVVVDD#"')
text = text.replace('"#PPHAAAAAAAAAAAAABBB#"', '"#PPHAAAAAAAAAAAABBB#"')
text = text.replace('"#CCCCCCCCCDDDDDDDDDD#"', '"#CCCCCCCCCDDDDDDDDDDD#"')
text = text.replace('"#CCCCCDDDDDDDDDDDDDD#"', '"#CCCCCDDDDDDDDDDDDDDD#"')

with open("build_clean_frames.py", "w") as f:
    f.write(text)

print("build_clean_frames.py fully patched!")
