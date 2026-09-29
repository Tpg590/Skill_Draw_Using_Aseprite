---
name: file-structure
description: >-
  Quy chuẩn cấu trúc thư mục bắt buộc cho AI trong dự án Pixel Art: phân loại
  output (Sheet, gif, aseprite), mã nguồn python, ảnh preview test, và script Lua.
---

# 📁 Quy Chuẩn Cấu Trúc Thư Mục Dự Án Pixel Art

Kỹ năng này quy định cách phân chia và tổ chức tập tin trong không gian làm việc. Mọi thao tác tạo file mã nguồn, file script, ảnh kết quả và ảnh thử nghiệm đều bắt buộc tuân theo cấu trúc này.

---

## 1. Sơ Đồ Cây Thư Mục Chuẩn

```
Skill_Trainning/
├── .agent/
│   ├── rules/
│   │   └── pixel_art.md               # Quy chuẩn nghệ thuật và thông số kỹ thuật
│   └── skills/
│       └── file-structure/
│           └── SKILL.md               # Kỹ năng định hướng cấu trúc thư mục
├── output/
│   ├── Sheet/                         # Chứa tất cả Spritesheet (*_sheet.png) hoặc ảnh PNG tĩnh
│   ├── gif/                           # Chứa tất cả file ảnh động (*.gif)
│   └── aseprite/                      # Chứa tất cả file source Aseprite (*.aseprite)
├── scripts/                           # Chứa toàn bộ file kịch bản Aseprite Lua (*.lua)
├── python/                            # Chứa toàn bộ file mã nguồn Python (*.py)
├── test/                              # Chứa toàn bộ ảnh preview, ảnh test trung gian (*.png, *.gif)
├── run_draw.bat                       # Script CLI gọi Aseprite thực thi mã Lua
└── Readme.md
```

---

## 2. Quy Định Chi Tiết Từng Thư Mục

### A. Thư mục `output/` (Chia làm 3 folder con)
Tuyệt đối không lưu file rời trực tiếp dưới `output/`. Tất cả file xuất ra từ Aseprite CLI phải đi vào đúng 3 thư mục con:
1. **`output/Sheet/`**:
   * Chứa các dải Spritesheet nằm ngang: `output/Sheet/<ten_file>_sheet.png`.
   * Chứa ảnh PNG thành phẩm đơn lẻ nếu là asset dạng Static: `output/Sheet/<ten_file>.png`.
2. **`output/gif/`**:
   * Chứa ảnh động dạng GIF được render từ chu kỳ animation: `output/gif/<ten_file>.gif`.
3. **`output/aseprite/`**:
   * Chứa file gốc của Aseprite lưu giữ layers và frames: `output/aseprite/<ten_file>.aseprite`.

### B. Thư mục `scripts/`
* Chứa toàn bộ mã nguồn script Aseprite Lua độc lập: `scripts/<ten_file>.lua`.
* Trong mã Lua, hàm xuất file bắt buộc trỏ tới đúng 3 thư mục con của `output/`:
  ```lua
  sprite:saveCopyAs("output/aseprite/<ten_file>.aseprite")
  if #sprite.frames > 1 then
      sprite:saveCopyAs("output/gif/<ten_file>.gif")
      -- (Tạo dải sheet)
      sheetSprite:saveCopyAs("output/Sheet/<ten_file>_sheet.png")
  else
      sprite:saveCopyAs("output/Sheet/<ten_file>.png")
  end
  ```

### C. Thư mục `python/`
* Tất cả các file mã nguồn Python (`.py`) dùng để tính toán ma trận pixel, kiểm tra dữ liệu, tiền xử lý hoặc sinh mã Lua **bắt buộc phải đặt trong `python/`**:
  * Ví dụ: `python/build_fountain.py`, `python/build_slime.py`, `python/export_tree_lua.py`.
* **CẤM:** Không được tạo file `.py` trực tiếp ở thư mục gốc của dự án.

### D. Thư mục `test/`
* Tất cả các file ảnh preview, ảnh phóng to (2x, 4x), ảnh test trung gian được sinh ra khi chạy script Python để kiểm tra trực quan **bắt buộc phải lưu vào `test/`**:
  * Ví dụ: `test/preview_tree_4x.png`, `test/test_slime_sheet.png`, `test/clean_tree_4x.png`.
* **CẤM:** Không được ném ảnh preview/test vào thư mục gốc hay vào thư mục `output/`.

---

## 3. Quy Trình Làm Việc Tiêu Chuẩn Cho AI

1. **Khởi tạo / Tính toán bằng Python:**
   * Tạo script tại `python/<ten_script>.py`.
   * Khi render ảnh preview kiểm tra, lưu vào `test/<ten_anh_preview>.png`.
2. **Xuất kịch bản Lua:**
   * Tạo file tại `scripts/<ten_asset>.lua`.
   * Cấu hình đường dẫn xuất file trong script đúng 3 thư mục: `output/aseprite/`, `output/gif/`, `output/Sheet/`.
3. **Thực thi Aseprite CLI:**
   * Chạy lệnh `.\run_draw.bat scripts\<ten_asset>.lua`.
   * Kiểm tra kết quả tại `output/aseprite/`, `output/gif/`, `output/Sheet/`.
