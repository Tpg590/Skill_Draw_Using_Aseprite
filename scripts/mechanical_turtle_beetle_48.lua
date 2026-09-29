-- scripts/mechanical_turtle_beetle_48.lua
-- 48x48 Mechanical Turtle Beetle Walk Cycle (4 Frames, 6 FPS)
-- Art Style: Stardew Valley (Warm Brass, Hardwood Carapace, Diagonal Gait)

local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Turtle_Beetle"

-- Configure Frame 1 duration
sprite.frames[1].duration = frameDuration

local PALETTE = {
    ["."] = nil,
    ["S"] = "#1e1218", -- Soft contact ground shadow (Alpha 130)
    ["#"] = "#2a1610", -- Warm dark espresso outline (NO #000000)
    
    -- Polished Warm Brass / Gold Filigree
    ["A"] = "#ffe680", -- Specular brass highlight
    ["B"] = "#e6a820", -- Warm polished brass midtone
    ["C"] = "#9c6410", -- Shaded bronze/brass
    ["D"] = "#5c360c", -- Deep bronze recess
    
    -- Warm Hardwood Carapace Shell (Turtle plates)
    ["W"] = "#c87830", -- Shell highlight wood plate
    ["X"] = "#9e4a18", -- Shell warm amber midtone
    ["Z"] = "#5a240c", -- Shell deep mahogany shadow
    ["K"] = "#381408", -- Shell seam crevice
    
    -- Clockwork Gears & Mechanical Claw Legs (Iron/Bronze alloy)
    ["H"] = "#b4bec8", -- Metal leg highlight
    ["M"] = "#78828e", -- Metal leg midtone
    ["L"] = "#444c58", -- Metal leg shadow
    
    -- Glowing Topaz Eyes / Clockwork Energy Core
    ["E"] = "#ffee66", -- Glowing topaz yellow
    ["Q"] = "#e69000"  -- Deep amber glow
}


local frame1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "...................#........#...................",
    "..................#A#.####.#A#..................",
    "..................#B##AAAA##B#..................",
    "...................#CBBBBBBC#...................",
    "...................#BEBBBBEB#...................",
    "...................#CQBBBBQC#...................",
    ".................##BBABBABBAB##.................",
    "......#.........#ABWWWWWXXXXXAB#................",
    ".....#A######..#ABWWKWWXXXXKZZBA#...............",
    "....#HMLMMHHH##ABWWWKWXXXXXKZZZBB#.......#......",
    "....#HMLLLLLM#BBWWWWKXXXXXZKZZZZCC#######A#.....",
    ".....#HML#LLL#BBKKKKKKKKAKKKKKKKCC#LLLLLHML#....",
    ".....#HML#####BBXXXXKXXAAAZKZZZZCC######HML#....",
    "......#HL#...#BBXXXXKXBBDBBKZZZZCC#...#HMLL#....",
    "......#HA#...#BBXXXXKXXCCCZKZZZZCC#...#HML#.....",
    ".......##...##BBXXXXKXXXCZZKZZZZCC###.#HL#......",
    "..........##H#BBKKKKKKKKKKKKKKKKCC#HH##ML#......",
    ".........#HHHL#DCXXXKXXXZZZKZZZDC#LMMHHAL#......",
    ".......##HHML###DCXXKXXXZZZKZZDC###LLMHHH##.....",
    "......#HHMLL#...#DCZKZZZZZZKZDC#...##LLMHAH#....",
    ".....#AHML##.....#DCZZZZZZZZDC#......##LHML#....",
    "....#HMLL#........##CDCDCDCD##........#HMLL#....",
    "....#HHML#..........########.........#HMLL#.....",
    ".....#HML#.......SSSSSSSSSSSSSS......#MLL#......",
    "......#HML#....SSSSSSSSSSSSSSSSSS...#HLL#.......",
    "......#HML#...SSSSSSSSSSSSSSSSSSSS..#AL#........",
    ".......#HML#..SSSSSSSSSSSSSSSSSSSS...##.........",
    "........#HL#...SSSSSSSSSSSSSSSSSS...............",
    "........#HA#....SSSSSSSSSSSSSSSS................",
    ".........##S......SSSSSSSSSSSS.......S..........",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}

