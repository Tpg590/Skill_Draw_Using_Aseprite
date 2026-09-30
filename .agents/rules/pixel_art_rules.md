---
trigger: always_on
---

# 🎨 2D Pixel Top-Down Core Aesthetic Rules

Tài liệu này là quy chuẩn cưỡng chế bắt buộc đối với mọi pixel art được sinh ra. Mọi sản phẩm đồ họa phải tuân thủ nghiêm ngặt các rào cản kỹ thuật dưới đây.

## 0. Thứ bậc ưu tiên (Hierarchy of Authority)
Mặc định trong hệ thống agent: **File quy tắc chuyên môn sâu luôn ghi đè file khái quát.**
1. **Nguyên tắc ghi đè:** Khi có sự khác biệt giữa quy tắc thẩm mỹ cốt lõi (`pixel_art_rules.md`) và quy tắc chuyên môn sâu (`2D_physics_*.md`), **luật trong file chuyên ngành sở hữu bản quyền vấn đề đó có hiệu lực ưu tiên cao nhất.**
   * *Ví dụ 1 (Độ nhám bề mặt vs Cấm dithering):* Core cấm dithering/rải hạt lấm tấm, nhưng `2D_physics_material_rendering.md` cho phép dùng dăm pixel tối so le để tạo độ nhám vỏ cây/đá thô $\rightarrow$ Áp dụng theo `2D_physics_material_rendering.md`.
   * *Ví dụ 2 (Thang màu quang phổ nhiệt vs Giới hạn Palette):* Core giới hạn palette cơ bản 1 viền + 3 sắc độ + 2 phụ kiện, nhưng `2D_physics_thermal_weathering.md` yêu cầu dải 4 màu quang phổ nhiệt (Blackbody Hue-Shift: Trắng vàng $\rightarrow$ Vàng cam $\rightarrow$ Đỏ mận $\rightarrow$ Than đen) khi kim loại nung nóng phát xạ $\rightarrow$ Áp dụng theo `2D_physics_thermal_weathering.md`.
2. **Quyền sở hữu độc quyền (Exclusive Domain Ownership):** Mỗi hành vi vật lý, chất liệu, hình học chỉ được quy chuẩn tại **DUY NHẤT một file chuyên đề sở hữu bản quyền**. Tuyệt đối không định nghĩa lặp lại chéo giữa các file để bảo toàn dung lượng token và độ tập trung của AI.

## 1. Cấu hình bắt buộc
Mọi yêu cầu tạo sprite/animation phải xác nhận đủ 5 thông số:
*   **Grid Size:** `16x16`, `32x32`, `48x48`, `64x64` (hoặc custom trong dải 16–64, 1 cell/frame).
*   **Art Style:** `Terraria`, `Stardew Valley`, `FreeStyle`.
*   **Asset Type:** `Individual Sprite`, `Tilemap`, `Spritesheet`.
*   **Output Type:** `Static`, `Animation`.
*   **Animation FPS:** `4`, `6`, `8`, `12`, `16`, `24` (Mặc định: `8`).

## 2. Ràng buộc phong cách nghệ thuật
1.  **Terraria:** Khối dày, gồ ghề, tương phản cao. Viền sẫm tối (gần đen) bao quanh toàn bộ khối. Dùng dăm pixel nhỏ tạo độ nhám, rạn nứt bề mặt.
2.  **Stardew Valley:** Tươi sáng, ấm cúng, góc nhìn Top-Down 3/4. Viền ngoài mềm bằng chính tone tối của vật liệu (TUYỆT ĐỐI CẤM viền `#000000`). Bắt buộc có bóng râm tiếp đất (`S`) hình ellipse mờ.
3.  **FreeStyle:** Bắt buộc Hue-shifting (vùng sáng ngả vàng/cam, vùng tối ngả tím/xanh navy). Đường nét sắc sạch, không jaggies.

## 3. Rào cản mỹ thuật & Cấm kỵ tuyệt đối
1.  **CẤM BANDING:** Tuyệt đối không xếp các pixel cùng màu thành hàng/cột song song dọc theo cạnh khối. Sắc độ sáng/tối phải phân bổ so le hoặc uốn lượn tự nhiên.
2.  **GIỚI HẠN PALETTE:** Tối đa 1 màu viền + 3 sắc độ chính (Sáng / Nền / Tối) + 2 màu phụ kiện.
    *   *Ngoại lệ:* Được bổ sung tối đa 3 màu phát quang (vàng kim, cyan, neon) cho kho báu trong lòng hòm hoặc nguồn sáng ma thuật.
