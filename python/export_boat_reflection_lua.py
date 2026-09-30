import os
import math

W, H = 48, 48

# Single-character Palette Mapping
CHAR_MAP = {
    ".": ".",
    "S": "S",
    "#": "#",
    "A": "A",
    "B": "B",
    "C": "C",
    "D": "D",
    "L1": "F",
    "L2": "G",
    "L3": "K",
    "R1": "H",
    "R2": "M",
    "R3": "N",
    "RL1": "P",
    "RL2": "Q",
    "W1": "U",
    "W2": "V",
}

PALETTE_HEX = {
    ".": "nil",
    "S": "#0e1824",  # Soft aquatic shadow (Alpha 130)
    "#": "#0a121c",  # Clean dark navy-teal outline
    "A": "#e8a44c",  # Golden oak highlight
    "B": "#a45e26",  # Warm oak midtone
    "C": "#54280e",  # Deep oak shadow
    "D": "#30160a",  # Deepest interior crevice
    "F": "#fff8b0",  # White-gold flame core
    "G": "#f6a623",  # Radiant golden-amber glow
    "K": "#b85412",  # Lantern cage / bronze
    "H": "#528686",  # Reflected wood highlight (Teal-oak)
    "M": "#2a5258",  # Reflected wood body (Dark teal)
    "N": "#142e34",  # Deep aquatic under-crevice
    "P": "#aae6c3",  # Reflected lantern core shimmer
    "Q": "#69b99b",  # Reflected golden-teal lantern glow
    "U": "#386b80",  # Water ripple crest highlight
    "V": "#1a3848",  # Deep lake water tone
}

def empty_grid():
    return [["." for _ in range(W)] for _ in range(H)]

