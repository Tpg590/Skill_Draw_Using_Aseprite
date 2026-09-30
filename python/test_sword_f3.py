from PIL import Image

W, H = 48, 48

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "W": (255, 255, 255, 255), # Pure white core
    "H": (205, 250, 255, 255), # Soft cyan-white glow
    "A": (45, 240, 255, 255),  # Electric neon cyan
    "B": (0, 180, 235, 255),   # Rich vibrant cyan
    "C": (0, 115, 175, 255),   # Deep cyan shadow
    "D": (15, 55, 95, 255),    # Outer magical navy outline
    "Z": (6, 25, 48, 255),     # Deepest navy crevice
    "L": (230, 242, 250, 255), # Polished steel highlight
    "M": (155, 180, 200, 255), # Steel midtone
    "K": (85, 110, 135, 255),  # Steel shadow
    "X": (40, 58, 78, 255),    # Steel dark outline
    "Y": (255, 235, 120, 255), # Gold highlight
    "G": (230, 170, 35, 255),  # Rich gold midtone
    "O": (155, 95, 18, 255),   # Gold shadow
    "Q": (75, 42, 10, 255),    # Dark gold outline
    "U": (135, 65, 30, 255),   # Leather grip highlight
    "V": (70, 30, 12, 255),    # Dark leather shadow
}

def set_pixel(grid, x, y, char):
    if 0 <= x < W and 0 <= y < H:
        grid[y][x] = char

def render_sword_down_left(grid, hx=30, hy=18, blade_len=20, glowing=True):
    # Pommel (gold diamond) in upper-right
    pom_x, pom_y = hx + 4, hy - 4
    set_pixel(grid, pom_x, pom_y, "Y")
    set_pixel(grid, pom_x, pom_y + 1, "G")
    set_pixel(grid, pom_x - 1, pom_y, "O")
    set_pixel(grid, pom_x, pom_y - 1, "Q")
    set_pixel(grid, pom_x + 1, pom_y, "Q")
    
    # Grip (leather wrapped, from pommel to guard)
    for step in range(1, 4):
        gx = pom_x - step
        gy = pom_y + step
        set_pixel(grid, gx, gy, "U")
        set_pixel(grid, gx + 1, gy, "V")
        
    # Crossguard
    set_pixel(grid, hx, hy, "W" if glowing else "A") # Central power gem
    set_pixel(grid, hx + 1, hy, "G")
    set_pixel(grid, hx, hy - 1, "O")
    set_pixel(grid, hx + 1, hy - 1, "Q")
    
    # Upper-left wing (-1, -1)
    set_pixel(grid, hx - 1, hy - 1, "G")
    set_pixel(grid, hx - 2, hy - 1, "Y")
    set_pixel(grid, hx - 2, hy - 2, "G")
    set_pixel(grid, hx - 3, hy - 2, "Y")
    set_pixel(grid, hx - 3, hy - 3, "Q")
    set_pixel(grid, hx - 2, hy - 3, "Q")
    set_pixel(grid, hx - 1, hy - 2, "O")
    
    # Lower-right wing (+1, +1)
    set_pixel(grid, hx + 1, hy + 1, "O")
    set_pixel(grid, hx + 1, hy + 2, "O")
    set_pixel(grid, hx + 2, hy + 2, "G")
    set_pixel(grid, hx + 2, hy + 3, "O")
    set_pixel(grid, hx + 3, hy + 3, "Q")
    set_pixel(grid, hx + 3, hy + 2, "Q")
    set_pixel(grid, hx + 2, hy + 1, "Q")
    
    # Blade: spine from (hx-1, hy+1) to (hx-blade_len, hy+blade_len)
    for k in range(1, blade_len):
        sx = hx - k
        sy = hy + k
        
        # Cutting edge (upper-left side: sx - 1, sy)
        set_pixel(grid, sx - 1, sy, "A" if k < blade_len - 3 else "W")
        set_pixel(grid, sx - 1, sy - 1, "D") # Outline
        
        # Spine (polished steel fuller)
        set_pixel(grid, sx, sy, "L" if k < blade_len - 4 else "H")
        
        # Back edge (lower-right side: sx, sy + 1)
        set_pixel(grid, sx, sy + 1, "M" if k < blade_len - 3 else "B")
        set_pixel(grid, sx + 1, sy + 1, "X") # Outline
        
    # Needle-sharp tip at (hx - blade_len, hy + blade_len)
    tx = hx - blade_len
    ty = hy + blade_len
    set_pixel(grid, tx, ty - 1, "H")
    set_pixel(grid, tx + 1, ty, "M")
    set_pixel(grid, tx, ty, "W") # Apex glint
    set_pixel(grid, tx - 1, ty, "D")
    set_pixel(grid, tx, ty + 1, "D")
    set_pixel(grid, tx - 1, ty - 1, "D")

grid3 = [["." for _ in range(W)] for _ in range(H)]
render_sword_down_left(grid3, 30, 18, 21, glowing=True)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = PALETTE.get(grid3[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_sword_f3_fixed.png")
print("Saved test/test_sword_f3_fixed.png")
