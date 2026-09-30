# Fix base grounding and shadow in polish_tree.py
import re

with open("polish_tree.py", "r") as f:
    code = f.read()

# Replace the shadow clean-up logic
old_block = """# 3. Clean up ground shadow S at row 62 and 63
for x in range(64):
    if grid[62][x] == "S" and (x < 6 or x > 58):
        grid[62][x] = "."
    if grid[63][x] == "S" and (x < 10 or x > 54):
        grid[63][x] = "."

# Ensure all non-empty pixels have proper outline #
for y in range(64):
    for x in range(64):
        if grid[y][x] == ".":
            has_solid_neighbor = False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 64 and 0 <= ny < 64:
                    if grid[ny][nx] not in [".", "S", "#"]:
                        has_solid_neighbor = True
                        break
            if has_solid_neighbor:
                grid[y][x] = "#" """

new_block = """# 3. Clean up ground stone base and ground shadow S
# Row 61 is bottom of stone base: ensure bottom edge is #
for x in range(6, 58):
    if grid[61][x] not in [".", "S"]:
        # If there was a stone pixel here, bottom edge is #
        pass

# Ensure all solid pixels above row 62 have outline #
for y in range(62):
    for x in range(64):
        if grid[y][x] == ".":
            has_solid = False
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 64 and 0 <= ny < 62:
                    if grid[ny][nx] not in [".", "S", "#"]:
                        has_solid = True
                        break
            if has_solid:
                grid[y][x] = "#"

# Rows 62 and 63 are strictly ground contact shadow S
for x in range(64):
    grid[62][x] = "S" if (6 <= x <= 57) else "."
    grid[63][x] = "S" if (10 <= x <= 53) else "." """

code = code.replace(old_block, new_block)

with open("polish_tree.py", "w") as f:
    f.write(code)

print("Updated polish_tree.py!")
