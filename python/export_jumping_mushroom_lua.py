import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_jumping_mushroom import frames, PALETTE, W, H

lua_content = """-- scripts/jumping_mushroom_48.lua
-- 48x48 FreeStyle Animated Jumping Mushroom Monster with Z-Axis Dynamic Shadow Scaling
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Jumping_Mushroom"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: FreeStyle rich hue-shifting
local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e0e26", -- Soft ground shadow (Alpha 130)
    
    -- Clean Outlines
    ["#"] = "#320a20", -- Cap outline
    ["$"] = "#281419", -- Stem outline
    
    -- Mushroom Cap
    ["H"] = "#ffd750", -- Specular warm gold highlight
    ["A"] = "#ff5555", -- Vibrant coral-red
    ["B"] = "#e11e3c", -- Crimson red base
    ["C"] = "#a00f41", -- Ruby red shadow
    ["Z"] = "#5f0a30", -- Dark plum crevice
    
    -- Polka Dots
    ["K"] = "#fffcdd", -- Pure cream highlight
    ["E"] = "#f5e1a0", -- Warm vanilla dot base
    ["Q"] = "#d2af78", -- Dot shadow
    
    -- Mushroom Stem
    ["T"] = "#fffae1", -- Stem highlight
    ["U"] = "#f5e1af", -- Stem cream base
    ["M"] = "#cda582", -- Stem warm peach shadow
    ["D"] = "#915f55", -- Stem deep shadow
    
    -- Eyes & Face
    ["X"] = "#190a14", -- Dark pupil
    ["W"] = "#ffffff", -- Eye glint
    ["L"] = "#ff8caa"  -- Blush cheeks
}

local function renderGrid(img, gridData, pal)
    for y = 1, #gridData do
        local line = gridData[y]
        for x = 1, #line do
            local char = line:sub(x, x)
            local hex = pal[char]
            if hex then
                local h = hex:gsub("#", "")
                local r = tonumber(h:sub(1, 2), 16) or 0
                local g = tonumber(h:sub(3, 4), 16) or 0
                local b = tonumber(h:sub(5, 6), 16) or 0
                local a = (char == "S") and 130 or 255
                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = a })
            else
                img:drawPixel(x - 1, y - 1, Color{ r = 0, g = 0, b = 0, a = 0 })
            end
        end
    end
end

"""

def format_grid(var_name, grid_rows):
    res = f"local {var_name} = {{\n"
    for r in grid_rows:
        line_str = "".join(r) if isinstance(r, (list, tuple)) else str(r)
        res += f'    "{line_str}",\n'
    res += "}\n"
    return res

for i, f_data in enumerate(frames):
    lua_content += format_grid(f"f{i+1}_grid", f_data)

lua_content += """
-- Render Frame 1
renderGrid(image, f1_grid, PALETTE)

-- Render Frame 2
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local img2 = layer:cel(2).image
renderGrid(img2, f2_grid, PALETTE)

-- Render Frame 3
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local img3 = layer:cel(3).image
renderGrid(img3, f3_grid, PALETTE)

-- Render Frame 4
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local img4 = layer:cel(4).image
renderGrid(img4, f4_grid, PALETTE)

-- Save Aseprite project
sprite:saveCopyAs("output/aseprite/jumping_mushroom_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/jumping_mushroom_48.gif")

-- Save Spritesheet
local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/jumping_mushroom_48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/jumping_mushroom_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/jumping_mushroom_48.lua successfully!")
