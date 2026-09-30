import os
from test_flawless_tail import frames, W, H

LUA_PATH = "scripts/scorpion_tail_strike_48.lua"

# Palette definition according to rules:
# "." is nil, "S" is alpha 130
PALETTE_LUA = """local PALETTE = {
    ["."] = nil,
    ["S"] = "#0a101a", -- Soft contact ground shadow (Alpha 130)
    ["#"] = "#0c101a", -- Clean dark navy-black outline
    
    -- Cold Blue-Steel Armor (FreeStyle)
    ["A"] = "#d8e8f6", -- Silvery specular highlight
    ["B"] = "#8aa0ba", -- Cold blue-gray steel midtone
    ["C"] = "#40526c", -- Deep navy-slate steel shadow
    ["D"] = "#1a2434", -- Dark crevice seam / recess
    
    -- Glowing Cyan Stinger & Plasma OSL
    ["W"] = "#ffffff", -- White-hot stinger tip / plasma core
    ["E"] = "#40f0ff", -- Radiant cyan plasma
    ["Q"] = "#14a4d8", -- Cyan glow halo / OSL bleed
    ["T"] = "#0c5488", -- Deep cyan aura shadow
    
    -- Brass Pivot Bolts & Mechanical Accents
    ["K"] = "#f4b038", -- Polished brass bolt highlight
    ["J"] = "#945c18", -- Bronze bolt shadow
    
    -- Stone Dais / Foundation
    ["M"] = "#828e9a", -- Stone highlight
    ["N"] = "#525e6c", -- Stone midtone
    ["P"] = "#2c3442"  -- Stone deep shadow
}
"""

def grid_to_lua_table(g, name):
    lines = [f"local {name} = {{"]
    for row in g:
        line_str = "".join(row)
        lines.append(f'    "{line_str}",')
    lines.append("}\n")
    return "\n".join(lines)

grids_lua = []
for idx, g in enumerate(frames):
    grids_lua.append(grid_to_lua_table(g, f"frame{idx+1}_grid"))

full_grids_str = "\n".join(grids_lua)

lua_script_content = f"""-- scripts/scorpion_tail_strike_48.lua
-- 48x48 Mechanical Scorpion Tail Whip-Strike (6 Frames, 8 FPS)
-- Art Style: FreeStyle (Cold Blue-Steel & Radiant Cyan Plasma)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Scorpion_Tail"

-- Configure Frame 1 duration
sprite.frames[1].duration = frameDuration

{PALETTE_LUA}

{full_grids_str}

local frame_grids = {{
    frame1_grid,
    frame2_grid,
    frame3_grid,
    frame4_grid,
    frame5_grid,
    frame6_grid
}}

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
                img:drawPixel(x - 1, y - 1, Color{{ r = r, g = g, b = b, a = a }})
            end
        end
    end
end

-- Render Frame 1
local img1 = sprite.cels[1].image
img1:clear()
renderGrid(img1, frame_grids[1], PALETTE)

-- Create and Render Frames 2 to 6
for i = 2, #frame_grids do
    local newFrame = sprite:newFrame()
    newFrame.duration = frameDuration
    local cel = layer:cel(i)
    if not cel then
        cel = sprite:newCel(layer, newFrame)
    end
    cel.image:clear()
    renderGrid(cel.image, frame_grids[i], PALETTE)
end

-- Save outputs as required
sprite:saveCopyAs("output/aseprite/scorpion_tail_strike_48.aseprite")
sprite:saveCopyAs("output/gif/scorpion_tail_strike_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/scorpion_tail_strike_48_sheet.png")
sheetSprite:close()
sprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open(LUA_PATH, "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Generated {LUA_PATH} successfully.")
