-- scripts/standing_void_gate.lua
-- 48x48 Ancient Stone Standing Arch Portal (6 Frames, 8 FPS)
-- Art Style: Terraria (Upright Gate, Vertical Void Membrane H > W, OSL Rim Lighting, Anchored Plinths)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Standing_Void_Gate"

sprite.frames[1].duration = frameDuration

local PALETTE = {
    ["."] = nil,
    ["#"] = "#0c0612",
    ["S"] = "#08040d",
    ["T"] = "#7d6e91",
    ["R"] = "#554869",
    ["G"] = "#342a46",
    ["D"] = "#1c1428",
    ["p"] = "#af4bf0",
    ["P"] = "#7326af",
    ["A"] = "#dc78ff",
    ["B"] = "#a537eb",
    ["C"] = "#6e19af",
    ["E"] = "#410c73",
    ["F"] = "#20043e",
    ["Z"] = "#040008",
    ["W"] = "#ffffff",
    ["I"] = "#38ffff",
    ["M"] = "#0ea0d2",
}

local frame1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCABBCC...#RGRRG#..........",
    "..........##GRRGR...CCAABBACC..#RGRRG#..........",
    "..........#TRGPP#...CBAABBAAC..#PPGRT#..........",
    "..........#RRGPp#..CBCCCCCCCBC.#pPGRR#..........",
    "..........#TRGPP#..ACCCCCCCCCB.#PPGRT#..........",
    "..........#TRDPp#.CCCCCCCCCCCCC#pPDRT#..........",
    "..........#RRGPP#.CCCEEEEEEECCC#PPGRR#..........",
    "..........#TRGPp#.BCCEEEEEEECCA#pPGRT#..........",
    "..........#TRGPP#.BCCEEEEEEECCB#PPGRT#..........",
    "..........#RRDPp#CBCEEFFFFFWMCB#pPDRR#..........",
    "..........#TRGPP#CACCEFZFZFECCB#PPGRT#..........",
    "..........#TRGPp#CACCEFZFZFECCB#pPGRT#..........",
    "..........#RRGPP#CAACEEFZFEECBB#PPGRR#..........",
    "..........#TRDPp#CABCCEFZFECCBB#pPDRT#..........",
    "..........#TRGPP#CBBCCEFZFECCBB#PPGRT#..........",
    "..........#RRGPp#IBBCCEFFFECCAB#pPGRR#..........",
    "..........#TRGPP#.BBCCEEFEECCAA#PPGRT#..........",
    "..........#TRDPp#.CAACEEFEECAAC#pPDRT#..........",
    "..........#RRGPP#.CAACEEEEECBAC#PPGRR#..........",
    "..........#TRGPp#..AACCEEECCBB.#pPGRT#..........",
    "..........#TRGPP#..CBCCEEECCBC.#PPGRT#..........",
    "..........#RRDPp#...CBCCCCCAC..#pPDRR#..........",
    "..........#TRGPP#...CCCCCCCCC..#PPGRT#..........",
    "..........#TRGPp#....CCACBCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCABBCC...#RGRRG#..........",
    "..........##GRRGR...CCAABBACC..#RGRRG#..........",
    "..........#TRGPP#...CBAACCCCC..#PPGRT#..........",
    "..........#RRGPp#..CBBACCCCCCC.#pPGRR#..........",
    "..........#TRGPP#..ABCCCCEECCB.#PPGRT#..........",
    "..........#TRDPp#.CACCCCEEEECCC#pPDRT#..........",
    "..........#RRGPP#.CCCCEEEEEECCC#PPGRR#..........",
    "..........#TRGPp#.BCCEEEEFFECCB#pPGRT#..........",
    "..........#TRGPP#.BCEEEEFFFECCA#PPGRT#..........",
    "..........#RRDPp#CCCEEFFFZFECCA#pPDRR#..........",
    "..........#TRGPP#CCCEEFFZZFMCCA#PPGRT#..........",
    "..........#TRGPp#CACEEFZZFIECAA#pPGRT#..........",
    "..........#RRGPP#CACEEFZZFEECBB#PPGRR#..........",
    "..........#TRDPp#CACCEEFZFECCBB#pPDRT#..........",
    "..........#TRGPP#CBWCEEEFFECCBB#PPGRT#..........",
    "..........#RRGPp#MBBCCEEFFECCAA#pPGRR#..........",
    "..........#TRGPP#.BBACCEEFECCAA#PPGRT#..........",
    "..........#TRDPp#.CAACCEEEECCAC#pPDRT#..........",
    "..........#RRGPP#.CAABCCEEECBAC#PPGRR#..........",
    "..........#TRGPp#..AABCCEECCBB.#pPGRT#..........",
    "..........#TRGPP#..CBBBCCCCCBC.#PPGRT#..........",
    "..........#RRDPp#...CBACCCCCC..#pPDRR#..........",
    "..........#TRGPP#...CCAACCCCC..#PPGRT#..........",
    "..........#TRGPp#....CCABBCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCBBBCC...#RGRRG#..........",
    "..........##GRRGR...CCAABBBCC..#RGRRG#..........",
    "..........#TRGPP#...CBAACCCAC..#PPGRT#..........",
    "..........#RRGPp#..CBBACCCCCAC.#pPGRR#..........",
    "..........#TRGPP#..ABBCCEEECAB.#PPGRT#..........",
    "..........#TRDPp#.CAACCEEEECCBC#pPDRT#..........",
    "..........#RRGPP#.CACCCEFFEECBC#PPGRR#..........",
    "..........#TRGPp#.BACCEEFFEECBA#pPGRT#..........",
    "..........#TRGPP#.BCCEEFZZFECAA#PPGRT#..........",
    "..........#RRDPp#CBCEEEFZZFECAA#pPDRR#..........",
    "..........#TRGPP#CCCEEFFZZFECCA#PPGRT#..........",
    "..........#TRGPp#CCCEFFZZFFECCB#pPGRT#..........",
    "..........#RRGPP#CCCEFZZZZFECCB#PPGRR#..........",
    "..........#TRDPp#CCCWEFFZZFECCB#pPDRT#..........",
    "..........#TRGPP#CBMEEFFFZFECAB#PPGRT#..........",
    "..........#RRGPp#.BCCEEEEFFECAA#pPGRR#..........",
    "..........#TRGPP#.BBCCEEEEEECAA#PPGRT#..........",
    "..........#TRDPp#.CACCCCEEECCAC#pPDRT#..........",
    "..........#RRGPP#.CAABCCCCCCCBC#PPGRR#..........",
    "..........#TRGPp#..AAIBCCCCCBB.#pPGRT#..........",
    "..........#TRGPP#..CABBACCCCBC.#PPGRT#..........",
    "..........#RRDPp#...CBAABBAAC..#pPDRR#..........",
    "..........#TRGPP#...CCAABBACC..#PPGRT#..........",
    "..........#TRGPp#....CCABBCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCAABCC...#RGRRG#..........",
    "..........##GRRGR...CCBAABBCC..#RGRRG#..........",
    "..........#TRGPP#...CBBCCCBAC..#PPGRT#..........",
    "..........#RRGPp#..CBBCCCCCAAC.#pPGRR#..........",
    "..........#TRGPP#..ABBCCECCAAB.#PPGRT#..........",
    "..........#TRDPp#.CABCCEEECCBBC#pPDRT#..........",
    "..........#RRGPP#.CAACEEEEECBBC#PPGRR#..........",
    "..........#TRGPp#.AACCEFFFECCBA#pPGRT#..........",
    "..........#TRGPP#.BBCCEFZFECCAA#PPGRT#..........",
    "..........#RRDPp#CBCCEEFZFEECCA#pPDRR#..........",
    "..........#TRGPP#CBCCEFFZFFECCA#PPGRT#..........",
    "..........#TRGPp#CACEEFZZZFEECB#pPGRT#..........",
    "..........#RRGPP#CACEFIZZZFFECB#PPGRR#..........",
    "..........#TRDPp#CCCEMZZZZZFECC#pPDRT#..........",
    "..........#TRGPP#CACEFFFFFFFECB#PPGRT#..........",
    "..........#RRGPp#.BCEEFFEFFEECA#pPGRR#..........",
    "..........#TRGPP#.BCCEEEEEEECCA#PPGRT#..........",
    "..........#TRDPp#.CCCEWEEEEECCC#pPDRT#..........",
    "..........#RRGPP#.CACCCCCCCCCBC#PPGRR#..........",
    "..........#TRGPp#..AAMCCCCCCBB.#pPGRT#..........",
    "..........#TRGPP#..CABBABBAABC.#PPGRT#..........",
    "..........#RRDPp#...CBBABBAAC..#pPDRR#..........",
    "..........#TRGPP#...CCAABBBCC..#PPGRT#..........",
    "..........#TRGPp#....CCABBCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCAABCC...#RGRRG#..........",
    "..........##GRRGR...CCBAABBCC..#RGRRG#..........",
    "..........#TRGPP#...CBCCCBBAC..#PPGRT#..........",
    "..........#RRGPp#..CACCCCCBAAC.#pPGRR#..........",
    "..........#TRGPP#..AACCCCCAAAB.#PPGRT#..........",
    "..........#TRDPp#.CBACEEECCABBC#pPDRT#..........",
    "..........#RRGPP#.CBBCEEEECCBBC#PPGRR#..........",
    "..........#TRGPp#.BBCCEFEECCBBI#pPGRT#..........",
    "..........#TRGPP#.BBCCEFFEECCAA#PPGRT#..........",
    "..........#RRDPp#CBBCEEFZEEECCA#pPDRR#..........",
    "..........#TRGPP#CBBCEEFZFFEECA#PPGRT#..........",
    "..........#TRGPp#CBBCEEFZZFFECC#pPGRT#..........",
    "..........#RRGPP#CACCEFZZZZFECC#PPGRR#..........",
    "..........#TRDPp#CACCEFZZZFFECC#pPDRT#..........",
    "..........#TRGPP#CACEEFZFFFFECC#PPGRT#..........",
    "..........#RRGPp#.BCEEWFFFEEECC#pPGRR#..........",
    "..........#TRGPP#.BCCEMFEEEECCA#PPGRT#..........",
    "..........#TRDPp#.CCCEEEEEECCCC#pPDRT#..........",
    "..........#RRGPP#.CACEEEECCCCBC#PPGRR#..........",
    "..........#TRGPp#..ACCCCCCCABB.#pPGRT#..........",
    "..........#TRGPP#..CACCCCBAABC.#PPGRT#..........",
    "..........#RRDPp#...CBBAABBAC..#pPDRR#..........",
    "..........#TRGPP#...CCBAABBCC..#PPGRT#..........",
    "..........#TRGPp#....CCAABCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
    ".......................###......................",
    ".....................##RTR##....................",
    "..................###RTGRGTR###.................",
    "................##RTRTRTRTRTRTR##...............",
    "...............#RRGRRGRRGRRGRRGRR#..............",
    ".............##GRRGRRGRRGRRGRRGRRG##............",
    ".............#RGRRGRR##...##RRGRRGR#............",
    "............#RRGRRG#.........#GRRGRR#...........",
    "...........##RRGRR.....CCC.....RRGRR##..........",
    "...........#GRRGR#...CCAABCC...#RGRRG#..........",
    "..........##GRRGR...CCBAABBCC..#RGRRG#..........",
    "..........#TRGPP#...CCCCABBAC..#PPGRT#..........",
    "..........#RRGPp#..CACCCCCBAAC.#pPGRR#..........",
    "..........#TRGPP#..ACCCCCCCABB.#PPGRT#..........",
    "..........#TRDPp#.CBCCEECCCCBBC#pPDRT#..........",
    "..........#RRGPP#.CBCEEEECCCCBC#PPGRR#..........",
    "..........#TRGPp#.BBCEEEEECCCAM#pPGRT#..........",
    "..........#TRGPP#.ABCEEFEEEEWCA#PPGRT#..........",
    "..........#RRDPp#CAACEFFFEEECCA#pPDRR#..........",
    "..........#TRGPP#CAACEFZFFFEECB#PPGRT#..........",
    "..........#TRGPp#CAACEEFZZFEECB#pPGRT#..........",
    "..........#RRGPP#CAACEEIZZFEECB#PPGRR#..........",
    "..........#TRDPp#CAACEEFZFFEECB#pPDRT#..........",
    "..........#TRGPP#CAACEEMZFEECCA#PPGRT#..........",
    "..........#RRGPp#.BBCEFFFEEECCA#pPGRR#..........",
    "..........#TRGPP#.BBCEEFFEECCAA#PPGRT#..........",
    "..........#TRDPp#.CBCEEFFEECCBC#pPDRT#..........",
    "..........#RRGPP#.CBCCEEEECCBBC#PPGRR#..........",
    "..........#TRGPp#..ACCEEECCCBB.#pPGRT#..........",
    "..........#TRGPP#..CACCECCCAAC.#PPGRT#..........",
    "..........#RRDPp#...CCCCCCBAC..#pPDRR#..........",
    "..........#TRGPP#...CCCCCBBCC..#PPGRT#..........",
    "..........#TRGPp#....CCAABCC...#pPGRT#..........",
    ".........#TTTTTT#......CCC.....#TTTTTT#.........",
    ".........#RRRRRR#..............#RRRRRR#.........",
    ".........########..............########.........",
    ".....#RRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGRRRGR#.....",
    ".....#DSSSSSSSSSSSDGGDGGDGGDGGSSSSSSSSSSSG#.....",
    "......#SSSSSSSSSSS############SSSSSSSSSSS#......",
    ".........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.........",
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
sprite:saveCopyAs("output/aseprite/standing_void_gate.aseprite")
sprite:saveCopyAs("output/gif/standing_void_gate.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/standing_void_gate_sheet.png")
sheetSprite:close()
sprite:close()
