-- scripts/void_portal.lua
-- 48x48 Void Portal on Ancient Stone Dais (6 Frames, 8 FPS)
-- Art Style: Terraria (Basalt Stone Dais, Absolute Black Singularity, Swirling Void Gradient, 3/4 Squashed Cyan Particle Spiral)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Void_Portal"

sprite.frames[1].duration = frameDuration

local PALETTE = {
    ["."] = nil,
    ["#"] = "#0a0410",
    ["S"] = "#08040d",
    ["T"] = "#76668a",
    ["R"] = "#524464",
    ["G"] = "#342844",
    ["D"] = "#1c1426",
    ["A"] = "#a840eb",
    ["B"] = "#7820ba",
    ["C"] = "#4e0e80",
    ["E"] = "#2c064a",
    ["F"] = "#140224",
    ["Z"] = "#020005",
    ["W"] = "#ffffff",
    ["I"] = "#38ffff",
    ["M"] = "#00c3e1",
    ["K"] = "#0e6080",
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRITRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTRTTRTTRTTRTTRTTRTTRTTRTT#.........",
    "........##RRGRRRGRR####AAB####RRGRRRGRR##.......",
    ".......##RRGRRRGR#AAABBAABBAABB#RRRGRRRG##......",
    "......##RRGRRRG##CCCCCCCCCCCCCCC##GRRRGRR##.....",
    "......#RRGRRRG#ACCCEEEEEEEEEEECCCB#RRGRRRG#.....",
    "......#RGRRRGR#BCCEEFFFZZZFFFEECCA#RGRRRGR#.....",
    "......#GRRRGR##AACCEEFFZZZFFEECCAA##RRRIRR#.....",
    "......#RRRGRRR#BBBCCCEEZZZEECCCBAA#RRRGRRR#.....",
    "......#RRGRRRG#AAAACCCEFFFECCCAABB#RRGRRRG#.....",
    "......##GRRRGRR##BBBCCEEEEECCBBA##RRGRRRG##.....",
    "......###GGGGDGGG#AAACCCCCCCABB#GDGGGGDG###.....",
    "......####DGGGGDGGG####AAB####DGGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGIGDGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRTTRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTRTTRTTRTTRTTRTIRTTRTTRTT#.........",
    "........##RRGRRRGRR####AAB###IRRGRRRGRR##.......",
    ".......##RRGRRRGR#AABCCCCCCCAAA#RRRGRRRG##......",
    "......##RRGRRRG##BBACCEEEEECCABB##GRRRGRR##.....",
    "......#RRGRRRG#AAAACCCEFFFECCCBAAA#RRGRRRG#.....",
    "......#RGRRRGR#BBBCCCEEZZZEECCCBBB#RGRRRGR#.....",
    "......#GRRRGRI#AACCEEFFZZZFFEECCAA##RRRGRR#.....",
    "......#RRRGRIR#BCCEEFFFZZZFFFEECCB#RRRGRRR#.....",
    "......#RRGRRRG#BCCCEEEEEEEEEEECCCB#RRGRRRG#.....",
    "......##GRRRGRR##CCCCCCCCCCCCCCC##RRGRRRG##.....",
    "......###GGGGDGGG#BAABBAABBAAAB#GDGGGGDG###.....",
    "......####DGGGGDGGG####AAA####IIGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGGGDGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRTTRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTRTTRTTRTTRTTRTTRTTRTTRTT#.........",
    "........##RRGRRRGRR####BAA####RRGRRRGRR##.......",
    ".......##RRGRRRGR#AAIWBBAABBBAA#RRRGRRRG##......",
    "......##RRGRRRG##CCCCCCCCCCCCCCC##GRRRGRR##.....",
    "......#RRGRRRG#ACCCEEEEEEEEEEECCCA#RRGRRRG#.....",
    "......#RGRRRGR#BCCEEFFFZZZFFFEECCB#RGRRRGR#.....",
    "......#GRRRGR##AACCEEFFZZZFFEECCWI##RRRGRR#.....",
    "......#RRRGRRR#ABBCCCEEZZZEECCCBBB#RRRGRRR#.....",
    "......#RRGRRRG#BBAACCCEFFFECCCAAAA#RRGRRRG#.....",
    "......##GRRRGRR##ABWCCEEEEECCBBB##RRGRRRG##.....",
    "......###GGGGDGGG#BAICCCCCCCAAA#GDGGGGDG###.....",
    "......####DGGGGDGGG####BAA####DGGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGGGDGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRTTRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTRTTRTTRTTRTTRTTRTTRTTRTT#.........",
    "........##RRGRRRGRR####BAA####RRGRRRGRR##.......",
    ".......##RRGRRRGR#BBACCCCCCCAAA#RRRGRRRG##......",
    "......##RRGRRRG##ABBCCEEEEEKCBBB##GRRRGRR##.....",
    "......#RRGRRRG#BBAACCCEFFFECMCAAAA#RRGRRRG#.....",
    "......#RGRRRGR#AABCMWEEZZZEEWCCBBB#RGRRRGR#.....",
    "......#GRRRGR##BBCKEEFFZZZFFEECCAA##RRRGRR#.....",
    "......#RRRGRRR#ACCEEFFFZZZFFFEECCB#RRRGRRR#.....",
    "......#RRGRRRG#BCCCEEEEEEEEEEECCCA#RRGRRRG#.....",
    "......##GRRRGRR##CCCCCCCWMKCCCCC##RRGRRRG##.....",
    "......###GGGGDGGG#BBAABBAABBAAA#GDGGGGDG###.....",
    "......####DGGGGDGGG####BAA####DGGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGGGDGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}

local frame5_grid = {
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRTTRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTRTTRTTRTTRTTRTTRTTRTTRTT#.........",
    "........##RRGRRRGRR####AAA####RRGRRRGRR##.......",
    ".......##RRGRRRGR#BAAABBAABBAAB#RRRGRRRG##......",
    "......##RRGRRRG##CCCCCCCKCCCCCCC##GRRRGRR##.....",
    "......#RRGRRRG#BCCCEEEEEEMEEEECCCB#RRGRRRG#.....",
    "......#RGRRRGR#BCCEEFFFZZWFFFEECCB#RGRRRGR#.....",
    "......#GRRRGR##BBCCEEMWZZZFFEECCAA##RRRGRR#.....",
    "......#RRRGRRR#AAACCKEEZZWMKCCCBBB#RRRGRRR#.....",
    "......#RRGRRRG#BBBBCCCEFFFECCCBAAA#RRGRRRG#.....",
    "......##GRRRGRR##AABCCEEEEECCABB##RRGRRRG##.....",
    "......###GGGGDGGG#BBACCCCCCCBAA#GDGGGGDG###.....",
    "......####DGGGGDGGG####BBA####DGGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGGGDGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
}

local frame6_grid = {
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".................#######T#######................",
    "..............##RTTRTTRTTRTTRTTRT##.............",
    "...........##TTRTTRTTRTTRTTRTTRTTRTT##..........",
    "..........#RTTKTTRTTRTTRTTRTTRTTRTTRTT#.........",
    "........##RRGRRRGRR####AAB####RRGRRRGRR##.......",
    ".......##RRGRRRGR#AAACCCCCCCAAB#RRRGRRRG##......",
    "......##RRGRRRG##BBBCCEEEEECCBBA##GRRRGRR##.....",
    "......#RRGRRRG#AAAACCCEFFFECCCAABB#RRGRKRG#.....",
    "......#RGRRRGR#BBBCCCEEZZZEECCCBBA#RGRRRGR#.....",
    "......#GRRRGR##BBCCEEFFZZZFFEECCAA##RRRGRR#.....",
    "......#RRRGRRR#ACCEEFFFZZZFFFEECCB#RRRGRRR#.....",
    "......#RRGRRRG#BCCCEEEEEEEEEEECCCA#RRGRRRG#.....",
    "......##GRRRGRR##CCCCCCCCCCCCCCC##RRGRRRG##.....",
    "......###GGGGDGGG#BBBAABBAABBAA#GDGGGGDG###.....",
    "......####DGGGGDGGG####BBA####DGGGGDGGG####.....",
    "......#####GDGGGGDGGGGDGGGGDGGGGDGGGGD#####.....",
    "......####R##GDGGGGKGGGGDGGGGDGGGGDG##G####.....",
    ".......###RRTD##DGGGGDGGGGDGGGGDG##DGDG###......",
    "........################G################.......",
    ".....SSSSSS###########################SSSSS.....",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
    "................SSSSSSSSSSSSSSSSS...............",
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
    frame4_grid,
    frame5_grid,
    frame6_grid
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

-- Create and Render Frames 2 to 6
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

-- Export outputs
sprite:saveCopyAs("output/aseprite/void_portal.aseprite")
sprite:saveCopyAs("output/gif/void_portal.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/void_portal_sheet.png")
sheetSprite:close()
sprite:close()
