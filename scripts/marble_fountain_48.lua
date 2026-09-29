-- scripts/marble_fountain_48.lua
-- 48x48 Stardew Valley Animated Marble Water Fountain
-- 4 Frames Looping Fountain Animation at 8 FPS

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley (Ấm cúng, viền mềm cùng tone màu, bóng râm S)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#2b2636", -- Viền sẫm slate tím ấm (Soft dark slate outline, no pure black)
    ["S"] = "#1a1624", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Chất liệu đá cẩm thạch trắng/xám sáng (White / Light Gray Marble)
    ["H"] = "#f5f5f7", -- Đốm phản quang ngà sáng (Specular ivory highlight trên gờ mép)
    ["L"] = "#d8dbe6", -- Thân đá cẩm thạch đón sáng (Bright marble lit body)
    ["M"] = "#9da2b5", -- Thân đá sắc độ trung (Midtone marble)
    ["D"] = "#6b7086", -- Đá vùng khuất sáng (Shadow marble)
    ["V"] = "#45485c", -- Khe rãnh nứt & bóng sâu lòng bồn (Deep crevice & inner basin shadow)

    -- Ngoại lệ Palette cho dòng nước (2-3 màu xanh dương/trắng cho nước & bọt sủi)
    ["W"] = "#ffffff", -- Bọt nước trắng xóa & đỉnh tia nước (White foam crest & bubbles)
    ["A"] = "#6ee2ff", -- Sắc nước sáng / bọt sủi sục khí (Bright cyan water spray & ripple)
    ["B"] = "#00aaff", -- Dòng nước chính trong biếc (User specified vibrant blue water stream)
    ["C"] = "#0c6ba8"  -- Nước sâu đáy bồn (Deep blue water depth in basin cavity)
}

-- 2.frame1_grid: Frame 1 - Tia nước đỉnh trào dâng, dòng nước cuộn đổ, bọt sủi tâm đài
local frame1_grid = {
    "................................................",
    "................................................",
    "................................................",
    ".......................W........................",
    ".....................WAAW.......................",
    "...................WBAAAABW.....................",
    "...................BBAAWWBAAB...................",
    "..................BBAAW..WAABB..................",
    ".................BBA...WW...ABB.................",
    ".................ABB...AA...BBA.................",
    ".................WBA...BB...ABW.................",
    ".................BAW...WA...WAB.................",
    ".................BBA.#HWWD#.ABB.................",
    ".................ABB.#HLMD#.BBA.................",
    "...............WBA#HLWAAWWAMD#ABW...............",
    "...............BA#HLWAAAAAAWMD#AB...............",
    "................BBA.#VVDDDD#.ABB................",
    "................ABB..#HWAD#..BBA................",
    "................WBA..#HAWD#..ABW................",
    "..............#HBAWHL#HBWD#MDWABD#..............",
    "..........#HHLLLBBALL#HABD#MMABBMMDDD#..........",
    ".......#HHHLLLLLABBLL#HWAD#MDBBALMMMDDDD#.......",
    ".....#HHLLLLLLLLWBALL#HAWD#MDABWMMMMMDDDDD#.....",
    "....#HVVVVDDDDDDBAWDD#HBWD#DMWABMMMDDDDDDDD#....",
    "....#HVVVDDDDDDDBBADD#HABD#DMABBMMMDDDDDDDD#....",
    "....#HVDCCCCCCWBACCCC#HWAD#CCABWCCCCCCCCMDD#....",
    "...#HVDCCBBBBBAWWABBB#HLLD#BBBAWWAABBBBCCMDD#...",
    "...#HVDCCBBBBAAWWAABB#HLLD#BBAAWWAABBBBCCMDD#...",
    "..#HVDCBBBAAWWWWAABB#HHLLDD#BBAAWWWWAABBBCMDD#..",
    "..#HVDCBAAWAAAAWAAB#HHLLMMDD#BAAWAAAAWAABCMDD#..",
    "..#HVDCBAAWAAWWAAAAW#VVDDDV#WAAAAWWAAWAAACMDD#..",
    "..#HVDCBAAWAAAAWWAAWAAAAWWAAAAWWAAWAAAAWACMDD#..",
    "..#HVDCBBAAAWWAAAAWWAAABBBBBBAAAWWAAAAWWACMDD#..",
    "..#HVDCBBBBAAWAAAAWAAAABBBBBBAAWAAAAWAAABCMDD#..",
    "...#HLLCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCMDD#...",
    "....#HHHHHHHHHHHHHLLLLLLLLLLMMMMMMMMDDDDDDD#....",
    "....#HHHLLLLLLLLLLLLLLLMMMMMMMMMMMMDDDDDDDD#....",
    "....#HHLLLLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDD#....",
    ".....#HLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDDDD#.....",
    ".......#VVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDD#.......",
    ".........#HHLLLLLLLLMMMMMMMMMMMMMDDDDD#.........",
    "............#HHLLLLLLMMMMMMMMMMMDDD#............",
    "...............#HLLLLMMMMMMMDDDD#...............",
    "..............#HHLLLLMMMMMMMMDDDD#..............",
    "........SSSS#HHLLLLLLMMMMMMMMMMMDDD#SSSS........",
    ".......SSSS#HLLLLLLLLMMMMMMMMMMMDDDD#SSSS.......",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS.........."
}

