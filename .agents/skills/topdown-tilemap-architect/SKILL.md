---
name: topdown-tilemap-architect
description: >-
  Chuyên gia thiết kế bộ Tilemap, Autotile kết nối địa hình liền mạch chuẩn góc
  nhìn Top-Down 3/4 (vách đá, bãi cỏ, mặt nước, hầm ngục) cho Game Engine (Godot,
  Unity). Kích hoạt khi nhắc tới tilemap, tileset, autotile, địa hình, vách núi,
  bờ sông, dungeon tile.
---

# 🗺️ Top-Down Tilemap & Autotile Architect Skill

Kỹ năng chuyên biệt hướng dẫn AI thiết kế bộ Tilemap, Autotile và Tileset địa hình kết nối liền mạch (Seamless Autotile) theo chuẩn góc nhìn Top-Down 3/4 cho các Game Engine (Godot, Unity, Defold).

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu người dùng khai báo kích thước cụ thể trong prompt (`16x16`, `24x24`, `32x32`, `48x48`, `64x64`), AI phải dựng ma trận tile theo đúng kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO: Sử dụng kích thước chuẩn công nghiệp `32x32` cho mỗi ô Tile cell.

---

## 2. Quy Chuẩn Ghép Mí Liền Mạch (Seamless Wrapping)
1. **Khớp nối chu kỳ ngang trục X (Horizontal Wrapping):**
   * BẮT BUỘC: Cột pixel đầu tiên bên trái ($X = 1$) phải trùng khớp 100% về cao độ đường nét và mã màu với cột cuối cùng bên phải ($X = W$).
   * TUYỆT ĐỐI CẤM: Để lệch 1px viền hoặc đổi tone màu ở 2 mép khiến khi ghép lặp trên tilemap lộ rõ đường chỉ nối (Visible Seams).
2. **Khớp nối chu kỳ dọc trục Y (Vertical Wrapping cho Floor Tiles):**
   * BẮT BUỘC: Với các tile nền phẳng lặp lại vô tận (sàn đá ngục, mặt nước mở, thảm cỏ rộng), hàng pixel đỉnh ($Y = 1$) phải khớp hoàn hảo với hàng đáy ($Y = H$).
3. **Phân bổ chi tiết ngẫu nhiên (Noise Distribution):**
   * BẮT BUỘC: Giữ diện tích bề mặt chính đồng nhất (chiếm 80% diện tích). Các chi tiết phụ (dăm đá, bụi hoa, vết ố) chỉ chiếm tối đa 15%–20% và phải phân bổ so le, tránh tập trung sát mép biên.
   * TUYỆT ĐỐI CẤM: Đặt chi tiết tương phản quá cao ở góc tile gây hiện tượng ô cờ (Grid Checkerboard Artifact) khi lặp lại trên bản đồ lớn.

---

## 3. Cấu Trúc Cao Độ Vách Núi Top-Down 3/4 (Cliff Elevation)
Mọi vách đá, bờ tường hoặc bậc thềm đứng trong góc nhìn Top-Down 3/4 BẮT BUỘC phân rã thành 3 tầng hình học rõ rệt:

```
[ TẦNG 1: MẶT TRÊN (TOP SURFACE) ] -> Vùng nhân vật đi lại (Walkable, đón sáng)
------------------------------------ -> Gờ viền nhô Overhang (1px rãnh bóng đổ k)
[ TẦNG 2: MẶT ĐỨNG (CLIFF FACE) ]   -> Thành vách dựng đứng (Nén trục Y, rãnh nứt dọc)
------------------------------------ -> Chân vách tiếp xúc nền sàn
[ TẦNG 3: BÓNG TIẾP XÚC (SHADOW) ]  -> Dải bóng tiếp xúc sàn đậm màu 'S'
```

1. **Mặt trên vách (Top/Walkable Surface):**
   * BẮT BUỘC đón sáng trực tiếp từ đỉnh canvas. Dùng dải màu sáng và trung tính (`Light -> Midtone`).
   * Gờ mép đón sáng có vệt phản quang nhẹ 1px trước khi rơi vào mép vách.
