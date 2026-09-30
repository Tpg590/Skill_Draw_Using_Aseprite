import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from perfect_acid_splash import frames, W, H

def generate_lua():
    lua_lines = []
    lua_lines.append('-- scripts/acid_drop_splash_32.lua')
    lua_lines.append('-- 32x32 FreeStyle Animated Magic Acid Drop Impact & Splash')
    lua_lines.append('-- 4 Frames Cycle: Fall -> Impact Squash -> Crown Splash -> Ellipse Ripple (8 FPS)')
    lua_lines.append('')
    lua_lines.append('local width = 32')
    lua_lines.append('local height = 32')
    lua_lines.append('local fps = 8')
    lua_lines.append('local frameDuration = 1.0 / fps')
    lua_lines.append('')
    lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
    lua_lines.append('local layer = sprite.layers[1]')
    lua_lines.append('layer.name = "Acid_Splash"')
    lua_lines.append('sprite.frames[1].duration = frameDuration')
    lua_lines.append('local image = sprite.cels[1].image')
    lua_lines.append('')
    lua_lines.append('-- 1. Palette: FreeStyle Hue-Shifting Toxic Green shifting to Neon Yellow')
    lua_lines.append('local PALETTE = {')
    lua_lines.append('    ["."] = nil,')
    lua_lines.append('    ["#"] = "#0a2214", -- Viền sẫm xanh thẫm sạch (Clean dark toxic pine outline)')
    lua_lines.append('    ["S"] = "#101a14", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 140)')
    lua_lines.append('    ["W"] = "#faffaa", -- Phản quang trắng ngả vàng neon (Specular white-yellow glint)')
    lua_lines.append('    ["A"] = "#d8ff36", -- Sáng: Vàng chanh neon rực rỡ (Hue-shifted neon yellow-lime)')
    lua_lines.append('    ["B"] = "#4ae022", -- Nền: Xanh lục độc quang chủ đạo (Primary toxic poison green)')
    lua_lines.append('    ["C"] = "#127838"  -- Tối: Xanh ngọc lục bảo sâu (Hue-shifted deep emerald shadow)')
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
    lua_lines.append('                local a = (char == "S") and 140 or 255')
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
        "Frame 1: Fall (Rơi tự do) - Giọt lệ thuôn dài nhọn đỉnh, căng đáy đang lao xuống",
        "Frame 2: Impact (Nén va đập) - Bẹp dí tẹt dày 2px, rộng 12px trên sàn",
        "Frame 3: Crown Splash (Vương miện bắn tóe) - Đáy lõm, tia nhọn vọt lên + 2 giọt bắn 1px",
        "Frame 4: Ripple & Dissipate (Lan tỏa sóng) - Ellipse 3/4 mỏng lan rộng + 2 giọt rơi xuống sàn"
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
    lua_lines.append('sprite:saveCopyAs("output/aseprite/acid_drop_splash_32.aseprite")')
    lua_lines.append('sprite:saveCopyAs("output/gif/acid_drop_splash_32.gif")')
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
    lua_lines.append('sheetSprite:saveCopyAs("output/Sheet/acid_drop_splash_32_sheet.png")')
    lua_lines.append('sheetSprite:close()')
    lua_lines.append('')

    output_path = "scripts/acid_drop_splash_32.lua"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lua_lines))
    print(f"Generated {output_path} successfully ({len(lua_lines)} lines).")

if __name__ == "__main__":
    generate_lua()