local frame2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "...................#........#...................",
    "..................#A#.####.#A#..................",
    "..................#B##AAAA##B#..................",
    "...................#CBBBBBBC#...................",
    "...................#BEBBBBEB#...................",
    "...................#CQBBBBQC#...................",
    ".................##BABBABBABB##.................",
    "................#BBWWWWWXXXXXBB#................",
    "......#........#BBWWKWWXXXXKZZAB#........#......",
    ".....#A########BBWWWKWXXXXXKZZZBA########A#.....",
    "....#HMLMMMMM#BBWWWWKXXXXXZKZZZZCC#HMMMMHML#....",
    "....#HMLLLLLL#BBKKKKKKKKAKKKKKKKCC#LLLLLHML#....",
    "....#HHML#####BBXXXXKXAAAAZKZZZZCC#####HMLL#....",
    ".....#HML#...#BBXXXXKXBBDBBKZZZZCC#...#HML#.....",
    "......#HL#...#BBXXXXKXXCCCZKZZZZCC#...#HL#......",
    "......#HL#.###BBXXXXKXXXCZZKZZZZCC###.#ML#......",
    "......#HA##HH#BBKKKKKKKKKKKKKKKKCC#HH##AL#......",
    "......S##HHHML#CDXXXKXXXZZZKZZZCD#LMHHH##S......",
    "......#HHHMLL###CDXXKXXXZZZKZZCD###LLMHHH#......",
    ".....#AHMLL##...#CDZKZZZZZZKZCD#...##LLMHA#.....",
    "....#HMLL##......#CDZZZZZZZZCD#......##LHML#....",
    "....#HHML#........##DCDCDCDC##........#HMLL#....",
    ".....#HML#......SSSS########SSSS......#HML#.....",
    "......#HML#...SSSSSSSSSSSSSSSSSSSS...#HML#......",
    "......#HML#..SSSSSSSSSSSSSSSSSSSSSS..#MLL#......",
    ".......#HML#.SSSSSSSSSSSSSSSSSSSSSS.#HML#.......",
    "........#HL#..SSSSSSSSSSSSSSSSSSSS..#HL#........",
    "........#HA#...SSSSSSSSSSSSSSSSSS...#AL#........",
    ".........##S.....SSSSSSSSSSSSSS.....S##.........",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}

local frame3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "...................#........#...................",
    "..................#A#.####.#A#..................",
    "..................#B##AAAA##B#..................",
    "...................#CBBBBBBC#...................",
    "...................#BEBBBBEB#...................",
    "...................#CQBBBBQC#...................",
    ".................##BBABBABBAB##.................",
    "................#ABWWWWWXXXXXAB#.........#......",
    "...............#ABWWKWWXXXXKZZBA#...#####A#.....",
    "......#.......#ABWWWKWXXXXXKZZZBB###HHMMHML#....",
    ".....#A#######BBWWWWKXXXXXZKZZZZCC#MLLLHMML#....",
    "....#HMLLLLLL#BBKKKKKKKKAKKKKKKKCC#LL##HML#.....",
    "....#HML######BBXXXXKXXAAAZKZZZZCC###.#HLL#.....",
    "....#HHML#...#BBXXXXKXBBDBBKZZZZCC#...#ML#......",
    ".....#HML#...#BBXXXXKXXCCCZKZZZZCC#...#AL#......",
    "......#HL#.###BBXXXXKXXXCZZKZZZZCC##...##.......",
    "......#HL##HH#BBKKKKKKKKKKKKKKKKCC#H##..........",
    "......#HAHHMML#DCXXXKXXXZZZKZZZDC#LHHH#.........",
    "......#HHHMLL###DCXXKXXXZZZKZZDC###LMHH##.......",
    ".....#AHMLL##...#DCZKZZZZZZKZDC#...#LLMHH#......",
    "....#HMLL##......#DCZZZZZZZZDC#.....##LMHA#.....",
    "....#HHML#........##CDCDCDCD##........#LHML#....",
    ".....#HHML#.........########..........#HMLL#....",
    "......#HHL#......SSSSSSSSSSSSSS.......#HML#.....",
    ".......#HHL#...SSSSSSSSSSSSSSSSSS....#HML#......",
    "........#HA#..SSSSSSSSSSSSSSSSSSSS...#MLL#......",
    ".........##...SSSSSSSSSSSSSSSSSSSS..#HML#.......",
    "...............SSSSSSSSSSSSSSSSSS...#HL#........",
    "................SSSSSSSSSSSSSSSS....#AL#........",
    "..........S.......SSSSSSSSSSSS......S##.........",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}

