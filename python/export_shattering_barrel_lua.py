import os
from perfect_shattering_barrel import frames, W, H

lua_script_path = "scripts/shattering_wine_barrel_48.lua"
os.makedirs("scripts", exist_ok=True)

lua_lines = []
lua_lines.append('-- scripts/shattering_wine_barrel_48.lua')
lua_lines.append('-- 48x48 Terraria Animated Shattering Wine Barrel (Oak Wood & Iron Bands with Rivets)')
lua_lines.append('-- 4 Frames Cycle: Squash & Crack -> Ground-Up Rupture -> Parabolic Trajectory -> Settled Debris (8 FPS)')
lua_lines.append('-- Strictly complies with Rules 4.1 (Ground-Up Impact vs Radial Bomb) and 4.2 (Anchored Iron Bands & Rivets)')
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
lua_lines.append('-- 1. Palette: Terraria High Contrast Oak Wood & Iron Metal Palette')
lua_lines.append('local PALETTE = {')
lua_lines.append('    ["."] = nil,')
lua_lines.append('    ["#"] = "#160c08", -- Viền sẫm gần đen (Terraria dark pitch outline)')
lua_lines.append('    ["S"] = "#140a18", -- Bóng tiếp đất mềm mại (Ground contact shadow, alpha 130)')
lua_lines.append('    ["A"] = "#e6a44c", -- Ván sồi sáng (Oak lit highlight grain)')
lua_lines.append('    ["B"] = "#9e5c26", -- Thân gỗ sồi ấm (Oak rich warm body)')
lua_lines.append('    ["C"] = "#4a220c", -- Rãnh bóng tối / nứt gỗ (Oak deep crevice shadow)')
lua_lines.append('    ["H"] = "#e4edf4", -- Đinh tán sáng bạc (Rivet glint & Iron highlight)')
lua_lines.append('    ["I"] = "#7e8c9c", -- Thân đai sắt (Metallic iron band midtone)')
lua_lines.append('    ["J"] = "#343c48", -- Rãnh bóng tối đai sắt (Iron crevice shadow)')
lua_lines.append('    ["W"] = "#ac142c", -- Rượu vang đỏ (Crimson red wine)')
lua_lines.append('    ["V"] = "#4c0612"  -- Vũng rượu sẫm (Dark wine puddle shadow)')
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
    "Frame 1: Pre-Impact - Đáy thùng vừa chạm mặt sàn đá, thân nén dẹp nhẹ Squash, nứt từ đáy",
    "Frame 2: Ground-Up Rupture - Đáy thùng đập nát bẹp dí toác ngang 2 bên sàn, nắp và thành trên văng bổng ngược lên hình vòm",
    "Frame 3: Parabolic Trajectory - Mảnh ván thành thùng và nắp bay bổng lên cao nhất theo hình vòm parabol",
    "Frame 4: Settled Debris - Toàn bộ mảnh gỗ rơi nằm yên trên sàn, mỗi mảnh có bóng râm 'S' nhỏ bên dưới"
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
lua_lines.append("-- 5. Xuất file CLI (Tuân thủ cấu trúc Workspace chuẩn)")
lua_lines.append('sprite:saveCopyAs("output/aseprite/shattering_wine_barrel_48.aseprite")')
lua_lines.append("if #sprite.frames > 1 then")
lua_lines.append('    sprite:saveCopyAs("output/gif/shattering_wine_barrel_48.gif")')
lua_lines.append("    local totalFrames = #sprite.frames")
lua_lines.append("    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)")
lua_lines.append("    local sheetImage = sheetSprite.cels[1].image")
lua_lines.append("    for i = 1, totalFrames do")
lua_lines.append("        local frameCel = layer:cel(i)")
lua_lines.append("        if frameCel then")
lua_lines.append("            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))")
lua_lines.append("        end")
lua_lines.append("    end")
lua_lines.append('    sheetSprite:saveCopyAs("output/Sheet/shattering_wine_barrel_48_sheet.png")')
lua_lines.append("    sheetSprite:close()")
lua_lines.append("else")
lua_lines.append('    sprite:saveCopyAs("output/Sheet/shattering_wine_barrel_48.png")')
lua_lines.append("end")
lua_lines.append("")

with open(lua_script_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lua_lines))

print(f"Exported Lua script to {lua_script_path} ({len(lua_lines)} lines)")
