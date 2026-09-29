-- scripts/mysterious_cape_statue_48.lua
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
local f1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "............####................................",
    "...........#PP##................................",
    "..........#PPVD#................................",
    ".........#PPVVD##...............................",
    ".........#YGYGOD##..............................",
    "........#P#KKKKK#D#.....................####....",
    "........#P#KAB#DD#.....................#Y##.....",
    "........#V#KKKKK#D#..######...........#Y#.#.....",
    ".........#V#KKK#D#.##YYYYYY#.........#G#.#......",
    ".........##VDD#####YYPPPPPPG##......#G#.##......",
    "........#PVVDDD#.##PPPPPPPPVGO##..##ODG##.......",
    ".......#YPVGYVDD###PPPPPPPPVDDOO##OODDV#........",
    ".......#YPGAYGDD###PPP####PVDDDDOODDDD#.........",
    ".......#GPGAGODZ######....##DDZZDDZZD#..........",
    ".......#VVPOGDDZ###.........##ZZZZZZ#...........",
    "........#VVDDDZZ#.............##ZZ##............",
    "........##DDDZZ##...............##..............",
    ".........#LMMMNN#...............................",
    "........#LMMMMNNN##.............................",
    ".......#LLLLLMMMMNN#............................",
    ".......#LMMMMMNNNNN#............................",
    ".......#MNNNNNNNNNN#............................",
    "........#MNNNNNNNN#.............................",
    "........#LMMMMNNNN#.............................",
    "........#LMMMNMNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMNBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMMNMNNN#.............................",
    ".......#LLLLMMMMNNN#............................",
    "......#LLMMMMMNNNNNN#...........................",
    "......#LLLLLMMMMMNNN#...........................",
    ".....#LLLMMMMMNNNNMNN#..........................",
    ".....#LMMMMMMMMMNMNNN#..........................",
    ".....#NN###########NN#..........................",
    ".....SSSSSSSSSSSSSSSSS..........................",
    "....SSSSSSSSSSSSSSSSSSS.........................",
    "......SSSSSSSSSSSSSSS...........................",
    ".........SSSSSSSSS..............................",
}

local f2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "............####................................",
    "...........#PP##................................",
    "..........#PPVD#................................",
    ".........#PPVVD##...............................",
    ".........#YGYGOD##..............................",
    "........#P#KKKKK#D#.............................",
    "........#P#KAB#DD#.........####.................",
    "........#V#KKKKK#D#......##YYYY#................",
    ".........#V#KKK#D#.....##YYPPPPY##..............",
    ".........##VDD#########GYPPPPPPPGG#.......#.....",
    "........#PVVDDD#.##OOOGVPPPPPPPPVDO#....###.....",
    ".......#YPVGYVDD###DDDDVPPP####PVDDO####O#......",
    ".......#YPGAYGDD###ZZDDVP##....#VDDDOOO##.......",
    ".......#GPGAGODZ###ZZDD##.......##DZDD#..#......",
    ".......#VVPOGDDZ#######...........#ZZZO###......",
    "........#VVDDDZZ#..................##ZZ##.......",
    "........##DDDZZ##....................##.........",
    ".........#LMMMNN#...............................",
    "........#LMMMMNNN##.............................",
    ".......#LLLLLMMMMNN#............................",
    ".......#LMMMMMNNNNN#............................",
    ".......#MNNNNNNNNNN#............................",
    "........#MNNNNNNNN#.............................",
    "........#LMMMMNNNN#.............................",
    "........#LMMMNMNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMNBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMMNMNNN#.............................",
    ".......#LLLLMMMMNNN#............................",
    "......#LLMMMMMNNNNNN#...........................",
    "......#LLLLLMMMMMNNN#...........................",
    ".....#LLLMMMMMNNNNMNN#..........................",
    ".....#LMMMMMMMMMNMNNN#..........................",
    ".....#NN###########NN#..........................",
    ".....SSSSSSSSSSSSSSSSS..........................",
    "....SSSSSSSSSSSSSSSSSSS.........................",
    "......SSSSSSSSSSSSSSS...........................",
    ".........SSSSSSSSS..............................",
}

