-- scripts/waving_flag_48.lua
-- 48x48 Stardew Valley Animated Waving Crimson Pennant Flag
local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Waving_Flag"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley warm palette (soft outline, NO #000000)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e1420", -- Soft ground shadow (Alpha 130)
    
    -- Wooden Flagpole & Finial
    ["#"] = "#361a0e", -- Soft dark wood outline
    ["T"] = "#d79b55", -- Mast wood highlight
    ["U"] = "#a06932", -- Mast wood midtone
    ["M"] = "#693c1a", -- Mast wood shadow
    
    -- Gold Finial & Flag Golden Trim
    ["Y"] = "#fff0a0", -- Pure gold highlight
    ["G"] = "#ffd23c", -- Golden trim bright
    ["O"] = "#d7961e", -- Golden trim midtone
    ["J"] = "#915a0f", -- Golden trim shadow / trough
    
    -- Flag Cloth (Crimson Red with Crease Shading)
    ["F"] = "#3a0c14", -- Flag soft dark outline
    ["A"] = "#ff6941", -- Wave crest highlight (bright coral/cam)
    ["B"] = "#e62d28", -- Wave crest bright red
    ["R"] = "#b91923", -- Flag base rich crimson
    ["C"] = "#820f1c", -- Wave trough deep red shadow
    ["Z"] = "#4b0a14", -- Crevice darkest crimson/wine
    
    -- Grass & Earthen Mound
    ["E"] = "#73af37", -- Grass bright highlight
    ["P"] = "#4b8723", -- Grass base green
    ["N"] = "#2d5519", -- Grass shadow green
    ["D"] = "#734626", -- Earth soil brown
    ["V"] = "#442614"  -- Earth deep soil
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
            else
                img:drawPixel(x - 1, y - 1, Color{ r = 0, g = 0, b = 0, a = 0 })
            end
        end
    end
end