-- 2.frame2_grid: Frame 2 - Tia nước nở rộng, dòng nước chuyển dịch 1px, vòng sóng nở ra
local frame2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "......................W.W.......................",
    "....................WWAAWW......................",
    "..................WAAWWWWAAW....................",
    "..................BBAAWAAWWABB..................",
    "..................ABAWW..WWABA..................",
    ".................ABB...AA...BBA.................",
    ".................WBA...BB...ABW.................",
    ".................BAW...WA...WAB.................",
    ".................BBA...WW...ABB.................",
    ".................ABB.#HAAD#.BBA.................",
    ".................WBA.#HLMD#.ABW.................",
    "...............BAW#HLAWWAAWMD#WAB...............",
    "...............WB#HLAWWAAWWAMD#BW...............",
    "................ABB.#VVDDDD#.BBA................",
    "................WBA..#HAWD#..ABW................",
    "................BAW..#HBWD#..WAB................",
    "..............#HBBAHL#HABD#MDABBD#..............",
    "..........#HHLLLABBLL#HWAD#MMBBAMMDDD#..........",
    ".......#HHHLLLLLWBALL#HAWD#MDABWLMMMDDDD#.......",
    ".....#HHLLLLLLLLBAWLL#HBWD#MDWABMMMMMDDDDD#.....",
    "....#HVVVVDDDDDDBBADD#HABD#DMABBMMMDDDDDDDD#....",
    "....#HVVVDDDDDDDABBDD#HWAD#DMBBAMMMDDDDDDDD#....",
    "....#HVDCCCCCCBAWCCCC#HAWD#CCWABCCCCCCCCMDD#....",
    "...#HVDCCBBBBAAWWAABB#HLLD#BBAAWWAABBBBCCMDD#...",
    "...#HVDCCBBBAAWWWWAAB#HLLD#BAAWWWWABBBCCCMDD#...",
    "..#HVDCBBAAWAAAAWAAB#HHLLDD#BAAWAAAAWAABBCMDD#..",
    "..#HVDCAAWAAWWAAWAB#HHLLMMDD#BAWAAWWAAWAACMDD#..",
    "..#HVDCBBBAAWAAAAWAA#VVDDDV#AAWAAAAWAABBBCMDD#..",
    "..#HVDCBBBAAWAAAWWAAAAWWAAWAAAWWAAAAWAABBCMDD#..",
    "..#HVDCBBBAAWAAAAAAWAAABBBBBBAAWAAAAAAWABCMDD#..",
    "..#HVDCBBBBAAAWAAWAAAAABBBBBBAAAWAAWAAAAACMDD#..",
    "...#HLLCCCCCCCBAAAACCCAAAACCCCCCCCCCCCCCCMDD#...",
    "....#HHHHHHHHHHHHHLLLLLLLLLLMMMMMMMMDDDDDDD#....",
    "....#HHHLLLLLLLLLLLLLLLMMMMMMMMMMMMDDDDDDDD#....",
    "....#HHLLLLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDD#....",
    ".....#HLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDDDD#.....",
    ".......#VVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDD#.......",
    ".........#HHLLLLLLLLMMMMMMMMMMMMMDDDDD#.........",
    "............#HHLLLLLLMMMMMMMMMMMDDD#............",
    "...............#HLLLLMMMMMMMDDDD#...............",
    "..............#HHLLLLMMMMMMMMDDDD#..............",
    "........SSSS#HHLLLLLLMMMMMMMMMMMDDD#SSSS........",
    ".......SSSS#HLLLLLLLLMMMMMMMMMMMDDDD#SSSS.......",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS.........."
}

