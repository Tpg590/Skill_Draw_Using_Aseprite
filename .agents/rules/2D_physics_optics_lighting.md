---
trigger: always_on
---

# 💡 2D Pixel Top-Down: Optics & Lighting Rules

Quy chuẩn cưỡng chế bắt buộc về quang học, tán xạ ánh sáng, đổ bóng và phản quang trong không gian Pixel Art Top-Down 3/4.

## 1. Nguồn sáng tự thân & Hắt sáng (OSL & Rim Lighting)
1. **HẮT SÁNG NGUỒN TỰ THÂN (OSL - Optical Self-Luminance):** 
   * Vật liệu nằm cạnh nguồn sáng (Lửa, Dung nham, Tinh thể phát quang, Năng lượng ma thuật) BẮT BUỘC đổi màu theo dải màu của nguồn sáng (Hue-shifting). 
   * Tuyệt đối CẤM để viền tiếp giáp mang màu đen/xám lạnh vô cảm.
2. **VÀNH ĐỠ HẮT SÁNG (RIM LIGHTING):** 
   * Giá đỡ kim loại, vành bát, chao đèn nằm ngay dưới nguồn phát sáng tự thân BẮT BUỘC phải có 1 đường viền pixel sáng mang sắc độ rực rỡ của nguồn sáng đó.
3. **KHOẢNG TỐI TUYỆT ĐỐI (DEPTH DARKNESS):** 
   * Khoang rỗng, miệng hang sâu, lòng giếng hoặc lòng hòm mở BẮT BUỘC có dải màu lùi dần vào màu tối nhất của Palette để tạo độ sâu thăm thẳm.

## 2. Quy tắc đổ bóng không gian (Cast Shadow Dynamics)
1. **BÓNG ĐỔ NGHỊCH HƯỚNG 180° (OPPOSING CAST SHADOW):** 
   * Khi nguồn sáng di chuyển xung quanh vật cản: Hướng đổ bóng của vật cản trên sàn LUÔN LUÔN ngược chiều 180 độ với vị trí nguồn sáng:
     * Nguồn sáng ở Trái ($X_{\text{sáng}} < X_{\text{vật}}$) $\rightarrow$ Bóng trên sàn BẮT BUỘC kéo dài sang Phải ($X_{\text{bóng}} > X_{\text{vật}}$).
     * Nguồn sáng ở Phải ($X_{\text{sáng}} > X_{\text{vật}}$) $\rightarrow$ Bóng trên sàn BẮT BUỘC kéo dài sang Trái ($X_{\text{bóng}} < X_{\text{vật}}$).
   * TUYỆT ĐỐI CẤM vẽ bóng đổ cùng phía với nguồn sáng.
2. **BÓNG ĐỔ VẬT THỂ THỦY TINH & CHẤT LỎNG TRONG SUỐT:** 
   * Bóng đổ của bình chứa chất lỏng trên mặt sàn BẮT BUỘC là màu bóng tối tiếp đất (`S`, Alpha mờ) có thể pha 1-2 pixel OSL mờ ở tâm.
   * TUYỆT ĐỐI CẤM tô màu nguyên chất của nước thuốc thành một mảng phẳng bệt trên sàn (tránh nhầm lẫn thành vũng nước thuốc bị đổ vỡ tràn ra ngoài).

## 3. Phản quang & Phản xạ bề mặt (Specular & Reflections)
1. **KHÓA BIÊN ĐỘ PHẢN QUANG TRONG LÒNG THỂ TÍCH (SPECULAR BOUNDARY CLAMPING):** 
   * Với vật thể xoay tròn trục đối xứng: Vệt phản quang đứng yên tại góc chiếu môi trường.
   * Với vật thể lắc lư/chao đảo (bình thuốc, chuông): Vệt phản quang được trượt động (Specular Drift) theo vòm cong đón sáng, **NHƯNG BẮT BUỘC PHẢI BỊ KHÓA CHẶT TRONG LÒNG THỂ TÍCH** (cách mép viền ngoài tối thiểu 1 pixel).
   * TUYỆT ĐỐI CẤM vệt sáng trượt lố đè lên viền ngoài hoặc văng ra ngoài không gian trống (`.`).
2. **PHẢN CHIẾU MẶT NƯỚC (INVERTED Y REFLECTION):** 
   * Vật thể nổi trên mặt nước TUYỆT ĐỐI KHÔNG vẽ bóng tiếp đất ellipse đen thui (`S`) tách rời đáy canvas.
   * Ngay dưới mép nước BẮT BUỘC vẽ hình ảnh phản chiếu LỘN NGƯỢC ĐẦU (Inverted Y), chiều cao nén dẹt còn 50%–70%, màu sắc hòa với nước và dịch chuyển zigzag $\pm 1\text{px}$ theo sóng nước.
