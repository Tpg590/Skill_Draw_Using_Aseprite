-- scripts/magic_torch_32x48.lua
-- 32x48 Terraria Animated Magic Violet/Pink Torch on Stone Pedestal
local width = 32
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Magic_Torch"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria chunky shading, near-black outline, magic violet/pink flame exception
local PALETTE = {
    ["."] = nil,
    ["#"] = "#120a14", -- Near-black Terraria outline with deep violet tint
    ["S"] = "#140a18", -- Soft ground shadow (Alpha 130)
    
    -- Iron Torch Brazier & Shaft
    ["I"] = "#a0acb9", -- Iron highlight
    ["F"] = "#555f70", -- Iron midtone
    ["L"] = "#2a303a", -- Iron shadow
    
    -- Carved Stone Pedestal
    ["G"] = "#7d8796", -- Stone highlight
    ["D"] = "#48505a", -- Stone midtone
    ["N"] = "#262a32", -- Stone shadow
    
    -- OSL Pink Glow on Metal
    ["O"] = "#ff82e6", -- Vivid magic pink glow reflection
    
    -- Magic Violet/Pink Flame
    ["W"] = "#ffffff", -- White hot flame core
    ["K"] = "#ffc3f5", -- Pale pink sparks / inner glow
    ["P"] = "#f541c3", -- Vivid hot magenta/pink
    ["M"] = "#9b19af", -- Deep violet-purple flame
    ["V"] = "#4b0869"  -- Dark magic flame rim/smoke
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
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    ".....................KW.........",
    "....................VPMV........",
    "..........KW.......VPPPMV.......",
    "........VPMV......VPPKPMV.......",
    ".........KW......VPPKWKPMV......",
    "........VPMV....VPPKKWKKPMV.....",
    ".......VPPPMV..VPPKKWWKKKPMV....",
    "......VPPKWPMVVPPKKWWWWKKPMV....",
    "......VPPKWWPKKPPKKWWWWKKPMV....",
    "......VPPKKWWWWKKKKWWWWKKPMV....",
    ".......VPPKKWWWWWWWWWWKKPPMV....",
    "........VPPPKKKWWWWWKKKPPMV.....",
    ".........VVPPPPKKKKKPPPPMV......",
    ".......###OOOOOOOOOOOOO###......",
    "......#IIF#OOOOOOOOOOO#LFF#.....",
    ".......#IIF###########LFF#......",
    "........#IIFFFFFFFFFFFLL#.......",
    ".........###IIFFFFFLL###........",
    "..............#III#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "............#IIIFLLL#...........",
    ".............##FIL##............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "...........##########...........",
    "..........#GGGGGDDDDD#..........",
    "........################........",
    ".......#GGGGGGGGDDDDDDDN#.......",
    ".......#GGGGDDDDDDDNNNNN#.......",
    "......SSSSSSSSSSSSSSSSSSSS......",
    "........SSSSSSSSSSSSSSSS........",
    "...........SSSSSSSSSS...........",
    "................................",
}
local f2_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "......................KW........",
    "................................",
    ".........KW.....................",
    "................................",
    "............KW..................",
    "................................",
    "........VPMV....................",
    ".......VPPPMV.........VPMV......",
    "......VPPKWPMV.......VPPPMV.....",
    "......VPPKWWPMV.....VPPKPMV.....",
    "......VPPKKWWPMV...VPPKKWPMV....",
    "......VPPKKWWKKPPKKWWKKKKPMV....",
    "......VPPKKWWWWWWWWWWKKKKPMV....",
    ".......VPPPKKKWWWWWKKKPPMV......",
    "........VVPPPPKKKKKPPPPMV.......",
    ".........VVVPPPPPPPPPVV.........",
    ".......###OOOOOOOOOOOOO###......",
    "......#IIF#OOOOOOOOOOO#LFF#.....",
    ".......#IIF###########LFF#......",
    "........#IIFFFFFFFFFFFLL#.......",
    ".........###IIFFFFFLL###........",
    "..............#III#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "............#IIIFLLL#...........",
    ".............##FIL##............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "...........##########...........",
    "..........#GGGGGDDDDD#..........",
    "........################........",
    ".......#GGGGGGGGDDDDDDDN#.......",
    ".......#GGGGDDDDDDDNNNNN#.......",
    "......SSSSSSSSSSSSSSSSSSSS......",
    "........SSSSSSSSSSSSSSSS........",
    "...........SSSSSSSSSS...........",
    "................................",
}
local f3_grid = {
    "................................",
    "................................",
    ".....................KW.........",
    "................................",
    "..........KW....................",
    "................................",
    ".............KW.................",
    "................................",
    "................................",
    "....................VPMV........",
    "................................",
    ".......VPMV.........VPMV........",
    "......VPPPMV.......VPPPMV.......",
    ".....VPPKWPMV.....VPPKWPMV......",
    ".....VPPKWWPMV...VPPKWWPMV......",
    ".....VPPKKWWPMVVVPPKKWWPMV......",
    "......VPPKKWWKKKKKWWKKKKPMV.....",
    "......VPPKKWWWWWWWWWWKKKPMV.....",
    ".......VPPPKKKWWWWWKKKPPMV......",
    "........VVPPPPKKKKKPPPPMV.......",
    ".........VVVPPPPPPPPPVV.........",
    ".......###OOOOOOOOOOOOO###......",
    "......#IIF#OOOOOOOOOOO#LFF#.....",
    ".......#IIF###########LFF#......",
    "........#IIFFFFFFFFFFFLL#.......",
    ".........###IIFFFFFLL###........",
    "..............#III#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "............#IIIFLLL#...........",
    ".............##FIL##............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "...........##########...........",
    "..........#GGGGGDDDDD#..........",
    "........################........",
    ".......#GGGGGGGGDDDDDDDN#.......",
    ".......#GGGGDDDDDDDNNNNN#.......",
    "......SSSSSSSSSSSSSSSSSSSS......",
    "........SSSSSSSSSSSSSSSS........",
    "...........SSSSSSSSSS...........",
    "................................",
}
local f4_grid = {
    "................................",
    "...........KW...................",
    "................................",
    "..............KW................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "...............VPMV.............",
    "..............VPPPMV............",
    ".............VPPKWPMV...........",
    "......VPMV..VPPKWWPMV...........",
    ".....VPPPMVVPPKKWWPMV...VPMV....",
    ".....VPPKWKKWWWWKKPMV..VPPPMV...",
    "......VPPKKWWWWWKKPMVVVPPKWPMV..",
    "......VPPKKWWWWWWWWWWKKKKPMV....",
    "......VPPKKWWWWWWWWWWKKKKPMV....",
    ".......VPPPKKKWWWWWKKKPPMV......",
    "........VVPPPPKKKKKPPPPMV.......",
    ".........VVVPPPPPPPPPVV.........",
    ".......###OOOOOOOOOOOOO###......",
    "......#IIF#OOOOOOOOOOO#LFF#.....",
    ".......#IIF###########LFF#......",
    "........#IIFFFFFFFFFFFLL#.......",
    ".........###IIFFFFFLL###........",
    "..............#III#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "............#IIIFLLL#...........",
    ".............##FIL##............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    "..............#FIL#.............",
    ".............##FIL##............",
    "...........##########...........",
    "..........#GGGGGDDDDD#..........",
    "........################........",
    ".......#GGGGGGGGDDDDDDDN#.......",
    ".......#GGGGDDDDDDDNNNNN#.......",
    "......SSSSSSSSSSSSSSSSSSSS......",
    "........SSSSSSSSSSSSSSSS........",
    "...........SSSSSSSSSS...........",
    "................................",
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
sprite:saveCopyAs("output/aseprite/magic_torch_32x48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/magic_torch_32x48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/magic_torch_32x48_sheet.png")
sheetSprite:close()
