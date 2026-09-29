-- scripts/wooden_fence_32.lua
-- 32x32 Stardew Valley Seamless Wooden Fence Tilemap
-- Static Tilemap: Horizontally Seamless at col 1 & col 32

local width = 32
local height = 32

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
local image = sprite.cels[1].image

-- 1. Palette: Stardew Valley (Gam màu ấm, viền mềm nâu vỏ cây, bóng râm S)
local PALETTE = {
    ["."] = nil,
    ["#"] = "#341910", -- Viền sẫm nâu ấm (Warm dark mahogany/bark outline, no pure black)
    ["S"] = "#1c1224", -- Bóng tiếp đất ngang liền mạch (Ground contact shadow, alpha 130)

    -- Chất liệu gỗ hàng rào (Warm Cedar / Pine Wood)
    ["H"] = "#f2be68", -- Đốm sáng thớ gỗ / viền ván trên (Golden pine highlight)
    ["L"] = "#d68936", -- Gỗ sáng đón sáng (Light cedar wood body)
    ["M"] = "#a65c22", -- Gỗ sắc độ trung (Midtone wood base)
    ["D"] = "#6e3414", -- Gỗ vùng tối & rãnh thớ (Shadow wood & grain grooves)
    ["V"] = "#3d1b0a", -- Rãnh nẹp & khe nứt sâu (Plank seam & deep crevice)

    -- Đinh sắt rèn đính nẹp ngang (Forged Iron Hardware)
    ["P"] = "#fff0bc", -- Điểm phản quang đinh sắt (Ivory specular nail glint)
    ["Q"] = "#584e62"  -- Đầu đinh sắt rèn tối (Dark forged iron nail head)
}

-- 2. Ma trận ký tự 32x32: Khớp nối Seamless hoàn hảo giữa cột đầu tiên và cột cuối cùng
local frame1_grid = {
    "................................",
    "................................",
    "................................",
    "................................",
    ".......##..............##.......",
    "......#HH#............#HL#......",
    ".....#HLLM#..........#LHMD#.....",
    ".....#LHML#..........#HLLM#.....",
    ".....#LLMD#..........#LMDL#.....",
    ".....#HMLM#..........#MLHM#.....",
    "######HLML#D##########LHMD#D####",
    "HLHLH#LPQD#DHLHLHLHLH#HPQM#DHLHH",
    "LMLML#LQMM#VLMLMLMLML#HQDL#VLMLL",
    "MDMDM#HMLD#VDMDMDMDMD#LHMM#VDMDM",
    "######LLHM#V##########HLLD#V####",
    ".....#DVDL#..........#LHML#.....",
    ".....#LDMD#..........#MLHM#.....",
    ".....#HLLM#..........#HMLD#.....",
    ".....#LHML#..........#LLHM#.....",
    "######HLMD#D##########LHMD#D####",
    "HLHLH#LPQM#DHLHLHLHLH#HPQL#DHLHH",
    "LMLML#LQDD#VLMLMLMLML#HQDM#VLMLL",
    "MDMDM#HLLM#VDMDMDMDMD#LHMD#VDMDM",
    "######LHML#V##########HLLM#V####",
    ".....#HLLD#..........#LHML#.....",
    ".....#LLHM#..........#HLLD#.....",
    ".....#LHML#..........#MLHM#.....",
    "SSSSS#DMMD#SSSSSSSSSS#DMVD#SSSSS",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "................................"
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

-- Render Frame 1 (Static Tile)
renderGrid(image, frame1_grid, PALETTE)

-- 4. Pipeline xuất file đa định dạng an toàn cho Aseprite CLI
-- A. Xuất file gốc lưu lại Layer & Frame
sprite:saveCopyAs("output/wooden_fence_32.aseprite")

-- B. Nếu là Static: xuất ảnh PNG tĩnh đơn lẻ
sprite:saveCopyAs("output/wooden_fence_32.png")
