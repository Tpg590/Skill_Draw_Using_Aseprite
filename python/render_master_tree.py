import os
import math
from PIL import Image

PALETTE = {
    ".": None,
    "#": (24, 15, 20, 255),       # Viền tối sẫm Terraria (Near-black outline)
    "S": (18, 10, 16, 130),       # Bóng râm tiếp đất (Ground shadow, Alpha 130)
    "H": (191, 163, 130, 255),    # Gỗ sáng / Vết nứt đón sáng (Pale aged bark highlight)
    "M": (130, 99, 77, 255),      # Màu gỗ chính / Gạch đá (Mid aged brown/gray wood & stone)
    "D": (74, 50, 38, 255),       # Gỗ tối / Cành phía sau (Deep shadow wood & background branches)
    "V": (42, 24, 18, 255),       # Rãnh xoắn sâu / Khe nứt gạch (Deepest twist crevice & fissure)
}

grid = [["." for _ in range(64)] for _ in range(64)]

def set_px(x, y, ch, force=False):
    if 0 <= x < 64 and 0 <= y < 64:
        if force or grid[y][x] == ".":
            grid[y][x] = ch

def get_px(x, y):
    if 0 <= x < 64 and 0 <= y < 64:
        return grid[y][x]
    return "."

def draw_circle(cx, cy, r, ch, force=False):
    for dy in range(-int(r)-1, int(r)+2):
        for dx in range(-int(r)-1, int(r)+2):
            if dx*dx + dy*dy <= r*r:
                set_px(int(cx + dx), int(cy + dy), ch, force)

def draw_line(x0, y0, x1, y1, r, ch, force=False):
    dist = math.hypot(x1 - x0, y1 - y0)
    steps = max(1, int(dist * 2))
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        draw_circle(x, y, r, ch, force)

print("Canvas helpers ready.")
