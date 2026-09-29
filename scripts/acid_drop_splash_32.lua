-- scripts/acid_drop_splash_32.lua
-- 32x32 FreeStyle Animated Magic Acid Drop Impact & Splash
-- 4 Frames Cycle: Fall -> Impact Squash -> Crown Splash -> Ellipse Ripple (8 FPS)

local width = 32
local height = 32
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Acid_Splash"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: FreeStyle Hue-Shifting Toxic Green shifting to Neon Yellow
local PALETTE = {
    ["."] = nil,
    ["#"] = "#0a2214", -- Viền sẫm xanh thẫm sạch (Clean dark toxic pine outline)
    ["S"] = "#101a14", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 140)
    ["W"] = "#faffaa", -- Phản quang trắng ngả vàng neon (Specular white-yellow glint)
    ["A"] = "#d8ff36", -- Sáng: Vàng chanh neon rực rỡ (Hue-shifted neon yellow-lime)
    ["B"] = "#4ae022", -- Nền: Xanh lục độc quang chủ đạo (Primary toxic poison green)
    ["C"] = "#127838"  -- Tối: Xanh ngọc lục bảo sâu (Hue-shifted deep emerald shadow)
}

-- 2. Render function (with explicit transparent pixel clearing)
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
                local a = (char == "S") and 140 or 255
                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = a })
            else
                img:drawPixel(x - 1, y - 1, Color{ r = 0, g = 0, b = 0, a = 0 })
            end
        end
    end
end

-- 3.1. Frame 1: Fall (Rơi tự do) - Giọt lệ thuôn dài nhọn đỉnh, căng đáy đang lao xuống
local f1_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...............#................",
    "..............#W#...............",
    "..............#WA#..............",
    "..............#WB#..............",
    "..............#AB#..............",
    "..............#AB#..............",
    ".............#WBBC#.............",
    ".............#ABBC#.............",
    ".............#ABBC#.............",
    "............#WABBCC#............",
    "............#AABBCC#............",
    "...........#WWBBBCCC#...........",
    "...........#WABBBCCC#...........",
    "...........#AABBBCCC#...........",
    "...........#AABBBCCC#...........",
    "...........#AAABBBCC#...........",
    "............#BBBCCC#............",
    ".............######.............",
    "................................",
    "................................",
    "................................",
    ".............SSSSSS.............",
    "..............SSSS..............",
    "................................",
    "................................",
    "................................",
    "................................",
}

-- 3.2. Frame 2: Impact (Nén va đập) - Bẹp dí tẹt dày 2px, rộng 12px trên sàn
local f2_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...........##########...........",
    "..........#AWWAABBCCC#..........",
    "..........#AAABBBBCCC#..........",
    "........SS############SS........",
    "..........SSSSSSSSSSSS..........",
    "................................",
    "................................",
    "................................",
    "................................",
}

-- 3.3. Frame 3: Crown Splash (Vương miện bắn tóe) - Đáy lõm, tia nhọn vọt lên + 2 giọt bắn 1px
local f3_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    ".......W........................",
    "........................A.......",
    "................................",
    "................................",
    "........#..............#........",
    ".......#W#............#A#.......",
    ".......#A#...#....#...#B#.......",
    ".......#WA#.#W#..#A#.#BC#.......",
    ".......#AAB##AB##BC##BCC#.......",
    ".......#AAAABB###BCCCCCC#.......",
    ".......#AAAABBBBBCCCCCCC#.......",
    "........#AAAABBBBBCCCCC#........",
    "........#AAAABBBBBCCCCC#........",
    "........################........",
    ".......SSSSSSSSSSSSSSSSSS.......",
    ".........SSSSSSSSSSSSSS.........",
    "................................",
    "................................",
    "................................",
    "................................",
}

-- 3.4. Frame 4: Ripple & Dissipate (Lan tỏa sóng) - Ellipse 3/4 mỏng lan rộng + 2 giọt rơi xuống sàn
local f4_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    ".........................##.....",
    ".........#############..#BC#....",
    "........#WAAAAABBBBCCC#..##.....",
    ".....##.#WA#SSSSSSSS#BC#.SS.....",
    "....#WA##ABBBBCCCCCCCC#.........",
    ".....##..#############..........",
    ".....SS....SSSSSSSSSS...........",
    "................................",
    "................................",
    "................................",
}

-- 4. Render các frame hoạt ảnh
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
sprite:saveCopyAs("output/aseprite/acid_drop_splash_32.aseprite")
sprite:saveCopyAs("output/gif/acid_drop_splash_32.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/acid_drop_splash_32_sheet.png")
sheetSprite:close()
