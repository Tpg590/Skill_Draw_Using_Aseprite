import math
from PIL import Image

W, H = 48, 48

colors = {
    ".": (0, 0, 0, 0),
    "W": (255, 255, 255, 255), # Pure white core (radiant energy)
    "H": (205, 250, 255, 255), # Soft cyan-white glow
    "A": (45, 240, 255, 255),  # Electric neon cyan
    "B": (0, 180, 235, 255),   # Vibrant mid cyan
    "C": (0, 115, 175, 255),   # Deep cyan
    "D": (15, 55, 95, 255),    # Outer navy outline
}

def build_centered_arc_slash():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # Outer curve (cutting boundary)
    P0 = (42.0, 6.0)
    P1 = (13.0, 11.0)
    P2 = (6.0, 42.0)
    
    # Inner curve (trailing boundary)
    Q0 = (42.0, 6.0)
    Q1 = (19.0, 17.0)
    Q2 = (6.0, 42.0)
    
    steps = 1200
    for s in range(steps + 1):
        t = s / steps
        # Outer point
        ox = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
        oy = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
        
        # Inner point
        ix = (1 - t)**2 * Q0[0] + 2 * (1 - t) * t * Q1[0] + t**2 * Q2[0]
        iy = (1 - t)**2 * Q0[1] + 2 * (1 - t) * t * Q1[1] + t**2 * Q2[1]
        
        seg_len = math.hypot(ix - ox, iy - oy)
        sub_steps = max(1, int(math.ceil(seg_len * 4)))
        
        for k in range(sub_steps + 1):
            u = k / sub_steps # 0 is outer curve, 1 is inner curve
            px = int(round(ox + (ix - ox) * u))
            py = int(round(oy + (iy - oy) * u))
            
            if not (0 <= px < W and 0 <= py < H):
                continue
                
            # Distance from center line (center is u = 0.5)
            # dist_from_center: 0 at center, 1 at boundaries
            dist_c = abs(u - 0.5) * 2.0
            
            # If segment is very thin (near ends), favor white/bright cyan
            if seg_len < 1.2:
                col = "W" if dist_c < 0.6 else "A"
            else:
                if dist_c <= 0.35:
                    col = "W" # Brilliant pure white core!
                elif dist_c <= 0.65:
                    col = "H" # Soft cyan-white
                elif dist_c <= 0.85:
                    col = "A" # Electric cyan
                elif dist_c <= 0.96:
                    col = "B" # Vibrant cyan
                else:
                    col = "C" # Deep cyan rim
                    
            grid[py][px] = col
            
    # Add crisp 1px outline D around the boundary
    outline_candidates = []
    for y in range(H):
        for x in range(W):
            if grid[y][x] != ".":
                continue
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H:
                    if grid[ny][nx] in ("W", "H", "A", "B", "C"):
                        outline_candidates.append((x, y))
                        break
                        
    for x, y in outline_candidates:
        grid[y][x] = "D"
        
    return grid

grid = build_centered_arc_slash()
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = colors.get(grid[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_centered_arc.png")
print("Saved test/test_centered_arc.png")
