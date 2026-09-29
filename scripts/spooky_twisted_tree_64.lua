-- scripts/spooky_twisted_tree_64.lua
-- 64x64 Terraria Style Spooky Twisted Tree with Overlapping Branches & Stone Masonry Base
-- Static Asset: High Contrast, Heavy Silhouette, Corkscrew Wood Grain, 5-7 Colors

local width = 64
local height = 64

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
local image = sprite.cels[1].image

-- 1. Palette: Terraria High-Contrast Petrified Wood & Ancient Stone
-- Toàn bộ tác phẩm được giải quyết bằng đúng 5 màu đặc + 1 bóng tiếp đất S (Tổng 6 màu)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#180f14", -- Viền tối sẫm Terraria (Near-black plum/brown outline)
    ["S"] = "#120a10", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Sắc độ thân gỗ xoắn, cành nhánh & gạch đá chân đế
    ["H"] = "#bfa382", -- Vệt sáng thớ gỗ khô / Gờ đá sứt mẻ (Pale aged bark highlight & stone rim)
    ["M"] = "#82634d", -- Màu gỗ chính / Mặt gạch đá cổ (Mid aged bark & stone masonry face)
    ["D"] = "#4a3226", -- Gỗ tối / Bóng thân / Cành phía sau (Deep shadow wood & background branches)
    ["V"] = "#2a1812"  -- Rãnh xoắn sâu / Khe nứt gạch đá (Deepest twist crevice & stone fissure)
}

