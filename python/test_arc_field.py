import math
from PIL import Image

W, H = 48, 48

# Color map for test
colors = {
    ".": (0, 0, 0, 0),
    "W": (255, 255, 255, 255),
    "H": (205, 250, 255, 255),
    "A": (45, 240, 255, 255),
    "B": (0, 180, 235, 255),
    "C": (0, 115, 175, 255),
    "D": (15, 55, 95, 255),
}

def rasterize_arc(p0, p1, p2, max_thickness=4.0):
    grid = [["." for _ in range(W)] for _ in range(H)]
    
    # Parametric Bezier
    # To avoid gaps, we can sample u very densely, e.g. 1000 steps
    # And we also draw a filled polygon or distance field!
    
    # Distance Field Approach:
    # Compute distance from each pixel (x, y) to the Bezier curve!
    num_samples = 600
    curve_pts = []
    for i in range(num_samples + 1):
        u = i / num_samples
        bx = (1 - u)**2 * p0[0] + 2 * (1 - u) * u * p1[0] + u**2 * p2[0]
        by = (1 - u)**2 * p0[1] + 2 * (1 - u) * u * p1[1] + u**2 * p2[1]
        curve_pts.append((bx, by, u))
        
    for y in range(H):
        for x in range(W):
            # Find closest point on curve
            min_dist = 999.0
            best_u = 0.5
            for bx, by, u in curve_pts:
                d = math.hypot(x - bx, y - by)
                if d < min_dist:
                    min_dist = d
                    best_u = u
                    
            # Thickness envelope along the curve:
            # Tapers to 0 at ends (u=0, u=1)
            # Peaks at u=0.5 with max_thickness
            # Sine envelope: sin(u * pi)^0.8
            half_t = (math.sin(best_u * math.pi) ** 0.75) * (max_thickness / 2.0)
            
            # Check if within arc envelope
            if min_dist <= half_t + 0.6:
                # Color based on normalized distance from spine
                norm_d = min_dist / max(0.1, half_t + 0.6)
                if min_dist <= 0.6:
                    grid[y][x] = "W" # Radiant core
                elif norm_d <= 0.35:
                    grid[y][x] = "H"
                elif norm_d <= 0.65:
                    grid[y][x] = "A"
                elif norm_d <= 0.88:
                    grid[y][x] = "B"
                elif norm_d <= 1.0:
                    grid[y][x] = "C"
                else:
                    grid[y][x] = "D"
                    
    return grid

p0 = (42.0, 7.0)
p1 = (14.0, 11.0)
p2 = (7.0, 42.0)

grid = rasterize_arc(p0, p1, p2, max_thickness=4.5)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = colors.get(grid[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_arc_field.png")
print("Saved test/test_arc_field.png")
