import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from perfect_swamp_firefly import perfect_frames, W, H

CODE_MAP = {
    ".": ".",
    "S": "S",
    "#": "#",
    "P1": "A",
    "P2": "B",
    "P3": "C",
    "M1": "D",
    "M2": "E",
    "E1": "F",
    "E2": "G",
    "W1": "H",
    "W2": "I",
    "W3": "J",
    "F0": "K",
    "F1": "L",
    "O1": "N",
    "O2": "O",
}

def generate_lua():
    lua_lines = []
    lua_lines.append('-- scripts/mossy_pillar_firefly_48.lua')
    lua_lines.append('-- 48x48 Terraria Animated Ancient Stone Pillar in Swamp Islet with Firefly & Hollow Ripple')
    lua_lines.append('-- 4 Frames Cycle: Opposing Cast Shadow & 1px Hollow Concentric Ripple (6 FPS)')
    lua_lines.append('')
    lua_lines.append('local width = 48')
    lua_lines.append('local height = 48')
    lua_lines.append('local fps = 6')
    lua_lines.append('local frameDuration = 1.0 / fps')
    lua_lines.append('')
    lua_lines.append('local sprite = Sprite(width, height, ColorMode.RGB)')
    lua_lines.append('local layer = sprite.layers[1]')
    lua_lines.append('layer.name = "Main"')
    lua_lines.append('sprite.frames[1].duration = frameDuration')
    lua_lines.append('local image = sprite.cels[1].image')
    lua_lines.append('')
    lua_lines.append('-- 1. Palette: Terraria Heavy Shading with Opposing Shadows & Magic Firefly OSL')
    lua_lines.append('local PALETTE = {')
    lua_lines.append('    ["."] = nil,')
    lua_lines.append('    ["#"] = "#100e14", -- Terraria viền sẫm tối')
    lua_lines.append('    ["S"] = "#120e18", -- Opposing cast shadow (Alpha 140)')
    lua_lines.append('    ["A"] = "#8a92a2", -- P1: Đá cọc sáng (Slate highlight)')
    lua_lines.append('    ["B"] = "#525866", -- P2: Đá cọc nền (Slate midtone)')
    lua_lines.append('    ["C"] = "#2a2e38", -- P3: Đá cọc tối (Slate shadow)')
    lua_lines.append('    ["D"] = "#72b036", -- M1: Rêu sáng (Vibrant moss highlight)')
    lua_lines.append('    ["E"] = "#3e6e22", -- M2: Rêu tối (Deep moss green)')
    lua_lines.append('    ["F"] = "#422b1c", -- E1: Đất bùn đầm lầy (Swamp peat soil)')
    lua_lines.append('    ["G"] = "#24160c", -- E2: Bùn rãnh tối (Dark mud crevice)')
    lua_lines.append('    ["H"] = "#5ee0e8", -- W1: Gợn sóng rỗng 1px / Giọt sương (Hollow ripple / Dewdrop)')
    lua_lines.append('    ["I"] = "#1b3a3e", -- W2: Mặt nước đầm lầy (Murky swamp water surface)')
    lua_lines.append('    ["J"] = "#0e1e22", -- W3: Vùng nước sâu đầm lầy (Deep water pool)')
    lua_lines.append('    ["K"] = "#ffffff", -- F0: Lõi đom đóm trắng chói (Firefly white-hot core)')
    lua_lines.append('    ["L"] = "#42f5d7", -- F1: Vầng sáng cyan đom đóm (Firefly cyan aura)')
    lua_lines.append('    ["N"] = "#50d4b8", -- O1: Hắt sáng OSL đá rực (OSL stone highlight)')
    lua_lines.append('    ["O"] = "#287a6c"  -- O2: Hắt sáng OSL đá ấm (OSL stone midtone)')
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
        "Frame 1: Đom đóm TRÊN-TRÁI -> Bóng đổ cọc đá ngả dài sang PHẢI (X_bóng > X_cọc)",
        "Frame 2: Đom đóm ĐỈNH CỌC (GIỮA) -> Bóng đổ thu ngắn ngay dưới chân cọc",
        "Frame 3: Đom đóm TRÊN-PHẢI -> Bóng đổ ngả dài sang TRÁI (X_bóng < X_cọc) + Giọt sương rơi",
        "Frame 4: Đom đóm lùi nhẹ về tâm -> Gợn sóng ellipse RỖNG RUỘT 1px lan tỏa trên mặt nước"
    ]

    for f_idx, fr in enumerate(perfect_frames):
        grid_var = f"f{f_idx + 1}_grid"
        lua_lines.append(f"-- 3.{f_idx + 1}. {descriptions[f_idx]}")
        lua_lines.append(f"local {grid_var} = {{")
        for y in range(H):
            row_str = "".join(CODE_MAP[fr[y][x]] for x in range(W))
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
    lua_lines.append('sprite:saveCopyAs("output/aseprite/mossy_pillar_firefly_48.aseprite")')
    lua_lines.append('sprite:saveCopyAs("output/gif/mossy_pillar_firefly_48.gif")')
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
    lua_lines.append('sheetSprite:saveCopyAs("output/Sheet/mossy_pillar_firefly_48_sheet.png")')
    lua_lines.append('sheetSprite:close()')
    lua_lines.append('')

    output_path = "scripts/mossy_pillar_firefly_48.lua"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lua_lines))
    print(f"Generated {output_path} successfully ({len(lua_lines)} lines).")

if __name__ == "__main__":
    generate_lua()
