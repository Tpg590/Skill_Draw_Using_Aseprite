import clean_final_tree

lines = clean_final_tree.lines
assert len(lines) == 64 and all(len(r) == 64 for r in lines)

grid_lua = ["local tree_grid = {"]
for i, r in enumerate(lines):
    comma = "," if i < 63 else ""
    grid_lua.append(f'    "{r}"{comma}')
grid_lua.append("}\n")
grid_str = "\n".join(grid_lua)

lua_script = f"""-- scripts/spooky_twisted_tree_64.lua
-- 64x64 Terraria Style Spooky Twisted Tree with Overlapping Branches & Stone Masonry Base
-- Static Asset: High Contrast, Heavy Silhouette, Corkscrew Wood Grain, 5-7 Colors

local width = 64
local height = 64

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
local image = sprite.cels[1].image

-- 1. Palette: Terraria High-Contrast Petrified Wood & Ancient Stone
-- Toàn bộ tác phẩm được giải quyết bằng đúng 5 màu đặc + 1 bóng tiếp đất S (Tổng 6 màu)
local PALETTE = {{
    ["."] = nil,
    ["#"] = "#180f14", -- Viền tối sẫm Terraria (Near-black plum/brown outline)
    ["S"] = "#120a10", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Sắc độ thân gỗ xoắn, cành nhánh & gạch đá chân đế
    ["H"] = "#bfa382", -- Vệt sáng thớ gỗ khô / Gờ đá sứt mẻ (Pale aged bark highlight & stone rim)
    ["M"] = "#82634d", -- Màu gỗ chính / Mặt gạch đá cổ (Mid aged bark & stone masonry face)
    ["D"] = "#4a3226", -- Gỗ tối / Bóng thân / Cành phía sau (Deep shadow wood & background branches)
    ["V"] = "#2a1812"  -- Rãnh xoắn sâu / Khe nứt gạch đá (Deepest twist crevice & stone fissure)
}}

-- 2. Ma trận ký tự (64x64)
{grid_str}
-- 3. Hàm render ma trận ký tự
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
                img:drawPixel(x - 1, y - 1, Color{{ r = r, g = g, b = b, a = a }})
            end
        end
    end
end

renderGrid(image, tree_grid, PALETTE)

-- 4. Pipeline xuất file CLI an toàn
sprite:saveCopyAs("output/spooky_twisted_tree_64.aseprite")
sprite:saveCopyAs("output/spooky_twisted_tree_64.png")
"""

with open("scripts/spooky_twisted_tree_64.lua", "w", encoding="utf-8") as f:
    f.write(lua_script)

print("Exported scripts/spooky_twisted_tree_64.lua successfully!")
