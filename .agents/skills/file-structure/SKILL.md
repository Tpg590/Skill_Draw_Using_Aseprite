---
name: file-structure
description: >-
  Quy chuẩn cấu trúc thư mục bắt buộc cho AI trong dự án Pixel Art: phân loại
  output (Sheet, gif, aseprite), mã nguồn python, ảnh preview test, và script Lua.
---

# 📁 Quy Chuẩn Cấu Trúc Thư Mục Dự Án Pixel Art

Kỹ năng này quy định cách phân chia và tổ chức tập tin trong không gian làm việc. Mọi thao tác tạo file mã nguồn, file script, ảnh kết quả và ảnh thử nghiệm đều bắt buộc tuân theo cấu trúc này.

## 1. Sơ Đồ Cây Thư Mục Chuẩn

```text
Skill_Trainning/
├── .agents/
│   ├── rules/
│   │   ├── pixel_art_rules.md                 # Quy tắc mỹ thuật & cấm kỵ cốt lõi
│   │   ├── 2D_physics_spatial_perspective.md  # Quy tắc hình học 3D, nan trụ & góc 3/4
│   │   ├── 2D_physics_optics_lighting.md      # Quy tắc quang học, hắt sáng & phản quang
│   │   ├── 2D_physics_kinematics_motion.md    # Quy tắc động lực học, mắt xích, bóng trục Z
│   │   ├── 2D_physics_impact_mechanics.md     # Quy tắc va chạm sàn, đàn hồi & bản lề
│   │   ├── 2D_physics_material_rendering.md   # Quy tắc chất liệu, tán xạ SSS & nếp rủ
│   │   ├── 2D_physics_fluid_gas_vfx.md        # Quy tắc thủy động học, bọt khí & khói
│   │   ├── 2D_physics_thermal_weathering.md   # Quy tắc bức xạ nhiệt, đóng băng & rỉ sét
│   │   └── 2D_physics_fracture_destruction.md # Quy tắc nứt gỗ, móp kim loại & vỡ kính
│   └── skills/
│       ├── file-structure/
│       │   └── SKILL.md               # Kỹ năng tổ chức thư mục
│       └── aseprite-lua-generator/
│           └── SKILL.md               # Kỹ năng viết script Lua & render CLI
├── output/
│   ├── Sheet/                         # Chứa Spritesheet (_sheet.png) hoặc PNG tĩnh
│   ├── gif/                           # Chứa ảnh động (.gif)
│   └── aseprite/                      # Chứa file source Aseprite (.aseprite)
├── scripts/                           # Chứa file script Aseprite Lua (.lua)
├── python/                            # Chứa mã nguồn Python tính toán (.py)
├── test/                              # Chứa ảnh preview, test trung gian (.png, *.gif)
├── run_draw.bat                       # Script CLI gọi Aseprite thực thi
└── Readme.md
```

## 2. Quy Định Phân Tuyến Tập Tin
1. **`output/Sheet/`**: Chứa `output/Sheet/<ten_file>_sheet.png` (dải ngang) hoặc `output/Sheet/<ten_file>.png` (ảnh tĩnh).
2. **`output/gif/`**: Chứa `output/gif/<ten_file>.gif` render từ chu kỳ animation.
3. **`output/aseprite/`**: Chứa `output/aseprite/<ten_file>.aseprite` lưu trữ đầy đủ layers và cels.
4. **`scripts/`**: Chứa `scripts/<ten_file>.lua`.
5. **`python/`**: Toàn bộ file Python tiền xử lý hoặc tính toán ma trận pixel bắt buộc đặt tại `python/<ten_script>.py`. CẤM để file `.py` ở thư mục gốc.
6. **`test/`**: Toàn bộ ảnh preview test từ Python bắt buộc lưu tại `test/<ten_anh>.png`. CẤM để ảnh test ở thư mục gốc.
