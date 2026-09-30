import math
from PIL import Image

W, H = 48, 48

colors = {
    ".": (0, 0, 0, 0),
    "W": (255, 255, 255, 255), # Pure white core
    "H": (205, 250, 255, 255), # Cyan-white
    "A": (45, 240, 255, 255),  # Electric cyan
    "B": (0, 180, 235, 255),   # Mid cyan
    "C": (0, 115, 175, 255),   # Deep cyan
    "D": (15, 55, 95, 255),    # Magical navy outline
}

def rasterize_vfx_arc():
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # Parametric Leading Edge Curve (outer convex boundary)
    # Sweeps from Top-Right (42, 6) through (21, 14) to Bottom-Left (6, 42)
    p0 = (42.0, 7.0)
    p1 = (13.0, 11.0)
    p2 = (7.0, 42.0)
    
    num_samples = 800
    curve_pts = []
    for i in range(num_samples + 1):
        u = i / num_samples
        bx = (1 - u)**2 * p0[0] + 2 * (1 - u) * u * p1[0] + u**2 * p2[0]
        by = (1 - u)**2 * p0[1] + 2 * (1 - u) * u * p1[1] + u**2 * p2[1]
        
        # Derivative (tangent)
        dx = 2 * (1 - u) * (p1[0] - p0[0]) + 2 * u * (p2[0] - p1[0])
        dy = 2 * (1 - u) * (p1[1] - p0[1]) + 2 * u * (p2[1] - p1[1])
        length = math.hypot(dx, dy)
        if length > 0:
            # Inward normal pointing towards the inside of the crescent (inner concave side)
            # Leading curve arches towards (-1, -1), inward normal points towards (+1, +1)
            # Tangent (dx, dy) points towards bottom-left (-dx, +dy)
            # Inward normal: (-dy, dx) points towards bottom-right if dx < 0, dy > 0
            # Let's verify: dx ~ -30, dy ~ +35.
            # (-dy, dx) = (-35, -30) which is outward (up-left)!
            # So inward normal is (+dy, -dx) = (+35, +30) which points down-right (inward)!
            nx = dy / length
            ny = -dx / length
        else:
            nx, ny = 0.0, 0.0
            
        curve_pts.append((bx, by, nx, ny, u))
        
    for y in range(H):
        for x in range(W):
            min_dist = 999.0
            best_pt = None
            for pt in curve_pts:
                d = math.hypot(x - pt[0], y - pt[1])
                if d < min_dist:
                    min_dist = d
                    best_pt = pt
                    
            if best_pt is None:
                continue
                
            bx, by, nx, ny, u = best_pt
            
            # Envelope thickness at position u:
            # 0 at u=0, peaks at u=0.5 with thickness ~4.0, 0 at u=1
            thick = (math.sin(u * math.pi) ** 0.7) * 4.2
            
            # Vector from curve point to pixel (x, y)
            vx = x - bx
            vy = y - by
            
            # Dot product with inward normal (signed distance along inward direction)
            # positive means inside the crescent (trailing side)
            # negative means outside the leading edge (ahead of the blade)
            inward_dist = vx * nx + vy * ny
            
            # Leading edge has very small tolerance (-0.5 to -0.8 for crisp cutting line)
            # Trailing side extends up to `thick`
            if -0.8 <= inward_dist <= thick + 0.5:
                # Along the tangent distance
                tangent_dist = math.hypot(vx - inward_dist * nx, vy - inward_dist * ny)
                if tangent_dist > 1.2:
                    continue
                    
                if inward_dist < -0.2:
                    grid[y][x] = "D" # Crisp outer dark blue outline
                elif -0.2 <= inward_dist <= 0.6:
                    grid[y][x] = "W" # Brilliant razor-sharp white cutting spine!
                elif 0.6 < inward_dist <= 1.4:
                    grid[y][x] = "H" # Cyan-white
                elif 1.4 < inward_dist <= 2.4:
                    grid[y][x] = "A" # Electric neon cyan
                elif 2.4 < inward_dist <= thick:
                    grid[y][x] = "B" # Vibrant cyan
                elif inward_dist <= thick + 0.8:
                    grid[y][x] = "C" # Trailing deep cyan
                    
    # Clean up ends so they taper cleanly to 1px points
    # Tail point: (42, 7)
    grid[7][42] = "A"
    grid[6][43] = "B"
    grid[5][44] = "D"
    
    # Tip point: (7, 42)
    grid[42][7] = "W"
    grid[43][6] = "A"
    grid[44][5] = "D"
    
    return grid

grid = rasterize_vfx_arc()
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = colors.get(grid[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_arc_asymmetric.png")
print("Saved test/test_arc_asymmetric.png")
