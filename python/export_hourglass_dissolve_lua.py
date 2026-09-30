import os
from design_hourglass_dissolve import frames, W, H

LUA_PATH = "scripts/golden_hourglass_dissolve_48.lua"

PALETTE_LUA = """local PALETTE = {
    ["."] = nil,
    ["S"] = "#1a1620", -- Soft contact ground shadow (Alpha 130)
    ["#"] = "#281008", -- Clean dark brown/copper outline
    
    -- Ornate Gold Frame (Hue-shifting gold -> orange -> burnt sienna)
    ["A"] = "#fff090", -- Specular gold highlight
    ["B"] = "#ffcc30", -- Radiant gold midtone
    ["C"] = "#d87810", -- Warm orange/amber shadow
    ["D"] = "#803810", -- Deep copper/crevice shadow
    
    -- Golden Sand Particles & Flow
    ["G"] = "#ffe650", -- Glowing sand highlight
    ["F"] = "#f0a820", -- Sand grain midtone
    ["O"] = "#b86810", -- Sand grain shadow
    
    -- Clear Glass & Reflection Glints
    ["W"] = "#ffffff", -- Pure white glint
    ["L"] = "#e0f4ff", -- Glass reflection tint
    ["T"] = "#a0c8e0", -- Glass shaded rim
    
    -- Ancient Stone Dais / Plinth
    ["M"] = "#9098a0", -- Stone highlight
    ["N"] = "#5c646c", -- Stone midtone
    ["P"] = "#343840"  -- Stone deep shadow
}
"""

def grid_to_lua_table(g, name):
    lines = [f"local {name} = {{"]
    for row in g:
        line_str = "".join(row)
        assert len(line_str) == W, f"Row length error: {len(line_str)}"
        lines.append(f'    "{line_str}",')
    lines.append("}\n")
    return "\n".join(lines)

grids_lua = []
for idx, g in enumerate(frames):
    grids_lua.append(grid_to_lua_table(g, f"frame{idx+1}_grid"))

full_grids_str = "\n".join(grids_lua)

lua_script_content = f"""-- scripts/golden_hourglass_dissolve_48.lua
-- 48x48 Golden Hourglass Wind Dissolution Animation (6 Frames, 8 FPS)
-- Art Style: FreeStyle (Hue-Shifting Gold/Amber & Directional Wind Erosion)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Hourglass_Dissolve"

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

-- Create and Render Frames 2 to 6 with clean cel initialization
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
sprite:saveCopyAs("output/aseprite/golden_hourglass_dissolve_48.aseprite")
sprite:saveCopyAs("output/gif/golden_hourglass_dissolve_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/golden_hourglass_dissolve_48_sheet.png")
sheetSprite:close()
sprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open(LUA_PATH, "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Generated {LUA_PATH} successfully.")
