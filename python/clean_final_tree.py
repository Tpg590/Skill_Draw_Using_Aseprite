import copy
from PIL import Image
import polish_tree

grid = copy.deepcopy(polish_tree.grid)
PALETTE = polish_tree.PALETTE

# Row 61: Ensure the bottom of the stone foundation has a solid # outline along row 61
for x in range(64):
    if grid[60][x] not in [".", "S"] and grid[61][x] not in ["#", "."]:
        grid[61][x] = "#"

# Rows 62 and 63: MUST BE STRICTLY "." OR "S" (Alpha 130 shadow)
for x in range(64):
    grid[62][x] = "S" if (5 <= x <= 58) else "."
    grid[63][x] = "S" if (8 <= x <= 55) else "."

# Validate all rows are 64 chars
lines = ["".join(row) for row in grid]
assert len(lines) == 64
for idx, r in enumerate(lines):
    assert len(r) == 64, f"Row {idx} len {len(r)} != 64"

# Validate palette: only allowed characters
allowed_chars = set(PALETTE.keys())
for y, row in enumerate(lines):
    for x, ch in enumerate(row):
        assert ch in allowed_chars, f"Invalid char '{ch}' at ({x}, {y})"

print("clean_final_tree: All 64 rows strictly valid!")

# Render preview
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
for y in range(64):
    for x in range(64):
        ch = grid[y][x]
        col = PALETTE.get(ch)
        if col:
            img.putpixel((x, y), col)

img.save("clean_tree_1x.png")
img4x = img.resize((256, 256), Image.NEAREST)
img4x.save("clean_tree_4x.png")

print("Generated clean_tree_1x.png and clean_tree_4x.png!")