def draw_boat_pro(grid, yw):
    # Keel is at yw, real boat extends from yw - 10 to yw (height = 11px)
    
    # 1. Stern (left transom & sheer line)
    grid[yw - 6][7] = "#"; grid[yw - 6][8] = "#"
    grid[yw - 5][6] = "#"; grid[yw - 5][7] = "A"; grid[yw - 5][8] = "B"; grid[yw - 5][9] = "#"
    grid[yw - 4][7] = "#"; grid[yw - 4][8] = "B"; grid[yw - 4][9] = "C"; grid[yw - 4][10] = "#"
    grid[yw - 3][8] = "#"; grid[yw - 3][9] = "C"; grid[yw - 3][10] = "#"
    grid[yw - 2][9] = "#"; grid[yw - 2][10] = "#"
    grid[yw - 1][10] = "#"; grid[yw - 1][11] = "#"
    
    # 2. Far Gunwale (mạn thuyền xa):
    for x in range(9, 35):
        grid[yw - 7][x] = "#"
        grid[yw - 6][x] = "C" # inner shadow wall
        
    # Interior floorboards & shadows (lòng thuyền, vệt ván ngang):
    for x in range(10, 34):
        grid[yw - 5][x] = "D" if (x // 4) % 2 == 0 else "C"
        
    # Stern bench (ghế lái): X=8..12
    for x in range(8, 13):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"
        
    # Midships rowing seat bench (ghế chèo giữa): X=19..25
    for x in range(19, 26):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"
        grid[yw - 4][x] = "C" # shadow under bench
        
    # Bow seat bench (ghế mũi): X=30..33
    for x in range(30, 34):
        grid[yw - 6][x] = "A"
        grid[yw - 5][x] = "B"

    # 3. Near Gunwale & Hull Planking (mạn thuyền gần):
    # Top railing of near gunwale (bright sun highlight along sheer line)
    for x in range(7, 36):
        grid[yw - 5][x] = "#"
        grid[yw - 4][x] = "A"
        
    # Upper clinker plank: vệt ngang 4 ký tự
    for x in range(9, 36):
        grid[yw - 3][x] = "A" if (x // 4) % 2 == 0 else "B"
        
    # Middle clinker plank: vệt ngang 4 ký tự
    for x in range(10, 35):
        grid[yw - 2][x] = "B" if (x // 4) % 2 == 1 else "C"
        
    # Lower clinker plank & keel curve
    for x in range(11, 34):
        grid[yw - 1][x] = "C" if (x // 5) % 2 == 0 else "B"
        
    # Keel touching water line
    for x in range(12, 33):
        grid[yw][x] = "#"

    # 4. Bow / Prow (mũi thuyền vươn cao sang phải):
    grid[yw - 5][35] = "A"; grid[yw - 5][36] = "#"
    grid[yw - 4][35] = "A"; grid[yw - 4][36] = "B"; grid[yw - 4][37] = "#"
    grid[yw - 3][35] = "B"; grid[yw - 3][36] = "C"; grid[yw - 3][37] = "#"
    grid[yw - 2][34] = "C"; grid[yw - 2][35] = "#"
    grid[yw - 1][33] = "C"; grid[yw - 1][34] = "#"

    # Graceful stem post curving up
    grid[yw - 6][36] = "A"; grid[yw - 6][37] = "#"
    grid[yw - 7][37] = "A"; grid[yw - 7][38] = "#"
    grid[yw - 8][38] = "A"; grid[yw - 8][39] = "#"
    grid[yw - 9][39] = "#"; grid[yw - 9][40] = "#"
    
    # Curved iron davit bracket extending right to hang lantern
    grid[yw - 10][40] = "#"; grid[yw - 10][41] = "#"; grid[yw - 10][42] = "#"
    grid[yw - 9][42] = "#" # hook
    
    # 5. Golden Storm Lantern hanging at X=42:
    lx, ly = 42, yw - 7
    # Cap / chimney roof
    grid[ly - 1][lx - 1] = "#"; grid[ly - 1][lx] = "L3"; grid[ly - 1][lx + 1] = "#"
    # Glass globe with radiant golden core
    grid[ly][lx - 1] = "L3"; grid[ly][lx] = "L1"; grid[ly][lx + 1] = "L3"
    grid[ly + 1][lx - 1] = "L3"; grid[ly + 1][lx] = "L2"; grid[ly + 1][lx + 1] = "L3"
    # Brass base
    grid[ly + 2][lx - 1] = "#"; grid[ly + 2][lx] = "L3"; grid[ly + 2][lx + 1] = "#"

    # OSL Golden Glow onto Prow Stem Post & Deck
    grid[yw - 8][38] = "L2"
    grid[yw - 7][37] = "L2"
    grid[yw - 6][36] = "L3"

def outline_boat_pro(grid, yw):
    for y in range(0, yw + 1):
        for x in range(W):
            c = grid[y][x]
            if c not in (".", "S", "#"):
                for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny <= yw and grid[ny][nx] == ".":
                        grid[ny][nx] = "#"

def draw_inverted_reflection_pro(grid, yw, f_phase):
    # Real boat height = 11 px (from yw - 10 to yw).
    # Reflected height must be strictly 60% - 70% of real boat height:
    # 11 * 0.60 = 6.6 px, 11 * 0.70 = 7.7 px
    # Therefore, reflected height MUST be exactly 7 pixels (depth d = 1..7)!
    # Ratio = 7 / 11 = 63.64% (Strictly within [60%, 70%]!).
    
    shifts = [int(round(math.sin(d * 1.35 - f_phase * 1.57))) for d in range(1, 8)]
    
    # d = 1 (Y = yw + 1): Keel contact reflection
    s1 = shifts[0]
    for x in range(11 + s1, 34 + s1):
        if 0 <= x < W: grid[yw + 1][x] = "R3"
    if 0 <= 9 + s1 < W: grid[yw + 1][9 + s1] = "W1"
    if 0 <= 10 + s1 < W: grid[yw + 1][10 + s1] = "W2"
    if 0 <= 34 + s1 < W: grid[yw + 1][34 + s1] = "W2"
    if 0 <= 35 + s1 < W: grid[yw + 1][35 + s1] = "W1"

    # d = 2 (Y = yw + 2): Inverted lower planking
    s2 = shifts[1]
    for x in range(10 + s2, 35 + s2):
        if 0 <= x < W:
            grid[yw + 2][x] = "R2" if (x // 4) % 2 == 0 else "R3"
    if 0 <= 8 + s2 < W: grid[yw + 2][8 + s2] = "W1"
    if 0 <= 36 + s2 < W: grid[yw + 2][36 + s2] = "W1"

    # d = 3 (Y = yw + 3): Inverted mid planking & near sheer
    s3 = shifts[2]
    for x in range(9 + s3, 36 + s3):
        if 0 <= x < W:
            grid[yw + 3][x] = "R1" if (x // 4) % 2 == 1 else "R2"
    if 0 <= 37 + s3 < W: grid[yw + 3][37 + s3] = "R3"

    # d = 4 (Y = yw + 4): Inverted gunwales & interior shadow
    s4 = shifts[3]
    for x in range(8 + s4, 35 + s4):
        if 0 <= x < W:
            grid[yw + 4][x] = "R2" if (x // 3) % 2 == 0 else "R3"
    # Stem post curving down-right
    for x in range(35 + s4, 38 + s4):
        if 0 <= x < W: grid[yw + 4][x] = "R1"
    if 0 <= 38 + s4 < W: grid[yw + 4][38 + s4] = "R3"

    # d = 5 (Y = yw + 5): Inverted stern transom tip & prow stem post
    s5 = shifts[4]
    # Left stern tip
    for x in range(8 + s5, 14 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Mid water break
    for x in range(20 + s5, 27 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R3"
    # Prow stem post
    for x in range(36 + s5, 39 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "R2"
    # Lantern top reflection
    for x in range(41 + s5, 44 + s5):
        if 0 <= x < W: grid[yw + 5][x] = "RL2"

    # d = 6 (Y = yw + 6): Inverted stem tip & radiant lantern flame core
    s6 = shifts[5]
    if 0 <= 22 + s6 < W: grid[yw + 6][22 + s6] = "W2"
    if 0 <= 23 + s6 < W: grid[yw + 6][23 + s6] = "R3"
    if 0 <= 38 + s6 < W: grid[yw + 6][38 + s6] = "R3"
    if 0 <= 40 + s6 < W: grid[yw + 6][40 + s6] = "RL2"
    if 0 <= 41 + s6 < W: grid[yw + 6][41 + s6] = "RL1"
    if 0 <= 42 + s6 < W: grid[yw + 6][42 + s6] = "RL1"
    if 0 <= 43 + s6 < W: grid[yw + 6][43 + s6] = "RL2"

    # d = 7 (Y = yw + 7): Inverted lantern base & hook shimmer (deepest point of reflection)
    s7 = shifts[6]
    if 0 <= 41 + s7 < W: grid[yw + 7][41 + s7] = "RL2"
    if 0 <= 42 + s7 < W: grid[yw + 7][42 + s7] = "RL2"
    if 0 <= 43 + s7 < W: grid[yw + 7][43 + s7] = "W1"

def draw_water_pro(grid, yw, f_phase):
    # Surrounding lake ripples (W1, W2) in soft oval bounds
    y1 = yw + 4
    if y1 < H:
        for x in (5, 6, 7):
            if grid[y1][x] == ".": grid[y1][x] = "W1" if x == 6 else "W2"
        for x in (42, 43, 44):
            if grid[y1][x] == ".": grid[y1][x] = "W2" if x == 44 else "W1"
            
    y2 = yw + 7
    if y2 < H:
        for x in (7, 8):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
        for x in (44, 45):
            if grid[y2][x] == ".": grid[y2][x] = "W2"
            
    # Soft aquatic shadow S anchored at the bottom of the canvas (Y = 39 to 45)
    ellipse_spans = {
        39: 11,
        40: 14,
        41: 16,
        42: 16,
        43: 14,
        44: 10,
        45: 6,
    }
    for y, span in ellipse_spans.items():
        for x in range(24 - span, 24 + span):
            if grid[y][x] == ".":
                grid[y][x] = "S"

def build_pro_frame(f_idx):
    grid = empty_grid()
    bob_offsets = [0, 1, 0, -1]
    yw = 29 + bob_offsets[f_idx]
    
    draw_boat_pro(grid, yw)
    outline_boat_pro(grid, yw)
    draw_inverted_reflection_pro(grid, yw, f_idx)
    draw_water_pro(grid, yw, f_idx)
    
    return grid, yw

frames = []
for i in range(4):
    g, yw = build_pro_frame(i)
    # Convert to single chars
    char_grid = []
    for y in range(H):
        row = "".join([CHAR_MAP[g[y][x]] for x in range(W)])
        assert len(row) == 48, f"Row {y} in frame {i} length != 48"
        char_grid.append(row)
    assert len(char_grid) == 48, f"Frame {i} rows != 48"
    frames.append(char_grid)

print("Frames built successfully. Formatting Lua code...")

# Generate Lua script
lua_lines = []
lua_lines.append('-- scripts/boat_water_reflection_48.lua')
lua_lines.append('local width = 48')
lua_lines.append('local height = 48')
lua_lines.append('local fps = 6')
lua_lines.append('local frameDuration = 1.0 / fps')
lua_lines.append('')
lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
lua_lines.append('local layer = sprite.layers[1]')
lua_lines.append('layer.name = "Boat"')
lua_lines.append('sprite.frames[1].duration = frameDuration')
lua_lines.append('')
lua_lines.append('-- 1. Palette: FreeStyle Aquatic Hue-Shifting')
lua_lines.append('local PALETTE = {')
lua_lines.append('    ["."] = nil,')
lua_lines.append('    ["S"] = "#0e1824", -- Soft aquatic shadow (Alpha 130)')
lua_lines.append('    ["#"] = "#0a121c", -- Clean dark navy-teal outline')
lua_lines.append('    ["A"] = "#e8a44c", -- Golden oak highlight')
lua_lines.append('    ["B"] = "#a45e26", -- Warm oak midtone')
lua_lines.append('    ["C"] = "#54280e", -- Deep oak shadow')
lua_lines.append('    ["D"] = "#30160a", -- Deepest interior crevice')
lua_lines.append('    ["F"] = "#fff8b0", -- White-gold flame core')
lua_lines.append('    ["G"] = "#f6a623", -- Radiant golden-amber glow')
lua_lines.append('    ["K"] = "#b85412", -- Lantern cage / bronze')
lua_lines.append('    ["H"] = "#528686", -- Reflected wood highlight (Teal-oak)')
lua_lines.append('    ["M"] = "#2a5258", -- Reflected wood body (Dark teal)')
lua_lines.append('    ["N"] = "#142e34", -- Deep aquatic under-crevice')
lua_lines.append('    ["P"] = "#aae6c3", -- Reflected lantern core shimmer')
lua_lines.append('    ["Q"] = "#69b99b", -- Reflected golden-teal lantern glow')
lua_lines.append('    ["U"] = "#386b80", -- Water ripple crest highlight')
lua_lines.append('    ["V"] = "#1a3848", -- Deep lake water tone')
lua_lines.append('}')
lua_lines.append('')

for f_idx, fr in enumerate(frames):
    lua_lines.append(f'local frame{f_idx + 1}_grid = {{')
    for y_idx, row in enumerate(fr):
        comma = "," if y_idx < len(fr) - 1 else ""
        lua_lines.append(f'    "{row}"{comma}')
    lua_lines.append('}')
    lua_lines.append('')

lua_lines.append('local frames_data = { frame1_grid, frame2_grid, frame3_grid, frame4_grid }')
lua_lines.append('')
lua_lines.append('-- 2. Render Function')
lua_lines.append('local function renderGrid(img, gridData, pal)')
lua_lines.append('    for y = 1, #gridData do')
lua_lines.append('        local line = gridData[y]')
lua_lines.append('        for x = 1, #line do')
lua_lines.append('            local char = line:sub(x, x)')
lua_lines.append('            local hex = pal[char]')
lua_lines.append('            if hex then')
lua_lines.append('                local h = hex:gsub("#", "")')
lua_lines.append('                local r = tonumber(h:sub(1, 2), 16) or 0')
lua_lines.append('                local g = tonumber(h:sub(3, 4), 16) or 0')
lua_lines.append('                local b = tonumber(h:sub(5, 6), 16) or 0')
lua_lines.append('                local a = (char == "S") and 130 or 255')
lua_lines.append('                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = a })')
lua_lines.append('            end')
lua_lines.append('        end')
lua_lines.append('    end')
lua_lines.append('end')
lua_lines.append('')
lua_lines.append('-- Render Frame 1 into initial cel')
lua_lines.append('renderGrid(sprite.cels[1].image, frame1_grid, PALETTE)')
lua_lines.append('')
lua_lines.append('-- Render Frames 2 to 4')
lua_lines.append('for i = 2, #frames_data do')
lua_lines.append('    local frame = sprite:newEmptyFrame()')
lua_lines.append('    frame.duration = frameDuration')
lua_lines.append('    local img = Image(width, height, ColorMode.RGB)')
lua_lines.append('    renderGrid(img, frames_data[i], PALETTE)')
lua_lines.append('    sprite:newCel(layer, frame, img)')
lua_lines.append('end')
lua_lines.append('')
lua_lines.append('-- 3. Export Files via CLI')
lua_lines.append('sprite:saveCopyAs("output/aseprite/boat_water_reflection_48.aseprite")')
lua_lines.append('if #sprite.frames > 1 then')
lua_lines.append('    sprite:saveCopyAs("output/gif/boat_water_reflection_48.gif")')
lua_lines.append('    local totalFrames = #sprite.frames')
lua_lines.append('    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)')
lua_lines.append('    local sheetImage = sheetSprite.cels[1].image')
lua_lines.append('    for i = 1, totalFrames do')
lua_lines.append('        local frameCel = layer:cel(i)')
lua_lines.append('        if frameCel then')
lua_lines.append('            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))')
lua_lines.append('        end')
lua_lines.append('    end')
lua_lines.append('    sheetSprite:saveCopyAs("output/Sheet/boat_water_reflection_48_sheet.png")')
lua_lines.append('    sheetSprite:close()')
lua_lines.append('else')
lua_lines.append('    sprite:saveCopyAs("output/Sheet/boat_water_reflection_48.png")')
lua_lines.append('end')

lua_script_content = "\n".join(lua_lines) + "\n"

os.makedirs("scripts", exist_ok=True)
with open("scripts/boat_water_reflection_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Exported scripts/boat_water_reflection_48.lua successfully! ({len(lua_lines)} lines)")
