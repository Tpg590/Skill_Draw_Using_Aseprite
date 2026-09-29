-- scripts/blacksmith_forge_64.lua
-- 64x64 Terraria Style Animated Blacksmith Forge
-- 3 Frames Looping Fire Animation at 6 FPS

local width = 64
local height = 64
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Phong cách Terraria (Khối dày, viền sẫm tối #100c14, tương phản gắt)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#100c14", -- Viền sẫm đen đặc trưng Terraria (Near-black solid outline)
    ["S"] = "#0c0812", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Chất liệu gạch nung đỏ/xám sậm (Terracotta Red Brick Body)
    ["H"] = "#d46242", -- Gạch đón sáng (Brick highlight edge)
    ["L"] = "#a83d28", -- Gạch đỏ nung chính (Base red brick body)
    ["M"] = "#73271a", -- Gạch sắc độ sẫm (Dark brick tone)
    ["D"] = "#451712", -- Vùng tối & khe vữa (Mortar joint seam & shadow)
    ["V"] = "#210b0b", -- Rãnh nứt sâu & hốc tối gạch (Deepest brick fissure)

    -- Chất liệu kim loại ống khói & mái che (Heavy Iron Metal Hood & Chimney)
    ["P"] = "#ffffff", -- Đốm phản quang kim loại & đinh tán (Specular highlight & rivets)
    ["Q"] = "#a0a8b8", -- Thép sáng đón sáng (Light steel-iron facet)
    ["R"] = "#5a6275", -- Thép xám thân chính (Mid iron sheet body)
    ["T"] = "#323847", -- Thép vùng khuất sáng (Dark iron shadow)
    ["U"] = "#1c1f29", -- Rãnh nối kim loại đinh tán (Metal seam & joint crevice)

    -- Chiều sâu 3D lòng miệng lò (3D Hearth Cavity Depth)
    ["K"] = "#180e0c", -- Góc tối đen sâu trong hốc lò (Deep cavity black corners)
    ["G"] = "#521c10", -- Thành trong hắt ánh lửa (Fire glow on inner brick jamb)

    -- Ngoại lệ Palette cho ngọn lửa rực sáng & than hồng (Animated Roaring Fire & Coals)
    ["W"] = "#ffffff", -- Lõi lửa cực nhiệt trắng chói (White-hot core)
    ["Y"] = "#ffee55", -- Vàng rực rỡ (Brilliant yellow flame)
    ["O"] = "#ff8811", -- Cam rực lửa (Blazing orange flame)
    ["F"] = "#d92200", -- Đỏ lửa rìa ngoài (Deep scarlet outer flame)
    ["E"] = "#ffaa22"  -- Tàn lửa & than hồng bay (Flying spark / ember mote)
}

-- 2.frame1_grid: Frame 1 - Lửa bốc cao trung bình, cuộn sang trái, than hồng rực đỏ
local frame1_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "........................#PQQQRRRRRTTTTT#........................",
    "........................#PQQQRRRRRTTTTT#........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PQPQRRPQRTTT#.........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PPQQRRRRTTTT#.........................",
    "......................#PPQQQRRRRRRRRTTTTT#......................",
    "....................#PPQQQQRRRRRRRRRRRTTTTT#....................",
    "..................#PPQQQQQRRRRRRRRRRRRRTTTTTT#..................",
    "................#PPQQQQQQRRRRRRRRRRRRRRRTTTTTTT#................",
    "..............#PQPQRRPQRRPQRRPQRRPQRTTTPRTTTPRTTT#..............",
    "..............#UTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT#..............",
    "............#PPQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#............",
    "...........#PPQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#...........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    "............#VVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDDDD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLM#HLLLDDDDDDDDDDLLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#HLLDDDDDDDDDDDDLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#KKKK...E..E...KKKK#HLLMDHLLM#............",
    "............#HLLMDHLLMDMKKK...E...E..KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKKK...F..F...KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKK..FFOOFF...KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKK.FFOYYOOFF.KKKGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMK.FFOYYYYOOFF.KKGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMK.FOOYYYYYYOOF.KGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMKFOOYYWWYYOOFFKKGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMKFOYYWWWWYYOOFKKGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMKFOOYYWWWWYYOOFKGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMFFOYYWWWWWWYYOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOYYWWWWWWYYOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFYYWWWWWWYYOFFFGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMFFFOYYWWWWYYOFFFGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMFFFOOYYYYYYOOFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFFOOYYYYOOFFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFFFOOOOOOFFFFFGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMTTUTTYYYYTTUTTTTGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMFOYYOWWWOYYOFOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOOOOOOOOOOOFFFGLHLLMDHLLM#............",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#VVVVVVVVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDD#..........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    "....SSSS#HHLLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDD#SSSS....",
    "....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..............SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.............."
}

