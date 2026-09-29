-- scripts/blood_flask_roots_48.lua
-- 48x48 FreeStyle Animated Blood Flask on Twisted Roots
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Flask_Roots"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: "." = transparent, "S" = ground contact shadow (Alpha 130)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#16080e", -- Deep wine-black outline
    ["S"] = "#180c12", -- Ground shadow (Alpha 130)
    
    -- Glass & Specular Gloss
    ["P"] = "#ffffff", -- Specular pure white highlight
    ["K"] = "#d2ebf5", -- Pale glass reflection
    ["J"] = "#505f6e", -- Dark glass rim
    
    -- Cork Stopper
    ["E"] = "#b98755", -- Cork light wood
    ["U"] = "#734b2d", -- Cork dark wood
    
    -- Glowing Crimson Liquid (Hue-shifting)
    ["W"] = "#ffffff", -- Hot bubble core
    ["Y"] = "#ffe15a", -- Glowing intense yellow
    ["R"] = "#ff3746", -- Radiant glowing crimson
    ["B"] = "#c31432", -- Deep ruby red
    ["Q"] = "#690a1e", -- Dark wine red shadow
    
    -- Twisted Roots with OSL Color Bleed
    ["H"] = "#ffa04b", -- OSL fiery peach highlight
    ["O"] = "#e65f23", -- OSL warm glowing orange
    ["T"] = "#a03219", -- OSL warm terracotta-red
    ["M"] = "#5a241a", -- Withered bark warm midtone
    ["D"] = "#301412", -- Withered bark dark shadow
    ["V"] = "#180a0c"  -- Deepest root crevice shadow
}

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

