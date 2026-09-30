import os
from design_mechanical_beetle import frames, W, H

LUA_PATH = "scripts/mechanical_turtle_beetle_48.lua"

PALETTE_LUA = """local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e1218", -- Soft contact ground shadow (Alpha 130)
    ["#"] = "#2a1610", -- Warm dark espresso outline (NO #000000)
    
    -- Polished Warm Brass / Gold Filigree
    ["A"] = "#ffe680", -- Specular brass highlight
    ["B"] = "#e6a820", -- Warm polished brass midtone
    ["C"] = "#9c6410", -- Shaded bronze/brass
    ["D"] = "#5c360c", -- Deep bronze recess
    
    -- Warm Hardwood Carapace Shell (Turtle plates)
    ["W"] = "#c87830", -- Shell highlight wood plate
    ["X"] = "#9e4a18", -- Shell warm amber midtone
    ["Z"] = "#5a240c", -- Shell deep mahogany shadow
    ["K"] = "#381408", -- Shell seam crevice
    
    -- Clockwork Gears & Mechanical Claw Legs (Iron/Bronze alloy)
    ["H"] = "#b4bec8", -- Metal leg highlight
    ["M"] = "#78828e", -- Metal leg midtone
    ["L"] = "#444c58", -- Metal leg shadow
    
    -- Glowing Topaz Eyes / Clockwork Energy Core
    ["E"] = "#ffee66", -- Glowing topaz yellow
    ["Q"] = "#e69000"  -- Deep amber glow
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

lua_script_content = f"""-- scripts/mechanical_turtle_beetle_48.lua
-- 48x48 Mechanical Turtle Beetle Walk Cycle (4 Frames, 6 FPS)
-- Art Style: Stardew Valley (Warm Brass, Hardwood Carapace, Diagonal Gait)

local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Turtle_Beetle"

-- Configure Frame 1 duration
sprite.frames[1].duration = frameDuration

{PALETTE_LUA}

{full_grids_str}

local frame_grids = {{
    frame1_grid,
    frame2_grid,
    frame3_grid,
    frame4_grid
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

-- Create and Render Frames 2 to 4 with clean cel initialization
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
sprite:saveCopyAs("output/aseprite/mechanical_turtle_beetle_48.aseprite")
sprite:saveCopyAs("output/gif/mechanical_turtle_beetle_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/mechanical_turtle_beetle_48_sheet.png")
sheetSprite:close()
sprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open(LUA_PATH, "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Generated {LUA_PATH} successfully.")
