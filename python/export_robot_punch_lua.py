import os
from test_flawless_punch import frames, W, H

LUA_PATH = "scripts/robot_piston_punch_48.lua"

PALETTE_LUA = """local PALETTE = {
    ["."] = nil,
    ["S"] = "#0e1016", -- Soft ground contact shadow (Alpha 130)
    ["#"] = "#101218", -- Terraria near-black heavy outline
    
    -- Cast Iron / Heavy Armor Steel (Terraria high contrast)
    ["A"] = "#e0eaf4", -- Specular steel highlight / chrome glint
    ["B"] = "#92a0b2", -- Steel armor midtone
    ["C"] = "#4c586a", -- Dark steel shadow
    ["D"] = "#262c38", -- Deep crevice / seam / joint recess
    
    -- Hydraulic Chrome Piston & Spikes
    ["W"] = "#ffffff", -- Pure white glint / spike tip / steam core
    ["L"] = "#b4cce0", -- Chrome cylinder body
    
    -- Bronze Rivets & Pivot Pins
    ["K"] = "#f0b43c", -- Polished brass rivet highlight
    ["J"] = "#946018", -- Bronze rivet shadow
    
    -- Gauge & Exhaust Steam
    ["R"] = "#e64030", -- Pressure gauge warning red
    ["V"] = "#c4def2", -- Steam puff midtone
    ["U"] = "#7c98b6", -- Steam puff trailing shadow (Alpha 180)
    
    -- Industrial Workshop Floor Foundation Plinth
    ["M"] = "#88909a", -- Stone plinth highlight
    ["N"] = "#58606c", -- Stone plinth midtone
    ["P"] = "#343a46"  -- Stone plinth shadow
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

lua_script_content = f"""-- scripts/robot_piston_punch_48.lua
-- 48x48 Robotic Piston Punch Arm (6 Frames, 8 FPS)
-- Art Style: Terraria (High Contrast Heavy Steel & Dynamic Piston Strike)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Robot_Piston_Punch"

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
                local a = 255
                if char == "S" then
                    a = 130
                elseif char == "U" then
                    a = 180
                end
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
sprite:saveCopyAs("output/aseprite/robot_piston_punch_48.aseprite")
sprite:saveCopyAs("output/gif/robot_piston_punch_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/robot_piston_punch_48_sheet.png")
sheetSprite:close()
sprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open(LUA_PATH, "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Generated {LUA_PATH} successfully.")
