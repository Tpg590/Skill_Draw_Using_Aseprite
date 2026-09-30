---
trigger: always_on
---

# ❄️ 2D Pixel Top-Down: Thermal & Weathering Rules

Quy chuẩn cưỡng chế bắt buộc về bức xạ nhiệt độ, đóng băng kết tinh, oxy hóa rỉ sét và phong hóa bề mặt.

## 1. Bức xạ nhiệt & Nung chảy (Thermal Glow & Incandescence)
1. **DẢI MÀU QUANG PHỔ NHIỆT (BLACKBODY RADIATION HUE-SHIFT):** 
   * Kim loại hoặc đá bị nung nóng phát sáng BẮT BUỘC tuân theo dải quang phổ nhiệt độ từ tâm ra rìa:
     * **Tâm cực nóng ($T_{\max}$):** Trắng vàng chói (`#FFFFA0`).
     * **Vùng trung gian:** Vàng cam rực rỡ (`#FF8800`).
     * **Vùng nguội dần:** Đỏ mận sẫm (`#8B1010`).
     * **Mép ngoài cùng:** Than đen nguội lạnh (`#1A0808`).
   * TUYỆT ĐỐI CẤM tô kim loại nóng chảy bằng một màu đỏ phẳng lì đơn sắc.
2. **HẮT SÁNG NHIỆT (THERMAL OSL):** Mọi chi tiết nằm cạnh điểm nung nóng BẮT BUỘC nhuộm ánh sáng cam đỏ rực rỡ.

## 2. Đóng băng & Kết tinh tuyết (Freezing & Frost Crystallization)
1. **GAI TINH THỂ BĂNG (NEEDLE FROST):** 
   * Băng giá đóng trên vật thể BẮT BUỘC hình thành các chóp gai nhọn 1–2px (Needle crystals) nhô ra ngoài đường viền gốc, sử dụng tone xanh tuyết Cyan nhạt pha điểm trắng tinh trên chóp.
   * CẤM phủ một lớp xanh lam phẳng lì bôi trơn lên bề mặt vật thể rồi gọi đó là đóng băng.

## 3. Oxy hóa, Rỉ sét & Phong hóa (Oxidation & Weathering)
1. **RỈ SÉT SẮT & TENG ĐỒNG (RUST & VERDIGRIS PATINA):** 
   * Sắt rỉ sét: Vết rỉ màu nâu cam sần sùi (`#8C3810`) BẮT BUỘC bám tụ tại **rãnh nối, khe nứt và chân đế tiếp xúc mặt đất ẩm**, không rải đều ngẫu nhiên như bụi bẩn.
   * Đồng oxy hóa (Patina): Loang lổ mảng xanh ngọc xỉn (`#409878`) xen kẽ bề mặt kim loại đồng thau.
2. **BÀO MÒN THEO MẶT ĐÓN GIÓ (WINDWARD EROSION):** 
   * Khi vật thể bị gió bão / cát thổi làm tan rã: Mép trực tiếp đón luồng gió BẮT BUỘC xói mòn và cuốn bay trước tiên. Mép khuất gió chỉ tan biến sau khi luồng gió đã thổi xuyên qua.
