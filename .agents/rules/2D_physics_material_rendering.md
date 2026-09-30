---
trigger: always_on
---

# 🛡️ 2D Pixel Top-Down: Material Rendering & Shading Rules

Quy chuẩn cưỡng chế bắt buộc về đặc tính bề mặt, tán xạ ánh sáng dưới bề mặt (SSS) và hành vi nếp gấp chất liệu.

## 1. Độ nhám & Độ bóng bề mặt (Roughness & Specular Response)
1. **KIM LOẠI BÓNG & TINH THỂ (HIGH SPECULAR / METALLIC):** 
   * Vệt Highlight BẮT BUỘC tập trung thành điểm/vạch sắc nét (1–2px) bằng màu trắng sáng nhất (`#FFFFFF` hoặc ánh kim).
   * Tương phản ánh sáng gắt (High Contrast): Chuyển sắc từ sáng chói sang vùng tối kim loại chỉ qua 1–2 bước chuyển ngắn, không chuyển êm đều như cao su.
2. **BỀ MẶT NHÁM & THÔ RÁP (MATTE / ROUGH - GỖ, ĐÁ, ĐẤT NUNG):** 
   * TUYỆT ĐỐI CẤM dùng điểm trắng tinh `#FFFFFF` làm highlight cho đá thô hoặc vỏ cây.
   * Vùng sáng phải phân bố tán xạ rộng, chuyển sắc êm qua các tone trung tính (Midtones) và dùng dăm pixel tối so le tạo độ nhám bề mặt.

## 2. Tán xạ dưới bề mặt & Biến dạng quang học (SSS & Dynamic Optics)
1. **DẢI BÃO HÒA ĐƯỜNG PHÂN GIỚI SÁNG/TỐI (TERMINATOR SATURATION BOOST):** 
   * Đối với chất liệu hữu cơ hoặc bán trong suốt (Thịt sống, Slime, Ngọc bích, Sáp nến, Lá cây): Đường biên tiếp giáp giữa vùng sáng và vùng tối (Terminator Line) BẮT BUỘC có một dải 1–2 pixel mang **độ bão hòa màu rực rỡ nhất (Saturation Peak)**:
     * Thịt/da hữu cơ: Dải chuyển tiếp ngả cam/đỏ hồng rực rỡ.
     * Ngọc bích / Lá cây: Dải chuyển tiếp ngả xanh lục bảo neon.
     * Slime tím: Dải chuyển tiếp ngả hồng tím phát quang.
   * TUYỆT ĐỐI CẤM đổ bóng chuyển thẳng từ màu nền sang màu xám đen xỉn làm vật thể bị đục như xi măng.
2. **ĐỘ DÀY QUANG HỌC KHI BIẾN DẠNG ĐÀN HỒI (DYNAMIC OPTICAL DENSITY):** 
   * Đối với chất nhầy, Slime, chất lỏng bán trong suốt khi co giãn hình thể:
     * **Pha Kéo Giãn (Stretch - $H > W$):** Lớp chất lỏng mỏng đi, độ xuyên thấu ánh sáng tăng cao. Diện tích dải màu sáng nhất BẮT BUỘC nở rộng (chiếm $\ge 50\%$ diện tích thân), độ bão hòa màu tăng rực rỡ, tạo cảm giác trong suốt lấp lánh.
     * **Pha Nén Bẹp (Squash - $H < W$):** Lớp chất lỏng dồn đặc cản sáng. Toàn bộ thân BẮT BUỘC sẫm màu xuống 1 tone, dải màu tối nhất dưới đáy dâng cao chiếm $\ge 60\%$ diện tích thân.
   * TUYỆT ĐỐI CẤM giữ nguyên tỷ lệ diện tích các dải màu sáng/tối cố định khi vật thể đang co giãn mạnh.
3. **BIẾN DẠNG VỆT PHẢN QUANG THEO TRỤC KÉO GIÃN (SPECULAR ELONGATION ON STRETCH):** 
   * Khi khối chất lỏng/nhầy tròn bị kéo giãn theo trục nào: Vệt Highlight trắng sáng nhất (`#FFFFFF`) BẮT BUỘC bị kéo biến dạng thành **dải vệt dọc/ngang (dài 3–5px, rộng 1px)** song song với trục kéo giãn đó.
   * CẤM giữ nguyên vệt phản quang thành một đốm chấm tròn tĩnh khi thân đang biến dạng hình ống/trụ.

## 3. Độ nặng & Nếp gấp chất liệu (Drape & Fabric Weight)
1. **VẢI LỤA MỎNG & BĂNG VẢI NHẸ:** 
   * Độ dày nếp vải chỉ 1px, nếp uốn lượn cong mềm mại, biên độ dao động lớn theo gió.
2. **DA THUỘC & VẢI BẠT NẶNG (HEAVY LEATHER & CANVAS):** 
   * Khối viền vải dày tối thiểu 2–3px, nếp gấp gãy góc dứt khoát hình khối hộp, độ trĩu nặng do trọng lực lấn át sức gió.
   * CẤM vẽ áo choàng da nặng uốn lượn sóng sin phập phồng như dải ruy băng.