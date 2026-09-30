import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_magic_torch import frames, PALETTE, W, H

lua_content = """-- scripts/magic_torch_32x48.lua
-- 32x48 Terraria Animated Magic Violet/Pink Torch on Stone Pedestal
local width = 32
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Magic_Torch"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria chunky shading, near-black outline, magic violet/pink flame exception
local PALETTE = {
    ["."] = nil,
    ["#"] = "#120a14", -- Near-black Terraria outline with deep violet tint
    ["S"] = "#140a18", -- Soft ground shadow (Alpha 130)
    
    -- Iron Torch Brazier & Shaft
    ["I"] = "#a0acb9", -- Iron highlight
    ["F"] = "#555f70", -- Iron midtone
    ["L"] = "#2a303a", -- Iron shadow
    
    -- Carved Stone Pedestal
    ["G"] = "#7d8796", -- Stone highlight
    ["D"] = "#48505a", -- Stone midtone
    ["N"] = "#262a32", -- Stone shadow
    
    -- OSL Pink Glow on Metal
    ["O"] = "#ff82e6", -- Vivid magic pink glow reflection
    
    -- Magic Violet/Pink Flame
    ["W"] = "#ffffff", -- White hot flame core
    ["K"] = "#ffc3f5", -- Pale pink sparks / inner glow
    ["P"] = "#f541c3", -- Vivid hot magenta/pink
    ["M"] = "#9b19af", -- Deep violet-purple flame
    ["V"] = "#4b0869"  -- Dark magic flame rim/smoke
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
            end
        end
    end
end

"""

def format_grid(var_name, grid_rows):
    res = f"local {var_name} = {{\n"
    for r in grid_rows:
        res += f'    "{r}",\n'
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
sprite:saveCopyAs("output/aseprite/magic_torch_32x48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/magic_torch_32x48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/magic_torch_32x48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/magic_torch_32x48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/magic_torch_32x48.lua successfully!")
