-- scripts/green_potion_32.lua
-- 32x32 Stardew Valley Animated Green Potion in Spherical Glass Flask
-- 4 Frames Looping Rising Bubbles Animation at 8 FPS

local width = 32
local height = 32
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley (Gam màu ấm cúng, viền mềm không viền đen, bóng râm S)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#1a3330", -- Viền sẫm xanh lam xám mềm (Soft dark teal outline, no pure black)
    ["S"] = "#181220", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Nút bần (Cork Stopper)
    ["K"] = "#f0b669", -- Sáng nút bần đón sáng (Cork highlight)
    ["N"] = "#ae6224", -- Thân nút bần nâu ấm (Cork midtone)
    ["J"] = "#5a2810", -- Vùng tối nút bần (Cork shadow)

    -- Vỏ bình thủy tinh trong suốt (Transparent Glass Flask & Specular Highlight)
    ["W"] = "#ffffff", -- Vệt sáng cong phản quang trơn bóng vắt ngang bình (Specular highlight)
    ["T"] = "#d0efe5", -- Sắc thủy tinh sáng (Light glass reflection)
    ["U"] = "#74a89e", -- Thân thủy tinh trong (Mid glass body tint)
    ["Z"] = "#355e58", -- Thủy tinh khuất sáng & khúc xạ (Dark glass refraction)
    ["X"] = "#24443f", -- Đường viền đáy thủy tinh lộ rõ dưới đáy (Glass bottom contour)

    -- Chất lỏng ma thuật xanh lục (Magical Green Liquid & Meniscus)
    ["L"] = "#90f488", -- Viền bề mặt chất lỏng hình ellipse (Meniscus ellipse rim)
    ["G"] = "#44d655", -- Xanh lục ma thuật phát sáng (Bright glowing green)
    ["M"] = "#1ea838", -- Thân chất lỏng xanh lục (Mid green liquid)
    ["D"] = "#0e6620", -- Vùng sâu tối của chất lỏng (Deep green liquid shadow)
    ["V"] = "#084014", -- Chất lỏng đáy bình (Deepest liquid shade)

    -- Bọt khí sủi tăm (Animated Rising Bubbles)
    ["B"] = "#b8ffaa", -- Thân bọt khí xanh nhạt (Light green bubble dome)
    ["b"] = "#ffffff"  -- Đốm sáng bọt khí & bọt vỡ trên mặt nước (Bubble glint & pop mote)
}

-- 2.frame1_grid: Frame 1 - Bọt khí sinh ra từ đáy bình, bọt phải lơ lửng giữa lòng chất lỏng
local frame1_grid = {
    "................................",
    "................................",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    "...........#WTTUUZZZ#...........",
    "............#TTUUZZ#............",
    "............#WTTUUZ#............",
    "............#TTTUUZ#............",
    "...........#WTTTUUZZ#...........",
    ".........#TTWTTTTTUUZZ#.........",
    ".......#TWWTTTTTTTTUUUZZ#.......",
    "......#TWTTTTTTTTTTTUUUZZ#......",
    ".....#TWTTTTTTTTTTTTTUUUZZ#.....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTLGGGGGGGGGGDDUUUUZZ#....",
    "....#TTWLGGGMMMMMMMMDDUUUZZ#....",
    "....#TTWLGGMMMMMMDMMDDUUUZZ#....",
    "....#TTTWMGGMMMbBDMMDDUUUZZ#....",
    "....#TTTTWMGGMbMDDMMDDUUUZZ#....",
    ".....#TTTTWMMGMMDDDMDDUUZZ#.....",
    "......#TTTTWMMDMDDDMDDUZZ#......",
    ".......#TTTTMMDDDbBMDDUZ#.......",
    ".........#TTTMDDDDDDUZ#.........",
    "..........#TTXXUUZZZZ#..........",
    "...........#TTXXUUZZ#...........",
    ".....SSSSSS#TTXXUUZZ#SSSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSS.....",
    "........SSSSSSSSSSSSSSSS........",
    "................................"
}

-- 2.frame2_grid: Frame 2 - Bọt khí dâng lên tầng giữa, bọt phải tiếp cận sát bề mặt ellipse
local frame2_grid = {
    "................................",
    "................................",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    "...........#WTTUUZZZ#...........",
    "............#TTUUZZ#............",
    "............#WTTUUZ#............",
    "............#TTTUUZ#............",
    "...........#WTTTUUZZ#...........",
    ".........#TTWTTTTTUUZZ#.........",
    ".......#TWWTTTTTTTTUUUZZ#.......",
    "......#TWTTTTTTTTTTTUUUZZ#......",
    ".....#TWTTTTTTTTTTTTTUUUZZ#.....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTLGGGGGGGGGGDDUUUUZZ#....",
    "....#TTWLGGGMMbBMMMMDDUUUZZ#....",
    "....#TTWLGGMMMMMMDMMDDUUUZZ#....",
    "....#TTTWMGGMbMMMDMMDDUUUZZ#....",
    "....#TTTTWMGGbBMDDMMDDUUUZZ#....",
    ".....#TTTTWMMGbBMDDMDDUUZZ#.....",
    "......#TTTTWMMDMDDDMDDUZZ#......",
    ".......#TTTTMMDDDDDMDDUZ#.......",
    ".........#TTTMDDDDDDUZ#.........",
    "..........#TTXXUUZZZZ#..........",
    "...........#TTXXUUZZ#...........",
    ".....SSSSSS#TTXXUUZZ#SSSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSS.....",
    "........SSSSSSSSSSSSSSSS........",
    "................................"
}

