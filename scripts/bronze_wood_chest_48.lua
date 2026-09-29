-- scripts/bronze_wood_chest_48.lua
-- 48x48 Stardew Valley Animated Chest (Bronze & Wood)
-- 3 Frames: Closed -> Ajar -> Fully Open at 8 FPS

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley warm tones, no pure #000000 outline
local PALETTE = {
    ["."] = nil,
    ["#"] = "#2d1510", -- Viền sẫm nâu ấm (Soft dark mahogany outline)
    ["S"] = "#1e1220", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Chất liệu gỗ (Warm Cedar / Oak)
    ["H"] = "#f0b669", -- Đốm sáng thớ gỗ (Wood grain highlight)
    ["L"] = "#d88c40", -- Gỗ sáng (Light wood)
    ["M"] = "#ae6224", -- Gỗ màu chính (Mid wood base)
    ["D"] = "#703414", -- Gỗ vùng tối / mắt gỗ (Shadow wood & knots)
    ["V"] = "#441c0c", -- Rãnh ván gỗ & hốc tối (Plank seam & deep crevice)

    -- Chất liệu đai đồng (Warm Burnished Bronze / Copper)
    ["P"] = "#fff4c0", -- Điểm phản quang đinh tán (Ivory specular rivet highlight)
    ["Q"] = "#ebac4a", -- Đồng sáng bóng (Light polished bronze)
    ["R"] = "#bc7228", -- Đồng màu chính (Mid burnished bronze)
    ["T"] = "#7c3e16", -- Viền tối đai đồng (Dark bronze shadow)
    ["U"] = "#50220e", -- Khe nối đai đồng (Bronze seam & joint)

    -- Chiều sâu lòng rương & kho báu bên trong (Interior depth & gold treasure)
    ["I"] = "#24100a", -- Bóng sâu lòng hòm (Deepest chest cavity shadow)
    ["J"] = "#441e0e", -- Bóng đổ thành trong rương (Inner wall cast shadow)
    ["K"] = "#6a3517", -- Thành trong đón sáng (Inner wall lit)
    ["G"] = "#ffd238", -- Vàng lấp lánh (Gleaming treasure gold)
    ["Y"] = "#c88a1a", -- Vàng sắc độ trung (Gold mid tone)
    ["Z"] = "#8e580e"  -- Bóng khe tiền vàng (Gold coin shadow)
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
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    ".........##############################.........",
    "........#HLLTQRTLLLLLLTQRTLLLLLLTQRTLLH#........",
    ".......#LHHMTPLRLHHLHLMTPLLHHLHLTPLRLHHM#.......",
    ".......#LLLMTQRTLLHLLLMTQRLLHLLLTQRTLLLM#.......",
    ".......#MLLMTQRTMLLLLMLTQRMLLLLMTQRTMLLM#.......",
    ".......#MMMMTQRTMMHLLMLTQRMMHLLMTQRTMMMM#.......",
    ".......#LMMMTQRTLMLLLMLTQRLMLLLMTQRTLMMM#.......",
    ".......#MMMMTQRTMMMDMMLTQRMMMMDMTQRTMMMM#.......",
    ".......#LLMMTQRTLLMMLLLTQRLLMMLLTQRTLLMM#.......",
    "......#HLLLLTQRTLLLLLLPQRRLLLLLLTQRTLLLLH#......",
    "......#LLMMMTPLRLMLLLMPQRPLMLLLMTPLRLLMMM#......",
    "......#MMMMMTQRTMMMMMMPQRRMMMMMMTQRTMMMMM#......",
    "......#TQQPRTQPRTTQQPRPQRPTTQQPRTQPRTTQPR#......",
    ".......#VVVVTQRTVVVVVVPQRPVVVVVVTQRTVVVV#.......",
    ".......#LLHLTQRTLLHHLLPQRRLLHHLLTQRTLLHL#.......",
    ".......#LLLMTPLRLLHLLMPPRPLLHLLMTPLRLLLM#.......",
    ".......#MMMMTQRTMMDDMMTIITMMMMMMTQRTMMMM#.......",
    ".......#MMLMTQRTMDMMMLURRUMMMLMMTQRTMMLM#.......",
    ".......#MMMMTRRTMMLLMMMMLLMMLLMMTRRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMDDMDMMMMDTQRTDMMM#.......",
    ".......#VVVVTQRTVVVVVVVDVVVVVVVVTQRTVVVV#.......",
    ".......#LLLMTQRTLLLHLLMLMLLLLHLLTQRTLLLM#.......",
    ".......#LHLMTPLRLHHMLLMLHLLHHMLLTPLRLHLM#.......",
    ".......#MMLLTQRTMLLLMMDMLMMLLLMMTQRTMMLL#.......",
    ".......#MMMMTQRTMMMMMMMDMMMMMMMMTQRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMMMMDMMMMDTQRTDMMM#.......",
    ".......#TRRTTTRTTMMRTRRTTMMRTRRTTTRTTRRT#.......",
    ".......##################################.......",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "...........SSSSSSSSSSSSSSSSSSSSSSSSSS...........",
    "................................................"
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
    ".........##############################.........",
    "........#HLLTQRTLLLLLLTQRTLLLLLLTQRTLLH#........",
    ".......#LHHMTPLRLHHLHLMTPLLHHLHLTPLRLHHM#.......",
    ".......#LLLMTQRTLLHLLLMTQRLLHLLLTQRTLLLM#.......",
    "......#HLLLLTQRTLLLLLLPQRRLLLLLLTQRTLLLLH#......",
    "......#LLMMMTPLRLMLLLMPQRPLMLLLMTPLRLLMMM#......",
    "......#TQQPRTQPRTTQQPRPQRPTTQQPRTQPRTTQPR#......",
    "............TTRT......URRU......TTRT............",
    ".......#LMIIIIIIIIIIIIIIIIIIIIIIIIIIIIMD#.......",
    ".......#LMIIIIIIIIIIIIIIIIIIIIIIIIIIIIMD#.......",
    ".......#LMIIIIIIIIIIIIYYYYYYIIIIIIIIIIMD#.......",
    ".......#LMIIIIIIIIJJJYYYYGGYYYYYIIIIIIMD#.......",
    ".......#LMIIIIIIJJYYYYGGPGGYYYYYIIIIIIMD#.......",
    ".......#LMIIIIIJJYYYYGGYYGGYYYYYZZIIIIMD#.......",
    ".......#LMIIIIJJJJYYYYGGYYYYYYZZZZIIIIMD#.......",
    ".......#LMVVVVZZZZYYYYGGYYYYZZZZZVVVVVMD#.......",
    ".......#HLLMTQPTMHLLMLPQRRMLLHLMTQPTMMLL#.......",
    ".......#LLHLTQRTLLHHLLPQRRLLHHLLTQRTLLHL#.......",
    ".......#LLLMTPLRLLHLLMPPRPLLHLLMTPLRLLLM#.......",
    ".......#MMMMTQRTMMDDMMTIITMMMMMMTQRTMMMM#.......",
    ".......#MMLMTQRTMDMMMLURRUMMMLMMTQRTMMLM#.......",
    ".......#MMMMTRRTMMLLMMMMLLMMLLMMTRRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMDDMDMMMMDTQRTDMMM#.......",
    ".......#VVVVTQRTVVVVVVVDVVVVVVVVTQRTVVVV#.......",
    ".......#LLLMTQRTLLLHLLMLMLLLLHLLTQRTLLLM#.......",
    ".......#LHLMTPLRLHHMLLMLHLLHHMLLTPLRLHLM#.......",
    ".......#MMLLTQRTMLLLMMDMLMMLLLMMTQRTMMLL#.......",
    ".......#MMMMTQRTMMMMMMMDMMMMMMMMTQRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMMMMDMMMMDTQRTDMMM#.......",
    ".......#TRRTTTRTTMMRTRRTTMMRTRRTTTRTTRRT#.......",
    ".......##################################.......",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "...........SSSSSSSSSSSSSSSSSSSSSSSSSS...........",
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
    "................................................",
    ".........##############################.........",
    "........#DDDTTRTDDDDDDTTRTDDDDDDTTRTDDD#........",
    ".......#JDDMTTRTJDDDDDTTRTDDDDDJTTRTMDDJ#.......",
    ".......#JJDDTTRTJJDDDDTTRTDDDDJJTTRTDDJJ#.......",
    ".......#JJJDTTRTJJJDDDTTRTDDDJJJTTRTDJJJ#.......",
    ".......#JJJJTTRTJJJJDDTTRTDDJJJJTTRTJJJJ#.......",
    ".......#JJJJTPLRJJJJDDTPLRDDJJJJTPLRJJJJ#.......",
    ".......#JJJJTQRTJJJJDDTQRTDDJJJJTQRTJJJJ#.......",
    ".......#JJJJTQRTJJJJDDTQRTDDJJJJTQRTJJJJ#.......",
    ".......#VVVVTTRTVVVVDDTTRTDDVVVVTTRTVVVV#.......",
    ".......##################################.......",
    ".......#LMIIIIIIIIIIIIIIIIIIIIIIIIIIIIMD#.......",
    ".......#LMIIIIIIIIJJJIIIIIIIYYYYYIIIIIMD#.......",
    ".......#LMIIIIIIJJIIJJJJJYYYYGGYYYYYIIMD#.......",
    ".......#LMIIIIJJJJIIJJYYYYGGPGGYYYYYJJMD#.......",
    ".......#LMIIIJJJJJJYYYYPGGYGPPGGYYYYZZMD#.......",
    ".......#LMIIJJJJJJYYYYGGYYGGPGGYYYYYZZMD#.......",
    ".......#LMIJJJJJJZYYGGPGGYYPGGYYYYZZZZMD#.......",
    ".......#LMJJJJJJZZZYYYGGYYYYYYZZZZZZJJMD#.......",
    ".......#LMVVVVZZZZYYYYGGYYYYZZZZZVVVVVMD#.......",
    ".......#LMVVVVIIIIIIIIIIIIIIIIIIIVVVVVMD#.......",
    ".......#HLLMTQPTMHLLMLPQRRMLLHLMTQPTMMLL#.......",
    ".......#LLHLTQRTLLHHLLPQRRLLHHLLTQRTLLHL#.......",
    ".......#LLLMTPLRLLHLLMPPRPLLHLLMTPLRLLLM#.......",
    ".......#MMMMTQRTMMDDMMTIITMMMMMMTQRTMMMM#.......",
    ".......#MMLMTQRTMDMMMLURRUMMMLMMTQRTMMLM#.......",
    ".......#MMMMTRRTMMLLMMMMLLMMLLMMTRRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMDDMDMMMMDTQRTDMMM#.......",
    ".......#VVVVTQRTVVVVVVVDVVVVVVVVTQRTVVVV#.......",
    ".......#LLLMTQRTLLLHLLMLMLLLLHLLTQRTLLLM#.......",
    ".......#LHLMTPLRLHHMLLMLHLLHHMLLTPLRLHLM#.......",
    ".......#MMLLTQRTMLLLMMDMLMMLLLMMTQRTMMLL#.......",
    ".......#MMMMTQRTMMMMMMMDMMMMMMMMTQRTMMMM#.......",
    ".......#DMMMTQRTDMMMMDMMMMDMMMMDTQRTDMMM#.......",
    ".......#TRRTTTRTTMMRTRRTTMMRTRRTTTRTTRRT#.......",
    ".......##################################.......",
    ".....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.....",
    ".......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.......",
    "...........SSSSSSSSSSSSSSSSSSSSSSSSSS...........",
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

-- Render Frame 1: Đóng nắp (Closed)
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Hé mở (Ajar)
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Mở hoàn toàn (Fully Open)
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/bronze_wood_chest_48.aseprite")

-- B. Nếu là Animation: xuất GIF động và dải spritesheet ngang độc lập CLI
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/bronze_wood_chest_48.gif")
    
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
    sheetSprite:saveCopyAs("output/bronze_wood_chest_48_sheet.png")
    sheetSprite:close()
else
    -- Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
    sprite:saveCopyAs("output/bronze_wood_chest_48.png")
end
