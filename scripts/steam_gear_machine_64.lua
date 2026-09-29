-- scripts/steam_gear_machine_64.lua
-- 64x64 Terraria Animated Steam Gear Machine on Stone Wall
local width = 64
local height = 64
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Gear_Machine"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Terraria aged bronze, dungeon stone wall, iron rivets & patina rust
local PALETTE = {
    ["."] = nil,
    ["#"] = "#0e0a0c", -- Near-black Terraria outline
    ["S"] = "#100c12", -- Drop shadow (Alpha 130)
    
    -- Dungeon Stone Wall
    ["K"] = "#878e98", -- Stone brick light/highlight
    ["G"] = "#555c66", -- Stone base gray
    ["N"] = "#30363e", -- Stone mortar & seam shadow
    
    -- Iron Brackets & Rivets
    ["I"] = "#afb9c3", -- Iron highlight
    ["F"] = "#646e7a", -- Iron body steel
    ["L"] = "#2d323a", -- Iron shadow
    
    -- Bronze Gear Wheel (Aged Rusted Bronze)
    ["P"] = "#fffceb", -- Specular highlight (1-2px ivory white)
    ["A"] = "#f5b94b", -- Golden shine
    ["B"] = "#c37d2a", -- Bronze body
    ["C"] = "#824818", -- Bronze dark shadow
    ["Z"] = "#4b2610", -- Bronze deep crevice shade
    
    -- Verdigris Patina Rust
    ["X"] = "#69b49b", -- Light turquoise verdigris
    ["V"] = "#2d6e5f", -- Dark oxidized green
    
    -- Center Axle & Screws
    ["E"] = "#dce1eb"  -- Bolt steel shine
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
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "....########################################################....",
    "....#GGGGGGGGKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGGGKGGGGG#....",
    "....#GG##F##GKGGGGGGNKGKGGGG########GGGGGGGKNKGGGGGG##F##GG#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGG#ABBBBB#GGGGGGGKNKGGGGG#FFFFF#G#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGG#FEEEF#G#....",
    "....#GFFEEEFFKGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGGFFEEEFFG#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGG#AAXXXX#SSGGGGGKNKGGGGG#FEEEF#G#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGG#AAXXXX#SSGGGGGKNKGGGGG#FFFFF#G#....",
    "....#GG##F##GKGGGGGGNKGKGGGG#AAXXXX#SSGGGGGKNKGGGGGG##F##GG#....",
    "....#GGGGGGGGKGGGGGGNKGKGG##ABBXVVVV##GGGGGKNKGG#####KGGGGG#....",
    "....#GGGGGGGGKGGGGGGNKG###AAABBXVVVVBB###GGKNKGG#FEF#KGGGGG#....",
    "....#GGGGGGGGKGGGGGGNK#PAAAAABBXVVVVBBBBB#GKNKGG#FFF#KGGGGG#....",
    "....#GGGGGGGGKGGGGGG##PPAAAAABBBBBBBBBBBBB##NKGFF####KGGGGG#....",
    "....#NNNNNNNNNNNNNN#PPPPPAAAABBBBBBBBBBBBBCC#NFFFNNNNNNNNNN#....",
    "....#KKKKKKKNKKKKK#PPPPAAAA##ABBBBB##BBBBCCCC#FFKKKKNKKKKKK#....",
    "....#GGGGGGGNKGGG#PPPPAAA##SS#AABB#SS##BCCCCCC#GGGGGNKGGGGG#....",
    "....#GGGGGGGNKGG#PPPPAAA#SSSS#AABB#SSSS#CCCCCCC#GGGGNKGGGGG#....",
    "....#GGGGGGGNKGG#PPPAA##SSSSS#AABB#SSGGS##CCCCC#SGGGNKGGGGG#....",
    "....#GGGGGGGNKG#PPPAA#SSSSSGG#AABB#SSGGGGS#CCCCC#SGGNKGGGGG#....",
    "....#GGGGGGGNK#PPPAAA#SSSSGGG#AABB#SSGGGGG#CCCCCC#GGNKGGGGG#....",
    "....#GGGGGGGNK#AAPAA#SSSGGGG#AAABBB#SGGGGGG#CCCCC#SGNKGGGGG#....",
    "....#GGGGGGGNK#AAAA#SSSSGGG#AAAABBBB#GGGGGGK#CCCC#SSNKGGGGG#....",
    "....#GGGGGGGN#AAAAA#SSSKGG#AAAAABBBBB#GGGGGK#CZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGKG#AAAAAABBBBBB#GGGGKG#ZZZZ#SNKGGGGG#....",
    "....#G#######AAAAA#SSSGK#AAAAAIIFFBBBBB#GGGKG#ZZZZZ#######G#....",
    "....#G#AAAAAABBBBBA#####AAAAAIIIFFFBBCCC#####ZZZZZZZZZZZZ#G#....",
    "....#G#BAAAAABBBBBBAAAAAAAAAIIIEEFFFCCCCCCCZZZZZZZZZZZZZZ#S#....",
    "....#G#BBBBBBBBBBBBAAAAAAAAAIIEEEEFFZZZZZZZZZZZZZZZZZZZZZ#S#....",
    "....#N#BBBBBBBBBBBBBBBBBBBBBFFEEEELLZZZZZZZZZZZVVVVVZZZZZ#S#....",
    "....#K#BBBBBBBBBBBBBBBBBBBBBFFFEELLLZZZZZZZZZZZVVVVVZZZZZ#S#....",
    "....#G#BBBBBBBBBBBB#####BBBBBFFFLLLZZZZZ#####ZZVVVVVZZZZZ#S#....",
    "....#G#######BBBBB#SSSSS#BBBBBFFLLZZZZZ#SSSSS#ZVVVV#######S#....",
    "....#GGGSSSSS#BBBB#SSSSSS#BBBBCZZZZZZZ#SSSSSS#ZZZZ#SSSSSSSS#....",
    "....#GGGSSSSS#BBBBB#SKNKGG#BBCCZZZZZZ#SSSSNK#ZZZZZ#SSSSSSSS#....",
    "....#GGGGGGGGK#BBBB#SKNKGGG#BCCZZZZZ#SSSSGNK#ZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBB#SNKGGGG#CCZZZZ#SSSSGGN#ZZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBCC#NKGGGGG#CZZZ#SSSSGGG#ZZZZZZ#SSGKGGGGG#....",
    "....#GGGGGGGGKG#BBCCC#SKGGGGG#CZZZ#SSSGGGG#ZZZZZ#SSSGKGGGGG#....",
    "....#GGGGGGGGKGG#CCCCC##GGGGG#CZZZ#SSGGG##ZZZZZ#SSSSGKGGGGG#....",
    "....#GGGGGGGGKGG#CCCCCCC#GGGG#ZZZZ#SSGG#ZZZZZZZ#SSSGGKGGGGG#....",
    "....#GGGGGGGGKGGG#CCCCCCC##GG#ZZZZ#SS##ZZZZZZZ#SSSGGGKGGGGG#....",
    "....#GGGGGGGGKGGGG#CCCCCCCC##ZZZZZZ##ZZZZZZZZ#SSSSGGGKGGGGG#....",
    "....#GGGGGGGGKGGGGG#CCCCCCZZZZZZZZZZZZZZZZZZ#SSSSGGGGKGGGGG#....",
    "....#NNNNNNNNNNNNNNN##CCCCZZZZZZZZZZZZZZZZ##SSSSNNNNNNNNNNN#....",
    "....#KKKKKKKKKNKKKKKKS#CCCZZZZZZZZZZZZZZZ#SSSSSKKKNKKKKKKKK#....",
    "....#GGGGGGGGKNGGGGGGKS###ZZZZZZZZZZZZ###SSSSSGGGGNGGKGGGGG#....",
    "....#GGGGGGGGKNGGGGGGKGKSS##ZZZZZZZZ##SSSSSSGKGGGGNGGKGGGGG#....",
    "....#GG##F##GKNGGGGGGKGKGSSS#ZZZZZZ#SSSSSSSKGKGGGGNG##F##GG#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGG#ZZZZZZ#SSSSGGGKGKGGGGN#FFFFF#G#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FEEEF#G#....",
    "....#GFFEEEFFKNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGNFFEEEFFG#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FEEEF#G#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FFFFF#G#....",
    "....#GG##F##GKNGGGGGGKGKGGGG########SSGGGGGKGKGGGGNG##F##GG#....",
    "....#GGGGGGGGKNGGGGGGKGKGGGGGGSSSSSSSSGGGGGKGKGGGGNGGKGGGGG#....",
    "....########################################################....",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
}
local f2_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "....########################################################....",
    "....#GGGGGGGGKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGGGKGGGGG#....",
    "....#GG##F##GKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGG##F##GG#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FFFFF#G#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FEEEF#G#....",
    "....#GFFEEEFFKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGFFEEEFFG#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FEEEF#G#....",
    "....#G#FFFFF#KG##GGGNKGKGGGGGGGGGGGGGGGGGGGKNKG##GG#FFFFF#G#....",
    "....#GG##F##GK#PP#GGNKGKGGGGGGGGGGGGGGGGGGGKNK#BB#GG##F##GG#....",
    "....#GGGGGGGG#PPPP#GNKGKGG############GGGGGKN#BBBB###KGGGGG#....",
    "....#GGGGGGG#PPPPPP#NKG###AAABBBBBBBBB###GGK#BBBBBB##KGGGGG#....",
    "....#GGGGGG#PPPPPAAA#K#PAAAAABBBBBBBBBBBB#G#BBBBBBBB#KGGGGG#....",
    "....#GGGGGG#PPPPAAAAP#PPAAAAABBBBBBBBBBBBB#CBBBVBBBB#SGGGGG#....",
    "....#NNNNNNN#PPAAAAPPPPPPAAAABBBBBBBBBBBBBCCCBVVVBB#SSSNNNN#....",
    "....#KKKKKKKN#PAAAPPPPPAAAA##########BBBBCCCCVVVVV#SSSSKKKK#....",
    "....#GGGGGGGNK#AAPPPPPAAA##SSSSSSSSSS##BCCCCVVVVV#SSSSGGGGG#....",
    "....#GGGGGGGNKG#PPPPPAAA#SSSSSSSSSSSSSS#CCCVVVVV#SSSSKGGGGG#....",
    "....#GGGGGGGNKGG#PPPAAAA#SSSSGGGGGGGGGG#CCCCVVV#SSSSNKGGGGG#....",
    "....#GGGGGGGNKG#PPPAAAAAA#SGGGGGGGGGGG#BBBCCCVVC#SSGNKGGGGG#....",
    "....#GGGGGGGNK#PPPAAAAAAAA#GGGGGGGGGG#BBBBCCCCCCC#GGNKGGGGG#....",
    "....#GGGGGGGNK#AAPAA##AAAAA##########BBBBB##CCCCC#SGNKGGGGG#....",
    "....#GGGGGGGNK#AAAA#SS#AAAAAAAAABBBBBBBBB#SS#CCCC#SSNKGGGGG#....",
    "....#GGGGGGGN#AAAAA#SSS#AAAAAAAABBBBBBBB#SSS#CZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGK#AAAAAAABBBBBBB#SSSSG#ZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGK#AAAAAIIFFBBBBB#SSSKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAAIIIFFFBBCC#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAIIIEEFFFCCC#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAIIEEEEFFZZZ#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#NNNNNNNN#BBBB#SSNNN#BBBFFEEEELLZZZ#SSNNN#ZZZZ#SSNNNNNN#....",
    "....#KKKKKKKK#BBBB#SSKNK#BBBFFFEELLLZZZ#SSNKK#ZZZZ#SSKKKKKK#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBFFFLLLZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBBFFLLZZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBBCZZZZZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBBB#SKN#BBBBBCCZZZZZZZZZ#SNK#ZZZZZ#SSKGGGGG#....",
    "....#GGGGGGGGK#BBBB#SK#BBBBBBCCZZZZZZZZZZ#NK#ZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBB##BBBBB##########ZZZZZ##ZZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBCCCBBBB#SSSSSSSSSS#ZZZZZZZZZZZ#SSGKGGGGG#....",
    "....#GGGGGGGGKG#BBCCCCBBB#SSSSSSSSSSSS#ZZZZZZZZZ#SSSGKGGGGG#....",
    "....#GGGGGGGGKGG#CCCCCCC#SSSSGGGGGGGGGG#ZZZZZZZ#SSSSGKGGGGG#....",
    "....#GGGGGGGGKG#CCCCCCCC#SSSGGGGGGGGGGG#ZZVVZZZZ#SSGGKGGGGG#....",
    "....#GGGGGGGGK#BBCCCCCCCC##GGGGGGGGGG##ZZVVVVZZZZ#GGGKGGGGG#....",
    "....#GGGGGGGG#BBBBCCCCCCCCC##########ZZZVVVVVVZZZZ#GGKGGGGG#....",
    "....#GGGGGGG#BBBBBBCCCCCCCZZZZZZZZZZZZZZZVVVVVZZZZZ#GKGGGGG#....",
    "....#NNNNNN#BBBBBBBBC#CCCCZZZZZZZZZZZZZZZZ#VVZZZZZZZ#NNNNNN#....",
    "....#KKKKKK#BBBBBBBB#S#CCCZZZZZZZZZZZZZZZ#S#ZZZZZZZZ#SKKKKK#....",
    "....#GGGGGGG#BBBBBB#SSS###ZZZZZZZZZZZZ###SSS#ZZZZZZ#SSSGGGG#....",
    "....#GGGGGGGG#BBBB#SSSSKSS############SSSSSSG#ZZZZ#SSSSGGGG#....",
    "....#GG##F##GK#BB#SSSSGKGSSSSSSSSSSSSSSSSSSKGK#ZZ#SS##F##GG#....",
    "....#G#FFFFF#KN##SSSSKGKGGGGSSSSSSSSSSSSGGGKGKG##SS#SFFFF#G#....",
    "....#G#FEEEF#KNGSSSSGKGKGGGGGGGGGGNGGGGGGGGKGKGGSSS#FEEEF#G#....",
    "....#GFFEEEFFKNGGSSGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGSSFFEEEFFG#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGN#FEEEF#G#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGN#FFFFF#G#....",
    "....#GG##F##GKNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGNG##F##GG#....",
    "....#GGGGGGGGKNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGNGGKGGGGG#....",
    "....########################################################....",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
}
local f3_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "....########################################################....",
    "....#GGGGGGGGKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGGGKGGGGG#....",
    "....#GG##F##GKGGGGGGNKGKGGGG########GGGGGGGKNKGGGGGG##F##GG#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGG#ABBBBB#GGGGGGGKNKGGGGG#FFFFF#G#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGG#FEEEF#G#....",
    "....#GFFEEEFFKGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGGFFEEEFFG#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGG#FEEEF#G#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGG#FFFFF#G#....",
    "....#GG##F##GKGGGGGGNKGKGGGG#AABBBB#SSGGGGGKNKGGGGGG##F##GG#....",
    "....#GGGGGGGGKGGGGGGNKGKGG##ABBBBBBB##GGGGGKNKGG#####KGGGGG#....",
    "....#GGGGGGGGKGGGGGGNKG###AAABBBBBBBBB###GGKNKGG#FEF#KGGGGG#....",
    "....#GGGGGGGGKGGGGGGNK#PAAAAABBBBBBBBBBBB#GKNKGG#FFF#KGGGGG#....",
    "....#GGGGGGGGKGGGGGG##PPAAAAABBBBBBBBBBBBB##NKGFF####KGGGGG#....",
    "....#NNNNNNNNNNNNNN#PPPPPAAAABBBBBBBBBBBBBCC#NFFFNNNNNNNNNN#....",
    "....#KKKKKKKNKKKKK#PPPPAAAA##ABBBBB##BBBBCCCC#FFKKKKNKKKKKK#....",
    "....#GGGGGGGNKGGG#PPPPAAA##SS#AABB#SS##BCCCCCC#GGGGGNKGGGGG#....",
    "....#GGGGGGGNKGG#PPPPAAA#SSSS#AABB#SSSS#CCCCCCC#GGGGNKGGGGG#....",
    "....#GGGGGGGNKGG#PPPAA##SSSSS#AABB#SSGGS##CCCCC#SGGGNKGGGGG#....",
    "....#GGGGGGGNKG#PPPAA#SSSSSGG#AABB#SSGGGGS#CCCCC#SGGNKGGGGG#....",
    "....#GGGGGGGNK#PPPAAA#SSSSGGG#AABB#SSGGGGG#CCCCCC#GGNKGGGGG#....",
    "....#GGGGGGGNK#AAPAA#SSSGGGG#AAABBB#SGGGGGG#CCCCC#SGNKGGGGG#....",
    "....#GGGGGGGNK#AAAA#SSSSGGG#AAAABBBB#GGGGGGK#CCCC#SSNKGGGGG#....",
    "....#GGGGGGGN#AAAAA#SSSKGG#AAAAABBBBB#GGGGGK#CZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGKG#AAAAAABBBBBB#GGGGKG#ZZZZ#SNKGGGGG#....",
    "....#G#######AAAAA#SSSGK#AAAAAIIFFBBBBB#GGGKG#ZZZZZ#######G#....",
    "....#G#AAAAAABBBBBA#####AAAAAIIIFFFBBCCC#####ZZZZZZZZZZZZ#G#....",
    "....#G#BAAAAABBBBBBAAAAAAAAAIIIEEFFFCCCCCCCZZZZZZZZZZZZZZ#S#....",
    "....#G#BBBBBBBBBBBBAAAAAAAAAIIEEEEFFZZZZZZZZZZZZVVVVVVZZZ#S#....",
    "....#N#BBBBBBBBBBBBBBBBBBBBBFFEEEELLZZZZZZZZZZZZVVVVVVZZZ#S#....",
    "....#K#BBBBBBBBBBBBBBBBBBBBBFFFEELLLZZZZZZZZZZZZVVVVVVZZZ#S#....",
    "....#G#BBBBBBBBBBBB#####BBBBBFFFLLLZZZZZ#####ZZZVVVVVVZZZ#S#....",
    "....#G#######BBBBB#SSSSS#BBBBBFFLLZZZZZ#SSSSS#ZZVVV#######S#....",
    "....#GGGSSSSS#BBBB#SSSSSS#BBBBCZZZZZZZ#SSSSSS#ZZZZ#SSSSSSSS#....",
    "....#GGGSSSSS#BBBBB#SKNKGG#BBCCZZZZZZ#SSSSNK#ZZZZZ#SSSSSSSS#....",
    "....#GGGGGGGGK#BBBB#SKNKGGG#BCCZZZZZ#SSSSGNK#ZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBB#SNKGGGG#CCZZZZ#SSSSGGN#ZZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBCC#NKGGGGG#CZZZ#SSSSGGG#ZZZZZZ#SSGKGGGGG#....",
    "....#GGGGGGGGKG#BBCCC#SKGGGGG#CZZZ#SSSGGGG#ZZZZZ#SSSGKGGGGG#....",
    "....#GGGGGGGGKGG#CCCCC##GGGGG#CZZZ#SSGGG##ZZZZZ#SSSSGKGGGGG#....",
    "....#GGGGGGGGKGG#CCCCCCC#GGGG#ZZZZ#SSGG#ZZZZZZZ#SSSGGKGGGGG#....",
    "....#GGGGGGGGKGGG#CCCCCCC##GG#ZZZZ#SS##ZZZZZZZ#SSSGGGKGGGGG#....",
    "....#GGGGGGGGKGGGG#CCCCCCCC##ZZZZZZ##ZZZZZZZZ#SSSSGGGKGGGGG#....",
    "....#GGGGGGGGKGGGGG#CCCCCCZZZZZZZZZZZZZZZZZZ#SSSSGGGGKGGGGG#....",
    "....#NNNNNNNNNNNNNNN##CCCCZZVVVVZZZZZZZZZZ##SSSSNNNNNNNNNNN#....",
    "....#KKKKKKKKKNKKKKKKS#CCCZZVVVVZZZZZZZZZ#SSSSSKKKNKKKKKKKK#....",
    "....#GGGGGGGGKNGGGGGGKS###ZZVVVVZZZZZZ###SSSSSGGGGNGGKGGGGG#....",
    "....#GGGGGGGGKNGGGGGGKGKSS##VVVVZZZZ##SSSSSSGKGGGGNGGKGGGGG#....",
    "....#GG##F##GKNGGGGGGKGKGSSS#VVVZZZ#SSSSSSSKGKGGGGNG##F##GG#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGG#ZZZZZZ#SSSSGGGKGKGGGGN#FFFFF#G#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FEEEF#G#....",
    "....#GFFEEEFFKNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGNFFEEEFFG#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FEEEF#G#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGG#ZZZZZZ#SSGGGGGKGKGGGGN#FFFFF#G#....",
    "....#GG##F##GKNGGGGGGKGKGGGG########SSGGGGGKGKGGGGNG##F##GG#....",
    "....#GGGGGGGGKNGGGGGGKGKGGGGGGSSSSSSSSGGGGGKGKGGGGNGGKGGGGG#....",
    "....########################################################....",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
}
local f4_grid = {
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
    "....########################################################....",
    "....#GGGGGGGGKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGGGKGGGGG#....",
    "....#GG##F##GKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGG##F##GG#....",
    "....#G#FFFFF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FFFFF#G#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FEEEF#G#....",
    "....#GFFEEEFFKGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGGFFEEEFFG#....",
    "....#G#FEEEF#KGGGGGGNKGKGGGGGGGGGGGGGGGGGGGKNKGGGGG#FEEEF#G#....",
    "....#G#FFFFF#KG##GGGNKGKGGGGGGGGGGGGGGGGGGGKNKG##GG#FFFFF#G#....",
    "....#GG##F##GK#PP#GGNKGKGGGGGGGGGGGGGGGGGGGKNK#BB#GG##F##GG#....",
    "....#GGGGGGGG#PPPP#GNKGKGG############GGGGGKN#BBBB###KGGGGG#....",
    "....#GGGGGGG#PPPPPP#NKG###AAABBBBBBBBB###GGK#BBBBBB##KGGGGG#....",
    "....#GGGGGG#PPPPPAAA#K#PAAAAABBBBBBBBBBBB#G#BBBBBBBB#KGGGGG#....",
    "....#GGGGGG#PPPPAAAAP#PPAAAAABBBBBBBBBBBBB#CBBBBBBBB#SGGGGG#....",
    "....#NNNNNNN#PPAAAAPPPPPPAAAABBBBBBBBBBBBBCCCBBBBBB#SSSNNNN#....",
    "....#KKKKKKKN#PAAAPPPPPAAAA##########BBBBCCCCCBBBB#SSSSKKKK#....",
    "....#GGGGGGGNK#AAPPPPPAAA##SSSSSSSSSS##BCCCCCCCBB#SSSSGGGGG#....",
    "....#GGGGGGGNKG#PPPPPAAA#SSSSSSSSSSSSSS#CCCCCCCC#SSSSKGGGGG#....",
    "....#GGGGGGGNKGG#PPPAAAA#SSSSGGGGGGGGGG#CCCCCCC#SSSSNKGGGGG#....",
    "....#GGGGGGGNKG#PPPAAAAAA#SGGGGGGGGGGG#BBBCCCCCC#SSGNKGGGGG#....",
    "....#GGGGGGGNK#PPPAAAAAAAA#GGGGGGGGGG#BBBBCCCCCCC#GGNKGGGGG#....",
    "....#GGGGGGGNK#AAPAA##AAAAA##########BBBBB##CCCCC#SGNKGGGGG#....",
    "....#GGGGGGGNK#AAAA#SS#AAAAAAAAABBBBBBBBB#SS#CCCC#SSNKGGGGG#....",
    "....#GGGGGGGN#AAAAA#SSS#AAAAAAAABBBBBBBB#SSS#CZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGK#AAAAAAABBBBBBB#SSSSG#ZZZZ#SNKGGGGG#....",
    "....#GGGGGGGN#AAAA#SSSGK#AAAAAIIFFBBBBB#SSSKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAAIIIFFFBBCC#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAIIIEEFFFCCC#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGN#BBBB#SSKGK#AAAIIEEEEFFZZZ#SSGKG#ZZZZ#SSKGGGGG#....",
    "....#NNNNNNNN#BBBB#SSNNN#BBBFFEEEELLZZZ#SSNNN#ZZZZ#SSNNNNNN#....",
    "....#KKKKKKKK#BBBB#SSKNK#BBBFFFEELLLZZZ#SSNKK#ZZZZ#SSKKKKKK#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBFFFLLLZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBBFFLLZZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBB#SSKNK#BBBBBCZZZZZZZZ#SSNKG#ZZZZ#SSKGGGGG#....",
    "....#GGGGGGGG#BBBBB#SKN#BBBBBCCZZZZZZZZZ#SNK#ZZZZZ#SSKGGGGG#....",
    "....#GGGGGGGGK#BBBB#SK#BBBBBBCCZZZZZZZZZZ#NK#ZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBBB##BBBBB##########ZZZZZ##ZZZZZ#SSSKGGGGG#....",
    "....#GGGGGGGGK#BBBVCCCBBBB#SSSSSSSSSS#ZZZZZZZZZZZ#SSGKGGGGG#....",
    "....#GGGGGGGGKG#BVVVCCBBB#SSSSSSSSSSSS#ZZZZZZZZZ#SSSGKGGGGG#....",
    "....#GGGGGGGGKGG#VVVVCCC#SSSSGGGGGGGGGG#ZZZZZZZ#SSSSGKGGGGG#....",
    "....#GGGGGGGGKG#VVVVVCCC#SSSGGGGGGGGGGG#ZZZVZZZZ#SSGGKGGGGG#....",
    "....#GGGGGGGGK#BXVVVCCCCC##GGGGGGGGGG##ZZZVVVZZZZ#GGGKGGGGG#....",
    "....#GGGGGGGG#BBBXVCCCCCCCC##########ZZZZVVVVVZZZZ#GGKGGGGG#....",
    "....#GGGGGGG#BBBBBBCCCCCCCZZZZZZZZZZZZZZZVVVVVVZZZZ#GKGGGGG#....",
    "....#NNNNNN#BBBBBBBBC#CCCCZZZZZZZZZZZZZZZZ#VVVVVZZZZ#NNNNNN#....",
    "....#KKKKKK#BBBBBBBB#S#CCCZZZZZZZZZZZZZZZ#S#VVVZZZZZ#SKKKKK#....",
    "....#GGGGGGG#BBBBBB#SSS###ZZZZZZZZZZZZ###SSS#VZZZZZ#SSSGGGG#....",
    "....#GGGGGGGG#BBBB#SSSSKSS############SSSSSSG#ZZZZ#SSSSGGGG#....",
    "....#GG##F##GK#BB#SSSSGKGSSSSSSSSSSSSSSSSSSKGK#ZZ#SS##F##GG#....",
    "....#G#FFFFF#KN##SSSSKGKGGGGSSSSSSSSSSSSGGGKGKG##SS#SFFFF#G#....",
    "....#G#FEEEF#KNGSSSSGKGKGGGGGGGGGGNGGGGGGGGKGKGGSSS#FEEEF#G#....",
    "....#GFFEEEFFKNGGSSGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGSSFFEEEFFG#....",
    "....#G#FEEEF#KNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGN#FEEEF#G#....",
    "....#G#FFFFF#KNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGN#FFFFF#G#....",
    "....#GG##F##GKNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGNG##F##GG#....",
    "....#GGGGGGGGKNGGGGGGKGKGGGGGGGGGGNGGGGGGGGKGKGGGGNGGKGGGGG#....",
    "....########################################################....",
    "................................................................",
    "................................................................",
    "................................................................",
    "................................................................",
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
sprite:saveCopyAs("output/aseprite/steam_gear_machine_64.aseprite")

-- Save Animated GIF
sprite:saveCopyAs("output/gif/steam_gear_machine_64.gif")

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
sheetSprite:saveCopyAs("output/Sheet/steam_gear_machine_64_sheet.png")
sheetSprite:close()