-- 2.frame3_grid: Frame 3 - Bọt khí trái dâng lên, bọt phải vỡ tan trên mặt nước tạo đốm sáng
local frame3_grid = {
    "................................",
    "................................",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    "...........#WTTUUZZZ#...........",
    "............#TTUUZZ#............",
    "............#WTTUUZ#............",
    "............#TTTUUZ#............",
    "...........#WTTTUUZZ#...........",
    ".........#TTWTTTTTUUZZ#.........",
    ".......#TWWTTTTTTTTUUUZZ#.......",
    "......#TWTTTTTTTTTTTUUUZZ#......",
    ".....#TWTTTTTTTTTTTTTUUUZZ#.....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTLGGGGGGbGGGDDUUUUZZ#....",
    "....#TTWLGGGbMMMMMMMDDUUUZZ#....",
    "....#TTWLGGbBMMMMDMMDDUUUZZ#....",
    "....#TTTWMGGMMMMMDMMDDUUUZZ#....",
    "....#TTTTWMGGMMMDDMMDDUUUZZ#....",
    ".....#TTTTWMMGMMDDDMDDUUZZ#.....",
    "......#TTTTWMMDMDDDMDDUZZ#......",
    ".......#TTTTMMDDDDDMDDUZ#.......",
    ".........#TTTMDDDDDDUZ#.........",
    "..........#TTXXUUZZZZ#..........",
    "...........#TTXXUUZZ#...........",
    ".....SSSSSS#TTXXUUZZ#SSSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSS.....",
    "........SSSSSSSSSSSSSSSS........",
    "................................"
}

-- 2.frame4_grid: Frame 4 - Bọt khí trái vỡ tan trên mặt nước, bọt mới hình thành ở đáy lặp chu kỳ
local frame4_grid = {
    "................................",
    "................................",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    ".............#KNNJ#.............",
    "...........#WTTUUZZZ#...........",
    "............#TTUUZZ#............",
    "............#WTTUUZ#............",
    "............#TTTUUZ#............",
    "...........#WTTTUUZZ#...........",
    ".........#TTWTTTTTUUZZ#.........",
    ".......#TWWTTTTTTTTUUUZZ#.......",
    "......#TWTTTTTTTTTTTUUUZZ#......",
    ".....#TWTTTTTTTTTTTTTUUUZZ#.....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTTTTTTTTTTTTTTUUUUZZ#....",
    "....#TWTLGbGGGGGGGGDDUUUUZZ#....",
    "....#TTWLGGGMMMMMMMMDDUUUZZ#....",
    "....#TTWLGGMMbBMMDMMDDUUUZZ#....",
    "....#TTTWMGGMMMMMDMMDDUUUZZ#....",
    "....#TTTTWMGGMMbBDMMDDUUUZZ#....",
    ".....#TTTTWMMGMMbMDMDDUUZZ#.....",
    "......#TTTTWMMDMDbBMDDUZZ#......",
    ".......#TTTTMMDDDDDMDDUZ#.......",
    ".........#TTTMDDDDDDUZ#.........",
    "..........#TTXXUUZZZZ#..........",
    "...........#TTXXUUZZ#...........",
    ".....SSSSSS#TTXXUUZZ#SSSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSS.....",
    "........SSSSSSSSSSSSSSSS........",
    "................................"
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

-- Render Frame 1: Khởi đầu chu kỳ bọt khí
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Bọt dâng cao
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Bọt chạm mặt nước
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- Render Frame 4: Bọt vỡ tan & hồi lưu
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local cel4 = layer:cel(4)
if cel4 then
    cel4.image:clear()
    renderGrid(cel4.image, frame4_grid, PALETTE)
end

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/green_potion_32.aseprite")

-- B. Nếu là Animation: xuất GIF động và dải spritesheet ngang độc lập CLI
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/green_potion_32.gif")
    
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
    sheetSprite:saveCopyAs("output/green_potion_32_sheet.png")
    sheetSprite:close()
else
    -- Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
    sprite:saveCopyAs("output/green_potion_32.png")
end
