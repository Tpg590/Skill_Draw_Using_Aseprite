import os
import math
from refine_desert_scarf import clean_desert_frames, W, H

CHAR_MAP = {
    ".": ".",
    "S": "S",
    "#": "#",
    "D1": "E", # Sand bright highlight
    "D2": "D", # Sand golden base
    "D3": "V", # Sand shadow
    "W1": "T", # Wood highlight
    "W2": "U", # Wood midtone
    "W3": "M", # Wood deep shadow
    "M1": "I", # Iron marker highlight
    "M2": "J", # Iron marker shadow
    "C":  "C", # Soft dark cloth outline
    "K1": "Y", # Saffron silk crest glint
    "K2": "G", # Golden turmeric silk midtone
    "K3": "A", # Amber turmeric silk shadow
    "O1": "O", # Warm orange trim crest
    "O2": "R", # Terracotta orange trim shadow
}

frame_strings = []
for f_idx, fr in enumerate(clean_desert_frames):
    lines = []
    for y in range(H):
        row_chars = []
        for x in range(W):
            tok = fr[y][x]
            ch = CHAR_MAP[tok]
            row_chars.append(ch)
        line = "".join(row_chars)
        assert len(line) == 48, f"Row {y} in Frame {f_idx+1} length {len(line)} != 48"
        lines.append(line)
    assert len(lines) == 48, f"Frame {f_idx+1} has {len(lines)} lines != 48"
    frame_strings.append(lines)

print("Verified 4 frames: 48 lines x 48 characters.")

lua_code = """-- scripts/desert_scarf_post_48.lua
-- 48x48 Stardew Valley Animated Desert Scarf Post (Cột mốc sa mạc khăn lụa vàng viền cam)
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Desert_Scarf_Post"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley Art Style (Gam màu ấm, viền mềm, CẤM #000000)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#2c1e18", -- Bóng tiếp đất mềm dạng ellipse (Alpha 130)
    ["#"] = "#341c10", -- Viền mềm nâu đậm thân gỗ & cát (Soft dark outline)
    
    -- Gò cát sa mạc (Desert Sand Dune)
    ["E"] = "#f0c880", -- Sáng đỉnh gò cát (Sand bright highlight)
    ["D"] = "#d49b4c", -- Cát vàng sa mạc (Golden desert sand)
    ["V"] = "#9e682e", -- Bóng sườn cát (Desert sand shadow)
    
    -- Cột mốc gỗ cũ (Weathered Wooden Landmark Post)
    ["T"] = "#c4935a", -- Thớ sáng gỗ phong hóa (Wood highlight)
    ["U"] = "#8c5828", -- Thớ gỗ nâu ấm (Wood grain midtone)
    ["M"] = "#562e12", -- Vân rãnh nứt gỗ sâu (Wood deep crevice)
    ["I"] = "#d8c8b0", -- Bản đinh sắt cổ sáng (Iron plate highlight)
    ["J"] = "#706054", -- Bản đinh sắt cổ tối (Iron plate shadow)
    
    -- Dải khăn lụa vàng nghệ viền cam ấm (Turmeric Gold Silk & Orange Trim)
    ["C"] = "#4a1808", -- Viền sẫm mềm dải lụa (Cloth soft dark outline)
    ["Y"] = "#fff275", -- Ánh lụa sáng rực đỉnh sóng (Saffron silk crest glint)
    ["G"] = "#f0b824", -- Màu lụa vàng nghệ ấm (Golden turmeric silk midtone)
    ["A"] = "#b87a14", -- Vùng tối thân lụa rãnh sóng (Amber silk shadow)
    ["O"] = "#f06a18", -- Viền cam ấm sáng (Warm glowing orange trim)
    ["R"] = "#a63e0c"  -- Viền cam sẫm vùng tối (Terracotta orange trim shadow)
}

-- 2. Render Grid Function
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

-- 3. Ma trận ký tự 4 frame (Khóa tĩnh cột/gò cát 100%, Độ võng trọng lực, Tịnh tiến nếp sóng)
"""

for f_idx, lines in enumerate(frame_strings):
    lua_code += f"local f{f_idx+1}_grid = {{\n"
    for line in lines:
        lua_code += f'    "{line}",\n'
    lua_code += "}\n\n"

lua_code += """-- 4. Render các frame hoạt ảnh
renderGrid(image, f1_grid, PALETTE)

local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local img2 = layer:cel(2).image
renderGrid(img2, f2_grid, PALETTE)

local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local img3 = layer:cel(3).image
renderGrid(img3, f3_grid, PALETTE)

local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local img4 = layer:cel(4).image
renderGrid(img4, f4_grid, PALETTE)

-- 5. Xuất file CLI (Tuân thủ cấu trúc thư mục chuẩn)
sprite:saveCopyAs("output/aseprite/desert_scarf_post_48.aseprite")
sprite:saveCopyAs("output/gif/desert_scarf_post_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/desert_scarf_post_48_sheet.png")
sheetSprite:close()
"""

with open("scripts/desert_scarf_post_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_code)

print("Saved scripts/desert_scarf_post_48.lua successfully.")
