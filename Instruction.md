# 📖 Hướng Dẫn Sử Dụng & Cấu Hình Môi Trường (System Instruction)

Tài liệu này cung cấp hướng dẫn toàn diện từ cách ra lệnh (prompting), quy trình kết xuất tự động, đến cách cấu hình đường dẫn phần mềm Aseprite, LibreSprite hoặc các công cụ thay thế.

---

## 📑 Mục Lục
1. [Quy Trình Tạo Asset Từ Prompt Đến Thành Phẩm](#1-quy-trình-tạo-asset-từ-prompt-đến-thành-phẩm)
2. [Cấu Hình Đường Dẫn Ứng Dụng (Aseprite, LibreSprite & Tùy Biến)](#2-cấu-hình-đường-dẫn-ứng-dụng)
   - [Trường hợp 1: Aseprite Cài Ở Thư Mục Khác](#trường-hợp-1-aseprite-cài-ở-thư-mục-khác)
   - [Trường hợp 2: Sử Dụng LibreSprite (Mã Nguồn Mở Miễn Phí)](#trường-hợp-2-sử-dụng-libresprite-mã-nguồn-mở-miễn-phí)
   - [Trường hợp 3: Thêm Aseprite / LibreSprite Vào Biến Môi Trường (System PATH)](#trường-hợp-3-thêm-vào-system-path)
   - [Trường hợp 4: Kết Xuất Bằng Python Thuần (Không Cần Aseprite)](#trường-hợp-4-kết-xuất-bằng-python-thuần-không-cần-aseprite)
   - [Trường hợp 5: Chạy Trên Linux / macOS](#trường-hợp-5-chạy-trên-linux--macos)
3. [Thư Viện Prompt Mẫu Cho 9 Nhóm Đối Tượng](#3-thư-viện-prompt-mẫu-cho-9-nhóm-đối-tượng)
4. [Xử Lý Sự Cố Thường Gặp (Troubleshooting)](#4-xử-lý-sự-cố-thường-gặp-troubleshooting)

---

## 🚀 1. Quy Trình Tạo Asset Từ Prompt Đến Thành Phẩm

Quy trình phát triển đồ họa trong hệ thống diễn ra khép kín qua 4 bước:

```
[Prompt Yêu Cầu] ──► [AI Kích Hoạt Skill + Rules] ──► [Mã Nguồn scripts/<tên>.lua] ──► [Chạy run_draw.bat] ──► [Thư Mục output/]
```

### Bước 1: Gửi Prompt Có Đủ 5 Thông Số Kỹ Thuật
Khi yêu cầu AI vẽ sprite hoặc hoạt ảnh, bạn chỉ cần cung cấp đủ 5 tham số định lượng:
* **Grid Size**: `16x16`, `32x32`, `48x48`, `64x64` (hoặc tùy biến 16–64).
* **Art Style**: `Terraria` (viền đen dày, gồ ghề), `Stardew Valley` (viền mềm, ấm áp), hoặc `FreeStyle` (Hue-shifting hiện đại).
* **Asset Type**: `Individual Sprite`, `Tilemap`, hoặc `Spritesheet`.
* **Output Type**: `Static` (tĩnh) hoặc `Animation` (hoạt ảnh).
* **Animation FPS**: `4`, `6`, `8`, `12`, `16`, `24` (Mặc định: `8`).

### Bước 2: AI Tự Động Sinh Script Lua Độc Lập
AI sẽ tự động đối chiếu các bộ luật vật lý (`rules/`) và kỹ năng chuyên biệt (`skills/`) để sinh ra file script hoàn chỉnh tại thư mục:
```text
scripts/<ten_file>.lua
```
Trong đó, toàn bộ hình ảnh được biểu diễn bằng **ma trận ký tự 1:1** và bảng màu `PALETTE` trích xuất từ [color-palette-vault](.agents/skills/color-palette-vault/SKILL.md).

### Bước 3: Chạy Lệnh Render Bằng File Batch
Mở Terminal / PowerShell tại thư mục gốc của project và gõ:
```powershell
.\run_draw.bat scripts\<ten_file>.lua
```
*Ví dụ thực tế:*
```powershell
.\run_draw.bat scripts\purple_acid_slime.lua
.\run_draw.bat scripts\warhammer_shockwave_impact.lua
```

### Bước 4: Nhận Thành Phẩm Tại Thư Mục `output/`
Hệ thống tự động phân loại và xuất đủ 3 định dạng:
1. `output/Sheet/<ten_file>_sheet.png`: Spritesheet dạng dải ngang, nạp trực tiếp vào Unity (Sprite Editor), Godot (`AnimatedSprite2D`), Unreal Engine hoặc GameMaker.
2. `output/gif/<ten_file>.gif`: Ảnh động chạy chuẩn FPS để xem trước và review chuyển động.
3. `output/aseprite/<ten_file>.aseprite`: File gốc bảo toàn các layer, cels, frame duration để bạn mở bằng Aseprite và chỉnh sửa pixel thủ công nếu muốn.

---

## ⚙️ 2. Cấu Hình Đường Dẫn Ứng Dụng

File thực thi kết xuất chính là [run_draw.bat](run_draw.bat). Dưới đây là các phương án chỉnh sửa đường dẫn phù hợp với từng môi trường:

### Trường hợp 1: Aseprite Cài Ở Thư Mục Khác
Mở file [run_draw.bat](run_draw.bat) bằng bất kỳ trình soạn thảo nào, tìm dòng định nghĩa `set ASEPRITE=` và thay bằng đường dẫn thực tế trên máy bạn:

```bat
:: Mặc định (hoặc đường dẫn thực tế của bạn):
set ASEPRITE="C:\Program Files\Aseprite\aseprite.exe"

:: Ví dụ 1: Cài qua Steam mặc định
set ASEPRITE="C:\Program Files (x86)\Steam\steamapps\common\Aseprite\aseprite.exe"

:: Ví dụ 2: Cài vào Program Files (64-bit)
set ASEPRITE="C:\Program Files\Aseprite\aseprite.exe"

:: Ví dụ 3: Bản Portable trên ổ D hoặc E
set ASEPRITE="D:\Tools\Aseprite\aseprite.exe"
```

> [!IMPORTANT]
> **Lưu ý dấu ngoặc kép (`"..."`)**: Nếu đường dẫn chứa khoảng trắng (như `Program Files`), bạn **bắt buộc** phải bọc đường dẫn trong cặp dấu ngoặc kép.

---

### Trường hợp 2: Sử Dụng LibreSprite (Mã Nguồn Mở Miễn Phí)
[LibreSprite](https://libresprite.github.io/) là phần mềm mã nguồn mở hoàn toàn miễn phí, được phân nhánh (fork) trực tiếp từ Aseprite phiên bản mã mở cuối cùng. Giao diện và tập lệnh CLI của LibreSprite tương thích gần như 100% với Aseprite API.

Để sử dụng LibreSprite, sửa dòng `set ASEPRITE=` trong [run_draw.bat](run_draw.bat):

```bat
:: Sửa đường dẫn trỏ tới LibreSprite:
set ASEPRITE="C:\Program Files\LibreSprite\libresprite.exe"

:: Hoặc bản Portable LibreSprite:
set ASEPRITE="D:\Tools\LibreSprite\libresprite.exe"
```

Lệnh thực thi dòng 17 trong file `.bat`:
```bat
%ASEPRITE% -b --script "%~1"
```
vẫn hoạt động hoàn hảo vì LibreSprite hỗ trợ cờ lệnh `-b` (batch/headless mode) và `--script <file.lua>`.

---

### Trường hợp 3: Thêm Vào System PATH
Nếu bạn đã thêm thư mục chứa `aseprite.exe` hoặc `libresprite.exe` vào biến môi trường **PATH** của Windows:
1. Mở file [run_draw.bat](run_draw.bat).
2. Sửa lại ngắn gọn:
```bat
set ASEPRITE=aseprite
:: Hoặc nếu dùng LibreSprite:
:: set ASEPRITE=libresprite
```
Khi đó Windows sẽ tự động tìm kiếm chương trình mà không phụ thuộc vào đường dẫn tuyệt đối.

---

### Trường hợp 4: Kết Xuất Bằng Python Thuần (Không Cần Aseprite)
Nếu máy bạn chưa cài đặt Aseprite hoặc LibreSprite, hệ sinh thái hỗ trợ kết xuất trực tiếp ma trận sang PNG/GIF thông qua Python và thư viện `Pillow` trong thư mục `python/`:

1. Cài đặt thư viện:
```powershell
pip install pillow
```
2. Thư mục `python/` chứa hàng loạt script chuyển đổi ma trận ký tự thành ảnh PNG từng frame, Spritesheet nối dài và file GIF chuyển động.
3. Cấu trúc hàm vẽ ma trận bằng Python tương đương:
```python
from PIL import Image

def render_matrix(matrix, palette, width, height):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char in palette and palette[char] is not None:
                color = palette[char] # Hex hoặc RGBA tuple
                pixels[x, y] = color
    return img
```

---

### Trường hợp 5: Chạy Trên Linux / macOS
Nếu làm việc trên Linux hoặc macOS, bạn có thể tạo file `run_draw.sh` ngay tại thư mục gốc:

```bash
#!/bin/bash
if [ -z "$1" ]; then
    echo "[Lỗi] Vui lòng truyền đường dẫn file lua!"
    echo "Ví dụ: ./run_draw.sh scripts/chest.lua"
    exit 1
fi

# Đường dẫn Aseprite trên Linux/macOS
# Linux: aseprite hoặc /usr/bin/aseprite
# macOS: /Applications/Aseprite.app/Contents/MacOS/aseprite
ASEPRITE="aseprite"

mkdir -p output/aseprite output/gif output/Sheet

echo "Đang vẽ bằng Aseprite CLI..."
"$ASEPRITE" -b --script "$1"
echo "[Xong!] Kiểm tra kết quả tại output/"
```
Cấp quyền thực thi và chạy:
```bash
chmod +x run_draw.sh
./run_draw.sh scripts/purple_acid_slime.lua
```

---

## 🎨 3. Thư Viện Prompt Mẫu Cho 9 Nhóm Đối Tượng

Dưới đây là các mẫu câu lệnh tối ưu đã được kiểm nghiệm, tự động kích hoạt chính xác Skill và bộ quy chuẩn vật lý tương ứng:

### 🏰 Mẫu 1: Bộ Địa Hình & Autotile (Kích hoạt `topdown-tilemap-architect`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 32x32
* Art Style: Stardew Valley
* Asset Type: Tilemap
* Output Type: Static

**Mô tả ý tưởng:**
Một vách núi đá cổ kính bên bờ suối:
Mặt thảm cỏ xanh bên trên có gờ viền nhô rộng (overhang) đổ bóng xuống thành vách đứng. Thành vách có các đường rãnh nứt dọc zigzag nhọn và vết nứt móp cạnh. Chân vách đá chạm bờ nước trong suốt có gợn sóng rỗng ruột và bóng tiếp xúc chân vách S.
```

---

### 🤺 Mẫu 2: Nhân Vật Người Đi Bộ (Kích hoạt `humanoid-character-sprite`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 32x32
* Art Style: Terraria
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một hiệp sĩ mặc giáp bạc bước đi (Walk Cycle hướng Xuống +Y):
Đầu và thân nhấp nhô theo nhịp trùng chân - nhón chân, hai tay và chân đánh so le ngược pha, bóng tiếp đất khóa chết cố định tại mặt sàn bên dưới.
```

---

### 🐺 Mẫu 3: Thú 4 Chân Chạy Trotting (Kích hoạt `quadruped-beast-animator`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: FreeStyle
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một con sói tuyết chạy bước săn mồi:
Chân sau có khớp gập chữ Z, bước so le chéo góc (Trước-Trái đi cùng Sau-Phải), móng chân cắm sàn có đốm bóng tiếp xúc S. Lông bờm cổ nhấp nhô trễ pha quán tính.
```

---

### 🦅 Mẫu 4: Chim Sải Cánh Bay (Kích hoạt `avian-bird-animator`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 32x32
* Art Style: Terraria
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 6

**Mô tả ý tưởng:**
Một con quạ đen đậu cành rồi đập cánh bay vọt lên cao:
Cánh vỗ chúc xuống sinh lực đẩy thân vọt lên (-Y), bóng tiếp đất trên sàn thu nhỏ dần tỉ lệ nghịch với cao độ bay.
```

---

### 🐊 Mẫu 5: Bò Sát Bò Trườn (Kích hoạt `reptile-crawler-animator`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: FreeStyle
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một con kỳ đà sa mạc bò trườn về phía trước:
Bốn chân choãi ngang sườn, bụng quét sát sàn, cột sống và đuôi uốn lượn sóng ngang hình sin liên tục, vảy da nhám tương phản.
```

---

### 🦑 Mẫu 6: Thủy Sinh Biển Bơi Lội (Kích hoạt `marine-aquatic-animator`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: Terraria
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 6

**Mô tả ý tưởng:**
Một con mực nang phát quang đang bơi:
Khoang áo phình to hút nước rồi co siết phụt luồng nước bắn vọt tới, chùm xúc tu duỗi thẳng ra sau sinh bọt khí, sau đó xòe bung mềm mại.
```

---

### 🧪 Mẫu 7: Chất Lỏng, Slime & Hóa Chất (Kích hoạt `2D_physics_fluid_gas_vfx`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: FreeStyle
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một khối slime độc nhảy nảy sàn (Jumping Acid Slime):
Pha nén bẹp tiếp đất (Squash) phình rộng ngang, sẫm màu đáy cản sáng; pha bật cao (Stretch) thân thu hẹp vút cao, dải màu trong suốt bừng sáng. Lõi nhân bên trong trễ pha 1 frame so với vỏ ngoài.
```

---

### 💥 Mẫu 8: Va Chạm Cơ Khí & Nổ Vỡ (Kích hoạt `2D_physics_fracture_destruction`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: Terraria
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một búa chiến nện sấm sét xuống sàn đá (Warhammer Shockwave Impact):
Búa giáng xuống tạo tâm nứt vỡ chân chim tại điểm tiếp sàn Y_floor, gạch vỡ văng parabol lên cao, tia sét rãnh zíc-zắc chói lòa tỏa nhánh phụ.
```

---

### ❄️ Mẫu 9: Nhiệt Độ, Lửa & Băng Giá (Kích hoạt `2D_physics_thermal_weathering`)
```markdown
Tạo asset pixel art bằng script Lua cho Aseprite theo đúng các quy chuẩn hệ thống:

**Thông số kỹ thuật bắt buộc:**
* Grid Size: 48x48
* Art Style: FreeStyle
* Asset Type: Individual Sprite
* Output Type: Animation
* Animation FPS: 8

**Mô tả ý tưởng:**
Một khối lõi cổ thạch ma thuật tỏa năng lượng nhiệt và băng giá (Elemental Frost-Fire Core):
Lõi trung tâm rực lửa tuân thủ dải Blackbody (Trắng vàng #FFFFA0 -> Vàng cam #FF8800 -> Đỏ mận #8B1010 -> Than đen #1A0808) và hắt sáng nhiệt OSL. Nửa đối diện kết tinh gai băng nhọn (Needle Frost) 1-2px viền chóp trắng. Chân bệ đá tiếp sàn có rỉ sét cam sần sùi bám tụ rãnh nứt và bóng tiếp đất S.
```

---

## 🛠️ 4. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

### 1. Lỗi: `'aseprite' is not recognized as an internal or external command`
* **Nguyên nhân**: File `run_draw.bat` trỏ tới đường dẫn không tồn tại hoặc chưa cài Aseprite.
* **Cách sửa**: 
  1. Kiểm tra lại đường dẫn file `.exe` trên máy bạn.
  2. Mở file [run_draw.bat](run_draw.bat), chỉnh lại biến `set ASEPRITE="<đường_dẫn_chính_xác>"`.

### 2. Lỗi: Màu rêu than / thực vật bị mờ xuyên thấu
* **Nguyên nhân**: Đang sử dụng nhầm ký tự `S` cho màu `#313638`. Trong hệ thống, ký tự `S` bị cưỡng chế `Alpha = 130` để làm bóng đất tiếp xúc.
* **Cách sửa**: 
  * Sử dụng ký tự sóng `~` cho màu rêu than `#313638` (được hiển thị với Alpha 255 sắc nét).
  * Chỉ dùng duy nhất ký tự `S` cho đốm bóng đổ tiếp đất.

### 3. Lỗi: Không thấy file tạo ra trong `output/`
* **Nguyên nhân**: Thư mục `output` chưa được tạo hoặc quyền truy cập bị giới hạn.
* **Cách sửa**: File `run_draw.bat` đã tích hợp lệnh tự động tạo các thư mục con `output\aseprite`, `output\gif`, `output\Sheet`. Hãy đảm bảo bạn chạy file batch từ đúng thư mục gốc dự án.

### 4. Lỗi: Aseprite không xuất Spritesheet hoặc GIF
* **Nguyên nhân**: Script Lua thiếu khối lệnh lưu trữ ở cuối file hoặc gọi phương thức không tương thích trên một số phiên bản headless.
* **Cách sửa**: Mọi file script chuẩn đều phải chứa đoạn mã xuất 3 thư mục sử dụng đối tượng `Sprite` theo quy định của [aseprite-lua-generator](.agents/skills/aseprite-lua-generator/SKILL.md):
```lua
sprite:saveCopyAs("output/aseprite/<ten_file>.aseprite")
if #sprite.frames > 1 then
    sprite:saveCopyAs("output/gif/<ten_file>.gif")
    local totalFrames = #sprite.frames
    local sheetSprite = Sprite(width * totalFrames, height, ColorMode.RGB)
    local sheetImage = sheetSprite.cels[1].image
    for i = 1, totalFrames do
        local frameCel = layer:cel(i)
        if frameCel then
            sheetImage:drawImage(frameCel.image, Point((i - 1) * width, 0))
        end
    end
    sheetSprite:saveCopyAs("output/Sheet/<ten_file>_sheet.png")
    sheetSprite:close()
else
    sprite:saveCopyAs("output/Sheet/<ten_file>.png")
end
```