-- 2.frame3_grid: Frame 3 - Tia nước tỏa bung hai bên, dòng nước chảy xiết, sóng lan tỏa thành bồn
local frame3_grid = {
    "................................................",
    "................................................",
    "................................................",
    ".....................W...W......................",
    "....................WBAAB.W.....................",
    "..................WBAAB..BAABW..................",
    "..................WBAAW..WAABW..................",
    ".................BBAAW....WAABB.................",
    ".................WBA...BB...ABW.................",
    ".................BAW...WA...WAB.................",
    ".................BBA...WW...ABB.................",
    ".................ABB...AA...BBA.................",
    ".................WBA.#HBBD#.ABW.................",
    ".................BAW.#HLMD#.WAB.................",
    "...............BBA#HLAAWWAAMD#ABB...............",
    "...............AW#HLAAWWWWAAMD#WA...............",
    "................WBA.#VVDDDD#.ABW................",
    "................BAW..#HBWD#..WAB................",
    "................BBA..#HABD#..ABB................",
    "..............#HABBHL#HWAD#MDBBAD#..............",
    "..........#HHLLLWBALL#HAWD#MMABWMMDDD#..........",
    ".......#HHHLLLLLBAWLL#HBWD#MDWABLMMMDDDD#.......",
    ".....#HHLLLLLLLLBBALL#HABD#MDABBMMMMMDDDDD#.....",
    "....#HVVVVDDDDDDABBDD#HWAD#DMBBAMMMDDDDDDDD#....",
    "....#HVVVDDDDDDDWBADD#HAWD#DMABWMMMDDDDDDDD#....",
    "....#HVDCCCCCCBBACCCC#HBWD#CCABBCCCCCCCCMDD#....",
    "...#HVDCCBBBBAAWWAABB#HLLD#BBAAWWAABBBBCCMDD#...",
    "...#HVDCCBBAAWAAAAWAA#HLLD#AAWAAAAWAABBCCMDD#...",
    "..#HVDCBAAWAAWWAAWAB#HHLLDD#BAWAAWWAAWAAACMDD#..",
    "..#HVDCBAAWWWWAABBB#HHLLMMDD#BBBAAWWWWAABCMDD#..",
    "..#HVDCBBAAWWWWAABBW#VVDDDV#WBBAAWWWWAABBCMDD#..",
    "..#HVDCBAAWAAAAWWAAWAAAAWWAAAAWWAAWAAAAWACMDD#..",
    "..#HVDCBBAAAWWAAAAWWAAABBBBBBAAAWWAAAAWWACMDD#..",
    "..#HVDCBBBBAAWAAAAWAAAABBBBBBAAWAAAAWAAABCMDD#..",
    "...#HLLCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCMDD#...",
    "....#HHHHHHHHHHHHHLLLLLLLLLLMMMMMMMMDDDDDDD#....",
    "....#HHHLLLLLLLLLLLLLLLMMMMMMMMMMMMDDDDDDDD#....",
    "....#HHLLLLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDD#....",
    ".....#HLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDDDD#.....",
    ".......#VVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDD#.......",
    ".........#HHLLLLLLLLMMMMMMMMMMMMMDDDDD#.........",
    "............#HHLLLLLLMMMMMMMMMMMDDD#............",
    "...............#HLLLLMMMMMMMDDDD#...............",
    "..............#HHLLLLMMMMMMMMDDDD#..............",
    "........SSSS#HHLLLLLLMMMMMMMMMMMDDD#SSSS........",
    ".......SSSS#HLLLLLLLLMMMMMMMMMMMDDDD#SSSS.......",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS.........."
}