local f1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "..........##....................................",
    ".........#YG#...................................",
    ".........#OJ#...................................",
    "..........##....................................",
    ".........#TU#...................................",
    ".........#TUYFF.................................",
    ".........#TU#YYFFF.....FFFFFFF..................",
    ".........#TU#AAYYGFFFFFJJJGGYYF...........F.....",
    ".........#TU#AAAABGJJJJCCCRBAAYF.........F......",
    ".........#TU#AAAABRCCCCCCCRBAAAYFF......F.......",
    ".........#TU#AAAABRCCCCCCCRBAAAAYYF...FFF.......",
    ".........#TU#AAAABRCCCCCCCCBBBAAAAYFFFJF........",
    ".........#TU#BBBBBCCCCCCCCCBBBBAAAAGGJF.........",
    ".........#TU#BBBBBCCCCCZZZCRBBBBAAABRF..........",
    ".........#TU#BBBBRCZZZZZZZCRBBBBBBGBFF..........",
    ".........#TU#BBBBRCZZZZZZZCRBBBBBBBF......F.....",
    ".........#TU#BBBBRCZZZZZJJOOGGGBBBGF....FFF.....",
    ".........#TU#BBBBRCZZZJJFFFFFFFGBBBF...FJF......",
    ".........#TU#GGGGOOJJJFF.......FGBBRFFFJF.......",
    ".........#TUYFFFFFFFFF..........FGGRCJJF........",
    ".........#TU#....................FFOOFF.........",
    ".........#TU#......................FF...........",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    "......##E#TU#PEPE##.............................",
    "......#PP#TU#NNNNN#.............................",
    "...##PPPPPDDDDDDDDDDD##.........................",
    "...#DDDDDDDDDDVVVVVVVV#.........................",
    "...#VVVVVVVVVVVVVVVVVV#.........................",
    "....SSSSSSSSSSSSSSSSSS..........................",
    "......SSSSSSSSSSSSSS............................",
    ".........SSSSSSSS...............................",
    "................................................",
}
local f2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "..........##....................................",
    ".........#YG#...................................",
    ".........#OJ#...................................",
    "..........##....................................",
    ".........#TU#...................................",
    ".........#TUYFFFF...............................",
    ".........#TU#GYYYFF.........FFFFFF..............",
    ".........#TU#RBAAYYFFF....FFJJJGYYF.............",
    ".........#TU#RBAAAAYYYFFFFJJCCRRBAYF............",
    ".........#TU#RBAAAAAABGJJJCCCCRRBAAYF...........",
    ".........#TU#RBAAAAAABRRCCCCCCCRBAAAYF..........",
    ".........#TU#RBBBAAAABRRCCCCCCCRBBGAAYFF..F.....",
    ".........#TU#RBBBBBAABRRCCCCCCCRRBBGFAFYFFF.....",
    ".........#TU#RRBBBBBBBRCCCCCZZCRRBGF.F.FF.......",
    ".........#TU#RRBBBBBBRRCCCZZZZCRRBBF............",
    ".........#TU#RRBBBBBBRRCZZZZZZJOGGBF............",
    ".........#TU#RRBBBBBBRRCZZZZJJFFFFGBF...........",
    ".........#TU#RRGGGBBBRRCZZZJFF....FGBF..........",
    ".........#TU#OGFFFGGGGRCJJJF.......FGGF.........",
    ".........#TUYFF...FFFFOJFFF.........FFGFF.......",
    ".........#TU#.........FF..............FGOFF.....",
    ".........#TU#..........................FFF......",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    "......##E#TU#PEPE##.............................",
    "......#PP#TU#NNNNN#.............................",
    "...##PPPPPDDDDDDDDDDD##.........................",
    "...#DDDDDDDDDDVVVVVVVV#.........................",
    "...#VVVVVVVVVVVVVVVVVV#.........................",
    "....SSSSSSSSSSSSSSSSSS..........................",
    "......SSSSSSSSSSSSSS............................",
    ".........SSSSSSSS...............................",
    "................................................",
}
local f3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "..........##....................................",
    ".........#YG#...................................",
    ".........#OJ#...................................",
    "..........##....................................",
    ".........#TU#...................................",
    ".........#TUYFFFFFFF............................",
    ".........#TU#JJJJGGYFF...........FFFFF..........",
    ".........#TU#CCCCRBAYYFF........FJJGGYF.........",
    ".........#TU#CCCCRBAAAYYFF....FFJCCRBAFF........",
    ".........#TU#CCCCRBAAAAAYYFFFFJJCCCRFF.FF.......",
    ".........#TU#CCCCRBAAAAAAAGGJJCCCCJF....FF......",
    ".........#TU#CCCCCBBAAAAAABRCCCCCCCF.....FF.....",
    ".........#TU#CCCCCBBBBBAAABRCCCCCCJF......F.....",
    ".........#TU#ZZZZCRBBBBBBABRCCCCZZZCFF..........",
    ".........#TU#ZZZZCRBBBBBBBBCCCCZZZZCOBF.........",
    ".........#TU#ZZZZCRBBBBBBBBCCZZZZZJOFGGF........",
    ".........#TU#ZZZZCRBBBBBBBRCZZZZJJFF.FFGF.......",
    ".........#TU#ZZZJOOGGGGBBBRCZZZJFF.....FF.......",
    ".........#TU#JJJFFFFFFFGGBRCZJJF........F.......",
    ".........#TUYFFF.......FFGOOJFF..........F......",
    ".........#TU#............FFFF.............F.....",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    "......##E#TU#PEPE##.............................",
    "......#PP#TU#NNNNN#.............................",
    "...##PPPPPDDDDDDDDDDD##.........................",
    "...#DDDDDDDDDDVVVVVVVV#.........................",
    "...#VVVVVVVVVVVVVVVVVV#.........................",
    "....SSSSSSSSSSSSSSSSSS..........................",
    "......SSSSSSSSSSSSSS............................",
    ".........SSSSSSSS...............................",
    "................................................",
}
local f4_grid = {
    "................................................",
    "................................................",
    "................................................",
    "..........##....................................",
    ".........#YG#...................................",
    ".........#OJ#...................................",
    "..........##....................................",
    ".........#TU#...................................",
    ".........#TUYFF......FFF........................",
    ".........#TU#GJFFFFFFJGYFF............FFFF......",
    ".........#TU#RRJJJJJJRRBYYF..........FJJFFF.....",
    ".........#TU#RRCCCCCCRRBAAYFF.......FJFF........",
    ".........#TU#RRCCCCCCRRBAAAYYF....FFJF..........",
    ".........#TU#RRCCCCCCCRBAAAAAYFFFFJJCF..........",
    ".........#TU#RCCCCCCCCRBBAAAAAYGJJCCF...........",
    ".........#TU#RCCCCCCCCRRBBBAAABRRCCF............",
    ".........#TU#RCCCCZZZCRRBBBBBABRRCJF....F.......",
    ".........#TU#RCZZZZZZCRRBBBBBBBRCCCF.FFFF.......",
    ".........#TU#RCZZZZZZCRRBBBBBBBRCCJJFZJFFFF.....",
    ".........#TU#RCZZZZZZJOGGBBBBBRRCZZZZJF...F.....",
    ".........#TU#RCZZZJJJFFFFGGBBBRRCZZZJF..........",
    ".........#TU#OJJJJFFF....FFGGBRRCZJJF...........",
    ".........#TUYFFFFF.........FFGGOJJFF............",
    ".........#TU#................FFFFF..............",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    ".........#TU#...................................",
    "......##E#TU#PEPE##.............................",
    "......#PP#TU#NNNNN#.............................",
    "...##PPPPPDDDDDDDDDDD##.........................",
    "...#DDDDDDDDDDVVVVVVVV#.........................",
    "...#VVVVVVVVVVVVVVVVVV#.........................",
    "....SSSSSSSSSSSSSSSSSS..........................",
    "......SSSSSSSSSSSSSS............................",
    ".........SSSSSSSS...............................",
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

-- Ensure output directories exist
-- (Handled by runner batch or OS)

-- Save Aseprite project
sprite:saveCopyAs("output/aseprite/waving_flag_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/waving_flag_48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/waving_flag_48_sheet.png")
sheetSprite:close()