local f1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "......................####......................",
    "......................#EEU#.....................",
    "......................#EEU#.....................",
    "....................########....................",
    "...................#PKKKKKKJ#...................",
    "....................#PKKKKJ#....................",
    ".....................#PKKJ#.....................",
    ".....................#P..J#.....................",
    ".....................#P..J#.....................",
    "...................#PK....KJ#...................",
    ".................#PK........KJ#.................",
    "...............#PK..PP........KJ#...............",
    "..............#PK..PP..........KJ#..............",
    ".............#PK..PP............KJ#.............",
    "............#PK..PP..............KJ#............",
    "...........#PK..PP................KJ#...........",
    "...........#K..PP.QQBBBBBBBBBBQQ...J#...........",
    "..........#PK.PP.QBBBRRYYYYYYRRBBQ..J#..........",
    "..........#PK.P.QBRRYWWYYYYWWYRRBQ..J#..........",
    "..........#PK.P.BRYYRRRRRRRRRRYYRB..J#..........",
    ".........#..#.P.BYRRRRRRRRRRRRRRYB..J#..#.......",
    "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......",
    "........#HO#.#..BRRRRRRRRRRWRRRB...#.#MD#.......",
    ".......#THO#.#..QBRRRRRRRRYRRRB...#..#TMD#......",
    ".......#THOM#.#.QQBRRWYRRRRRRBQ..#..#OTMD#......",
    ".......#TTHOM#.##QQBRRYRRRRRBQQ.##..#HOTMD#.....",
    "........#TTHOM##..QQBBRRRRRRBQQ..##.#HHOTMD#....",
    "........#DTHOMM##..QQQBBBBQQQ..##..#HHOTMDD#....",
    ".........#DDTHOMM###.########.###.##HHOTMDD#....",
    "..........#VDDTHOMMM#OHHHHHHO#MMMMHHOTMDDV#.....",
    "...........#VVDDTTHOMHOTTTTTOHMMHHOTMDDVV#......",
    "............#VVVDTTOMHOTTTTMTHHHOTMDDVVV#.......",
    ".............#VVDTTMMOTTTMMMMTHOTMMDVV#.........",
    "............#VDDTMMMMTTMMMMMDTTOMMDV#...........",
    "...........#VDDTMMMDV##VMMMMMMDV##DTMMDV#.......",
    "..........#VDDTMMMDV#...#VMMMMV#...#VDTMMDV#....",
    "..........#VDTMMMDV#....#VMMMMV#....#VDTMMDV#...",
    ".........#VVDTMMMDV#.....#DMMD#......#VDTMMDV#..",
    "........#VVDMMMMDV#......#DMMD#.......#VDMMMDV#.",
    ".......#VVDMMMMMDV#......#VMMV#........#VDMMMDV#",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    "................................................",
}
local f2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "......................####......................",
    "......................#EEU#.....................",
    "......................#EEU#.....................",
    "....................########....................",
    "...................#PKKKKKKJ#...................",
    "....................#PKKKKJ#....................",
    ".....................#PKKJ#.....................",
    ".....................#P..J#.....................",
    ".....................#P..J#.....................",
    "...................#PK....KJ#...................",
    ".................#PK........KJ#.................",
    "...............#PK..PP........KJ#...............",
    "..............#PK..PP..........KJ#..............",
    ".............#PK..PP............KJ#.............",
    "............#PK..PP..............KJ#............",
    "...........#PK..PP................KJ#...........",
    "...........#K..PP.QQBBBBBBBBBBQQ...J#...........",
    "..........#PK.PP.QBBBRRYYYYYYRRBBQ..J#..........",
    "..........#PK.P.QBRRYWWYYYYWWYRRBQ..J#..........",
    "..........#PK.P.BRYYRRRRRRRRRRYYRB..J#..........",
    ".........#..#.P.BYRRRRRRRRRRWRRRYB..J#..#.......",
    "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......",
    "........#HO#.#..BRRWYRRRRRRWRRRB...#.#MD#.......",
    ".......#THO#.#..QBRRYRRRRRRYRRRB...#..#TMD#......",
    ".......#THOM#.#.QQBRRRRRRRRRRRBQ..#..#OTMD#......",
    ".......#TTHOM#.##QQBRRYRRRRRBQQ.##..#HOTMD#.....",
    "........#TTHOM##..QQBBRRRRWRRBQQ..##.#HHOTMD#....",
    "........#DTHOMM##..QQQBBBBQQQ..##..#HHOTMDD#....",
    ".........#DDTHOMM###.########.###.##HHOTMDD#....",
    "..........#VDDTHOMMM#OHHHHHHO#MMMMHHOTMDDV#.....",
    "...........#VVDDTTHOMHOTTTTTOHMMHHOTMDDVV#......",
    "............#VVVDTTOMHOTTTTMTHHHOTMDDVVV#.......",
    ".............#VVDTTMMOTTTMMMMTHOTMMDVV#.........",
    "............#VDDTMMMMTTMMMMMDTTOMMDV#...........",
    "...........#VDDTMMMDV##VMMMMMMDV##DTMMDV#.......",
    "..........#VDDTMMMDV#...#VMMMMV#...#VDTMMDV#....",
    "..........#VDTMMMDV#....#VMMMMV#....#VDTMMDV#...",
    ".........#VVDTMMMDV#.....#DMMD#......#VDTMMDV#..",
    "........#VVDMMMMDV#......#DMMD#.......#VDMMMDV#.",
    ".......#VVDMMMMMDV#......#VMMV#........#VDMMMDV#",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    "................................................",
}
local f3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "......................####......................",
    "......................#EEU#.....................",
    "......................#EEU#.....................",
    "....................########....................",
    "...................#PKKKKKKJ#...................",
    "....................#PKKKKJ#....................",
    ".....................#PKKJ#.....................",
    ".....................#P..J#.....................",
    ".....................#P..J#.....................",
    "...................#PK....KJ#...................",
    ".................#PK........KJ#.................",
    "...............#PK..PP........KJ#...............",
    "..............#PK..PP..........KJ#..............",
    ".............#PK..PP............KJ#.............",
    "............#PK..PP..............KJ#............",
    "...........#PK..PP................KJ#...........",
    "...........#K..PP.QQBBBBBBBBBBQQ...J#...........",
    "..........#PK.PP.QBBBRRYYYYYYWWBBQ..J#..........",
    "..........#PK.P.QBRWYWWYYYYWWYRRBQ..J#..........",
    "..........#PK.P.BRYYRRRRRRRRRRYYRB..J#..........",
    ".........#..#.P.BYRRRRRRRRRRRRRRYB..J#..#.......",
    "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......",
    "........#HO#.#..BRRRRRRRRRRRRRRB...#.#MD#.......",
    ".......#THO#.#..QBRRRRRRRRYRRRB...#..#TMD#......",
    ".......#THOM#.#.QQBRRRRRRRRWYRBQ..#..#OTMD#......",
    ".......#TTHOM#.##QQBRRYRRRRRBQQ.##..#HOTMD#.....",
    "........#TTHOM##..QQBBRRRRRRBQQ..##.#HHOTMD#....",
    "........#DTHOMM##..QQQBBBBQQQ..##..#HHOTMDD#....",
    ".........#DDTHOMM###.########.###.##HHOTMDD#....",
    "..........#VDDTHOMMM#OHHHHHHO#MMMMHHOTMDDV#.....",
    "...........#VVDDTTHOMHOTTTTTOHMMHHOTMDDVV#......",
    "............#VVVDTTOMHOTTTTMTHHHOTMDDVVV#.......",
    ".............#VVDTTMMOTTTMMMMTHOTMMDVV#.........",
    "............#VDDTMMMMTTMMMMMDTTOMMDV#...........",
    "...........#VDDTMMMDV##VMMMMMMDV##DTMMDV#.......",
    "..........#VDDTMMMDV#...#VMMMMV#...#VDTMMDV#....",
    "..........#VDTMMMDV#....#VMMMMV#....#VDTMMDV#...",
    ".........#VVDTMMMDV#.....#DMMD#......#VDTMMDV#..",
    "........#VVDMMMMDV#......#DMMD#.......#VDMMMDV#.",
    ".......#VVDMMMMMDV#......#VMMV#........#VDMMMDV#",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    "................................................",
}
local f4_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "......................####......................",
    "......................#EEU#.....................",
    "......................#EEU#.....................",
    "....................########....................",
    "...................#PKKKKKKJ#...................",
    "....................#PKKKKJ#....................",
    ".....................#PKKJ#.....................",
    ".....................#P..J#.....................",
    ".....................#P..J#.....................",
    "...................#PK....KJ#...................",
    ".................#PK........KJ#.................",
    "...............#PK..PP........KJ#...............",
    "..............#PK..PP..........KJ#..............",
    ".............#PK..PP............KJ#.............",
    "............#PK..PP..............KJ#............",
    "...........#PK..PP................KJ#...........",
    "...........#K..PP.QQBBBBBBBBBBQQ...J#...........",
    "..........#PK.PP.QBBBRRYYYYYYRRBBQ..J#..........",
    "..........#PK.P.QBRRYWWYYYYWWYRRBQ..J#..........",
    "..........#PK.P.BRYYRRRRRRRRRRYYRB..J#..........",
    ".........#..#.P.BYRRRRRRRRRRRRRRYB..J#..#.......",
    "........#O#.#.K.BYRRRRRRRRRRYRRRYB..J#.#D#......",
    "........#HO#.#..BRRRRRRRRRRWYRRB...#.#MD#.......",
    ".......#THO#.#..QBRRRRRRRRRRRRRB...#..#TMD#......",
    ".......#THOM#.#.QQBRRRRRRRRRRRBQ..#..#OTMD#......",
    ".......#TTHOM#.##QQBRRYRRRRRBQQ.##..#HOTMD#.....",
    "........#TTHOM##..QQBBRRRRRRBQQ..##.#HHOTMD#....",
    "........#DTHOMM##..QQQBBWBBQQQ..##..#HHOTMDD#....",
    ".........#DDTHOMM###.########.###.##HHOTMDD#....",
    "..........#VDDTHOMMM#OHHHHHHO#MMMMHHOTMDDV#.....",
    "...........#VVDDTTHOMHOTTTTTOHMMHHOTMDDVV#......",
    "............#VVVDTTOMHOTTTTMTHHHOTMDDVVV#.......",
    ".............#VVDTTMMOTTTMMMMTHOTMMDVV#.........",
    "............#VDDTMMMMTTMMMMMDTTOMMDV#...........",
    "...........#VDDTMMMDV##VMMMMMMDV##DTMMDV#.......",
    "..........#VDDTMMMDV#...#VMMMMV#...#VDTMMDV#....",
    "..........#VDTMMMDV#....#VMMMMV#....#VDTMMDV#...",
    ".........#VVDTMMMDV#.....#DMMD#......#VDTMMDV#..",
    "........#VVDMMMMDV#......#DMMD#.......#VDMMMDV#.",
    ".......#VVDMMMMMDV#......#VMMV#........#VDMMMDV#",
    "......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    "................................................",
}

-- Render Frame 1
renderGrid(image, f1_grid, PALETTE)

-- Render Frame 2
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local img2 = layer:cel(2).image
renderGrid(img2, f2_grid, PALETTE)

-- Render Frame 3
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local img3 = layer:cel(3).image
renderGrid(img3, f3_grid, PALETTE)

-- Render Frame 4
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local img4 = layer:cel(4).image
renderGrid(img4, f4_grid, PALETTE)

-- Export files according to workspace rules
sprite:saveCopyAs("output/aseprite/blood_flask_roots_48.aseprite")
sprite:saveCopyAs("output/gif/blood_flask_roots_48.gif")

-- Export horizontal Spritesheet
local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/blood_flask_roots_48_sheet.png")
sheetSprite:close()
