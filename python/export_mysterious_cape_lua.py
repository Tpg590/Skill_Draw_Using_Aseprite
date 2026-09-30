import os
from perfect_tail_sculptor import clean_frames, W, H

# Mapping from multi-char tokens to single characters
CHAR_MAP = {
    ".": ".",
    "S": "S",
    "#": "#",
    "P1": "P", # Bright orchid highlight
    "P2": "V", # Royal purple midtone
    "P3": "D", # Shadow purple
    "P4": "Z", # Deep crevice darkest purple
    "Y1": "Y", # Specular gold highlight
    "Y2": "G", # Warm gold midtone
    "Y3": "O", # Shadow bronze gold
    "M1": "L", # Stone highlight
    "M2": "M", # Stone midtone
    "M3": "N", # Stone shadow
    "K":  "K", # Pitch black void under hood
    "E1": "A", # Glowing cyan arcane highlight
    "E2": "B", # Glowing cyan arcane shade
}

# Convert each frame to list of 48-char strings
frame_strings = []
for f_idx, fr in enumerate(clean_frames):
    lines = []
    for y in range(H):
        row_chars = []
        for x in range(W):
            token = fr[y][x]
            ch = CHAR_MAP[token]
            row_chars.append(ch)
        line = "".join(row_chars)
        assert len(line) == 48, f"Row {y} in Frame {f_idx+1} length is {len(line)} != 48"
        lines.append(line)
    assert len(lines) == 48, f"Frame {f_idx+1} has {len(lines)} lines != 48"
    frame_strings.append(lines)

print("All 4 frames verified: 48 lines x 48 characters.")

lua_code = """-- scripts/mysterious_cape_statue_48.lua
-- 48x48 Terraria Animated Mysterious Cape Statue (Bức tượng bán thân bục ma thuật áo choàng tím viền vàng)
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Mysterious_Cape_Statue"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria Art Style (Thương phẩm chuẩn kỹ thuật)
-- "." là trong suốt, "S" là bóng tiếp đất (Alpha 130)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#160a1e", -- Ground contact shadow (Alpha 130)
    ["#"] = "#120c18", -- Viền sẫm tối Terraria (Near-black deep purple night)
    
    -- Áo choàng bí ẩn màu tím sẫm (Deep Royal Purple Cloth)
    ["P"] = "#a65cd8", -- Đỉnh sóng sáng rực (Wave crest orchid highlight)
    ["V"] = "#6c2e98", -- Màu nền tím hoàng gia (Rich royal purple midtone)
    ["D"] = "#3c165c", -- Vùng tối tà áo (Wave trough shadow purple)
    ["Z"] = "#220c36", -- Rãnh nếp gấp tối thẳm (Deep crease velvet purple)
    
    -- Viền vàng & Trâm cài ma thuật (Burnished Gold Trim & Brooch)
    ["Y"] = "#ffeb78", -- Điểm phản quang viền vàng (Specular gold glint)
    ["G"] = "#e0a020", -- Viền vàng rực (Warm gold midtone)
    ["O"] = "#8a520a", -- Bóng đồng sẫm viền vàng (Shadow bronze gold)
    
    -- Bục đá cổ & Bán thân (Ancient Carved Stone Pedestal & Mount)
    ["L"] = "#98a4b8", -- Gờ sáng đá (Stone highlight)
    ["M"] = "#5e6a7e", -- Thân đá nhám (Stone midtone with micro-cracks)
    ["N"] = "#343a4a", -- Vùng tối bục đá (Stone deep shadow)
    
    -- Vực thẳm huyền bí & Cổ tự ma thuật phát sáng (OSL Exception)
    ["K"] = "#0a060f", -- Hố đen tuyệt đối che giấu khuôn mặt dưới mũ trùm (Face void)
    ["A"] = "#70ffff", -- Mắt ma thuật & Cổ tự phát sáng (Cyan arcane glow highlight)
    ["B"] = "#26a0c4"  -- Quầng sáng ma thuật (Cyan arcane glow shade)
}

-- 2. Render function
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

-- 3. Ma trận ký tự 4 frame (Khóa tĩnh bục/vai 100%, Pha truyền sóng vải X_1 < X_2 < X_3 < X_4)
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
sprite:saveCopyAs("output/aseprite/mysterious_cape_statue_48.aseprite")
sprite:saveCopyAs("output/gif/mysterious_cape_statue_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/mysterious_cape_statue_48_sheet.png")
sheetSprite:close()
"""

with open("scripts/mysterious_cape_statue_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_code)

print("Generated scripts/mysterious_cape_statue_48.lua successfully.")
