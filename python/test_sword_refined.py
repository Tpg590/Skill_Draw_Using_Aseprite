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

def render_diagonal_sword_up_right(grid, hx=17, hy=31, blade_len=20, tip_glow=True):
    # Pommel (gold diamond)
    pom_x, pom_y = hx - 4, hy + 4
    grid[pom_y][pom_x] = "Y"
    grid[pom_y - 1][pom_x] = "G"
    grid[pom_y][pom_x + 1] = "O"
    grid[pom_y + 1][pom_x] = "Q"
    grid[pom_y][pom_x - 1] = "Q"
    
    # Grip (leather wrapped, from pommel to guard)
    for step in range(1, 4):
        gx = pom_x + step
        gy = pom_y - step
        grid[gy][gx] = "U"
        grid[gy + 1][gx] = "V"
        
    # Crossguard (seamless connection)
    # Center block
    grid[hy][hx] = "W" if tip_glow else "A" # Central power gem
    grid[hy][hx - 1] = "G"
    grid[hy + 1][hx] = "O"
    grid[hy + 1][hx - 1] = "Q"
    
    # Upper-left wing (facing cutting side)
    grid[hy - 1][hx - 1] = "G"
    grid[hy - 1][hx - 2] = "Y"
    grid[hy - 2][hx - 2] = "G"
    grid[hy - 2][hx - 3] = "Y"
    grid[hy - 3][hx - 3] = "Q"
    grid[hy - 3][hx - 2] = "Q"
    grid[hy - 2][hx - 1] = "O"
    
    # Lower-right wing (facing back side)
    grid[hy + 1][hx + 1] = "O"
    grid[hy + 2][hx + 1] = "O"
    grid[hy + 2][hx + 2] = "G"
    grid[hy + 3][hx + 2] = "O"
    grid[hy + 3][hx + 3] = "Q"
    grid[hy + 2][hx + 3] = "Q"
    grid[hy + 1][hx + 2] = "Q"
    
    # Blade: spine from (hx+1, hy-1) to (hx+blade_len, hy-blade_len)
    for k in range(1, blade_len):
        sx = hx + k
        sy = hy - k
        
        # Upper cutting edge (radiant cyan magic)
        # Uniform glowing cyan edge
        grid[sy - 1][sx] = "A" if k < blade_len - 3 else "W"
        grid[sy - 1][sx - 1] = "D" # Outline
        
        # Spine (polished steel fuller)
        grid[sy][sx] = "L" if k < blade_len - 4 else "H"
        
        # Lower edge (steel shadow & blue reflection)
        grid[sy][sx + 1] = "M" if k < blade_len - 3 else "B"
        grid[sy + 1][sx + 1] = "X"
        
    # Needle sharp tip
    tx = hx + blade_len
    ty = hy - blade_len
    # Tapering: 1 step before tip
    grid[ty + 1][tx - 1] = "H"
    grid[ty + 1][tx] = "A"
    grid[ty][tx] = "W" # Extreme sharp tip point!
    grid[ty - 1][tx] = "D"
    grid[ty][tx + 1] = "D"
    grid[ty - 1][tx - 1] = "D"
    
    if tip_glow:
        # Gathering energy motes around tip
        grid[ty - 2][tx] = "A"
        grid[ty - 1][tx + 2] = "H"
        grid[ty + 1][tx + 2] = "B"
        grid[ty - 3][tx + 1] = "W"
        grid[ty - 2][tx - 2] = "B"
        grid[ty + 2][tx + 3] = "C"

grid1 = [["." for _ in range(W)] for _ in range(H)]
render_diagonal_sword_up_right(grid1, 17, 31, 21, tip_glow=True)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pix = img.load()
for y in range(H):
    for x in range(W):
        pix[x, y] = PALETTE.get(grid1[y][x], (0, 0, 0, 0))

img.resize((W * 6, H * 6), Image.NEAREST).save("test/test_sword_f1_refined.png")
print("Saved test/test_sword_f1_refined.png")
