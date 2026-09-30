-- ========================================================
-- Magic Cauldron Boiling Animation (FreeStyle 48x48)
-- Output: 6 frames @ 6 FPS
-- ========================================================

local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Magic_Cauldron"
sprite.frames[1].duration = frameDuration

local PALETTE = {
    ["S"] = Color{ r = 25, g = 20, b = 35, a = 130 },
    ["D"] = Color{ r = 36, g = 22, b = 16, a = 255 },
    ["B"] = Color{ r = 82, g = 50, b = 28, a = 255 },
    ["M"] = Color{ r = 144, g = 95, b = 46, a = 255 },
    ["H"] = Color{ r = 210, g = 155, b = 80, a = 255 },
    ["P"] = Color{ r = 52, g = 135, b = 115, a = 255 },
    ["k"] = Color{ r = 12, g = 52, b = 30, a = 255 },
    ["g"] = Color{ r = 22, g = 130, b = 68, a = 255 },
    ["G"] = Color{ r = 48, g = 220, b = 110, a = 255 },
    ["Y"] = Color{ r = 180, g = 255, b = 140, a = 255 },
    ["W"] = Color{ r = 245, g = 255, b = 230, a = 255 },
    ["m"] = Color{ r = 60, g = 90, b = 105, a = 130 },
    ["T"] = Color{ r = 100, g = 180, b = 170, a = 170 },
    ["t"] = Color{ r = 175, g = 240, b = 225, a = 210 },
}

local frame_grids = {
    -- Frame 1
    {
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
        ".................T...........T..................",
        "..................tT........mm..................",
        ".................TT.........mm..................",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkkkkkkkkkkkggggggggg.HD..........",
        "..........DBggggYWGGGGGYGGGGGGYYYYYYHD..........",
        "..........DBggggggGGGGGGGGGGYGYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
    -- Frame 2
    {
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
        ".................TtT............................",
        "................TTtTT.........m.................",
        ".................TTT.........mTm................",
        ".............................mm.................",
        "................................................",
        "................................................",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkWYkkkkkkkkggggggggg.HD..........",
        "..........DBggggYGGGGGGGGGGGGYYYYYYYHD..........",
        "..........DBggggggGGGGYWGGGGWWYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
    -- Frame 3
    {
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "..................TTT...........................",
        ".................TTttT..........................",
        "..................TTT.......TTT.................",
        "............................TT..................",
        "................................................",
        ".................m..............................",
        "..................m.............................",
        "................W...............................",
        "................Y...............................",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkWGkkkkkkkkggggggggg.HD..........",
        "..........DBggggggGGGGGGWYGGGGYYYYYYHD..........",
        "..........DBggggggGGGGGGYGGGGGYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
    -- Frame 4
    {
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "....................TtT.........................",
        "...................TTtTT........................",
        "....................TTT....T....................",
        "..........................m.....................",
        "................m...............................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "............DDDDDGDDDDDDDDDDDDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkkkkkkkkkWWggggggggg.HD..........",
        "..........DBggggggGGGGGYYGkGGGYYYWYYHD..........",
        "..........DBggggggGGGGGGGGGGGGYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
    -- Frame 5
    {
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        ".....................TtT........................",
        ".....................TT..m......................",
        "..................m.......m.....................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "........................Y.......................",
        "................................................",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkkkkkkkkWkWWgggggggg.HD..........",
        "..........DBggggggGGGGGYGGYGGGYYWYYYHD..........",
        "..........DBggggggGGGGGGGGGGGGYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
    -- Frame 6
    {
        "................................................",
        "................................................",
        "................................................",
        "......................m.........................",
        ".......................m........................",
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
        "............DDDDDDTDDDDDDDDDmDDDDDDD............",
        "...........DBBBBBBBBBBBBBBBBBBBBBBBBD...........",
        "..........DB.kkkkkkkkkkkgGggggggggg.HD..........",
        "..........DBggggggYGGGGGGGGGGGYYYYYYHD..........",
        "..........DBggggggGGGGGGGGGGGGYYYYYYHD..........",
        "..........DB.gggggggGGGGGGGGGGGGGGG.HD..........",
        "...........DBBBBBBGGGGGGGGGGGGHHHHHHD...........",
        "............DDDDDDDDDDDDDDDDDDDDDDDD............",
        "..........DBBMggggggggggggggggggggMHHD..........",
        ".......D.DBBMMMMMMMMMMMMMMMMMMMMMMMMHHD.D.......",
        "......DMDBBMPMMMMMMMMMMMMMMMMMMMMMMMMHHDHD......",
        "......DBDBBMPPMMMMMMMMMMMMMMMMMMMMMMMHHDMD......",
        ".......DDBBMMPMMMMMMMMMMMMMMMMMMMMMMMHHDD.......",
        "........DBBMMMMMMMMMMMMMMMMMMMMMPMMMMHHD........",
        ".........DBBMMMPMMMMMMMMMMMMMMMMMMMMHHD.........",
        "..........DBBMMPMMMMMMMMMMMMMMMMMMMHHD..........",
        "...........DBBMMMMMMMMMMMMMMMMMMMMMMD...........",
        ".............DBBMMMMMMMMMMMMMMMMMMD.............",
        "...............DBBBBBBBBBBBBBBBBD...............",
        "...............D.DBBBBBBBBBBBBD.D...............",
        "..............D....DDDDDDDDDD....D..............",
        ".............DB........DD........BD.............",
        ".............DM........DD........MD.............",
        "............DBP........BD........HBD............",
        "............DB.........BD.........BD............",
        "...........DB..........BD..........BD...........",
        "...........DDSSSSSSSSSSSSSSSSSSSSSSDD...........",
        "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
        "...............SSSSSSSSSSSSSSSSSS...............",
        "................................................",
        "................................................",
        "................................................",
    },
}

local function renderGrid(img, gridData, pal)
    for y = 1, #gridData do
        local line = gridData[y]
        for x = 1, #line do
            local char = line:sub(x, x)
            local color = pal[char]
            if color then
                img:drawPixel(x - 1, y - 1, color)
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

os.execute('mkdir output\\Sheet 2>nul')
os.execute('mkdir output\\gif 2>nul')
os.execute('mkdir output\\aseprite 2>nul')

sprite:saveCopyAs("output/aseprite/magic_cauldron_boiling.aseprite")
sprite:saveCopyAs("output/gif/magic_cauldron_boiling.gif")

local totalFrames = #sprite.frames
local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
local sheetImage = sheetSprite.cels[1].image
for i = 1, totalFrames do
    local frameCel = layer:cel(i)
    if frameCel then
        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
    end
end
sheetSprite:saveCopyAs("output/Sheet/magic_cauldron_boiling_sheet.png")
sheetSprite:close()
sprite:close()
print("[XONG] magic_cauldron_boiling animation rendered!")
