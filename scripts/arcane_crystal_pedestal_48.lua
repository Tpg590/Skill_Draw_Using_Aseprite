-- scripts/arcane_crystal_pedestal_48.lua
-- 48x48 Terraria Style Animated Magic Crystal on Cracked Stone Pedestal
-- 4 Frames Looping Bobbing Cycle at 6 FPS

local width = 48
local height = 48
local fps = 6
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Phong cách Terraria (Độ tương phản cao, outline sẫm tối, khối đá gồ ghề nứt nẻ)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#110e14", -- Viền sẫm đen đặc trưng Terraria (Near-black solid outline)
    ["S"] = "#0d0b12", -- Bóng tiếp đất tiếp xúc (Ground contact shadow, alpha 130)

    -- Chất liệu đá nứt nẻ cổ xưa (Rugged Ancient Granite / Slate)
    ["E"] = "#a8a3b8", -- Sắc trắng bạc dăm đá sứt mẻ (Chipped stone highlight)
    ["K"] = "#756f8a", -- Màu sáng mặt khối đá (Stone light midtone)
    ["N"] = "#4a445e", -- Thân đá phong hóa (Stone base body)
    ["D"] = "#2b263b", -- Vùng tối & khe nứt (Stone shadow & crack fissure)
    ["V"] = "#1a1626", -- Rãnh nứt sâu hốc đá (Deep stone crevice)

    -- Pha lê ma thuật Mana Crystal (Faceted, high contrast, glowing)
    ["P"] = "#ffffff", -- Đốm phản quang cực sáng (Specular glint & sparkle)
    ["A"] = "#a6ffff", -- Lõi năng lượng neon cyan (Hyper-bright neon cyan core)
    ["B"] = "#36d6e7", -- Sắc xanh lam ma thuật rực rỡ (Bright mana cyan)
    ["C"] = "#128fa8", -- Sắc xanh huyền bí trung tính (Mid arcane cyan)
    ["F"] = "#0c536e", -- Diện tối cạnh pha lê (Deep facet teal)
    ["X"] = "#08283b", -- Góc khuất pha lê (Darkest facet edge)

    -- Hiệu ứng phát sáng & bụi mana lơ lửng (Crystal Glow & VFX motes)
    ["G"] = "#259cb0", -- Vầng sáng mana phản chiếu bệ đá (Altar mana glow)
    ["g"] = "#18556b"  -- Ánh sáng lan tỏa mờ (Subtle ambient aura)
}

-- 2. Ma trận ký tự các khung hình (48x48)
local frame1_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".......................##.......................",
    "......................#PP#......................",
    ".....................#PAAF#.....................",
    "....................#PAABCF#....................",
    ".............A.....#PAABCCFF#...................",
    "............G.....#PAABBCCCFF#..................",
    ".................#PAAABCCCCFFF#.................",
    "................#PAAAABBCCCCFFF#................",
    ".................#PAAABCCCCFFF#.................",
    "..................#PAABBCCCFF#..................",
    "...................#PAABCCFF#...................",
    "....................#PAABCF#......B.............",
    ".....................#PAAF#........G............",
    "......................#PP#......................",
    ".......................##.......................",
    "................................................",
    "................................................",
    "....................G...........................",
    "................................................",
    "................................................",
    "...........##########################...........",
    "..........#EEKNNNDDNgGGGGGGgNDDNNKKEE#..........",
    ".........#EEKKNNNDDNGBAABAGGNDDNNKKEEE#.........",
    ".........#EKKNNDNNDNgGBAABGgNNDNDNKEEE#.........",
    ".........#EEEKKNNNDNNDGGDDGNDNNDNNKKEE#.........",
    ".........#VVV#VVVDDVVNDDVVNDDVVVVV#VVV#.........",
    ".............#EKKNDDNNgGDNNNDNNKEE#.............",
    ".............#KKNDDDNNgGDNVDDDNKKD#.............",
    ".............#KNDDVNDNGgDDVVDDDNKE#.............",
    ".............#NDDDVVNDggNDDNVVDDNK#.............",
    ".............#DDVVNDNNDggNDNDVVDDN#.............",
    ".............#DNVDDDNNNDgGDNNDVVDN#.............",
    ".............#NNNDDNNNNNDGgNDNDVVD#.............",
    ".............#KKNNDDNNNNDGgNDNDVEE#.............",
    "...........#EEKKNNDDNNNDDGgNDNNDKKEE#...........",
    ".........#EEKKNNDDNNNDDDNNNDDNNKKEEEEE#.........",
    ".........##############################.........",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
    "..............SSSSSSSSSSSSSSSSSSSS..............",
    "................................................"
}

