-- scripts/hanging_cage_48.lua
-- 48x48 Terraria Suspended Iron Cage with Glowing Jade Spirit Orb (6 FPS)
local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Hanging_Cage"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria Heavy Iron Metal & Radiant Jade Spirit
local PALETTE = {
    ["."] = nil,
    
    -- Heavy Iron Cage & Chain
    ["#"] = "#12151c", -- Dark iron outline
    ["I"] = "#dce5ec", -- Specular iron highlight / rivets
    ["T"] = "#9db0c0", -- Light iron metal
    ["M"] = "#5e6e7e", -- Iron midtone shadow
    ["K"] = "#343f4a", -- Iron dark crevice
    ["B"] = "#1c222a", -- Back recessed bars (Z-index behind orb)
    
    -- Glowing Jade Spirit Orb
    ["W"] = "#ffffff", -- Radiant pure white core
    ["H"] = "#c2ffea", -- Bright mint highlight
    ["A"] = "#2ff6b0", -- Electric jade green
    ["E"] = "#00c882", -- Deep rich emerald
    ["G"] = "#068656", -- Jade shadow
    ["J"] = "#044b30", -- Outer aura boundary
    ["Z"] = "#022416", -- Deepest soul mist
    
    -- Rule 3.6: Front Bar Rim Lighting Over Glowing Orb
    ["R"] = "#d5fff4", -- Front bar rim specular
    ["S"] = "#4eeab8", -- Front bar rim jade glow
    ["F"] = "#146848"  -- Front bar rim dark outline
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
                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = 255 })
            else
                img:drawPixel(x - 1, y - 1, Color{ r = 0, g = 0, b = 0, a = 0 })
            end
        end
    end
end

