import math
from PIL import Image

W, H = 64, 64
cx, cy = 32.0, 32.0

def test_radii(r_outer=18.5, r_inner=13.0, r_hub=7.5, r_bolt=3.5, r_tooth=25.5):
    # Print profile of pixels
    grid = [["." for _ in range(W)] for _ in range(H)]
    for y in range(H):
        dy = (y + 0.5) - cy
        for x in range(W):
            dx = (x + 0.5) - cx
            dist = math.hypot(dx, dy)
            if dist <= r_bolt:
                grid[y][x] = "E"
            elif dist <= r_hub:
                grid[y][x] = "H"
            elif r_inner <= dist <= r_outer:
                grid[y][x] = "R"
    
    # Check circle smoothness (no jaggies)
    # Check steps on rim outer:
    return grid

grid = test_radii()
print("Generated circular grid successfully.")