local frame2_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".......................##.......................",
    "......................#PP#......................",
    ".....................#PPAF#.B...................",
    "....................#PPAACF#....................",
    "............P......#PPAABCFX#...................",
    "...........A......#PPAABBCCFF#..................",
    ".................#PPAAABCCCFFF#.................",
    "................#PPAAAABCCCCFFF#................",
    ".................#PPAAABCCCFFF#.................",
    "..................#PPAABBCCFF#.....A............",
    "...................#PPAABCFX#.......G...........",
    "....................#PPAACF#....................",
    ".....................#PPAF#.....................",
    "......................#PP#......................",
    ".......................##.......................",
    "................................................",
    "................................................",
    "...................g............................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "...........##########################...........",
    "..........#EEKNNNDDNgGGGGGGgNDDNNKKEE#..........",
    ".........#EEKKNNNDDNGBAABAGGNDDNNKKEEE#.........",
    ".........#EKKNNDNNDNgGBAABGgNNDNDNKEEE#.........",
    ".........#EEEKKNNNDNNDGGDDGNDNNDNNKKEE#.........",
    ".........#VVV#VVVDDVVNDDVVNDDVVVVV#VVV#.........",
    ".............#EKKNDDNNgGDNNNDNNKEE#.............",
    ".............#KKNDDDNNgGDNVDDDNKKD#.............",
    ".............#KNDDVNDNGgDDVVDDDNKE#.............",
    ".............#NDDDVVNDggNDDNVVDDNK#.............",
    ".............#DDVVNDNNDggNDNDVVDDN#.............",
    ".............#DNVDDDNNNDgGDNNDVVDN#.............",
    ".............#NNNDDNNNNNDGgNDNDVVD#.............",
    ".............#KKNNDDNNNNDGgNDNDVEE#.............",
    "...........#EEKKNNDDNNNDDGgNDNNDKKEE#...........",
    ".........#EEKKNNDDNNNDDDNNNDDNNKKEEEEE#.........",
    ".........##############################.........",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
    "..............SSSSSSSSSSSSSSSSSSSS..............",
    "................................................"
}

