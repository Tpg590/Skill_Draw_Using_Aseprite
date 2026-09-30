import os
from design_poison_flask_shaking import frames, PALETTE_HEX, W, H

LUA_PATH = "scripts/poison_flask_shaking.lua"

palette_lua_entries = []
for k, v in PALETTE_HEX.items():
    if v is None:
        palette_lua_entries.append(f'    ["{k}"] = nil,')
    else:
        palette_lua_entries.append(f'    ["{k}"] = "{v}",')
pal_str = "\n".join(palette_lua_entries)

grids_lua = []
for idx, g in enumerate(frames):
    lines = [f"local frame{idx+1}_grid = {{"]
    for row in g:
        line_str = "".join(row)
        assert len(line_str) == W, f"Row length error in frame {idx+1}: {len(line_str)}"
        lines.append(f'    "{line_str}",')
    lines.append("}\n")
    grids_lua.append("\n".join(lines))

full_grids_str = "\n".join(grids_lua)

lua_script_content = f"""-- scripts/poison_flask_shaking.lua
-- 48x48 Shaking Poison Flask Animation (6 Frames, 6 FPS)
-- Art Style: FreeStyle (Hue-shifting Neon Pink to Deep Violet, Static Specular Highlight)

local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Poison_Flask"

sprite.frames[1].duration = frameDuration

local PALETTE = {{
{pal_str}
}}

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

-- Export outputs
sprite:saveCopyAs("output/aseprite/poison_flask_shaking.aseprite")
sprite:saveCopyAs("output/gif/poison_flask_shaking.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/poison_flask_shaking_sheet.png")
sheetSprite:close()
sprite:close()
"""

os.makedirs("scripts", exist_ok=True)
with open(LUA_PATH, "w", encoding="utf-8") as f:
    f.write(lua_script_content)

print(f"Generated {LUA_PATH} successfully.")