local f3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "............####................................",
    "...........#PP##................................",
    "..........#PPVD#................................",
    ".........#PPVVD##...............................",
    ".........#YGYGOD##..............................",
    "........#P#KKKKK#D#..............##.............",
    "........#P#KAB#DD#............###YY#............",
    "........#V#KKKKK#D#..........#YYYPPY##..........",
    ".........#V#KKK#D#..........#YPPPPPPYG#.........",
    ".........##VDD########....##GPPPPPPPPVG#........",
    "........#PVVDDD#.##OOO####OGVPPP###PPVDO#.......",
    ".......#YPVGYVDD###DDDOOOODDVP##...##VD#O#......",
    ".......#YPGAYGDD###DZDDDDDDDV#.......##.####....",
    ".......#GPGAGODZ###DZZZZZZDD#.........##..##....",
    ".......#VVPOGDDZ#####ZZZZZ##...........####.....",
    "........#VVDDDZZ#....#####..............###.....",
    "........##DDDZZ##...............................",
    ".........#LMMMNN#...............................",
    "........#LMMMMNNN##.............................",
    ".......#LLLLLMMMMNN#............................",
    ".......#LMMMMMNNNNN#............................",
    ".......#MNNNNNNNNNN#............................",
    "........#MNNNNNNNN#.............................",
    "........#LMMMMNNNN#.............................",
    "........#LMMMNMNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMNBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMMNMNNN#.............................",
    ".......#LLLLMMMMNNN#............................",
    "......#LLMMMMMNNNNNN#...........................",
    "......#LLLLLMMMMMNNN#...........................",
    ".....#LLLMMMMMNNNNMNN#..........................",
    ".....#LMMMMMMMMMNMNNN#..........................",
    ".....#NN###########NN#..........................",
    ".....SSSSSSSSSSSSSSSSS..........................",
    "....SSSSSSSSSSSSSSSSSSS.........................",
    "......SSSSSSSSSSSSSSS...........................",
    ".........SSSSSSSSS..............................",
}

local f4_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "............####................................",
    "...........#PP##................................",
    "..........#PPVD#................................",
    ".........#PPVVD##...............................",
    ".........#YGYGOD##..............................",
    "........#P#KKKKK#D#.................#####.......",
    "........#P#KAB#DD#.................#YYY##.......",
    "........#V#KKKKK#D#...............#YPP#.##......",
    ".........#V#KKK#D#.####.........##YPPPY#..#.....",
    ".........##VDD#####YYYG##......#GGPPP#####G#....",
    "........#PVVDDD#.##PPPVGO######ODVPP#...####....",
    ".......#YPVGYVDD###PPPVDDOOOOOODDVP#............",
    ".......#YPGAYGDD###PPPVDDDDDDDDDDV#.............",
    ".......#GPGAGODZ#######DDZZZZZZD##..............",
    ".......#VVPOGDDZ###....##ZZZZZZ#................",
    "........#VVDDDZZ#........######.................",
    "........##DDDZZ##...............................",
    ".........#LMMMNN#...............................",
    "........#LMMMMNNN##.............................",
    ".......#LLLLLMMMMNN#............................",
    ".......#LMMMMMNNNNN#............................",
    ".......#MNNNNNNNNNN#............................",
    "........#MNNNNNNNN#.............................",
    "........#LMMMMNNNN#.............................",
    "........#LMMMNMNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMNBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMBABNNN#.............................",
    "........#LMMMAMNNN#.............................",
    "........#LMMMNMNNN#.............................",
    ".......#LLLLMMMMNNN#............................",
    "......#LLMMMMMNNNNNN#...........................",
    "......#LLLLLMMMMMNNN#...........................",
    ".....#LLLMMMMMNNNNMNN#..........................",
    ".....#LMMMMMMMMMNMNNN#..........................",
    ".....#NN###########NN#..........................",
    ".....SSSSSSSSSSSSSSSSS..........................",
    "....SSSSSSSSSSSSSSSSSSS.........................",
    "......SSSSSSSSSSSSSSS...........................",
    ".........SSSSSSSSS..............................",
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
