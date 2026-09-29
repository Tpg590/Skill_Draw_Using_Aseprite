-- scripts/campfire_roast_meat_48.lua
-- 48x48 Stardew Valley Animated Campfire with Spit Roast Meat
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Campfire_Meat"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley Warm Palette (Soft outlines, NO #000000)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e1420", -- Soft purple-brown ground shadow (Alpha 130)
    
    -- Spit Wood & Stands
    ["#"] = "#361a0e", -- Soft dark wood outline
    ["T"] = "#c3874b", -- Spit wood light
    ["U"] = "#915a30", -- Spit wood base
    ["I"] = "#5f341c", -- Spit wood shadow
    
    -- Campfire Firewood Logs
    ["L"] = "#d29655", -- Firewood bark light
    ["M"] = "#94582a", -- Firewood bark midtone
    ["D"] = "#5c2e16", -- Firewood bark dark
    ["V"] = "#34180e", -- Firewood deep crevice
    ["C"] = "#e6be8c", -- Log cut-end pale wood
    
    -- Giant Roast Meat
    ["Z"] = "#401210", -- Charred roast crust / grill marks
    ["G"] = "#af3228", -- Roast meat rich red-brown
    ["J"] = "#d7503c", -- Roast meat succulent pink-red
    ["K"] = "#f58c6e", -- Roast meat juicy highlight / fat
    ["B"] = "#f5f0e1", -- Ham bone ivory-white
    ["P"] = "#c8b9a5", -- Ham bone shadow
    
    -- Fire & Flames
    ["W"] = "#ffffff", -- Core white hot heat
    ["Y"] = "#ffeb46", -- Blazing bright yellow
    ["O"] = "#ff871e", -- Radiant flame orange
    ["R"] = "#e12d19", -- Flame crimson red
    ["Q"] = "#7d140f", -- Flame dark red tip
    
    -- OSL Color Bleed
    ["H"] = "#ffcd50", -- OSL intense yellow-gold glow
    ["A"] = "#f57d23"  -- OSL warm amber-orange glow
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
    "................................................",
    "..................ZZZZZZZZZZ....................",
    "................ZKKKKKKKKKKKKZ..................",
    "...............ZKKZJJJJZJJJJJJJZ................",
    "......#..#....ZJJZGGGGZGGGGGGGGZ.......#..#.....",
    "....##BB..#..ZJJZGGGGZGGGGGGGGGGZ.....#..##.....",
    "...#TTBBP#TT#ZBBGGGGZGGGGGGGGGGGGZ###TTTTTT#....",
    "..#TTTBBPP###ZBPGGGZGGGGGGGGGGGGGGZ#TTTTTTUU#...",
    "...#TTTII#..#ZBPGGZGGGGGGGGGGGGGGGGZ#TTTTUU#....",
    "....#II##...ZBBGZGGGGGGGGGGGGGGGGGZ..#II##......",
    "....#TU#....ZJJZGGGGGGGGGGGGGGGGGZ...#TU#.......",
    "....#TU#.....ZJJJGGGGGGGGGGGGGGGZ....#TU#.......",
    "....#TU#......ZZGGGGGGGGGGGGGGZZ.....#TU#.......",
    "....#TU#........ZZAAHHHHHHAAZZ.......#TU#.......",
    "....#TU#..........ZZAAHHAAZZ...Y.....#TU#.......",
    "....#TU#............ZZZZZZ....OY.....#TU#.......",
    "....#TU#............RR.....OOYY......#TU#.......",
    "....#TU#...........RYYO...OYYWWY.....#TU#.......",
    "....#TU#..........RYWWYO.OYYWWYYO....#TU#.......",
    "....#TU#.........OYYWWYYOYYWWYYRO....#TU#.......",
    "....#TU#.........OYYWWYYYYWWYYRO.....#TU#.......",
    "....#TU#........ROYYWWWWWWWWYYRO.....#TU#.......",
    "....#TU#........ROYYYYWWWWYYYYRO.....#TU#.......",
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......",
    "....#TU#.........RROOOOOOOOOORR......#TU#.......",
    "....#TU#..........RRRRRRRRRRRR.......#TU#.......",
    "....#TU#...........RRRRRRRRRR........#TU#.......",
    "....#TU#........####.WYYYYW.####.....#TU#.......",
    "....#TU#.....###LLHH#WYYYYW#HHLL###..#TU#.......",
    "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#.......",
    "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#.......",
    "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#.....",
    "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#....",
    "....#TU##MMDDV#.......#####......#VDDMM#TU#.....",
    "...##TUI##DDDV#...###########....#VDDD##TUI##...",
    "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#..",
    ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#..",
    "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#..",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    ".SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.",
    "...SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...",
    "................................................",
    "................................................",
}
local f2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "..................ZZZZZZZZZZ....................",
    "................ZKKKKKKKKKKKKZ..................",
    "...............ZKKZJJJJZJJJJJJJZ................",
    "......#..#....ZJJZGGGGZGGGGGGGGZ.......#..#.....",
    "....##BB..#..ZJJZGGGGZGGGGGGGGGGZ.....#..##.....",
    "...#TTBBP#TT#ZBBGGGGZGGGGGGGGGGGGZ###TTTTTT#....",
    "..#TTTBBPP###ZBPGGGZGGGGGGGGGGGGGGZ#TTTTTTUU#...",
    "...#TTTII#..#ZBPGGZGGGGGGGGGGGGGGGGZ#TTTTUU#.Y..",
    "....#II##...ZBBGZGGGGGGGGGGGGGGGGGZ..#II##......",
    "....#TU#....ZJJZGGGGGGGGGGGGGGGGGZ...#TU#.......",
    "....#TU#.....ZJJJGGGGGGGGGGGGGGGZ....#TU#.......",
    "....#TU#......ZZGGGGGGGGGGGGGGZZ.....#TU#.......",
    "....#TU#........ZZAAHHHHHHAAZZ.......#TU#.......",
    "....#TU#........Y.ZZAAHHAAZZ.........#TU#.......",
    "....#TU#............ZZZZZZ...........#TU#.......",
    "....#TU#...........OOYY......RR......#TU#.......",
    "....#TU#..........OYYWWY....RYYO.....#TU#.......",
    "....#TU#.........OYYWWYYO..RYWWYO....#TU#.......",
    "....#TU#.........ROYYWWYYOYYWWYYO....#TU#.......",
    "....#TU#.........ROYYWWYYYYWWYYO.....#TU#.......",
    "....#TU#........ROYYYYWWWWWWYYRO.....#TU#.......",
    "....#TU#........RROYYYYWWWWYYYYRO....#TU#.......",
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......",
    "....#TU#.........RROOOOOOOOOORR......#TU#.......",
    "....#TU#..........RRRRRRRRRRRR.......#TU#.......",
    "....#TU#...........RRRRRRRRRR........#TU#.......",
    "....#TU#........####.WWYYWW.####.....#TU#.......",
    "....#TU#.....###LLHH#WWYYWW#HHLL###..#TU#.......",
    "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#.......",
    "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#.......",
    "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#.....",
    "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#....",
    "....#TU##MMDDV#.......#####......#VDDMM#TU#.....",
    "...##TUI##DDDV#...###########....#VDDD##TUI##...",
    "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#..",
    ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#..",
    "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#..",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    ".SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.",
    "...SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...",
    "................................................",
    "................................................",
}
local f3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "..................ZZZZZZZZZZ....................",
    "................ZKKKKKKKKKKKKZ..Y...............",
    "...............ZKKZJJJJZJJJJJJJZ................",
    "......#..#....ZJJZGGGGZGGGGGGGGZ.......#..#.....",
    "....##BB..#..ZJJZGGGGZGGGGGGGGGGZ.....#..##.....",
    "...#TTBBP#TT#ZBBGGGGZGGGGGGGGGGGGZ###TTTTTT#....",
    "..#TTTBBPP###ZBPGGGZGGGGGGGGGGGGGGZ#TTTTTTUU#...",
    "...#TTTII#..#ZBPGYGGGGGGGGGGGGGGGGGZ#TTTTUU#....",
    "....#II##...ZBBGZGGGGGGGGGGGGGGGGGZ..#II##......",
    "....#TU#....ZJJZGGGGGGGGGGGGGGGGGZ...#TU#.......",
    "....#TU#.....ZJJJGGGGGGGGGGGGGGGZ....#TU#.......",
    "....#TU#......ZZGGGGGGGGGGGGGGZZ.....#TU#.......",
    "....#TU#........ZZAAHHHHHHAAZZ.......#TU#.......",
    "....#TU#..........ZZAAHHAAZZ...Y.....#TU#.......",
    "....#TU#............ZZZZZZ...........#TU#.......",
    "....#TU#..........RYYO.....RYYO......#TU#.......",
    "....#TU#.........RYWWYO...OYYWWY.....#TU#.......",
    "....#TU#.........OYYWWYYOOYYWWYYO....#TU#.......",
    "....#TU#.........OYYWWYYYYWWYYRO.....#TU#.......",
    "....#TU#........ROYYWWWWWWWWYYRO.....#TU#.......",
    "....#TU#........ROYYYYWWWWYYYYRO.....#TU#.......",
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......",
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......",
    "....#TU#.........RROOOOOOOOOORR......#TU#.......",
    "....#TU#..........RRRRRRRRRRRR.......#TU#.......",
    "....#TU#...........RRRRRRRRRR........#TU#.......",
    "....#TU#........####.YYYYYY.####.....#TU#.......",
    "....#TU#.....###LLHH#WYYYYW#HHLL###..#TU#.......",
    "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#.......",
    "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#.......",
    "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#.....",
    "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#....",
    "....#TU##MMDDV#.......#####......#VDDMM#TU#.....",
    "...##TUI##DDDV#...###########....#VDDD##TUI##...",
    "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#..",
    ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#..",
    "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#..",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    ".SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.",
    "...SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...",
    "................................................",
    "................................................",
}
local f4_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "..................ZZZZZZZZZZ....................",
    "...............YZKKKKKKKKKKKKZ..................",
    "...............ZKKZJJJJZJJJJJJJZ................",
    "......#..#....ZJJZGGGGZGGGGGGGGZ.......#..#.....",
    "....##BB..#..ZJJZGGGGZGGGGGGGGGGZ.....#..##.....",
    "...#TTBBP#TT#ZBBGGGGZGGGGGGGGGGGGZ###TTTTTT#....",
    "..#TTTBBPP###ZBPGGGZGGGGGGGGGGGGGGZ#TTTTTTUU#...",
    "...#TTTII#..#ZBPGGZGGGGGGGGGGGGGGGGZ#TTTTUU#....",
    "....#II##...ZBBGZGGGGGGGGGGGGGGGGGZ..#II##......",
    "....#TU#....ZJJZGGGGGGGGGGGGGGGGGZ...#TU#.......",
    "....#TU#.....ZJJJGGGGGGGGGGGGGGGZ....#TU#.......",
    "....#TU#......ZZGGGGGGGGGGGGGGZZ.....#TU#.......",
    "....#TU#........ZZAAHHHHHHAAZZ.......#TU#.......",
    "....#TU#..........ZZAAHHAAZZ...Y.....#TU#.......",
    "....#TU#............ZZZZZZ...........#TU#.......",
    "....#TU#...........RR.......OO.......#TU#.......",
    "....#TU#..........RYYO.....OYYO......#TU#.......",
    "....#TU#.........RYWWYO...RYWWYO.....#TU#.......",
    "....#TU#.........OYYWWYYOYYWWYYO.....#TU#.......",
    "....#TU#.........OYYWWYYYYWWYYRO.....#TU#.......",
    "....#TU#........ROYYWWWWWWWWYYRO.....#TU#.......",
    "....#TU#........ROYYYYWWWWYYYYRO.....#TU#.......",
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......",
    "....#TU#.........RROOOOOOOOOORR......#TU#.......",
    "....#TU#..........RRRRRRRRRRRR.......#TU#.......",
    "....#TU#...........RRRRRRRRRR........#TU#.......",
    "....#TU#........####.WYYYYW.####.....#TU#.......",
    "....#TU#.....###LLHH#WYYYYW#HHLL###..#TU#.......",
    "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#.......",
    "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#.......",
    "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#.....",
    "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#....",
    "....#TU##MMDDV#.......#####......#VDDMM#TU#.....",
    "...##TUI##DDDV#...###########....#VDDD##TUI##...",
    "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#..",
    ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#..",
    "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#..",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    ".SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.",
    "...SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...",
    "................................................",
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

-- Save Aseprite project
sprite:saveCopyAs("output/aseprite/campfire_roast_meat_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/campfire_roast_meat_48.gif")

-- Save Spritesheet
local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/campfire_roast_meat_48_sheet.png")
sheetSprite:close()
