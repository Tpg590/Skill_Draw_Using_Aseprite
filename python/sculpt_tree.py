import os
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

class Canvas64:
    def __init__(self):
        self.w = 64
        self.h = 64
        self.grid = [["." for _ in range(64)] for _ in range(64)]

    def set(self, x, y, ch):
        if 0 <= x < 64 and 0 <= y < 64:
            self.grid[y][x] = ch

    def get(self, x, y):
        if 0 <= x < 64 and 0 <= y < 64:
            return self.grid[y][x]
        return "."

    def fill_rect(self, x1, y1, x2, y2, ch):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.set(x, y, ch)

    def draw_outline(self):
        # Add outline # around all non-empty non-S pixels
        to_outline = []
        for y in range(64):
            for x in range(64):
                if self.grid[y][x] == ".":
                    # Check 4 neighbors
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 64 and 0 <= ny < 64:
                            neigh = self.grid[ny][nx]
                            if neigh not in [".", "S", "#"]:
                                to_outline.append((x, y))
                                break
        for x, y in to_outline:
            self.grid[y][x] = "#"

    def render(self):
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        for y in range(64):
            for x in range(64):
                ch = self.grid[y][x]
                col = PALETTE.get(ch)
                if col:
                    img.putpixel((x, y), col)
        return img

    def get_rows(self):
        return ["".join(r) for r in self.grid]

print("Canvas64 initialized.")
