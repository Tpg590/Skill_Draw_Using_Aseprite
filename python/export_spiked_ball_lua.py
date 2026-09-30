import os
from perfect_interlock_swing import frames, W, H

lua_script_path = "scripts/swinging_spiked_ball_48.lua"
os.makedirs("scripts", exist_ok=True)

lua_lines = []
lua_lines.append('-- scripts/swinging_spiked_ball_48.lua')
lua_lines.append('-- 48x48 Stardew Valley Animated Swinging Spiked Ball on Interlocking 4-Link Chain (6 FPS)')
lua_lines.append('-- 4 Frames Cycle: Swing Left -> Passing Center (C-curve Follow-Through) -> Swing Right -> Return Center (Inverted C-curve)')
lua_lines.append('-- Strict Technical Requirements: Follow-Through chain inertia, Locked Pivot Point (24, 7), 10 o\'clock static highlight')
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
lua_lines.append('-- 1. Palette: Stardew Valley Warm & Soft Palette (NO #000000!)')
lua_lines.append('local PALETTE = {')
lua_lines.append('    ["."] = nil,')
lua_lines.append('    ["S"] = "#26182c", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)')
lua_lines.append('    ["#"] = "#261e2c", -- Viền sẫm nâu tím ấm mềm (Soft dark purple-charcoal outline, NO #000000!)')
lua_lines.append('    ["H"] = "#d8e2ea", -- Điểm phản quang 10h & gờ sáng bạc (10 o\'clock Specular Glint)')
lua_lines.append('    ["A"] = "#9aa6b6", -- Sắt xám sáng ấm (Lit metal highlight)')
lua_lines.append('    ["B"] = "#626e80", -- Thân sắt xám chính (Metal body midtone)')
lua_lines.append('    ["C"] = "#384050", -- Hốc rãnh bóng tối kim loại (Metal deep shadow / crevice)')
lua_lines.append('    ["K"] = "#a49486", -- Đá xà ngang sáng (Warm stone beam highlight)')
lua_lines.append('    ["G"] = "#766658", -- Đá xà ngang màu chính (Stone beam midtone)')
lua_lines.append('    ["M"] = "#483c34"  -- Vùng tối xà đá (Stone beam shadow)')
lua_lines.append('}')
lua_lines.append('')
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

descriptions = [
    "Frame 1: Swing Left - Quả cầu gai vung sang cực đại bên TRÁI, chuỗi 4 mắt xích uốn nhẹ sang trái",
    "Frame 2: Passing Center / Follow-Through - Móc treo và 2 mắt xích trên đã về giữa, quả cầu và mắt xích dưới trễ nhịp tạo chữ C mềm",
    "Frame 3: Swing Right - Quả cầu gai vung sang cực đại bên PHẢI, chuỗi 4 mắt xích căng sang phải",
    "Frame 4: Return Center - Quả cầu lắc ngược lại về giữa, chuỗi mắt xích uốn theo chiều ngược lại (chữ C ngược)"
]

for f_idx, fr in enumerate(frames):
    grid_var = f"frame{f_idx + 1}_grid"
    lua_lines.append(f"-- 3.{f_idx + 1}. {descriptions[f_idx]}")
    lua_lines.append(f"local {grid_var} = {{")
    for y in range(H):
        row_str = "".join(fr[y][x] for x in range(W))
        comma = "," if y < H - 1 else ""
        lua_lines.append(f'    "{row_str}"{comma}')
    lua_lines.append("}")
    lua_lines.append("")

lua_lines.append("local all_frames = { frame1_grid, frame2_grid, frame3_grid, frame4_grid }")
lua_lines.append("")
lua_lines.append("-- 4. Render các frame hoạt ảnh")
lua_lines.append("for i = 1, #all_frames do")
lua_lines.append("    if i > 1 then")
lua_lines.append("        sprite:newFrame()")
lua_lines.append("        sprite.frames[i].duration = frameDuration")
lua_lines.append("    end")
lua_lines.append("    local curImage = layer:cel(i).image")
lua_lines.append("    renderGrid(curImage, all_frames[i], PALETTE)")
lua_lines.append("end")
lua_lines.append("")
lua_lines.append("-- 5. Xuất file CLI theo đúng quy chuẩn Workspace")
lua_lines.append('sprite:saveCopyAs("output/aseprite/swinging_spiked_ball_48.aseprite")')
lua_lines.append("if #sprite.frames > 1 then")
lua_lines.append('    sprite:saveCopyAs("output/gif/swinging_spiked_ball_48.gif")')
lua_lines.append("    local totalFrames = #sprite.frames")
lua_lines.append("    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)")
lua_lines.append("    local sheetImage = sheetSprite.cels[1].image")
lua_lines.append("    for i = 1, totalFrames do")
lua_lines.append("        local frameCel = layer:cel(i)")
lua_lines.append("        if frameCel then")
lua_lines.append("            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))")
lua_lines.append("        end")
lua_lines.append("    end")
lua_lines.append('    sheetSprite:saveCopyAs("output/Sheet/swinging_spiked_ball_48_sheet.png")')
lua_lines.append("    sheetSprite:close()")
lua_lines.append("else")
lua_lines.append('    sprite:saveCopyAs("output/Sheet/swinging_spiked_ball_48.png")')
lua_lines.append("end")
lua_lines.append("")

with open(lua_script_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lua_lines))

print(f"Exported Lua script successfully to {lua_script_path} ({len(lua_lines)} lines)")
