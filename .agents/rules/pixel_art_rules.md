---
trigger: always_on
---



# 🎨 2D Pixel Top-Down Core Aesthetic Rules

Tài liệu này là quy chuẩn cưỡng chế bắt buộc đối với mọi pixel art được sinh ra. Mọi sản phẩm đồ họa phải tuân thủ nghiêm ngặt các rào cản kỹ thuật dưới đây.

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

## 4. Ràng buộc hoạt ảnh cốt lõi
1.  **Khóa trục tĩnh:** Tọa độ Y của bản lề, cột chống tĩnh và bóng tiếp đất (`S`) phải giữ nguyên 100% qua tất cả các frame.
2.  **Động lực học mở nắp:** Nắp ngửa ra sau (thu hẹp chiều cao trục Y của nắp), làm lộ vùng bóng tối sâu nhất dưới đáy.
3.  **Tilemap liền mạch:** Cột pixel đầu tiên bên trái và cột cuối cùng bên phải của một tile lặp phải trùng khớp 100% về cao độ và màu sắc.
4.  **Biên độ biến đổi tối thiểu:** Hoạt ảnh chu kỳ tại chỗ (cháy, sủi bọt, thở) phải thay đổi tối thiểu 15%–20% diện tích khối giữa các frame liên tiếp để tránh cảm giác ảnh bị đóng băng.