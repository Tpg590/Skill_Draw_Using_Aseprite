# Quick fix for lengths
import re

with open("build_clean_frames.py", "r") as f:
    code = f.read()

# Replace the 37-char line in f2 with 36-char
code = code.replace("#BBBAAAGYYYYWWWWWWWWYYYYGAAACCCCCCCC#", "#BBBAAAGYYYYWWWWWWWWYYYYGAAACCCCCCC#")

with open("build_clean_frames.py", "w") as f:
    f.write(code)

print("Replaced!")
