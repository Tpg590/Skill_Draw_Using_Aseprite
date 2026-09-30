from test_detailed_segments import frames, W, H, PALETTE_RGBA

def check_naked_pixels(grid):
    naked = []
    for y in range(H):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#", "E", "W", "Q", "T"): # OSL glow particles don't require black outline
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if grid[ny][nx] == ".":
                            naked.append((x, y, c, nx, ny))
    return naked

for i, g in enumerate(frames):
    n = check_naked_pixels(g)
    print(f"Frame {i+1} naked pixels: {len(n)}")
    if len(n) > 0:
        for item in n[:5]:
            print("  Naked:", item)
