import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_ships_helm import frames, PALETTE, W, H

lua_content = """-- scripts/ships_helm_wheel_48.lua
-- 48x48 Stardew Valley Animated Rotating Ship's Helm Wheel
local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Ship_Helm"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley warm palette (soft outline, NO #000000)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#201424", -- Soft ground shadow (Alpha 130)
    
    -- Oak Wood (Rim, Spokes, Handles, Pedestal)
    ["#"] = "#3a1c10", -- Soft dark wood outline
    ["T"] = "#e1a55f", -- Oak highlight
    ["U"] = "#af7337", -- Oak midtone
    ["M"] = "#784620", -- Oak shadow
    ["D"] = "#4b2612", -- Oak dark crevice
    
    -- Bronze Band & Hub (Aged nautical brass)
    ["P"] = "#fff8d7", -- Specular ivory-white highlight
    ["A"] = "#f5be46", -- Bright golden shine
    ["B"] = "#c38226", -- Bronze base
    ["C"] = "#824b14", -- Bronze shadow
    ["Z"] = "#4b260c", -- Bronze deep shade
    
    -- Indicator Marker (King Spoke cord wrap)
    ["R"] = "#eb2d23", -- Vivid crimson marker wrap
    ["W"] = "#ffffff", -- Pure white cord accent
    ["K"] = "#f5d7a5"  -- Nautical rope cream
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
sprite:saveCopyAs("output/aseprite/ships_helm_wheel_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/ships_helm_wheel_48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/ships_helm_wheel_48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/ships_helm_wheel_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/ships_helm_wheel_48.lua successfully!")
