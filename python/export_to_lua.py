import refine_slime

f1 = refine_slime.f1
f2 = refine_slime.f2
f3 = refine_slime.f3
f4 = refine_slime.f4

assert len(f1) == 48 and all(len(r) == 48 for r in f1)
assert len(f2) == 48 and all(len(r) == 48 for r in f2)
assert len(f3) == 48 and all(len(r) == 48 for r in f3)
assert len(f4) == 48 and all(len(r) == 48 for r in f4)

def format_grid(grid, name):
    lines = [f"local {name} = {{"]
    for i, r in enumerate(grid):
        comma = "," if i < len(grid) - 1 else ""
        lines.append(f'    "{r}"{comma}')
    lines.append("}\n")
    return "\n".join(lines)

lua_code = f"""-- scripts/cyan_jelly_slime_48.lua
-- 48x48 FreeStyle Animated Translucent Slime Monster with Glowing Core
-- 4 Frames Looping: Rest -> Squash -> Stretch -> Fall / Recovery (8 FPS)

local width = 48
local height = 48
local fps = 8
local frameDuration = 1.0 / fps

local sprite = Sprite(width, height, ColorMode.RGB)
local layer = sprite.layers[1]
layer.name = "Main"
sprite.frames[1].duration = frameDuration
local image = sprite.cels[1].image

-- 1. Palette: FreeStyle Hue-Shifting (Vibrant Cyan to Deep Purple/Indigo)
local PALETTE = {{
    ["."] = nil,
    ["#"] = "#180529", -- Viền tím sậm mềm mại (Deep dark plum/purple outline)
    ["S"] = "#140520", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)

    -- Thạch trong suốt (Translucent Jelly Body: Hue-Shifting)
    ["P"] = "#ffffff", -- Đốm sáng phản quang thạch (Specular white highlight)
    ["H"] = "#b2ffff", -- Viền sáng xanh ngọc (Brilliant cyan specular halo)
    ["A"] = "#45ebfc", -- Xanh cyan rực rỡ (Vibrant outer jelly)
    ["B"] = "#0ea9cc", -- Xanh ngọc teal chủ đạo (Rich mid-tone core jelly)
    ["C"] = "#087396", -- Vùng chuyển bóng teal (Deep teal mid-shadow)
    ["D"] = "#3b1c61", -- Vùng tối tím sẫm (Hue-shifted deep purple body shadow)
    ["V"] = "#210b38", -- Vùng tối sâu đáy thạch (Deepest purple underside crevice)

    -- Lõi ma thuật & Hắt sáng OSL (Glowing Core & Color Bleed)
    ["W"] = "#ffffff", -- Tâm lõi phát quang trắng tinh khiết (White-hot core center)
    ["Y"] = "#b9ffff", -- Vòng halo neon của lõi (Neon cyan core halo)
    ["G"] = "#67f3ff"  -- Hắt sáng OSL tỏa vào lòng thạch (Inner glowing color bleed)
}}

-- 2. Ma trận ký tự các khung hình (48x48)
-- Frame 1: Nghỉ (Rest) - Khối vòm thạch cân đối, lõi tỏa sáng ở trung tâm
{format_grid(f1, "frame1_grid")}
-- Frame 2: Ép dẹp (Squash) - Chiều cao nén xuống, bề ngang nở rộng (Bảo toàn thể tích)
{format_grid(f2, "frame2_grid")}
-- Frame 3: Bật cao (Stretch) - Bề ngang bóp hẹp, chiều cao kéo dài phóng lên không trung
{format_grid(f3, "frame3_grid")}
-- Frame 4: Rơi xuống (Fall) - Rơi lơ lửng chuẩn bị tiếp đất, khép vòng lặp mượt mà
{format_grid(f4, "frame4_grid")}

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

-- Render Frame 1: Nghỉ (Rest)
renderGrid(image, frame1_grid, PALETTE)

-- Render Frame 2: Ép dẹp (Squash)
local frame2 = sprite:newFrame()
frame2.duration = frameDuration
local cel2 = layer:cel(2)
if cel2 then
    cel2.image:clear()
    renderGrid(cel2.image, frame2_grid, PALETTE)
end

-- Render Frame 3: Bật cao (Stretch)
local frame3 = sprite:newFrame()
frame3.duration = frameDuration
local cel3 = layer:cel(3)
if cel3 then
    cel3.image:clear()
    renderGrid(cel3.image, frame3_grid, PALETTE)
end

-- Render Frame 4: Rơi xuống (Fall)
local frame4 = sprite:newFrame()
frame4.duration = frameDuration
local cel4 = layer:cel(4)
if cel4 then
    cel4.image:clear()
    renderGrid(cel4.image, frame4_grid, PALETTE)
end

-- 4. Pipeline xuất file CLI
sprite:saveCopyAs("output/cyan_jelly_slime_48.aseprite")
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/cyan_jelly_slime_48.gif")
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/cyan_jelly_slime_48_sheet.png")
    sheetSprite:close()
else
    sprite:saveCopyAs("output/cyan_jelly_slime_48.png")
end
"""

with open("scripts/cyan_jelly_slime_48.lua", "w", encoding="utf-8") as f:
    f.write(lua_code)

print("Exported scripts/cyan_jelly_slime_48.lua successfully!")
