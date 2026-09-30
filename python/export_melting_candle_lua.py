import os
import sys

sys.path.append("python")
import design_melting_candle as d

W, H = 32, 48
fps = 6
frame_duration = 1.0 / fps

frames = d.frames

# Validate all frames
char_frames = []
for f_idx, grid in enumerate(frames):
    char_grid = []
    for y in range(H):
        row = "".join([grid[y][x] for x in range(W)])
        assert len(row) == 32, f"Row {y} in frame {f_idx} length != 32"
        char_grid.append(row)
    assert len(char_grid) == 48, f"Frame {f_idx} rows != 48"
    char_frames.append(char_grid)

print(f"Validated {len(char_frames)} frames (32x48).")

# Generate Lua script
lua_lines = []
lua_lines.append('-- scripts/melting_candle_32x48.lua')
lua_lines.append('local width = 32')
lua_lines.append('local height = 48')
lua_lines.append('local fps = 6')
lua_lines.append('local frameDuration = 1.0 / fps')
lua_lines.append('')
lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
lua_lines.append('local layer = sprite.layers[1]')
lua_lines.append('layer.name = "Candle"')
lua_lines.append('sprite.frames[1].duration = frameDuration')
lua_lines.append('')
lua_lines.append('-- 1. Palette: Terraria Crimson Wax & Brass Plate (High Contrast)')
lua_lines.append('local PALETTE = {')
lua_lines.append('    ["."] = nil,')
lua_lines.append('    ["S"] = "#140a10", -- Soft ground shadow (Alpha 130)')
lua_lines.append('    ["#"] = "#18060a", -- Terraria dark crimson-black outline')
lua_lines.append('    ["A"] = "#e83838", -- Crimson wax bright highlight')
lua_lines.append('    ["B"] = "#aa1828", -- Crimson wax rich midtone')
lua_lines.append('    ["C"] = "#660a18", -- Crimson wax deep shadow')
lua_lines.append('    ["D"] = "#38040c", -- Crimson wax deepest crevice')
lua_lines.append('    ["W"] = "#ffffff", -- Flame white-hot core')
lua_lines.append('    ["Y"] = "#ffe850", -- Flame bright yellow')
lua_lines.append('    ["O"] = "#f87818", -- Flame vibrant orange')
lua_lines.append('    ["R"] = "#c82010", -- Flame outer red')
lua_lines.append('    ["G"] = "#ffbe40", -- OSL golden molten wax rim')
lua_lines.append('    ["K"] = "#14080a", -- Charred wick')
lua_lines.append('    ["M"] = "#d8b878", -- Metal plate brass highlight')
lua_lines.append('    ["N"] = "#987840", -- Metal plate brass midtone')
lua_lines.append('    ["P"] = "#584020", -- Metal plate brass shadow')
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
lua_lines.append('-- Render Frames 2 to 6')
lua_lines.append('for i = 2, #frames_data do')
lua_lines.append('    local frame = sprite:newEmptyFrame()')
lua_lines.append('    frame.duration = frameDuration')
lua_lines.append('    local img = Image(width, height, ColorMode.RGB)')
lua_lines.append('    renderGrid(img, frames_data[i], PALETTE)')
lua_lines.append('    sprite:newCel(layer, frame, img)')
lua_lines.append('end')
lua_lines.append('')
lua_lines.append('-- 3. Export Files via CLI')
lua_lines.append('sprite:saveCopyAs("output/aseprite/melting_candle_32x48.aseprite")')
lua_lines.append('if #sprite.frames > 1 then')
lua_lines.append('    sprite:saveCopyAs("output/gif/melting_candle_32x48.gif")')
lua_lines.append('    local totalFrames = #sprite.frames')
lua_lines.append('    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)')
lua_lines.append('    local sheetImage = sheetSprite.cels[1].image')
lua_lines.append('    for i = 1, totalFrames do')
lua_lines.append('        local frameCel = layer:cel(i)')
lua_lines.append('        if frameCel then')
lua_lines.append('            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))')
lua_lines.append('        end')
lua_lines.append('    end')
lua_lines.append('    sheetSprite:saveCopyAs("output/Sheet/melting_candle_32x48_sheet.png")')
lua_lines.append('    sheetSprite:close()')
lua_lines.append('else')
lua_lines.append('    sprite:saveCopyAs("output/Sheet/melting_candle_32x48.png")')
lua_lines.append('end')

lua_script_content = "\n".join(lua_lines) + "\n"

os.makedirs("scripts", exist_ok=True)
with open("scripts/melting_candle_32x48.lua", "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Exported scripts/melting_candle_32x48.lua successfully! ({len(lua_lines)} lines)")
