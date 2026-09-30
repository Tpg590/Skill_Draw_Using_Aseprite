# Polishing script to perfect the Spooky Twisted Tree
import copy
from PIL import Image
import paint_full_masterpiece

grid = copy.deepcopy(paint_full_masterpiece.grid)
PALETTE = paint_full_masterpiece.PALETTE

# 1. Clean up foreground branch outline where it overlaps trunk
# The foreground branch travels from (28, 34) down-right to (48, 41)
# Top border of branch:
top_border = [
    (27, 33), (28, 33), (29, 33), (30, 34), (31, 34), (32, 34),
    (33, 35), (34, 35), (35, 35), (36, 36), (37, 36), (38, 36),
    (39, 37), (40, 37), (41, 37), (42, 38), (43, 38), (44, 38)
]
for x, y in top_border:
    grid[y][x] = "#"

# Bottom border of branch:
bot_border = [
    (28, 36), (29, 36), (30, 37), (31, 37), (32, 37), (33, 38),
    (34, 38), (35, 38), (36, 39), (37, 39), (38, 39), (39, 40),
    (40, 40), (41, 40), (42, 41), (43, 41), (44, 42), (45, 42)
]
for x, y in bot_border:
    grid[y][x] = "#"

# Cast shadow D and V on trunk directly below the bottom border
cast_shadow = [
    (29, 37), (30, 38), (31, 38), (32, 38), (33, 39), (34, 39),
    (35, 39), (36, 40), (37, 40), (38, 40), (39, 41), (40, 41),
    (41, 42), (42, 42), (43, 43), (44, 43),
    # Second row of cast shadow
    (30, 39), (31, 39), (32, 39), (33, 40), (34, 40), (35, 41),
    (36, 41), (37, 41), (38, 42), (39, 42), (40, 43), (41, 43)
]
for x, y in cast_shadow:
    if grid[y][x] not in [".", "S", "#"]:
        grid[y][x] = "V" if (x + y) % 3 == 0 else "D"

# Highlight H along top interior of foreground branch
fg_highlight = [
    (28, 34), (29, 34), (30, 35), (31, 35), (32, 35), (33, 36),
    (34, 36), (35, 36), (36, 37), (37, 37), (38, 37), (39, 38),
    (40, 38), (41, 38), (42, 39), (43, 39), (44, 39), (45, 40)
]
for x, y in fg_highlight:
    grid[y][x] = "H"

# 2. Enrich helical wood grain streaks across the trunk
# Streaks of 2-4 chars of H, M, D slanting at ~35 degrees
for y in range(25, 52):
    for x in range(23, 42):
        ch = grid[y][x]
        # Only adjust trunk wood pixels (not outline, not foreground branch)
        if ch in ["M", "D", "H"]:
            # Check if this pixel is inside the foreground branch area
            is_fg = (34 <= y <= 42) and (27 <= x <= 45) and ((x - 27) >= 1.5 * (y - 34) - 2) and ((x - 27) <= 1.5 * (y - 34) + 4)
            if not is_fg:
                # Diagonal helical coordinate
                val = (x - 1.2 * y + 100) % 14.0
                if val < 2.0:
                    grid[y][x] = "V"
                elif val < 4.5:
                    grid[y][x] = "H" if (x + y) % 4 != 0 else "M"
                elif val < 10.0:
                    grid[y][x] = "M" if (x * 2 + y) % 5 != 0 else "H"
                else:
                    grid[y][x] = "D"

# 3. Clean up ground shadow S at row 62 and 63
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
                grid[y][x] = "#"

# Validate all rows are 64 chars
lines = ["".join(row) for row in grid]
assert len(lines) == 64
for idx, r in enumerate(lines):
    assert len(r) == 64, f"Row {idx} len {len(r)} != 64"

print("Polished grid validated!")

# Render preview
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
for y in range(64):
    for x in range(64):
        ch = grid[y][x]
        col = PALETTE.get(ch)
        if col:
            img.putpixel((x, y), col)

img.save("polished_tree_1x.png")
img4x = img.resize((256, 256), Image.NEAREST)
img4x.save("polished_tree_4x.png")

print("Generated polished_tree_1x.png and polished_tree_4x.png!")
