import os
import sys

sys.path.append("python")
import test_bell_rotation as t

W, H = 48, 48
fps = 8
frame_duration = 1.0 / fps

frames_data = t.frames_data

# Validate all frames
char_frames = []
for f_idx, (grid, bx) in enumerate(frames_data):
    char_grid = []
    for y in range(H):
        row = "".join([grid[y][x] for x in range(W)])
        assert len(row) == 48, f"Row {y} in frame {f_idx} length != 48"
        char_grid.append(row)
    assert len(char_grid) == 48, f"Frame {f_idx} rows != 48"
    char_frames.append(char_grid)

print(f"Validated {len(char_frames)} frames.")

# Generate Lua script content
lua_lines = []
lua_lines.append('-- scripts/bronze_bell_swing_48.lua')
lua_lines.append('local width = 48')
lua_lines.append('local height = 48')
lua_lines.append('local fps = 8')
lua_lines.append('local frameDuration = 1.0 / fps')
lua_lines.append('')
lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
lua_lines.append('local layer = sprite.layers[1]')
lua_lines.append('layer.name = "BronzeBell"')
lua_lines.append('sprite.frames[1].duration = frameDuration')
lua_lines.append('')
lua_lines.append('-- 1. Palette: Stardew Valley Warm Bronze & Timber (NO #000000!)')
lua_lines.append('local PALETTE = {')
lua_lines.append('    ["."] = nil,')
lua_lines.append('    ["S"] = "#1a1620", -- Soft ground shadow on stone (Alpha 130)')
lua_lines.append('    ["#"] = "#381e12", -- Soft dark mahogany outline for wood/bronze')
lua_lines.append('    ["@"] = "#262220", -- Soft dark charcoal stone outline')
lua_lines.append('    ["A"] = "#ffdf88", -- Specular gold highlight (locked top-left)')
lua_lines.append('    ["B"] = "#e8a038", -- Bright polished bronze body')
lua_lines.append('    ["C"] = "#b8641c", -- Warm bronze midtone')
lua_lines.append('    ["D"] = "#743810", -- Deep aged bronze shadow')
lua_lines.append('    ["E"] = "#421a08", -- Inner bell cavity shadow')
lua_lines.append('    ["F"] = "#d49242", -- Oak timber highlight')
lua_lines.append('    ["G"] = "#945422", -- Oak timber midtone')
lua_lines.append('    ["H"] = "#562c10", -- Oak timber shadow')
lua_lines.append('    ["J"] = "#888292", -- Iron chain highlight')
lua_lines.append('    ["K"] = "#544c5c", -- Iron chain midtone')
lua_lines.append('    ["L"] = "#322a36", -- Iron chain shadow')
lua_lines.append('    ["M"] = "#8e8a80", -- Stone floor highlight')
lua_lines.append('    ["N"] = "#625e56", -- Stone floor midtone')
lua_lines.append('    ["P"] = "#3e3a34", -- Stone floor shadow')
lua_lines.append('}')
lua_lines.append('')

for f_idx, fr in enumerate(char_frames):
    lua_lines.append(f'local frame{f_idx + 1}_grid = {{')
    for y_idx, row in enumerate(fr):
        comma = "," if y_idx < len(fr) - 1 else ""
        lua_lines.append(f'    "{row}"{comma}')
    lua_lines.append('}')
    lua_lines.append('')

frame_names = [f"frame{i+1}_grid" for i in range(len(char_frames))]
lua_lines.append(f'local frames_data = {{ {", ".join(frame_names)} }}')
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
lua_lines.append('-- Render Frames 2 to 8')
lua_lines.append('for i = 2, #frames_data do')
lua_lines.append('    local frame = sprite:newEmptyFrame()')
lua_lines.append('    frame.duration = frameDuration')
lua_lines.append('    local img = Image(width, height, ColorMode.RGB)')
lua_lines.append('    renderGrid(img, frames_data[i], PALETTE)')
lua_lines.append('    sprite:newCel(layer, frame, img)')
lua_lines.append('end')
lua_lines.append('')
lua_lines.append('-- 3. Export Files via CLI')
lua_lines.append('sprite:saveCopyAs("output/aseprite/bronze_bell_swing_48.aseprite")')
lua_lines.append('if #sprite.frames > 1 then')
lua_lines.append('    sprite:saveCopyAs("output/gif/bronze_bell_swing_48.gif")')
lua_lines.append('    local totalFrames = #sprite.frames')
lua_lines.append('    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)')
lua_lines.append('    local sheetImage = sheetSprite.cels[1].image')
lua_lines.append('    for i = 1, totalFrames do')
lua_lines.append('        local frameCel = layer:cel(i)')
lua_lines.append('        if frameCel then')
lua_lines.append('            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))')
lua_lines.append('        end')
lua_lines.append('    end')
lua_lines.append('    sheetSprite:saveCopyAs("output/Sheet/bronze_bell_swing_48_sheet.png")')
lua_lines.append('    sheetSprite:close()')
lua_lines.append('else')
lua_lines.append('    sprite:saveCopyAs("output/Sheet/bronze_bell_swing_48.png")')
lua_lines.append('end')

lua_script_content = "\n".join(lua_lines) + "\n"

os.makedirs("scripts", exist_ok=True)
with open("scripts/bronze_bell_swing_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Exported scripts/bronze_bell_swing_48.lua successfully! ({len(lua_lines)} lines)")
