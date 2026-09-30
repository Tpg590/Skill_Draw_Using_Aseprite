---
trigger: always_on
---

# 📐 2D Pixel Top-Down: Spatial Geometry & Perspective Rules

Quy chuẩn cưỡng chế bắt buộc về hình học không gian 3D, phối cảnh góc nhìn Top-Down 3/4 và cấu trúc lồng ghép đa lớp.

## 1. Hình học trụ & Chiều sâu Z-Index (Cylinders & Z-Ordering)
1. **NAN HÌNH TRỤ & Z-INDEX:** 
   * Nan ở nửa sau hình trụ dùng màu kim loại tối nhất và bị lõi vật thể bên trong che khuất hoàn toàn. Nan ở nửa trước vẽ đè lên lõi.
   * Khoảng cách giữa các nan ở giữa lồng rộng nhất, càng ra mép hai bên càng xếp sát nhau để thể hiện độ cong trụ tự nhiên.
2. **CHIỀU SÂU LÒNG KHỐI (3D CAVITY DEPTH):**
   * Lòng hòm mở, miệng giếng, hang động: Bắt buộc vẽ thành trong dày tối thiểu 2–3px và đổ bóng xiên từ mép đón sáng xuống đáy để tạo chiều sâu 3 chiều.

## 2. Phối cảnh Top-Down 3/4 & Hướng chiếu (Projection & Reach)
1. **ĐỘ NÉN MẶT ĐỨNG GÓC NHÌN 3/4:** 
   * Mặt phẳng tròn/chữ nhật đặt dựng đứng vuông góc với sàn (mặt đồng hồ, bánh xe, miệng cổng) BẮT BUỘC nén trục Y lại tỉ lệ 85%–90% để thể hiện độ nghiêng phối cảnh 3/4.
2. **PHỐI CẢNH VƯƠN TỚI PHÍA TRƯỚC (FORWARD REACH IN TOP-DOWN 3/4):** 
   * Trong góc nhìn Top-Down 3/4, hướng "Phía trước mặt" (về phía người xem) BẮT BUỘC chiếu theo chiều $+Y$ (hướng chúc chéo xuống dưới màn hình). 
   * CẤM vẽ cánh tay vươn về phía trước mà lại chĩa ngược lên trên đỉnh canvas ($-Y$).
* **KHÔNG GIAN BAY CỦA ĐẠN HƯỚNG PHÍA TRƯỚC (+Y FORWARD CLEARANCE):**
  * Đạn/nước độc nhổ về phía trước người xem ($+Y$) BẮT BUỘC bay trên mặt phẳng sàn (cao hơn hoặc lướt trên bề mặt sàn bệ đỡ).
  * TUYỆT ĐỐI CẤM đạn xuyên thủng xuống dưới đáy bục đỡ hoặc rơi lọt qua sàn nhà ($Y_{\text{đạn}} \le Y_{\text{floor}}$).

3. **PHÂN ĐỊNH HÌNH HỌC CỔNG KHÔNG GIAN (STANDING GATE VS FLOOR PIT):** 
   * **Cổng Vòm Đứng (Standing Gate / Portal):** Nếu là cổng để nhân vật đi xuyên qua: BẮT BUỘC có khung vòm dựng đứng (2 cột trụ hai bên khóa chân đế xuống sàn, vòm trên cao $H > W$). Màng năng lượng bên trong BẮT BUỘC là mặt phẳng dựng thẳng (nén nhẹ trục $Y \approx 85\% - 90\%$, tuyệt đối không dẹt bệt xuống sàn). Chân 2 cột trụ cắm sàn phải có bóng tiếp đất (`S`), khoảng thông thủy bên dưới để lộ mặt sàn đi qua.
   * **Hố Sàn / Vòng Dịch Chuyển (Floor Pit / Teleport Pad):** Chỉ vẽ dạng bục tròn dẹt ($Y \approx 50\% X$) khi mô tả bệ triệu hồi, bẫy sụt lún hoặc hố ma thuật nhảy xuống sàn.

## 3. Điểm tiếp sàn & Khóa giới hạn (Ground Plane Alignment)
1. **TÂM TIẾP XÚC SÀN (GROUND-PLANE ALIGNMENT):** 
   * Tâm của bục đỡ, vòng sáng và hiệu ứng sàn BẮT BUỘC đặt tại **điểm tiếp xúc thấp nhất giữa vật thể và mặt sàn ($Y_{\text{floor}}$)**. 
   * TUYỆT ĐỐI CẤM đặt tâm hiệu ứng lơ lửng cắt ngang thân vật thể.
2. **CẤM SÀN TRÀN VIỀN:** 
   * Nền tiếp đất của Individual Sprite phải là bục tròn/oval giới hạn gọn gàng trong canvas. CẤM kẻ dải đen thẳng đuột nối liền hai mép canvas làm mất tính độc lập của sprite.
3. **BÓNG TIẾP ĐẤT CỦA VẬT THỂ TRÒN BAY TRÊN KHÔNG (AERIAL ELLIPSE SHADOW):** 
   * Bóng tiếp đất trên sàn của vật thể bay (hình cầu, con mắt máy, giọt nước bay) BẮT BUỘC là **hình ellipse dẹt (tỷ lệ $Y/X \approx 0.3 - 0.4$, bo cong 2 đầu)**. 
   * TUYỆT ĐỐI CẤM vẽ bóng sàn thành một thanh ngang chữ nhật thẳng đuột phẳng lì (`[_____]`).
4. **TIẾP ĐẤT ĐA ĐIỂM CỦA GIÁ ĐỠ 3 CHÂN (TRIPOD LEGS GROUNDING):** 
   * Với vật thể có 3 chân chống (vạc cổ, kiềng 3 chân, bọ máy): Chân chống phía sau trong góc nhìn 3/4 BẮT BUỘC phải cắm chạm tới mặt phẳng sàn và có bóng tiếp đất riêng. TUYỆT ĐỐI CẤM vẽ chân sau bị cắt cụt lơ lửng trên không trung.
5. **ĐƯỜNG ĐÁY TIẾP ĐẤT CONG CỦA VẬT THỂ TRỤ/TRÒN (CYLINDER BASE CONTACT ARC):** 
   * Mặt đáy tiếp xúc sàn của mọi khối hình trụ, hình cầu hoặc bục đá tròn (thùng gỗ, vạc nước, cột tháp) BẮT BUỘC là **đường cong vồng xuống dưới (hướng $+Y$, nhịp bước `1-2-1` hoặc bo góc cung)**.
   * TUYỆT ĐỐI CẤM kẻ phẳng đáy tiếp sàn bằng một đường thẳng nằm ngang cắt ngang khối.