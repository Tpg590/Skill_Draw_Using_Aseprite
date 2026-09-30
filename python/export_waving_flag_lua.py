import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_waving_flag import frames, W, H

HEX_PALETTE = {
    ".": None,
    "S": "#1e1420",  # Soft ground shadow (Alpha 130)
    
    # Wooden Flagpole & Finial
    "#": "#361a0e",  # Soft dark wood outline
    "T": "#d79b55",  # Mast wood highlight
    "U": "#a06932",  # Mast wood midtone
    "M": "#693c1a",  # Mast wood shadow
    
    # Gold Finial & Flag Golden Trim
    "Y": "#fff0a0",  # Pure gold highlight
    "G": "#ffd23c",  # Golden trim bright
    "O": "#d7961e",  # Golden trim midtone
    "J": "#915a0f",  # Golden trim shadow / trough
    
    # Flag Cloth (Crimson Red with Crease Shading)
    "F": "#3a0c14",  # Flag soft dark outline
    "A": "#ff6941",  # Wave crest highlight (bright coral/cam)
    "B": "#e62d28",  # Wave crest bright red
    "R": "#b91923",  # Flag base rich crimson
    "C": "#820f1c",  # Wave trough deep red shadow
    "Z": "#4b0a14",  # Crevice darkest crimson/wine
    
    # Grass & Earthen Mound
    "E": "#73af37",  # Grass bright highlight
    "P": "#4b8723",  # Grass base green
    "N": "#2d5519",  # Grass shadow green
    "D": "#734626",  # Earth soil brown
    "V": "#442614",  # Earth deep soil
}

lua_content = """-- scripts/waving_flag_48.lua
-- 48x48 Stardew Valley Animated Waving Crimson Pennant Flag
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Waving_Flag"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley warm palette (soft outline, NO #000000)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e1420", -- Soft ground shadow (Alpha 130)
    
    -- Wooden Flagpole & Finial
    ["#"] = "#361a0e", -- Soft dark wood outline
    ["T"] = "#d79b55", -- Mast wood highlight
    ["U"] = "#a06932", -- Mast wood midtone
    ["M"] = "#693c1a", -- Mast wood shadow
    
    -- Gold Finial & Flag Golden Trim
    ["Y"] = "#fff0a0", -- Pure gold highlight
    ["G"] = "#ffd23c", -- Golden trim bright
    ["O"] = "#d7961e", -- Golden trim midtone
    ["J"] = "#915a0f", -- Golden trim shadow / trough
    
    -- Flag Cloth (Crimson Red with Crease Shading)
    ["F"] = "#3a0c14", -- Flag soft dark outline
    ["A"] = "#ff6941", -- Wave crest highlight (bright coral/cam)
    ["B"] = "#e62d28", -- Wave crest bright red
    ["R"] = "#b91923", -- Flag base rich crimson
    ["C"] = "#820f1c", -- Wave trough deep red shadow
    ["Z"] = "#4b0a14", -- Crevice darkest crimson/wine
    
    -- Grass & Earthen Mound
    ["E"] = "#73af37", -- Grass bright highlight
    ["P"] = "#4b8723", -- Grass base green
    ["N"] = "#2d5519", -- Grass shadow green
    ["D"] = "#734626", -- Earth soil brown
    ["V"] = "#442614"  -- Earth deep soil
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

-- Ensure output directories exist
-- (Handled by runner batch or OS)

-- Save Aseprite project
sprite:saveCopyAs("output/aseprite/waving_flag_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/waving_flag_48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/waving_flag_48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/waving_flag_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/waving_flag_48.lua successfully!")
