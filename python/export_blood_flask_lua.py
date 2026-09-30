import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_flask_roots import f1, f2, f3, f4

# Lua script generator for blood_flask_roots_48.lua

lua_content = """-- scripts/blood_flask_roots_48.lua
-- 48x48 FreeStyle Animated Blood Flask on Twisted Roots
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Flask_Roots"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: "." = transparent, "S" = ground contact shadow (Alpha 130)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#16080e", -- Deep wine-black outline
    ["S"] = "#180c12", -- Ground shadow (Alpha 130)
    
    -- Glass & Specular Gloss
    ["P"] = "#ffffff", -- Specular pure white highlight
    ["K"] = "#d2ebf5", -- Pale glass reflection
    ["J"] = "#505f6e", -- Dark glass rim
    
    -- Cork Stopper
    ["E"] = "#b98755", -- Cork light wood
    ["U"] = "#734b2d", -- Cork dark wood
    
    -- Glowing Crimson Liquid (Hue-shifting)
    ["W"] = "#ffffff", -- Hot bubble core
    ["Y"] = "#ffe15a", -- Glowing intense yellow
    ["R"] = "#ff3746", -- Radiant glowing crimson
    ["B"] = "#c31432", -- Deep ruby red
    ["Q"] = "#690a1e", -- Dark wine red shadow
    
    -- Twisted Roots with OSL Color Bleed
    ["H"] = "#ffa04b", -- OSL fiery peach highlight
    ["O"] = "#e65f23", -- OSL warm glowing orange
    ["T"] = "#a03219", -- OSL warm terracotta-red
    ["M"] = "#5a241a", -- Withered bark warm midtone
    ["D"] = "#301412", -- Withered bark dark shadow
    ["V"] = "#180a0c"  -- Deepest root crevice shadow
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

def format_grid(var_name, rows):
    res = f"local {var_name} = {{\n"
    for r in rows:
        res += f'    "{r}",\n'
    res += "}\n"
    return res

lua_content += format_grid("f1_grid", f1)
lua_content += format_grid("f2_grid", f2)
lua_content += format_grid("f3_grid", f3)
lua_content += format_grid("f4_grid", f4)

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

-- Export files according to workspace rules
sprite:saveCopyAs("output/aseprite/blood_flask_roots_48.aseprite")
sprite:saveCopyAs("output/gif/blood_flask_roots_48.gif")

-- Export horizontal Spritesheet
local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/blood_flask_roots_48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/blood_flask_roots_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/blood_flask_roots_48.lua successfully!")
