import polish_tree
grid = polish_tree.grid

for y in range(58, 64):
    non_dots = [(x, grid[y][x]) for x in range(64) if grid[y][x] != "."]
    print(f"y={y}: min_x={non_dots[0][0] if non_dots else -1}, max_x={non_dots[-1][0] if non_dots else -1}")
    if y >= 61:
        print(f"y={y}: {[ch for x, ch in non_dots if x > 54]}")
