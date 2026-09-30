import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_gear_machine import frames_grid, PALETTE, W, H

lua_content = """-- scripts/steam_gear_machine_64.lua
-- 64x64 Terraria Animated Steam Gear Machine on Stone Wall
local width = 64
local height = 64
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Gear_Machine"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria aged bronze, dungeon stone wall, iron rivets & patina rust
local PALETTE = {
    ["."] = nil,
    ["#"] = "#0e0a0c", -- Near-black Terraria outline
    ["S"] = "#100c12", -- Drop shadow (Alpha 130)
    
    -- Dungeon Stone Wall
    ["K"] = "#878e98", -- Stone brick light/highlight
    ["G"] = "#555c66", -- Stone base gray
    ["N"] = "#30363e", -- Stone mortar & seam shadow
    
    -- Iron Brackets & Rivets
    ["I"] = "#afb9c3", -- Iron highlight
    ["F"] = "#646e7a", -- Iron body steel
    ["L"] = "#2d323a", -- Iron shadow
    
    -- Bronze Gear Wheel (Aged Rusted Bronze)
    ["P"] = "#fffceb", -- Specular highlight (1-2px ivory white)
    ["A"] = "#f5b94b", -- Golden shine
    ["B"] = "#c37d2a", -- Bronze body
    ["C"] = "#824818", -- Bronze dark shadow
    ["Z"] = "#4b2610", -- Bronze deep crevice shade
    
    -- Verdigris Patina Rust
    ["X"] = "#69b49b", -- Light turquoise verdigris
    ["V"] = "#2d6e5f", -- Dark oxidized green
    
    -- Center Axle & Screws
    ["E"] = "#dce1eb"  -- Bolt steel shine
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
        line_str = "".join(r)
        res += f'    "{line_str}",\n'
    res += "}\n"
    return res

for i, f_data in enumerate(frames_grid):
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
sprite:saveCopyAs("output/aseprite/steam_gear_machine_64.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/steam_gear_machine_64.gif")

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
sheetSprite:saveCopyAs("output/Sheet/steam_gear_machine_64_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/steam_gear_machine_64.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/steam_gear_machine_64.lua successfully!")
