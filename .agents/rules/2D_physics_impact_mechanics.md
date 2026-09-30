---
trigger: always_on
---

# 💥 2D Pixel Top-Down: Collision, Mechanics & Deformation Rules

Quy chuẩn cưỡng chế bắt buộc về lực va chạm, đàn hồi bảo toàn thể tích, cơ cấu bản lề cơ khí và phân rã vật chất.

## 1. Va chạm sàn & Đàn hồi (Impact & Elastic Deformation)
1. **LỰC VA CHẠM SÀN (GROUND-UP IMPACT):** 
   * Khi vật thể rơi xuống sàn vỡ nát: Tâm vỡ BẮT BUỘC nằm ở điểm đáy tiếp xúc mặt sàn. 
   * Đáy vỡ toác dẹt sát sàn, các mảnh thân và miệng phía trên bị phản lực hất văng bổng lên cao theo hình vòng cung parabol. CẤM bung mảnh vỡ đối xứng tỏa tròn như bom nổ giữa tâm.
2. **BẢO TOÀN THỂ TÍCH KHI CO GIÃN (VOLUME CONSERVATION - SQUASH & STRETCH):** 
   * Với vật thể đàn hồi (Slime, bóng cao su, cơ thể sinh vật): Diện tích bề mặt $H \times W$ phải bảo toàn không đổi. 
   * Khi nén dẹp ($H$ giảm) $\rightarrow$ Bề ngang BẮT BUỘC phình bè sang 2 bên ($W$ tăng tương ứng):
     $$\Delta W \approx -\Delta H \times \frac{W_0}{H_0}$$

## 2. Cơ cấu bản lề & Phụ kiện gắn liền (Hinges & Attached Props)
1. **CƠ HỌC BẢN LỀ NẮP & TOÁN HỌC NÉN PHỐI CẢNH (LID FORESHORTENING):** 
   * Nắp rương/nắp hòm khi mở BẮT BUỘC xoay quanh trục bản lề phía sau. 
   * Chiều cao hiển thị trục Y của nắp ở frame mở cực đại BẮT BUỘC phải nén dẹt phối cảnh:
     $$H_{\text{mở}} \approx 40\% - 50\% H_{\text{đóng}}$$
     *(Ví dụ: Nắp khi đóng cao 8px thì khi mở ngửa cực đại chỉ được cao 3-4px)*.
   * TUYỆT ĐỐI CẤM giữ nguyên chiều cao nắp rồi nhấc tịnh tiến thẳng đứng lên trên như thang máy.
2. **BẢO TOÀN PHỤ KIỆN GẮN LIỀN (ATTACHED PROP CONTINUITY):** 
   * Các phụ kiện đính trên khối chuyển động (then cài vàng, tay nắm, ổ khóa, đinh tán) BẮT BUỘC phải xuất hiện liên tục trên MỌI frame. 
   * CẤM để then cài/khóa biến mất ở các frame mở rồi đột ngột xuất hiện lại khi đóng.
3. **KHÓA NEO PHỤ KIỆN BỀ MẶT (SURFACE PROP ANCHORING):** 
   * Hoa, quả, đinh tán, đai sắt, nhân ngọc bên trong chất dẻo BẮT BUỘC phải luôn nằm tiếp xúc đè lên bề mặt hoặc trọn vẹn bên trong vật thể chủ. 
   * CẤM để phụ kiện trôi lơ lửng ngoài vùng trong suốt (`.`).

## 3. Khớp nối cơ khí (Mechanical Joints)
1. **BẢO TỒN RÃNH KHỚP CƠ KHÍ (MECHANICAL JOINT INTEGRITY):** 
   * Bộ phận cơ khí (cánh tay robot, càng kẹp, đuôi kim loại) BẮT BUỘC duy trì đường rãnh khớp nối phân đoạn qua toàn bộ các frame. 
   * CẤM làm mịn/hòa tan các đốt thành ống trơn liền mạch hoặc uốn dẻo như cao su trong pha vung đòn.