local f1_grid = {
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#IK#M#.....................",
    "....................#T....K#....................",
    ".....................#M..K#.....................",
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#T..M#.....................",
    ".....................#M..K#.....................",
    ".....................#TIIT#.....................",
    "..............#TTTTTTTTTTTTMMMMMM#..............",
    ".............##TITITTTTTTTTMMMMMM##.............",
    ".............##TTTTMMMMMMMMKKKKKK##.............",
    ".............#TTB##MMMMMKMMKK#B#KK#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M.H.MK...K#B#.K#.............",
    ".............#T.B##M...MK.A.K#B#.K#.............",
    ".............#I.B##T...RK...M#B#.M#.............",
    ".............#T.B##MJGGRKGGJK#B#.K#.............",
    ".............#T.B#FSEEERKEEESFB#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.B#FSAAHRKHAASFB#.M#.............",
    ".............#T.BJFSAHWRKHHASFJ#.K#.............",
    ".............#T.BGFSAWWRKWHASFG#.K#.............",
    ".............#T.BGFSHHWRKWHHSFG#.K#.............",
    ".............#I.BGFSAHWRKWHASFG#.M#.............",
    ".............#T.BJFSAHHRKHHASFJ#.K#.............",
    ".............#T.B#FSAAHRKHAASFB#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.B#FSEEERKEEESFB#.M#.............",
    ".............#T.B##MJGGRKGGJK#B#.K#.............",
    ".............#T.B##M...RK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#TITTTITTTITTTITTTITT#.............",
    ".............#TTTTTTTTMMMMMMKKKKKK#.............",
    "..............#MMMMMMMKKKKKKKKKKK#..............",
    "...............#MMMMMMKKKKKKKKKK#...............",
    ".................##KKKKKKKKKK##.................",
    ".....................######.....................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".......................##.......................",
    "................................................",
}
local f2_grid = {
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#IK#M#.....................",
    "....................#T....K#....................",
    ".....................#M..K#.....................",
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#T..M#.....................",
    ".....................#M..K#.....................",
    ".....................#TIIT#.....................",
    "..............#TTTTTTTTTTTTMMMMMM#..............",
    ".............##TITITTTTTTTTMMMMMM##.............",
    ".............##TTTTMMMMMMMMKKKKKK##.............",
    ".............#TTB##MMHMMKMMKK#B#KK#.............",
    ".............#I.B##TW..TM...M#B#.M#.............",
    ".............#T.B##M...MK..AK#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M..JRKJ..K#B#.K#.............",
    ".............#I.B#FSGGERKEGGSFB#.M#.............",
    ".............#T.E#FSEEERKEEESFB#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#T.BGFSAAHRKHAASFG#.K#.............",
    ".............#I.BGFSAHWRKHHASFG#.M#.............",
    ".............#T.JEFRHWWRKWHHRFEJ.K#.............",
    ".............#T.JEFRHWWRKWHHRFEJ.K#.............",
    ".............#T.JEFRHHWRKWHHRFEJ.K#.............",
    ".............#I.JEFRHHWRKWHHRFEJ.M#.............",
    ".............#T.BGFSAHHRKHHASFG#.K#.............",
    ".............#T.BGFSAAHRKHAASFG#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.B#FSEEERKEEESFB#.M#.............",
    ".............#T.B#FSGGERKEGGSFB#.K#.............",
    ".............#T.B##M..JRKJ..K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#TITTTITTTITTTITTTITT#.............",
    ".............#TTTTTTTTMMMMMMKKKKKK#.............",
    "..............#MMMMMMMKKKKKKKKKKK#..............",
    "...............#MMMMMMKKKKKKKKKK#...............",
    ".................##KKKKKKKKKK##.................",
    ".....................######.....................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".......................##.......................",
    "................................................",
}
local f3_grid = {
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#IK#M#.....................",
    "....................#T....K#....................",
    ".....................#M..K#.....................",
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#T..M#.....................",
    ".....................#M..K#.....................",
    ".....................#TIIT#.....................",
    "..............#TTTTTTTTTTTTMMMMMM#..............",
    ".............##TITITTTTTTTTMMMMMM##.............",
    ".............##TTTTMHMMMMMMEKKKKK##.............",
    ".............#TTB##MMMMMKMMKK#B#KK#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T..JRKJ..M#B#.M#.............",
    ".............#T.B##MJGERKEGJK#B#.K#.............",
    ".............#TAB#FSEEERKEEESFB#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.BJFSAAHRKHAASFJ#.M#.............",
    ".............#T.BGFSAHWRKHHASFG#.K#.............",
    ".............#T.BGFSAWWRKWHASFG#.K#.............",
    ".............#T.BGFRHHWRKWHHRFG#.K#.............",
    ".............#I.BGFSAHWRKWHASFG#.M#.............",
    ".............#T.BGFSAHHRKHHASFG#.K#.............",
    ".............#T.BJFSAAHRKHAASFJ#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.B#FSEEERKEEESFB#.M#.............",
    ".............#T.B##MJGERKEGJK#B#.K#.............",
    ".............#T.B##M..JRKJ..K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#TITTTITTTITTTITTTITT#.............",
    ".............#TTTTTTTTMMMMMMKKKKKK#.............",
    "..............#MMMMMMMKKKKKKKKKKK#..............",
    "...............#MMMMMMKKKKKKKKKK#...............",
    ".................##KKKKKKKKKK##.................",
    ".....................######.....................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".......................##.......................",
    "................................................",
}
local f4_grid = {
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#IK#M#.....................",
    "....................#T....K#....................",
    ".....................#M..K#.....................",
    ".......................TI.......................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".....................#T..M#.....................",
    ".....................#M..K#.....................",
    ".....................#TIIT#.....................",
    "..............#TTTTTTTTTTTTMMMMMM#..............",
    ".............##TITITTGTTTTTJMMMMM##.............",
    ".............##TTTTMMMMMMMMKKKKKK##.............",
    ".............#TTB##MMMMMKMMKK#B#KK#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...RK...K#B#.K#.............",
    ".............#T.B##M.GERKEG.K#B#.K#.............",
    ".............#T.B#FSEEERKEEESFB#.K#.............",
    ".............#I.B#FSEAARKAAESFB#.M#.............",
    ".............#T.B#FSAAHRKHAASFB#.K#.............",
    ".............#T.B#FSAHWRKHHASFB#.K#.............",
    ".............#T.B#FSAWWRKWHASFB#.K#.............",
    ".............#I.B#FSAHWRKWHASFB#.M#.............",
    ".............#T.B#FSAHHRKHHASFB#.K#.............",
    ".............#T.B#FSAAHRKHAASFB#.K#.............",
    ".............#T.B#FSEAARKAAESFB#.K#.............",
    ".............#I.B#FSEEERKEEESFB#.M#.............",
    ".............#T.B##M.GERKEG.K#B#.K#.............",
    ".............#T.B##M...RK...K#B#.K#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#I.B##T...TM...M#B#.M#.............",
    ".............#T.B##M...MK...K#B#.K#.............",
    ".............#TITTTITTTITTTITTTITT#.............",
    ".............#TTTTTTTTMMMMMMKKKKKK#.............",
    "..............#MMMMMMMKKKKKKKKKKK#..............",
    "...............#MMMMMMKKKKKKKKKK#...............",
    ".................##KKKKKKKKKK##.................",
    ".....................######.....................",
    "......................#TM#......................",
    "......................#MK#......................",
    ".......................##.......................",
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
sprite:saveCopyAs("output/aseprite/hanging_cage_48.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/hanging_cage_48.gif")

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
sheetSprite:saveCopyAs("output/Sheet/hanging_cage_48_sheet.png")
sheetSprite:close()