-- 2. Ma trận ký tự (64x64)
local tree_grid = {
    "................................................................",
    "............................####................................",
    "..................####......#HM##..........###..................",
    ".................##MM##.....##HM##........##M##.................",
    "......###........#MHDM#......#HMM#........#HDM#.........####....",
    ".....##D##......##HDD##.####.#HMM#...###..#MHD##.......##DD##...",
    ".....#DDD##.###.#MHDM#..#HH#.#HHM#...#H#..#MHDM#.###..##DDDD#...",
    ".....##DDD###D#.#MHD##..#H##.#MHM#...#H#..##HDD###D#.##DDDD##...",
    "......##DDD##D#.#HDM#...#H#..#MHM##..#H#...#MHDM##D###DDDD##....",
    ".......##DDD#D#.#HDM##..#H#..#MHMM#..#H#..##MHDM##D##DDDD##.....",
    "........##DDDD#.#MMDM#.##H#..#MHMM#..#H##.#MHDMM##D#DDDD##......",
    ".........##VDD###MHDM###MH##.#MHMM#..#HM###MHDM###DDVVD##.......",
    "..........##VDDD#MHDD##MMHM#.#MHM##..#MHM##MHDM#DDDVDD##........",
    "...........##VDDD#MHDM#MMM##.#HHM#...#MMM#MHDM#DDVVDD##.........",
    "............#DVDDDMHDMMMMM#..#HMM#...#MMMMHHDMDDVVDDD#..........",
    "###.........##DVDDDMMMMMMM#..#HMM#...#MMMMHMMMDVVDD###.......###",
    "#H#........##DDDVDDMHDMMM##..#HMM#...##MMMDDMDVVDDD##........#HH",
    "#H#.....####DDDDDVDDMHMMM#...#MMM#....#MMMDMDVVDDDDD####.....#H#",
    "#H##....#DDDDDDDDDVDMHMMM##..#HHM#...##MMMDMVVDDDDDDDDD##...##H#",
    "#HH##...#D###D####DVDMMMMD##.#MHM#..##HDMMMMVD#####D###D#..##HH#",
    "#MHH##..###.###..##DVMMMMDM###MHM####MHDMMMVD##...###.###.##MDHM",
    "##DDH##...........##DVMHDDDM##MHMM##MHDDDMVD##............#MHDM#",
    ".##DDH##...........##DVHDDDD##MHMM##HDDDDVD##............##MDD##",
    "..##DDM##........#####DDHDDDM##MMM#DHDDDMD#####.........##HMDM#.",
    "...##MDH####..####MMHHHHMHDMVHHMMMMMMHDMMHHHMM####...####HDDM##.",
    "....##DDHMM####MHHHHHDDMDDDDVVHMHMMHMMDDDDDHHHHHM#####MMMDDM##..",
    ".....##MMMHM##MHHDDDHDDMMMDDDVVVHHMMMHMMDDDDHDDHHH##MHHHMMM##...",
    "....##MMMDHHMHMMMDDDDMDMHMMDDDVVVMHMMMMHMDDMDDDDMMHHMHDDDMM##...",
    "....#MM#MMDDMMMMMDDDMDMMMMHMDDDVVVHHMMMMMHDDMDDDMMMDMDMM###M##..",
    "....#M####MMMMMMMDMMM##MMMMMHDDDVVVMHHHMMMD#MMDDMMMMMMM##.##M#..",
    "....###..##MMMMM#######HHHMMMMDDDVVVHHMMHMDD#####MMMM###...###..",
    ".........##MMM###.....#VHMMHMMMMDDDVVVHHMMDD#...###MMM##........",
    ".......###MMMM#.......#VVHHM#HMMMDDDVVVHMMDD#.....##MMM###......",
    ".......#MM##M##......##DVVH###MH#MDDDVVVHHDD#......##M#MM##.....",
    ".......#M#####.......#HDDVVDHH###HMD#DVVVHDD#.......#####M#.....",
    ".......###...........#HDVDVMDMHHH###DDDD#VDD#........######.....",
    "....................##HMVVDD##MDDHHM###DDDDD#...######HHH#......",
    "....................#HHMHVVDDV###DMMMMM###HM#####MMMHH####......",
    "...................##HHMMMVVDDVVD###DMMMDD###HMMMMMMHM#.........",
    "..................##HHMHMMMVVDVVVVDD###MMDHHHMMMMMMMM##.........",
    "..................#HHMMMMHMMVVDDVVDMDDV###MMDHMMMMHM##..........",
    "..................#HHMMMMMMHMMVDDDVVDVMDV###DDMMDDHHM#..........",
    ".................##HHMMHHMMMMHMVVDDVVMDVMDVD##DDMDDMM##.........",
    ".................#HHMMMVHMHMMMMHVVDDVVHHHVD##DDD##MMMM##........",
    ".................#HHHMMVVHHHHMMMMVVDDVVHMHD##########MM##.......",
    ".................#HHHHHDVVHMHMHMMMVVDDVVHHD#........###D##......",
    ".................#HHVHHDDDVVHHMMHMMVVDDDVVD##.........##D##.....",
    ".................#HHVVMDDDDVVMHMMMHMVVDDDVDD#..........##D#.....",
    ".................#HHDMHMDDDDVVHHMMMMHMDDDDDD##..........###.....",
    ".................#HHMHHHMDDDDVVMHHMMMMHDDDMDD#..................",
    "................##MMHHMMMHDDDDVVHHMHMMMMDDHMM##.................",
    "...............##MHHHDHMMMMHDDDDVVHHMHMMMMDHHM##................",
    "..............##MHHDDDDMMDVVHHMMMMMDMMDMMDDDHHM##...............",
    "............###HHHDDDDMM#####HMM##MDM###MDDDDHHH###.............",
    "...........##HHHDDHDDMM##...#MMM##MMD####MDDDHDHHH##............",
    ".........###HHDDDDDMM########HMM#VMMMM####MDMDDDDHH###..........",
    ".......###MMHHMDDDMM#HHHVHHHHHHMHVMMDMHHVVHMDDDDDMHMM#####......",
    ".......#HMHHMDMDDMMH#DMMVMMMMMMMMVDMDMMMVMMMDMDDDMDHHMHHH#......",
    "......##MHHMDMMMMMMD#DMMMVMMVMHMMVMMMMMMVMMMD#DMDMDDMHMMD#......",
    "......#MHHDMMMVMMVMD#DMMMVMMVMHHMVMMDMVMVMMMD#DMMVMDMDHMD#......",
    "......#MHDMMMMMVMVMD#DMMMMVMVMMHMVMDDMVMMMMMD#DMMMVMMDDHM#......",
    "......####################################################......",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    "........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS........"
}

-- 3. Hàm render ma trận ký tự
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

renderGrid(image, tree_grid, PALETTE)

-- 4. Pipeline xuất file CLI an toàn
sprite:saveCopyAs("output/spooky_twisted_tree_64.aseprite")
sprite:saveCopyAs("output/spooky_twisted_tree_64.png")
