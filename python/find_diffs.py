with open("build_clean_frames.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '("' in line and '",' in line:
        parts = line.strip().split('",')
        s = parts[0].strip().lstrip('("')
        w = int(parts[1].split(')')[0].strip())
        if len(s) != w:
            print(f"Line {i+1}: '{s}' len={len(s)}, target={w}, diff={w-len(s)}")
