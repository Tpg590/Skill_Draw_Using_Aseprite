-- scripts/melting_candle_32x48.lua
local width = 32
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Candle"
sprite.frames[1].duration = frameDuration

-- 1. Palette: Terraria Crimson Wax & Brass Plate (High Contrast)
local PALETTE = {
    ["."] = nil,
    ["S"] = "#140a10", -- Soft ground shadow (Alpha 130)
    ["#"] = "#18060a", -- Terraria dark crimson-black outline
    ["A"] = "#e83838", -- Crimson wax bright highlight
    ["B"] = "#aa1828", -- Crimson wax rich midtone
    ["C"] = "#660a18", -- Crimson wax deep shadow
    ["D"] = "#38040c", -- Crimson wax deepest crevice
    ["W"] = "#ffffff", -- Flame white-hot core
    ["Y"] = "#ffe850", -- Flame bright yellow
    ["O"] = "#f87818", -- Flame vibrant orange
    ["R"] = "#c82010", -- Flame outer red
    ["G"] = "#ffbe40", -- OSL golden molten wax rim
    ["K"] = "#14080a", -- Charred wick
    ["M"] = "#d8b878", -- Metal plate brass highlight
    ["N"] = "#987840", -- Metal plate brass midtone
    ["P"] = "#584020", -- Metal plate brass shadow
}

local frame1_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...............R................",
    "...............R................",
    "...............O................",
    "..............ROR...............",
    ".............ROYOR..............",
    ".............OYWYO..............",
    ".............OYWYO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA#####........",
    ".........#AGGGGGGGABCDAG#.......",
    ".........#AAAAABBBBBBBABC#......",
    ".........#AABBBBBBCCDDBBC#......",
    ".........#ABBBBBBCCCDDBC#.......",
    ".........#AABBBBBCCCDD##........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    "....######AABBBBBCCCDD######....",
    "....#MMMM##############NNNN#....",
    "....#MMNNNNNNNNNNNPPPPPPPP##....",
    ".....#NNNNNNNNNPPPPPPPPPPP#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frame2_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................R...............",
    "................R...............",
    "................O...............",
    "...............ROR..............",
    "...............OY...............",
    "..............OYYO..............",
    ".............OYWWO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA###..........",
    ".........#AGGGGGGGABCD#.........",
    ".........#AAAAABBBBBBBB#........",
    ".........#AABBBBBBCCDDB#........",
    ".........#ABBBBBBCCCDDB#........",
    ".........#AABBBBBCCCDDB#........",
    ".........#AABBBBBBCCDDB#........",
    ".........#ABBBBBBBCCDDB#........",
    ".........#AABBBBBCCCDDAB#.......",
    ".........#AABBBBBCCCDDABC#......",
    ".........#ABBBBBBBCCDDBBC#......",
    ".........#AABBBBBBCCDDCC#.......",
    ".........#AABBBBBCCCDD##........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    "....######AABBBBBCCCDD######....",
    "....#MMMM##############NNNN#....",
    "....#MMNNNNNNNNNNNPPPPPPPP##....",
    ".....#NNNNNNNNNPPPPPPPPPPP#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frame3_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................Y...............",
    "................................",
    "...............R................",
    "...............R................",
    "...............O................",
    "...............O................",
    "..............OYO...............",
    ".............R.Y.R..............",
    ".............OYWYO..............",
    ".............OYWYO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA###..........",
    ".........#AGGGGGGGABCD#.........",
    ".........#AAAAABBBBBBB#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBCCCDDB#........",
    ".........#ABBBBBBCCCDDB#........",
    ".........#AABBBBBBCCDDAB#.......",
    ".........#AABBBBBBCCDDABC#......",
    ".........#ABBBBBBCCCDDABC#......",
    ".........#AABBBBBCCCDDBBC#......",
    ".........#AABBBBBBCCDD#C#.......",
    ".........#ABBBBBBBCCDD##........",
    "....######AABBBBBCCCDD######....",
    "....#MMMM##############NNNN#....",
    "....#MMNNNNNNNNNNNPPPPPPPP##....",
    ".....#NNNNNNNNNPPPPPPPPPPP#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frame4_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "..............R.................",
    "..............R.................",
    "..............O.................",
    ".............ROR................",
    "..............YO................",
    ".............OYYO...............",
    ".............OWWYO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA###..........",
    ".........#AGGGGGGGABCD#.........",
    ".........#AAAAABBBBBBB#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBBCCDB#.........",
    ".........#AABBBBBBCCDC#.........",
    ".........#ABBBBBBCCCDD#..#......",
    ".........#AABBBBBCCCDD#.#A#.....",
    ".........#AABBBBBBCCDD#.#B#.....",
    ".........#ABBBBBBBCCDD#.###.....",
    "....######AABBBBBCCCDD######....",
    "....#MMMM##############NNNN#....",
    "....#MMNNNNNNNNNNNPPPPPPPP##....",
    ".....#NNNNNNNNNPPPPPPPPPPP#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frame5_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...............O................",
    "................................",
    "................R...............",
    "................R...............",
    "................O...............",
    "...............ROR..............",
    "...............OY...............",
    "..............OYYO..............",
    ".............OYWWO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA###..........",
    ".........#AGGGGGGGABCD#.........",
    ".........#AAAAABBBBBBB#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    "....######AABBBBBCCCDD######....",
    "....#MMMM############AABBC##....",
    "....#MMNNNNNNNNNNNPP#BBCC###....",
    ".....#NNNNNNNNNPPPPPP####P#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frame6_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...............R................",
    "...............R................",
    "...............O................",
    "..............ROR...............",
    ".............ROYOR..............",
    ".............OYWYO..............",
    ".............OYWYO..............",
    ".............RYWYR..............",
    "..............OWO...............",
    "..............R.R...............",
    "...............O................",
    "..............#K#...............",
    "...........####K#####...........",
    "..........##AAGKGAA####.........",
    ".........#AGGGGGGGABCDG#........",
    ".........#AAAAABBBBBBBAB#.......",
    ".........#AABBBBBBCCDD##........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBCCCDD#.........",
    ".........#AABBBBBCCCDD#.........",
    ".........#AABBBBBBCCDD#.........",
    ".........#ABBBBBBBCCDD#.........",
    "....######AABBBBBCCCDD######....",
    "....#MMMM#############BBC#N#....",
    "....#MMNNNNNNNNNNNPPP#CCD###....",
    ".....#NNNNNNNNNPPPPPPP###P#.....",
    "....SS####################SSS...",
    "......SSSSSSSSSSSSSSSSSSSSS.....",
    "..........SSSSSSSSSSSSS.........",
    "................................"
}

local frames_data = { frame1_grid, frame2_grid, frame3_grid, frame4_grid, frame5_grid, frame6_grid }

-- 2. Render Function
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

-- Render Frame 1 into initial cel
renderGrid(sprite.cels[1].image, frame1_grid, PALETTE)

-- Render Frames 2 to 6
for i = 2, #frames_data do
    local frame = sprite:newEmptyFrame()
    frame.duration = frameDuration
    local img = Image(width, height, ColorMode.RGB)
    renderGrid(img, frames_data[i], PALETTE)
    sprite:newCel(layer, frame, img)
end

-- 3. Export Files via CLI
sprite:saveCopyAs("output/aseprite/melting_candle_32x48.aseprite")
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/gif/melting_candle_32x48.gif")
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/Sheet/melting_candle_32x48_sheet.png")
    sheetSprite:close()
else
    sprite:saveCopyAs("output/Sheet/melting_candle_32x48.png")
end