-- 2.frame4_grid: Frame 4 - Tia nước hạ hồi lưu, dòng nước trút xuống lòng đài, chuẩn bị lặp chu kỳ
local frame4_grid = {
    "................................................",
    "................................................",
    "................................................",
    ".......................W........................",
    ".....................AW..WA.....................",
    "...................ABAWWWABBA...................",
    "...................BBAAWWAABB...................",
    "..................BAAWW..WWABA..................",
    ".................BAW...WA...WAB.................",
    ".................BBA...WW...ABB.................",
    ".................ABB...AA...BBA.................",
    ".................WBA...BB...ABW.................",
    ".................BAW.#HWAD#.WAB.................",
    ".................BBA.#HLMD#.ABB.................",
    "...............ABB#HLWAAWWAMD#BBA...............",
    "...............BA#HLWAAWWAAWMD#AB...............",
    "................BAW.#VVDDDD#.WAB................",
    "................BBA..#HABD#..ABB................",
    "................ABB..#HWAD#..BBA................",
    "..............#HWBAHL#HAWD#MDABWD#..............",
    "..........#HHLLLBAWLL#HBWD#MMWABMMDDD#..........",
    ".......#HHHLLLLLBBALL#HABD#MDABBLMMMDDDD#.......",
    ".....#HHLLLLLLLLABBLL#HWAD#MDBBAMMMMMDDDDD#.....",
    "....#HVVVVDDDDDDWBADD#HAWD#DMABWMMMDDDDDDDD#....",
    "....#HVVVDDDDDDDBAWDD#HBWD#DMWABMMMDDDDDDDD#....",
    "....#HVDCCCCCCABBCCCC#HABD#CCBBACCCCCCCCMDD#....",
    "...#HVDCCBBBBBAWWABBB#HLLD#BBBAWWAABBBBCCMDD#...",
    "...#HVDCCBBBBAAWWAABB#HLLD#BBAAWWAABBBBCCMDD#...",
    "..#HVDCBBBAAWWWWAABB#HHLLDD#BBAAWWWWAABBBCMDD#..",
    "..#HVDCBAAWAAAAWAAB#HHLLMMDD#BAAWAAAAWAABCMDD#..",
    "..#HVDCBAAWAAAAWAAAW#VVDDDV#WAAAAAAAWAAABCMDD#..",
    "..#HVDCBBBAAWAAAWWAAAAWWAAWAAAWWAAAAWAABBCMDD#..",
    "..#HVDCBBBAAWAAAAAAWAAABBBBBBAAWAAAAAAWABCMDD#..",
    "..#HVDCBBBBAAAWAAWAAAAABBBBBBAAAWAAWAAAAACMDD#..",
    "...#HLLCCCCCCCBAAAACCCAAAACCCCCCCCCCCCCCCMDD#...",
    "....#HHHHHHHHHHHHHLLLLLLLLLLMMMMMMMMDDDDDDD#....",
    "....#HHHLLLLLLLLLLLLLLLMMMMMMMMMMMMDDDDDDDD#....",
    "....#HHLLLLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDD#....",
    ".....#HLLLLLLLLLLLLMMMMMMMMMMMMMDDDDDDDDDD#.....",
    ".......#VVVVVVVVVVVDDDDDDDDDDDDDDDDDDDDD#.......",
    ".........#HHLLLLLLLLMMMMMMMMMMMMMDDDDD#.........",
    "............#HHLLLLLLMMMMMMMMMMMDDD#............",
    "...............#HLLLLMMMMMMMDDDD#...............",
    "..............#HHLLLLMMMMMMMMDDDD#..............",
    "........SSSS#HHLLLLLLMMMMMMMMMMMDDD#SSSS........",
    ".......SSSS#HLLLLLLLLMMMMMMMMMMMDDDD#SSSS.......",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS.........."
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

-- Render Frame 1: Khởi đầu chu kỳ phun nước
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Nước dâng cực đại & sóng lan rộng
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Nước trút xuống bồn & sóng gợn lăn tăn
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- Render Frame 4: Bọt sủi hồi lưu chuẩn bị lặp chu kỳ
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local cel4 = layer:cel(4)
if cel4 then
    cel4.image:clear()
    renderGrid(cel4.image, frame4_grid, PALETTE)
end

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/marble_fountain_48.aseprite")

-- B. Nếu là Animation: xuất GIF động và dải spritesheet ngang độc lập CLI
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/marble_fountain_48.gif")
    
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
    sheetSprite:saveCopyAs("output/marble_fountain_48_sheet.png")
    sheetSprite:close()
else
    -- Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
    sprite:saveCopyAs("output/marble_fountain_48.png")
end
