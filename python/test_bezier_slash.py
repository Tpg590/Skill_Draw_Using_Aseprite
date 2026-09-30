import math
from PIL import Image

W, H = 48, 48

colors = {
    ".": (0, 0, 0, 0),
    "W": (255, 255, 255, 255), # Pure white core
    "H": (205, 250, 255, 255), # Cyan-white
    "A": (45, 240, 255, 255),  # Electric cyan
    "B": (0, 180, 235, 255),   # Vibrant mid cyan
    "C": (0, 115, 175, 255),   # Deep cyan
    "D": (15, 55, 95, 255),    # Outer navy outline
}

def build_bezier_slash():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # Outer curve (cutting edge)
    P0 = (42.0, 6.0)
    P1 = (13.0, 11.0)
    P2 = (6.0, 42.0)
    
    # Inner curve (trailing wake)
    Q0 = (42.0, 6.0)
    Q1 = (18.5, 16.5)
    Q2 = (6.0, 42.0)
    
    # High resolution sampling to fill solidly
    steps = 1000
    for s in range(steps + 1):
        t = s / steps
        # Outer point
        ox = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
        oy = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
        
        # Inner point
        ix = (1 - t)**2 * Q0[0] + 2 * (1 - t) * t * Q1[0] + t**2 * Q2[0]
        iy = (1 - t)**2 * Q0[1] + 2 * (1 - t) * t * Q1[1] + t**2 * Q2[1]
        
        # Segment from outer to inner
        seg_len = math.hypot(ix - ox, iy - oy)
        sub_steps = max(1, int(math.ceil(seg_len * 4)))
        
        for k in range(sub_steps + 1):
            u = k / sub_steps # 0 is outer (cutting edge), 1 is inner (trailing wake)
            px = int(round(ox + (ix - ox) * u))
            py = int(round(oy + (iy - oy) * u))
            
            if not (0 <= px < W and 0 <= py < H):
                continue
                
            # Color based on u and position
            if u <= 0.25:
                col = "W" # Brilliant pure white cutting edge
            elif u <= 0.45:
                col = "H" # Soft cyan-white
            elif u <= 0.75:
                col = "A" # Electric cyan
            elif u <= 0.92:
                col = "B" # Vibrant cyan
            else:
                col = "C" # Trailing deep cyan
                
            grid[py][px] = col
            
    # Add crisp 1px outline D around the outer boundary
    for y in range(H):
        for x in range(W):
            if grid[y][x] != ".":
                continue
            # Check 4-neighborhood
            has_solid_neighbor = False
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    if grid[ny][nx] in ("W", "H", "A", "B", "C"):
                        has_solid_neighbor = True
                        break
            if has_solid_neighbor:
                # Only add outline on the outer side and ends, keep trailing wake soft
                grid[y][x] = "D"
                
    return grid

grid = build_bezier_slash()
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = colors.get(grid[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_bezier_slash.png")
print("Saved test/test_bezier_slash.png")