local frame3_grid = {
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".......................##.......................",
    "......................#PP#......................",
    ".....................#PAAF#.....................",
    "....................#PAABCF#....................",
    "...................#PAABCCFF#...................",
    "..................#PAABBCCCFF#..................",
    ".................#PAAABCCCCFFF#.................",
    "..............B.#PAAAABBCCCCFFF#................",
    ".............G...#PAAABCCCCFFF#.................",
    "..................#PAABBCCCFF#..................",
    "...................#PAABCCFF#...................",
    "....................#PAABCF#....................",
    ".....................#PAAF#.....................",
    "......................#PP#.......G..............",
    ".......................##.........g.............",
    "................................................",
    "................................................",
    "..........................G.....................",
    "................................................",
    "................................................",
    "...........##########################...........",
    "..........#EEKNNNDDNgGGGGGGgNDDNNKKEE#..........",
    ".........#EEKKNNNDDNGBAABAGGNDDNNKKEEE#.........",
    ".........#EKKNNDNNDNgGBAABGgNNDNDNKEEE#.........",
    ".........#EEEKKNNNDNNDGGDDGNDNNDNNKKEE#.........",
    ".........#VVV#VVVDDVVNDDVVNDDVVVVV#VVV#.........",
    ".............#EKKNDDNNgGDNNNDNNKEE#.............",
    ".............#KKNDDDNNgGDNVDDDNKKD#.............",
    ".............#KNDDVNDNGgDDVVDDDNKE#.............",
    ".............#NDDDVVNDggNDDNVVDDNK#.............",
    ".............#DDVVNDNNDggNDNDVVDDN#.............",
    ".............#DNVDDDNNNDgGDNNDVVDN#.............",
    ".............#NNNDDNNNNNDGgNDNDVVD#.............",
    ".............#KKNNDDNNNNDGgNDNDVEE#.............",
    "...........#EEKKNNDDNNNDDGgNDNNDKKEE#...........",
    ".........#EEKKNNDDNNNDDDNNNDDNNKKEEEEE#.........",
    ".........##############################.........",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
    "..............SSSSSSSSSSSSSSSSSSSS..............",
    "................................................"
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
    ".......................##.......................",
    "......................#PP#......................",
    ".....................#PAAF#.....................",
    "....................#PAABCF#....................",
    "...................#PAABCCFF#...................",
    "..................#PAABBCCCFF#..................",
    ".................#PAAABCCCCFFF#.................",
    "................#PAAAABBCCCCFFF#................",
    "...............G.#PAAABCCCCFFF#.................",
    "..................#PAABBCCCFF#..................",
    "...................#PAABCCFF#...B...............",
    "....................#PAABCF#....................",
    ".....................#PAAF#.....................",
    "......................#PP#......................",
    ".......................##.......................",
    "..................A..........B..................",
    ".......................P........................",
    "................................................",
    "...........##########################...........",
    "..........#EEKNNNDDNgGBAABGgNDDNNKKEE#..........",
    ".........#EEKKNNNDDNGBAAPBGGNDDNNKKEEE#.........",
    ".........#EKKNNDNNDNgGBAABGgNNDNDNKEEE#.........",
    ".........#EEEKKNNNDNNDGGDDGNDNNDNNKKEE#.........",
    ".........#VVV#VVVDDVVNDDVVNDDVVVVV#VVV#.........",
    ".............#EKKNDDNNgGDNNNDNNKEE#.............",
    ".............#KKNDDDNNgGDNVDDDNKKD#.............",
    ".............#KNDDVNDNGgDDVVDDDNKE#.............",
    ".............#NDDDVVNDggNDDNVVDDNK#.............",
    ".............#DDVVNDNNDggNDNDVVDDN#.............",
    ".............#DNVDDDNNNDgGDNNDVVDN#.............",
    ".............#NNNDDNNNNNDGgNDNDVVD#.............",
    ".............#KKNNDDNNNNDGgNDNDVEE#.............",
    "...........#EEKKNNDDNNNDDGgNDNNDKKEE#...........",
    ".........#EEKKNNDDNNNDDDNNNDDNNKKEEEEE#.........",
    ".........##############################.........",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "..........SSSSSSSSSSSSSSSSSSSSSSSSSSSS..........",
    "..............SSSSSSSSSSSSSSSSSSSS..............",
    "................................................"
}

-- 3. Hàm render lưới ký tự lên Canvas Cel
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

-- Render Frame 1: Vị trí trung bình - Đang bay lên (Mid - Rising)
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Vị trí cao nhất - Tỏa sáng cực đại (Peak - Highest)
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Vị trí trung bình - Đang hạ xuống (Mid - Falling)
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- Render Frame 4: Vị trí thấp nhất - Tụ quang trên bệ đá (Dip - Lowest)
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local cel4 = layer:cel(4)
if cel4 then
    cel4.image:clear()
    renderGrid(cel4.image, frame4_grid, PALETTE)
end

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/arcane_crystal_pedestal_48.aseprite")

-- B. Nếu là Animation: xuất GIF động và dải spritesheet ngang độc lập CLI
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/arcane_crystal_pedestal_48.gif")
    
    -- Tự động ghép nối các frame thành 1 dải Spritesheet ngang không lo lỗi giao diện
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/arcane_crystal_pedestal_48_sheet.png")
    sheetSprite:close()
else
    -- Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
    sprite:saveCopyAs("output/arcane_crystal_pedestal_48.png")
end
