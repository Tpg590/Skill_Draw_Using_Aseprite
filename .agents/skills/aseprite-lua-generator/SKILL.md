---
name: aseprite-lua-generator
description: >-
  Kỹ năng khởi tạo khung mã nguồn Aseprite Lua API độc lập qua ma trận ký tự
  trực quan cho dải kích thước chuẩn 16x16 đến 64x64 và render tự động qua CLI.
---

# 🛠️ Aseprite Lua Script Generation Skill

Kỹ năng này hướng dẫn AI khởi tạo file mã nguồn Lua hoàn chỉnh cho Aseprite API, ánh xạ ma trận ký tự thành pixel màu và tự động xuất thành phẩm ra đúng 3 thư mục `output/`.

---

## 1. Phạm Vi Kích Thước Áp Dụng (16x16 đến 64x64)
*   Áp dụng tối ưu cho các kích thước: `16x16`, `32x32`, `48x48`, `64x64` (hoặc custom trong dải 16–64).
*   Toàn bộ frame được biểu diễn bằng ma trận chuỗi ký tự ASCII (`frames_data`), đảm bảo kiểm soát chính xác từng pixel mà không bao giờ lo vượt ngưỡng token limit.

---

## 2. Khung Mã Nguồn Chuẩn (`scripts/<ten_file>.lua`)

Mọi file script Lua sinh ra bắt buộc tuân theo bộ khung chuẩn sau:

```lua
-- scripts/<ten_file>.lua
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration

-- 1. Định nghĩa Palette (Ký tự ánh xạ mã Hex)
-- "." là trong suốt (nil), "S" là bóng tiếp đất (Alpha 130)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#1a1016", -- Viền sẫm
    ["A"] = "#f4b41b", -- Vùng sáng / Highlight
    ["B"] = "#e67e22", -- Màu chính / Midtone
    ["C"] = "#8c3814", -- Vùng tối / Shadow
    ["S"] = "#140c1a"  -- Bóng đất tiếp xúc (Alpha 130)
}

-- 2. Ma trận ký tự các Frame (Số dòng = height, độ dài mỗi dòng = width)
local frames_data = {
    -- Frame 1
    {
        "................................................",
        -- (... Đủ height dòng cho Frame 1 ...)
    },
    -- Frame 2
    {
        "................................................",
        -- (... Đủ height dòng cho Frame 2 ...)
    }
}

-- 3. Hàm Render ma trận vào Image Cel
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

-- 4. Tạo Frame và vẽ dữ liệu
local img1 = sprite.cels[1].image
img1:clear()
renderGrid(img1, frames_data[1], PALETTE)

for i = 2, #frames_data do
    local newFrame = sprite:newFrame()
    newFrame.duration = frameDuration
    local cel = layer:cel(i)
    if not cel then
        cel = sprite:newCel(layer, newFrame)
    end
    cel.image:clear()
    renderGrid(cel.image, frames_data[i], PALETTE)
end

-- 5. Xuất file theo đúng quy chuẩn cấu trúc thư mục
sprite:saveCopyAs("output/aseprite/<ten_file>.aseprite")
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/gif/<ten_file>.gif")
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/Sheet/<ten_file>_sheet.png")
    sheetSprite:close()
else
    sprite:saveCopyAs("output/Sheet/<ten_file>.png")
end