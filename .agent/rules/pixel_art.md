---
trigger: always_on
---

# 🎨 2D Pixel Top-Down Skill Guide for Aseprite (Core)

Tài liệu này là quy chuẩn kỹ thuật bắt buộc để AI tạo pixel art thương phẩm thông qua Aseprite Lua Script. Mỗi phản hồi tạo ảnh phải sinh ra một file script Lua (`scripts/<ten_file>.lua`) hoàn chỉnh, tự chứa mã nguồn thực thi độc lập qua lệnh Aseprite CLI.

## 1. Cấu hình ban đầu
AI bắt buộc xác nhận 5 thông số cốt lõi:
*   **Grid Size:** `32x32`, `48x48`, `64x64`, hoặc custom (1 cell/frame).
*   **Art Style:** `Terraria`, `Stardew Valley`, `FreeStyle`.
*   **Asset Type:** `Individual Sprite`, `Tilemap`, `Spritesheet`.
*   **Output Type:** `Static`, `Animation`.
*   **Animation FPS:** `4`, `6`, `8`, `12`, `16`, `24` (Mặc định `8`).

## 2. Đặc tả phong cách nghệ thuật
1.  **Terraria:** Khối dày, gồ ghề. Tương phản cao, viền sẫm tối (gần đen) bao quanh khối. Dùng dăm pixel nhỏ tạo độ nhám, rạn nứt.
2.  **Stardew Valley:** Tươi sáng, ấm cúng. Góc nghiêng Top-Down 3/4. Viền ngoài mềm (dùng màu tối của vật thể, CẤM viền #000000). Luôn có bóng râm tiếp đất (`S`) hình ellipse mềm mại.
3.  **FreeStyle:** Bắt buộc hue-shifting (sáng ngả vàng/cam, tối ngả tím/xanh). Giữ nét sạch, không jaggies.

## 3. Các cấm kỵ mỹ thuật cốt lõi
1.  **CẤM BANDING:** Không xếp pixel cùng màu thành cột thẳng đứng trên mặt phẳng. Sáng tối phải rải đều.
2.  **GIỚI HẠN PALETTE:** 1 màu Viền + 3 sắc độ chính (Sáng/Nền/Tối) + 2 màu phụ kiện.
    *   *NGOẠI LỆ:* Được khai báo thêm tối đa 3 màu phụ (VD: `#ffd700`, `#00ffff`) cho vật phẩm trong lòng hòm, kho báu hoặc nguồn sáng ma thuật.
3.  **TÁCH KHỐI (OVERHANG):** Nắp hòm/mái hiên PHẢI nhô rộng hơn thân dưới ít nhất 1–2 pixel mỗi bên, có rãnh bóng tối dưới gờ.
    *   *TOÁN HỌC OVERHANG:* Nếu thân rộng từ block 10 đến 30 (20 block), thì mái/nắp BẮT BUỘC rộng từ block 9 đến 31 (22 block).
4.  **CĂN ĐÁY (GROUND ALIGNMENT):** Đáy và bóng râm (`S`) của vật thể phải nằm cố định sát mép dưới canvas. Cấm bay lơ lửng.
5.  **CẤM JAGGIES:** Bo góc phải đều (1-1-2-2). Cấm pixel thừa ở góc 90 độ. Khi co giãn (Squash & Stretch), phải duy trì đường cong bo viền mượt mà.
6.  **CẤM DITHERING & CÔNG THỨC VÂN GỖ:** Tuyệt đối không dùng pixel xếp chéo (caro) để lấp mảng trống.
    *   *Ép buộc cho Gỗ:* Ván ngang dùng vệt 3-5 ký tự. Cột dọc dùng chuỗi 2-4 ký tự dọc. Đan xen màu (VD: `A A B A A`) tạo sọc rãnh. Cấm dùng hạt lấm tấm.
7.  **CHIỀU SÂU LÒNG CƠ BẢN:**
    *   *Mở nắp:* Vẽ thành rương bên trong (dày 2-3px), đổ bóng xiên từ trái sang đáy.
    *   *Bồn chứa/Chất lỏng:* Chừa 1-2 dòng pixel mô tả *mặt trong thành bồn* nằm CẢN TRƯỚC và CAO HƠN mặt chất lỏng, có rãnh bóng đổ xuống mặt nước.
8.  **CẤU TRÚC HỮU CƠ CƠ BẢN:** Tuyệt đối không vẽ cành cây hoặc rễ bằng các đường chéo 1-pixel thẳng tắp (45 độ). Cành/rễ phải có độ cong và vuốt thon dần.

## 4. Quy tắc Animation cốt lõi
1.  **Khóa trục tĩnh (Hinge & Base Anchoring):** Khi làm hoạt ảnh, tọa độ Y của đường bản lề, thân cấu trúc tĩnh và bóng tiếp đất (`S`) phải **giữ nguyên không đổi** trên tất cả frames.
2.  **Động học mở nắp:** Nắp ngửa ra sau (thu hẹp chiều cao Y của nắp), lộ vùng bóng tối sâu nhất dưới đáy rương.
3.  **Tilemap Liền Mạch:** Cột ký tự đầu tiên bên trái và cột cuối cùng bên phải BẮT BUỘC khớp nhau 100% về cao độ (Y) và màu sắc.
4.  **Looping mượt mà:** Frame đầu và frame cuối phải liên kết nhịp nhàng với nhau nếu là hoạt ảnh chu kỳ.
5.  **Biên độ biến đổi khối tối thiểu:** Các hoạt ảnh lặp tại chỗ phải thay đổi vị trí/màu sắc pixel giữa các frame tối thiểu 10%–20% diện tích khối để tránh cảm giác bị đơ.

## 5. Cấu trúc mã Aseprite Lua API
Mọi script sinh ra phải tuân thủ khung mã lệnh và xuất file an toàn qua CLI:

```lua
-- scripts/<ten_file>.lua
local width = 32
local height = 32
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: "." là trong suốt, "S" là bóng tiếp đất (Alpha 130)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#2c1710", -- Viền sẫm
    ["A"] = "#f4b41b", -- Vùng sáng
    ["B"] = "#e67e22", -- Màu chính
    ["C"] = "#9c3d10", -- Vùng tối
    ["S"] = "#1e1423"  -- Bóng đất tiếp xúc
}

-- 2. Ma trận ký tự (Đảm bảo số dòng = height)
local frame1_grid = {
    "................................",
    "................................",
    ".............######.............",
    "............#AAAAAA#............",
    "...........#AABBBBAA#...........",
    "...........#BBBBBBBB#...........",
    "...........#BBCCCCBB#...........",
    "............#CCCCCC#............",
    ".............######.............",
    "..............#BB#..............",
    "..............#CC#..............",
    ".............#CCCC#.............",
    "............#CCCCCC#............",
    "...........SSSSSSSSSS...........",
    "............SSSSSSSS............",
    "................................"
}

-- 3. Render
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
renderGrid(image, frame1_grid, PALETTE)

-- 4. Xuất file CLI theo đúng cấu trúc Workspace
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