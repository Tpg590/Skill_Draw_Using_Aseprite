# 🎮 Hệ Sinh Thái AI Pixel Art Top-Down 3/4 & Aseprite Automation (Introduction)

> **Bộ khung quy chuẩn kỹ thuật toàn diện nhằm biến AI thành nghệ sĩ Pixel Art Top-Down 3/4 chuyên nghiệp, kiểm soát chính xác 100% từng pixel thông qua ma trận ký tự độc lập và tự động hóa kết xuất bằng CLI.**

---

## 📑 Mục Lục Giới Thiệu
1. [Vấn Đề & Triết Lý Phát Triển](#-1-vấn-đề--triết-lý-phát-triển)
2. [Kiến Trúc 4 Tầng Của Hệ Thống](#-2-kiến-trúc-4-tầng-của-hệ-thống)
3. [9 Bộ Quy Chuẩn Vật Lý & Mỹ Thuật (Rules Engine)](#-3-9-bộ-quy-chuẩn-vật-lý--mỹ-thuật-rules-engine)
4. [9 Kỹ Năng Hoạt Họa & Giải Phẫu Chuyên Biệt (Skills Vault)](#-4-9-kỹ-năng-hoạt-họa--giải-phẫu-chuyên-biệt-skills-vault)
5. [Chuẩn Hóa Bảng Màu & Độc Quyền Bóng Đất (Palette & Shadow)](#-5-chuẩn-hóa-bảng-màu--độc-quyền-bóng-đất-palette--shadow)
6. [Cấu Trúc Thư Mục Toàn Dự Án](#-6-cấu-trúc-thư-mục-toàn-dự-án)
7. [Bắt Đầu Sử Dụng (Quick Start)](#-7-bắt-đầu-sử-dụng-quick-start)

---

## 💡 1. Vấn Đề & Triết Lý Phát Triển

### Vấn đề cố hữu của AI Diffusion (Midjourney, DALL-E, Stable Diffusion):
* **Pixel bị nhòe và không đều lưới (Non-uniform Scaling)**: Ảnh xuất ra là bitmap nội suy, không thể đưa trực tiếp vào engine game.
* **Sai lệch thẩm mỹ nghiêm trọng**: Dithering lộn xộn, viền kép (Double outlines), đường bậc thang gãy (Jaggies), viền đen chết `#000000`.
* **Mất kiểm soát chuyển động & vật lý**: Khi làm hoạt ảnh (Animation), nhân vật bị biến dạng méo mó, tỷ lệ co giãn không bảo toàn thể tích, phụ kiện biến mất giữa chừng.
* **Lơ lửng mất gốc sàn (Ground Floating)**: Không đồng bộ được cao độ trục Z với vệt bóng tiếp xúc trên mặt đất.

### Giải pháp cốt lõi của Hệ Sinh Thái:
1. **Mã Nguồn Ma Trận Ký Tự Đơn (1:1 ASCII Token Matrix)**:
   Mọi khung hình được lập trình cụ thể từng pixel bằng các ký tự phân biệt trong script Lua độc lập. Mỗi ký tự đại diện cho 1 mã màu chuẩn xác.
2. **Cơ Chế Cưỡng Chế 2 Tầng (Rules & Skills)**:
   AI bị ràng buộc tuyệt đối bởi các quy tắc vật lý định lượng (công thức toán học cho Squash & Stretch, nhịp bo cong `1-2-1`, độ nén phối cảnh 3/4).
3. **Tự Động Hóa Kết Xuất (CLI Automation Pipeline)**:
   Thông qua lệnh CLI headless của Aseprite hoặc LibreSprite, file Lua tự động render thành 3 định dạng: **Spritesheet game-ready**, **ảnh động GIF xem trước**, và **file Aseprite gốc** bảo toàn layer/cels.

---

## 🏛️ 2. Kiến Trúc 4 Tầng Của Hệ Thống

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. RULES (Cơ chế cưỡng chế vật lý & thẩm mỹ không thể vi phạm)        │
│    ├── pixel_art_rules.md              (Core Aesthetic & Tỷ lệ chiếm)  │
│    ├── 2D_physics_spatial_perspective  (Phối cảnh 3/4, bệ đá, hướng +Y)│
│    ├── 2D_physics_optics_lighting      (Quang học, OSL, bóng 180°)     │
│    ├── 2D_physics_kinematics_motion    (Quán tính, bóng Z, pha so le)  │
│    ├── 2D_physics_impact_mechanics     (Squash & Stretch, bản lề nắp)  │
│    ├── 2D_physics_material_rendering   (Terminator SSS, kim loại, vảy) │
│    ├── 2D_physics_fluid_gas_vfx        (Meniscus, thắt eo, khói, bọt)  │
│    ├── 2D_physics_thermal_weathering   (Quang phổ nhiệt, rỉ sét, băng) │
│    └── 2D_physics_fracture_destruction (Nứt gỗ, rãnh đá, móp kim loại) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. SKILLS (Thư viện kỹ năng giải phẫu & hoạt họa chuyên sâu)          │
│    ├── topdown-tilemap-architect       (Tilemap 32x32 & Autotile)      │
│    ├── humanoid-character-sprite       (Nhân vật người, Walk Cycle)    │
│    ├── quadruped-beast-animator        (Thú 4 chân, Trotting, Chạy)    │
│    ├── avian-bird-animator             (Chim, Sải cánh, Bay lượn)      │
│    ├── reptile-crawler-animator        (Bò sát, Sóng ngang cột sống)   │
│    ├── marine-aquatic-animator         (Cá, Mực, Bơi lội phản lực)     │
│    ├── aseprite-lua-generator          (Khung script Lua API chuẩn)    │
│    ├── color-palette-vault             (Sunset & Resurrect-64 Palette) │
│    └── file-structure                  (Quy chuẩn cây thư mục)         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. SCRIPTS (Mã nguồn Lua độc lập sinh ra ma trận ký tự chuẩn)         │
│    └── scripts/<asset_name>.lua                                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. OUTPUT (Kết xuất Aseprite / LibreSprite CLI qua run_draw.bat)       │
│    ├── output/Sheet/<name>_sheet.png   (Spritesheet dải ngang nạp Game)│
│    ├── output/gif/<name>.gif           (Ảnh động preview đúng FPS)     │
│    └── output/aseprite/<name>.aseprite (File gốc chứa layer và timeline)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ 3. 9 Bộ Quy Chuẩn Vật Lý & Mỹ Thuật (Rules Engine)

Mọi pixel art sinh ra trong hệ thống đều phải tuân thủ nghiêm ngặt 9 bộ quy chuẩn (nằm trong thư mục `.agents/rules/`):

| Tên Bộ Quy Chuẩn | Phạm Vi Kiểm Soát & Nguyên Tắc Cưỡng Chế Cốt Lõi |
| :--- | :--- |
| [pixel_art_rules.md](.agents/rules/pixel_art_rules.md) | **Mỹ thuật cốt lõi:** Bounding Box vật thể chiếm `50%–75%` canvas; Tuyệt đối cấm Banding & Dithering rải hạt; Mái/nắp nhô rộng hơn thân 1–2px (Overhang); Nhịp bo góc đều `1-2-1` không jaggies; Khóa trục tĩnh $Y_{floor}$. |
| [2D_physics_spatial_perspective.md](.agents/rules/2D_physics_spatial_perspective.md) | **Hình học không gian Top-Down 3/4:** Mặt đứng nén `85%–90%`; Hướng vươn ra trước mặt là $+Y$ (hướng chúc xuống); Đáy bục tròn/trụ cong vồng $+Y$; Bóng sàn của vật thể bay là hình ellipse dẹt; Lòng sâu 3D có bóng xiên. |
| [2D_physics_optics_lighting.md](.agents/rules/2D_physics_optics_lighting.md) | **Quang học & Ánh sáng Top-Down 3/4:** Nguồn sáng tự thân hắt sáng OSL; Vành đỡ hắt sáng Rim Lighting; Bóng đổ sàn ngược 180° với nguồn sáng; Khóa vệt phản quang Specular drift trong lòng thể tích; Phản chiếu mặt nước Inverted-Y nén dẹt. |
| [2D_physics_kinematics_motion.md](.agents/rules/2D_physics_kinematics_motion.md) | **Động lực học & Chuyển động:** Cao độ trục Z phải khóa chết hàng bóng tiếp đất `S` trên sàn; Tiếp đất có hoãn xung (Landing Squash); Mắt xích trễ pha chữ S; Bọ máy 4 chân bước so le chéo góc; Loop animation có pha cooldown mượt. |
| [2D_physics_impact_mechanics.md](.agents/rules/2D_physics_impact_mechanics.md) | **Va chạm & Biến dạng đàn hồi:** Bảo toàn thể tích nén giãn $\Delta W \approx -\Delta H \times (W_0/H_0)$; Bản lề nắp mở nén phối cảnh $H_{mở} \approx 40\%-50\% H_{đóng}$; Phụ kiện (khóa, then cài) bảo toàn liên tục không biến mất; Tâm nổ vỡ nằm ở đáy tiếp sàn. |
| [2D_physics_material_rendering.md](.agents/rules/2D_physics_material_rendering.md) | **Chất liệu & Quang học bề mặt:** Kim loại có highlight gắt `#FFFFFF`; Đường Terminator chất hữu cơ/slime có dải bão hòa màu cực đỉnh (Saturation Peak); Pha kéo giãn mỏng trong suốt, pha nén sẫm màu; Vệt sáng dẹt theo trục kéo. |
| [2D_physics_fluid_gas_vfx.md](.agents/rules/2D_physics_fluid_gas_vfx.md) | **Thủy động & Khí động học:** Mặt thoáng Meniscus nghiêng ngược hướng bình; Rỉ chảy phải thắt eo (Neck Pinching) trước khi tách giọt; Gợn sóng nước rỗng ruột 1px; Slime nghỉ hình bánh bao Gumdrop ($H \approx 70\%-80\% W$); Tia sét rãnh zíc-zắc fractal. |
| [2D_physics_thermal_weathering.md](.agents/rules/2D_physics_thermal_weathering.md) | **Nhiệt độ & Phong hóa:** Bức xạ quang phổ nhiệt Blackbody (Trắng vàng $\rightarrow$ Vàng cam $\rightarrow$ Đỏ mận $\rightarrow$ Than đen); Băng đóng gai nhọn chóp trắng; Rỉ sét bám tụ rãnh nối và chân đế ẩm; Bào mòn xói lở mặt đón gió. |
| [2D_physics_fracture_destruction.md](.agents/rules/2D_physics_fracture_destruction.md) | **Cơ học nứt gãy & Biến dạng:** Thớ nứt gỗ dọc theo vân có dăm xơ 1px; Rãnh nứt đá zíc-zắc 1-2-1 cấm dithering; Mảnh kính vỡ tam giác nhọn có chóp trắng; Khuyết móp đường biên (Perimeter Notch); Kim loại dày bị móp méo lõm khối. |

---

## 🧰 4. 9 Kỹ Năng Hoạt Họa & Giải Phẫu Chuyên Biệt (Skills Vault)

Các kỹ năng (nằm tại `.agents/skills/`) đóng vai trò như các cẩm nang giải phẫu và hoạt ảnh chuyên biệt:

1. **[topdown-tilemap-architect](.agents/skills/topdown-tilemap-architect/SKILL.md)**: Thiết kế bộ địa hình (Grid 32x32), Autotile 47 mảnh, vách núi, mép cỏ chồng lấn, bờ nước trong suốt.
2. **[humanoid-character-sprite](.agents/skills/humanoid-character-sprite/SKILL.md)**: Giải phẫu nhân vật người (Grid 32x32 / 48x48), chu kỳ bước đi (Walk Cycle 4–8 frames), Idle thở, đánh tay ngược pha.
3. **[quadruped-beast-animator](.agents/skills/quadruped-beast-animator/SKILL.md)**: Hoạt họa động vật 4 chân (chó, sói, ngựa, gấu), bước chạy Trot so le chéo góc, khớp gập chữ Z chân sau, bờm cổ trễ pha.
4. **[avian-bird-animator](.agents/skills/avian-bird-animator/SKILL.md)**: Hoạt họa loài chim (quạ, đại bàng), cơ học sải cánh, đập cánh tạo lực đẩy nâng thân $-Y$, đuôi lái điều hướng.
5. **[reptile-crawler-animator](.agents/skills/reptile-crawler-animator/SKILL.md)**: Hoạt họa loài bò sát (thằn lằn, cá sấu, rắn), chân choãi ngang, bụng quét sát sàn, sóng uốn lượn ngang hình sin.
6. **[marine-aquatic-animator](.agents/skills/marine-aquatic-animator/SKILL.md)**: Hoạt họa sinh vật thủy sinh (cá, mực), khoang áo co bóp phụt nước phản lực, vây ngực giữ thăng bằng.
7. **[aseprite-lua-generator](.agents/skills/aseprite-lua-generator/SKILL.md)**: Cấu trúc bộ khung script Lua API chuẩn, hàm render ma trận ký tự `renderGrid()`, tự động xuất 3 thư mục `output/`.
8. **[color-palette-vault](.agents/skills/color-palette-vault/SKILL.md)**: Tra cứu nhanh bảng màu Sunset (20 màu) & Resurrect-64 (64 màu), dải ánh xạ 1 ký tự phân biệt.
9. **[file-structure](.agents/skills/file-structure/SKILL.md)**: Quy chuẩn đường dẫn, tổ chức thư mục đầu ra và quản lý tài nguyên.

---

## 🎨 5. Chuẩn Hóa Bảng Màu & Độc Quyền Bóng Đất (Palette & Shadow)

Hệ thống quy định nghiêm ngặt về bảng ánh xạ Palette để tránh lỗi hiển thị:

* **Ký tự `.`**: Đại diện cho khoảng trống trong suốt (`nil`).
* **Ký tự `S` — TỪ KHÓA ĐỘC QUYỀN TOÀN HỆ THỐNG**:
  * Được gán cố định cho **Bóng Đổ Tiếp Đất (Ground Contact Shadow)**.
  * Trong hàm render của [aseprite-lua-generator](.agents/skills/aseprite-lua-generator/SKILL.md), dòng lệnh sau tự động áp đặt:
    ```lua
    local a = (char == "S") and 130 or 255
    ```
    Toàn bộ pixel mang ký tự `S` sẽ có độ trong suốt **Alpha 130** mềm mại, ôm khít mặt sàn.
* **Mã màu Rêu than `#313638`**:
  * Đã được chuẩn hóa gán cho ký tự sóng `~` trong [Resurrect-64 Palette](.agents/skills/color-palette-vault/SKILL.md). Ký tự này có độ mờ đục đầy đủ (**Alpha 255**), đảm bảo thực vật và rêu đá không bị biến thành bóng mờ xuyên thấu.

---

## 📁 6. Cấu Trúc Thư Mục Toàn Dự Án

```text
Skill_Trainning/
├── .agents/
│   ├── rules/                          # 9 Bộ quy chuẩn vật lý & thẩm mỹ bắt buộc
│   │   ├── pixel_art_rules.md
│   │   ├── 2D_physics_spatial_perspective.md
│   │   ├── 2D_physics_optics_lighting.md
│   │   ├── 2D_physics_kinematics_motion.md
│   │   ├── 2D_physics_impact_mechanics.md
│   │   ├── 2D_physics_material_rendering.md
│   │   ├── 2D_physics_fluid_gas_vfx.md
│   │   ├── 2D_physics_thermal_weathering.md
│   │   └── 2D_physics_fracture_destruction.md
│   └── skills/                         # 9 Thư mục kỹ năng chuyên sâu
│       ├── topdown-tilemap-architect/
│       ├── humanoid-character-sprite/
│       ├── quadruped-beast-animator/
│       ├── avian-bird-animator/
│       ├── reptile-crawler-animator/
│       ├── marine-aquatic-animator/
│       ├── aseprite-lua-generator/
│       ├── color-palette-vault/
│       └── file-structure/
├── output/                             # Thư mục chứa thành phẩm sau render
│   ├── Sheet/                          # Spritesheet dải ngang cho Game Dev (.png)
│   ├── gif/                            # Hoạt ảnh GIF xem trước chuẩn FPS (.gif)
│   └── aseprite/                       # File Aseprite gốc bảo toàn layer/cels (.aseprite)
├── python/                             # Công cụ kiểm tra, phân tích & render Python
├── scripts/                            # Thư mục chứa mã nguồn Lua AI sinh ra (.lua)
├── Instruction.md                      # Hướng dẫn sử dụng & Cấu hình đường dẫn app
├── Readme.md                           # File giới thiệu tổng quan hệ thống (Introduction)
└── run_draw.bat                        # Script thực thi CLI render tự động trên Windows
```

---

## 🚀 7. Bắt Đầu Sử Dụng (Quick Start)

Để bắt đầu tạo asset ngay lập tức hoặc tìm hiểu cách chỉnh sửa đường dẫn phần mềm Aseprite / LibreSprite:

👉 **Vui lòng đọc tài liệu hướng dẫn chi tiết tại: [Instruction.md](Instruction.md)**

Nội dung trong [Instruction.md](Instruction.md) bao gồm:
* Quy trình chi tiết 4 bước từ Prompt đến Thành phẩm.
* Hướng dẫn đổi đường dẫn Aseprite / chuyển sang LibreSprite trong [run_draw.bat](run_draw.bat).
* Hướng dẫn phương án render bằng Python thuần (không cần cài phần mềm đồ họa).
* Thư viện 9 Prompt mẫu tối ưu cho Hiệp sĩ, Sói, Chim, Bò sát, Slime, Búa sấm sét, Lửa băng, Vách đá...
* Bảng tra cứu và xử lý mọi sự cố thường gặp.