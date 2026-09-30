with open("python/build_blood_flask.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    stripped = line.rstrip()
    if 'row("' in line and stripped.endswith('",'):
        line = stripped[:-2] + '"),\n'
    new_lines.append(line)

with open("python/build_blood_flask.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Fixed row parenthesis!")
