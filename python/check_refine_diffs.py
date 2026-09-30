# Check all tuple lengths in refine_slime.py
with open("refine_slime.py", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '("' in line and '",' in line:
        parts = line.strip().split('",')
        s = parts[0].strip().lstrip('("')
        w_str = parts[1].split(')')[0].strip()
        try:
            w = int(w_str)
            if len(s) != w:
                print(f"Line {i+1}: '{s}' len={len(s)}, target={w}, diff={w-len(s)}")
        except ValueError:
            pass