local frame4_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "...................#........#...................",
    "..................#A#.####.#A#..................",
    "..................#B##AAAA##B#..................",
    "...................#CBBBBBBC#...................",
    "...................#BEBBBBEB#...................",
    "...................#CQBBBBQC#...................",
    ".................##BBABBABBAB##.................",
    "................#ABWWWWWXXXXXAB#................",
    "...............#ABWWKWWXXXXKZZBA#...............",
    "......#.......#ABWWWKWXXXXXKZZZBB#.......#......",
    ".....#A#######BBWWWWKXXXXXZKZZZZCC#######A#.....",
    "....#HMLLLLLL#BBKKKKKKKKAKKKKKKKCC#LLLLLHML#....",
    "....#HML######BBXXXXKXXAAAZKZZZZCC######HML#....",
    "....#HHML#...#BBXXXXKXBBDBBKZZZZCC#...#HMLL#....",
    ".....#HML#...#BBXXXXKXXCCCZKZZZZCC#...#HML#.....",
    "......#HL#..##BBXXXXKXXXCZZKZZZZCC##..#HL#......",
    "......#HL###H#BBKKKKKKKKKKKKKKKKCC#H###ML#......",
    "......#HA#HHHL#DCXXXKXXXZZZKZZZDC#LHHH#AL#......",
    "......S##HHML###DCXXKXXXZZZKZZDC###LMHH##S......",
    "......#HHMLL#...#DCZKZZZZZZKZDC#...#LLMHH#......",
    ".....#AHML##.....#DCZZZZZZZZDC#.....##LMHA#.....",
    "....#HMLL#........##CDCDCDCD##........#LHML#....",
    "....#HHML#..........########..........#HMLL#....",
    ".....#HML#.......SSSSSSSSSSSSSS.......#HML#.....",
    "......#HML#....SSSSSSSSSSSSSSSSSS....#HML#......",
    "......#HML#...SSSSSSSSSSSSSSSSSSSS...#MLL#......",
    ".......#HML#..SSSSSSSSSSSSSSSSSSSS..#HML#.......",
    "........#HL#...SSSSSSSSSSSSSSSSSS...#HL#........",
    "........#HA#....SSSSSSSSSSSSSSSS....#AL#........",
    ".........##S......SSSSSSSSSSSS......S##.........",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}


local frame_grids = {
    frame1_grid,
    frame2_grid,
    frame3_grid,
    frame4_grid
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

-- Render Frame 1
local img1 = sprite.cels[1].image
img1:clear()
renderGrid(img1, frame_grids[1], PALETTE)

-- Create and Render Frames 2 to 4 with clean cel initialization
for i = 2, #frame_grids do
    local newFrame = sprite:newFrame()
    newFrame.duration = frameDuration
    local cel = layer:cel(i)
    if not cel then
        cel = sprite:newCel(layer, newFrame)
    end
    cel.image:clear()
    renderGrid(cel.image, frame_grids[i], PALETTE)
end

-- Save outputs as required
sprite:saveCopyAs("output/aseprite/mechanical_turtle_beetle_48.aseprite")
sprite:saveCopyAs("output/gif/mechanical_turtle_beetle_48.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/mechanical_turtle_beetle_48_sheet.png")
sheetSprite:close()
sprite:close()