2. **Gờ nhô tách tầng (Overhang Edge):**
   * BẮT BUỘC: Mép trên của vách đá phải có gờ nhô rộng hơn thân vách 1px và đổ bóng tối (`1px`) ngay phía dưới gờ để thể hiện chiều sâu nổi.
3. **Mặt đứng vách đá (Cliff Face):**
   * BẮT BUỘC: Nén phối cảnh trục Y. Các vết nứt, thớ nứt đá chạy dọc theo chiều đứng zíc-zắc (nhịp bước `1-2-1` pixel).
   * Dùng tone màu tối nhất của bảng màu đá để tô lòng rãnh nứt.
4. **Chân vách đá chạm sàn (Base Grounding):**
   * BẮT BUỘC: Hàng đáy tiếp xúc sàn của vách đá phải có đường bóng tiếp xúc tối `S` (Alpha 130 hoặc mã màu tối nhất của mặt đất bên dưới).
   * TUYỆT ĐỐI CẤM: Cắt ngang chân vách bằng một đường thẳng lì không có bóng chuyển tiếp.

---

## 4. Bộ Ghép Góc Autotile (Wang Tiles & 16-47 Blob Mapping)
Khi thiết kế bộ Autotile nối giữa 2 chất liệu (Ví dụ: Cỏ $\rightarrow$ Đất hoặc Đất $\rightarrow$ Nước), bắt buộc tuân theo bảng cấu hình 9 ô cơ bản (3x3 Minimal Set) hoặc 16 ô mở rộng:

| Mã Ô Tile | Vị trí / Công năng | Quy chuẩn hình học đường viền |
| :---: | :--- | :--- |
| **Center** | Lòng khối đặc ruột | 100% chất liệu phủ kín, không viền biên |
| **Top** | Viền bờ trên cùng | Đường cong ngang lồi lên trên, bóng đổ 1px xuống dưới |
| **Bottom** | Viền bờ đáy | Chân viền bo tròn răng cưa tự nhiên `1-2-1` |
| **Left / Right** | Viền bờ sườn trái/phải | Dải chuyển tiếp màu sắc 1–2px theo trục đứng |
| **Outer Corners** | 4 góc ngoài (TL, TR, BL, BR) | Bo góc theo nhịp bước `1-1-2-2` hoặc `1-2-3`. TUYỆT ĐỐI CẤM jaggies góc 90° |
| **Inner Corners** | 4 góc thụt trong | Góc khuyết lõm hình bậc thang mịn 1px |

* **Đường viền giao thoa giữa 2 chất liệu:**
  * BẮT BUỘC: Dùng kỹ thuật tỉa răng cưa hữu cơ (Organic Fringe). Cỏ lấn sang đất theo các nhánh dài 2–3px so le. Nước ôm bờ cát bằng đường viền bọt sóng mỏng 1px trắng/cyan.
  * TUYỆT ĐỐI CẤM: Kẻ đường ranh giới thẳng băng như vẽ bằng thước kẻ.

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** Sử dụng cấu trúc từ `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault` (Nhóm đá `l, m, r`, cỏ `N, O, P, Q`, nước `X, Y, Z, 0`).
* **Ví dụ mẫu trích xuất cho Tile cỏ viền vách đá:**
  ```lua
  local PALETTE = {
      ["."] = nil,       -- Trong suốt
      ["k"] = "#2E222F", -- Viền tối rãnh nứt
      ["m"] = "#625565", -- Thân vách đá
      ["l"] = "#3E3546", -- Vùng tối vách
      ["P"] = "#1EBC73", -- Mặt cỏ tươi sáng
      ["O"] = "#239063", -- Cỏ chuyển tiếp
      ["S"] = "#1A1018"  -- Bóng đổ chân vách (Alpha 130)
  }
  ```