-- 2.frame2_grid: Frame 2 - Lửa bùng sáng cực đại, lõi bung tỏa, tàn lửa bay vào ống khói
local frame2_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "........................#PQQQRRRRRTTTTT#........................",
    "........................#PQQQRRRRRTTTTT#........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PQPQRRPQRTTT#.........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PPQQRRRRTTTT#.........................",
    "......................#PPQQQRRRRRRRRTTTTT#......................",
    "....................#PPQQQQRRRRRRRRRRRTTTTT#....................",
    "..................#PPQQQQQRRRRRRRRRRRRRTTTTTT#..................",
    "................#PPQQQQQQRRRRRRRRRRRRRRRTTTTTTT#................",
    "..............#PQPQRRPQRRPQRRPQRRPQRTTTPRTTTPRTTT#..............",
    "..............#UTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT#..............",
    "............#PPQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#............",
    "...........#PPQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#...........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    "............#VVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDDDD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLM#HLLLDDDDDDDDDDLLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#HLLDDDDDDDDDDDDLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#KKK.E..E..E..EKKKK#HLLMDHLLM#............",
    "............#HLLMDHLLMDMKK...E..E...EKKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKK...FFOOFF..KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKK..FOOYYOOF.KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMK.FFOYYYYOOFF.KKGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMK.FOOYYYYYYOOF.KGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMKFOOYYWWYYOOFFKKGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMKFOYYWWWWYYOOFKKGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMKFOOYYWWWWYYOOFKGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMFFOYYWWWWWWYYOOFGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMFFOYYWWWWWWYYOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFYYWWWWWWYYOFFFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOYYWWWWYYOFFFFGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMFFFOOYYYYYYOOFFFGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMFFFFOOYYYYOOFFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFFFOOOOOOFFFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFFFFOOOOFFFFFFGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMTTUTTYYYYTTUTTTTGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMOYYYYWWWWYYYYOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFFOOOOOOOOOFFFFGLHLLMDHLLM#............",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#VVVVVVVVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDD#..........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    "....SSSS#HHLLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDD#SSSS....",
    "....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..............SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.............."
}

-- 2.frame3_grid: Frame 3 - Lửa hạ hồi lưu, cuộn sang phải, ánh sáng phập phồng lặp chu kỳ
local frame3_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "........................#PQQQRRRRRTTTTT#........................",
    "........................#PQQQRRRRRTTTTT#........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PQPQRRPQRTTT#.........................",
    ".........................#UTTTTTTTTTTT#.........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    "..........................#PQQRRRRTTT#..........................",
    ".........................#PPQQRRRRTTTT#.........................",
    "......................#PPQQQRRRRRRRRTTTTT#......................",
    "....................#PPQQQQRRRRRRRRRRRTTTTT#....................",
    "..................#PPQQQQQRRRRRRRRRRRRRTTTTTT#..................",
    "................#PPQQQQQQRRRRRRRRRRRRRRRTTTTTTT#................",
    "..............#PQPQRRPQRRPQRRPQRRPQRTTTPRTTTPRTTT#..............",
    "..............#UTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT#..............",
    "............#PPQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#............",
    "...........#PPQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#...........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    ".........#PPQQQQQQQQQQQQQQRRRRRRRRRRRRRRRRRRTTTTTTTTTT#.........",
    "............#VVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDDDD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMD#............",
    "............#HLLMDHLLM#HLLLDDDDDDDDDDLLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#HLLDDDDDDDDDDDDLLH#HLLMDHLLM#............",
    "............#HLLMDHLLM#KKKK....E...E.KKKK#HLLMDHLLM#............",
    "............#HLLMDHLLMDMKKK....E....KKKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKKK...F..E...KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKKK..FFOOFF..KKKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMKK..FOOYYOOFF.KKGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMKK.FFOYYYYOOFF.KGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMK.FFOYYYYYYOOF.KGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMK.FOOYYWWYYOOF.KGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMKFOOYYWWYYOOFFKKGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMKFOYYWWWWYYOOFKKGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMKFOOYYWWWWYYOOFKGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOYYWWWWWWYYOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOYYWWWWWWYYOOFGLHLLMDHLLM#............",
    "............#DDDDDDDDDDMFFYYWWWWWWYYOFFFGLDDDDDDDDD#............",
    "............#HMDHLLLLMDMFFFOYYWWWWYYOFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFOOYYYYYYOOFFFGLHLLLLMDHM#............",
    "............#HMDHLLLLMDMFFFFOOYYYYOOFFFFGLHLLLLMDHM#............",
    "............#DDDDDDDDDDMTTUTTYYYYTTUTTTTGLDDDDDDDDD#............",
    "............#HLLMDHLLMDMFOYYOWWWOYYOFOOFGLHLLMDHLLM#............",
    "............#HLLMDHLLMDMFFOOOOOOOOOOOFFFGLHLLMDHLLM#............",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HHLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#HLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDD#..........",
    "..........#VVVVVVVVVVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDDDD#..........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#HHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDD#.........",
    ".........#DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    ".........#HMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLLLMDHLLMDD#.........",
    "....SSSS#HHLLLLLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDD#SSSS....",
    "....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..............SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.............."
}

-- 3. Hàm render lưới ký tự lên Canvas Cel
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

-- Render Frame 1: Khởi đầu chu kỳ lửa bốc
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Lửa bùng sáng cực đại
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Lửa hạ hồi lưu chuẩn bị lặp chu kỳ
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/blacksmith_forge_64.aseprite")

-- B. Nếu là Animation: xuất GIF động và dải spritesheet ngang độc lập CLI
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/blacksmith_forge_64.gif")
    
    -- Tự động ghép nối các frame thành 1 dải Spritesheet ngang không lo lỗi giao diện
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/blacksmith_forge_64_sheet.png")
    sheetSprite:close()
else
    -- Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
    sprite:saveCopyAs("output/blacksmith_forge_64.png")
end