3.  **TOÁN HỌC TÁCH KHỐI (OVERHANG):** Nắp rương, mái hiên, vành mũ BẮT BUỘC nhô rộng hơn thân dưới tối thiểu 1–2 pixel mỗi bên và có rãnh bóng tối ngay dưới gờ.
    *   *Công thức:* Thân rộng từ tọa độ $X_1$ đến $X_2$ ($W = X_2 - X_1$) $\rightarrow$ Mái/nắp phải rộng từ $X_1 - 1$ đến $X_2 + 1$ ($W + 2$).
4.  **CĂN ĐÁY (GROUND ALIGNMENT):** Chân đế và bóng râm tiếp đất (`S`) của vật thể tĩnh phải nằm cố định sát mép dưới canvas, cấm vẽ lơ lửng giữa khung hình.
5.  **CẤM JAGGIES (NHỊP BO GÓC):** Bo viền cong phải theo nhịp bước đều (`1-1-2-2` hoặc `1-2-3`). Cấm pixel thừa tạo góc vuông 90 độ lồi ra ngoài. Khi co giãn hình thể (Squash & Stretch), vẫn phải bảo toàn nhịp bước cong này.
6.  **CẤM DITHERING & CÔNG THỨC VÂN GỖ:** Tuyệt đối không xếp pixel chéo caro để lấp mảng trống.
    *   *Vân gỗ:* Ván ngang dùng dải 3–5 pixel, cột dọc dùng dải 2–4 pixel. Đan xen màu có rãnh dọc/ngang (VD: `A A B A A`). Cấm rải hạt lấm tấm.
7.  **CHIỀU SÂU LÒNG KHỐI (3D Interior):**
    *   *Rương mở nắp:* Bắt buộc vẽ thành trong dày 2–3px và đổ bóng xiên từ góc đón sáng xuống đáy.
    *   *Thành bồn chứa chất lỏng:* Mặt trong thành bồn phía trước phải cao hơn mặt chất lỏng và có đường bóng râm đổ xuống mặt nước.
8.  **CẤU TRÚC HỮU CƠ:** Không vẽ cành cây, xúc tu bằng các đường chéo 1-pixel thẳng đuột (góc 45 độ). Thân nhánh phải cong tự nhiên, gốc to và ngọn vuốt nhọn.
9. **TỶ LỆ CHIẾM KHUNG & MẬT ĐỘ CHI TIẾT TỐI THIỂU (CANVAS OCCUPANCY & DETAIL DENSITY):**
   * **Tỷ lệ chiếm khung (Bounding Box):** Khối vật thể chính BẮT BUỘC phải chiếm từ **50% đến 75%** kích thước canvas (VD: Grid 48x48 thì chiều rộng hoặc chiều cao vật thể tối thiểu phải đạt 24–36px). TUYỆT ĐỐI CẤM vẽ vật thể tí hon lọt thỏm (<30% diện tích canvas) gây thiếu đất diễn chi tiết.
   * **Rãnh ghép & Cấu trúc cơ khí (Panels & Rivets):** Mọi vật thể kim loại/máy móc BẮT BUỘC phải có tối thiểu 2 mảng ghép vỏ (Seam lines dày 1px tối màu) và từ 3–4 điểm đinh tán (Rivets 1px tương phản). CẤM vẽ kim loại thành một mảng màu trơn nhẵn như nhựa đồ chơi.
   * **Mặt vát tinh thể & Đá (Faceting & Bevels):** Tinh thể, ngọc, đá quý BẮT BUỘC phải cắt vát thành các diện phẳng góc cạnh (tối thiểu 3–4 mặt vát sáng/tối khác nhau). CẤM vẽ tinh thể uốn cong tròn như viên thuốc hay lon nước ngọt.
   * **Độ nhớt & Hạt chìm thể tích (Internal Particulates):** Chất nhầy hữu cơ/Slime BẮT BUỘC phải có từ 2–3 bọt khí hoặc hạt nhân mờ chìm bên trong lòng thể tích để tạo độ sâu trong suốt.

## 4. Ràng buộc hoạt ảnh cốt lõi
1.  **Khóa trục tĩnh:** Tọa độ Y của bản lề, cột chống tĩnh và bóng tiếp đất (`S`) phải giữ nguyên 100% qua tất cả các frame.
2.  **Động lực học mở nắp:** Nắp ngửa ra sau (thu hẹp chiều cao trục Y của nắp), làm lộ vùng bóng tối sâu nhất dưới đáy.
3.  **Tilemap liền mạch:** Cột pixel đầu tiên bên trái và cột cuối cùng bên phải của một tile lặp phải trùng khớp 100% về cao độ và màu sắc.
4.  **Biên độ biến đổi tối thiểu:** Hoạt ảnh chu kỳ tại chỗ (cháy, sủi bọt, thở) phải thay đổi tối thiểu 15%–20% diện tích khối giữa các frame liên tiếp để tránh cảm giác ảnh bị đóng băng.