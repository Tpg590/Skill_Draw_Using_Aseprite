import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from perfect_shattering_pot import frames, W, H

def generate_lua():
    lua_lines = []
    lua_lines.append('-- scripts/shattering_terracotta_pot_48.lua')
    lua_lines.append('-- 48x48 Stardew Valley Animated Shattering Terracotta Pot')
    lua_lines.append('-- 4 Frames Cycle: Impact Cracks -> Fracture -> Parabolic Scatter -> Settled Debris (8 FPS)')
    lua_lines.append('')
    lua_lines.append('local width = 48')
    lua_lines.append('local height = 48')
    lua_lines.append('local fps = 8')
    lua_lines.append('local frameDuration = 1.0 / fps')
    lua_lines.append('')
    lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
    lua_lines.append('local layer = sprite.layers[1]')
    lua_lines.append('layer.name = "Main"')
    lua_lines.append('sprite.frames[1].duration = frameDuration')
    lua_lines.append('local image = sprite.cels[1].image')
    lua_lines.append('')
    lua_lines.append('-- 1. Palette: Stardew Valley Warm Terracotta Palette (Soft outlines, NO #000000!)')
    lua_lines.append('local PALETTE = {')
    lua_lines.append('    ["."] = nil,')
    lua_lines.append('    ["#"] = "#3c180e", -- Viền nâu đất nung sẫm mềm (Soft dark terracotta outline, NO #000000)')
    lua_lines.append('    ["S"] = "#26141c", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)')
    lua_lines.append('    ["A"] = "#f09a56", -- Đất nung sáng (Warm terracotta highlight)')
    lua_lines.append('    ["B"] = "#c8642a", -- Đất nung nền (Rich baked terracotta midtone)')
    lua_lines.append('    ["C"] = "#7a3216", -- Đất nung tối (Deep burnt sienna shadow)')
    lua_lines.append('    ["D"] = "#ffd28a", -- Men gốm vàng kem trang trí (Ceramic ornamental band & rim)')
    lua_lines.append('    ["E"] = "#9c481e", -- Lớp gốm vát cạnh trong (Inner ceramic fracture bevel)')
    lua_lines.append('    ["Z"] = "#280e08"  -- Vết nứt rạn va đập sâu (Deep fracture crack crevice)')
    lua_lines.append('}')
    lua_lines.append('')

    # Render function
    lua_lines.append('-- 2. Render function (with explicit transparent pixel clearing)')
    lua_lines.append('local function renderGrid(img, gridData, pal)')
    lua_lines.append('    for y = 1, #gridData do')
    lua_lines.append('        local line = gridData[y]')
    lua_lines.append('        for x = 1, #line do')
    lua_lines.append('            local char = line:sub(x, x)')
    lua_lines.append('            local hex = pal[char]')
    lua_lines.append('            if hex then')
    lua_lines.append('                local h = hex:gsub("#", "")')
    lua_lines.append('                local r = tonumber(h:sub(1, 2), 16) or 0')
    lua_lines.append('                local g = tonumber(h:sub(3, 4), 16) or 0')
    lua_lines.append('                local b = tonumber(h:sub(5, 6), 16) or 0')
    lua_lines.append('                local a = (char == "S") and 130 or 255')
    lua_lines.append('                img:drawPixel(x - 1, y - 1, Color{ r = r, g = g, b = b, a = a })')
    lua_lines.append('            else')
    lua_lines.append('                img:drawPixel(x - 1, y - 1, Color{ r = 0, g = 0, b = 0, a = 0 })')
    lua_lines.append('            end')
    lua_lines.append('        end')
    lua_lines.append('    end')
    lua_lines.append('end')
    lua_lines.append('')

    # Grids
    descriptions = [
        "Frame 1: Impact - Đáy chạm sàn, xuất hiện 2-3 đường nứt đậm dọc thân bình",
        "Frame 2: Fracture - Khối bình nổ bung ra thành 5 mảnh gốm lớn hình đa giác",
        "Frame 3: Scatter - Các mảnh văng xa theo hình vòng cung parabol + 3 mẩu dăm gốm nhỏ 1px",
        "Frame 4: Settle - Toàn bộ các mảnh gốm tiếp đất phân tán 3D tự nhiên, có bóng râm 'S'"
    ]

    for f_idx, fr in enumerate(frames):
        grid_var = f"f{f_idx + 1}_grid"
        lua_lines.append(f"-- 3.{f_idx + 1}. {descriptions[f_idx]}")
        lua_lines.append(f"local {grid_var} = {{")
        for y in range(H):
            row_str = "".join(fr[y][x] for x in range(W))
            lua_lines.append(f'    "{row_str}",')
        lua_lines.append("}")
        lua_lines.append("")

    # Draw frames
    lua_lines.append('-- 4. Render các frame hoạt ảnh')
    lua_lines.append('renderGrid(image, f1_grid, PALETTE)')
    lua_lines.append('')
    lua_lines.append('local frame2 = sprite:newFrame()')
    lua_lines.append('frame2.duration = frameDuration')
    lua_lines.append('local img2 = layer:cel(2).image')
    lua_lines.append('renderGrid(img2, f2_grid, PALETTE)')
    lua_lines.append('')
    lua_lines.append('local frame3 = sprite:newFrame()')
    lua_lines.append('frame3.duration = frameDuration')
    lua_lines.append('local img3 = layer:cel(3).image')
    lua_lines.append('renderGrid(img3, f3_grid, PALETTE)')
    lua_lines.append('')
    lua_lines.append('local frame4 = sprite:newFrame()')
    lua_lines.append('frame4.duration = frameDuration')
    lua_lines.append('local img4 = layer:cel(4).image')
    lua_lines.append('renderGrid(img4, f4_grid, PALETTE)')
    lua_lines.append('')

    # Export CLI
    lua_lines.append('-- 5. Xuất file CLI (Tuân thủ cấu trúc thư mục chuẩn)')
    lua_lines.append('sprite:saveCopyAs("output/aseprite/shattering_terracotta_pot_48.aseprite")')
    lua_lines.append('sprite:saveCopyAs("output/gif/shattering_terracotta_pot_48.gif")')
    lua_lines.append('')
    lua_lines.append('local totalFrames = #sprite.frames')
    lua_lines.append('local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)')
    lua_lines.append('local sheetImage = sheetSprite.cels[1].image')
    lua_lines.append('for i = 1, totalFrames do')
    lua_lines.append('    local frameCel = layer:cel(i)')
    lua_lines.append('    if frameCel then')
    lua_lines.append('        sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))')
    lua_lines.append('    end')
    lua_lines.append('end')
    lua_lines.append('sheetSprite:saveCopyAs("output/Sheet/shattering_terracotta_pot_48_sheet.png")')
    lua_lines.append('sheetSprite:close()')
    lua_lines.append('')

    output_path = "scripts/shattering_terracotta_pot_48.lua"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lua_lines))
    print(f"Generated {output_path} successfully ({len(lua_lines)} lines).")

if __name__ == "__main__":
    generate_lua()
