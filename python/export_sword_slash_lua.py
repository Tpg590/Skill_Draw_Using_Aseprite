import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_sword_slash import frames, W, H

lua_content = """-- scripts/sword_slash_48.lua
-- 48x48 FreeStyle Animated Knight Sword Arc Slash (8 FPS)
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Sword_Slash"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: FreeStyle High-Contrast Cyan & Steel Palette
local PALETTE = {
    ["."] = nil,
    
    -- Radiant Arc Energy & Magical Light (Core to Rim Hue-Shifting)
    ["W"] = "#ffffff", -- Radiant pure white core
    ["H"] = "#cdfaef", -- Soft cyan-white glow
    ["A"] = "#2df0ff", -- Electric neon cyan
    ["B"] = "#00b4eb", -- Vibrant cyan
    ["C"] = "#0073af", -- Deep cyan shadow
    ["D"] = "#0f375f", -- Outer magical navy outline
    ["Z"] = "#061930", -- Deepest navy crevice
    
    -- Knight Sword Polished Steel Blade
    ["L"] = "#e6f2fa", -- Polished steel highlight
    ["M"] = "#9bb4c8", -- Steel midtone
    ["K"] = "#556e87", -- Steel shadow
    ["X"] = "#283a4e", -- Steel dark outline
    
    -- Gilded Gold Crossguard & Pommel
    ["Y"] = "#ffeb78", -- Gold highlight
    ["G"] = "#e6aa23", -- Rich gold midtone
    ["O"] = "#9b5f12", -- Gold shadow
    ["Q"] = "#4b2a0a", -- Dark gold outline
    
    -- Leather Grip
    ["U"] = "#87411e", -- Leather grip highlight
    ["V"] = "#461e0c"  -- Dark leather shadow
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
                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = 255 })
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
-- Render Frame 1 (Anticipation)
renderGrid(image, f1_grid, PALETTE)

-- Render Frame 2 (Smear Arc Slash VFX)
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local img2 = layer:cel(2).image
renderGrid(img2, f2_grid, PALETTE)

-- Render Frame 3 (Impact & Shattered Sparks)
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local img3 = layer:cel(3).image
renderGrid(img3, f3_grid, PALETTE)

-- Render Frame 4 (Recovery & Runic Pulse)
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local img4 = layer:cel(4).image
renderGrid(img4, f4_grid, PALETTE)

-- Save Aseprite project
sprite:saveCopyAs("output/aseprite/sword_slash_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/sword_slash_48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/sword_slash_48_sheet.png")
sheetSprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open("scripts/sword_slash_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_content)

print("Exported scripts/sword_slash_48.lua successfully!")
