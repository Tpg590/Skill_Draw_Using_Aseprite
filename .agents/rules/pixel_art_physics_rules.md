---
trigger: always_on
---

# 🚀 2D Pixel Top-Down Physics & Kinematics Rules

Tài liệu này là quy chuẩn cưỡng chế bắt buộc về quang học, hình học không gian 3D và vật lý động lực học chuẩn hóa cho chu kỳ hoạt ảnh $N$ khung hình bất kỳ ($N = 4, 6, 8, 12, 16, 24, 32,...$).

## 1. Định luật quang học & Ánh sáng nâng cao
1.  **HẮT SÁNG NGUỒN TỰ THÂN (OSL):** Vật liệu nằm cạnh nguồn sáng (Lửa, Dung nham, Tinh thể) BẮT BUỘC đổi màu theo dải màu của nguồn sáng (Hue-shifting). Cấm để viền tiếp giáp mang màu đen/xám lạnh.
2.  **VÀNH ĐỠ HẮT SÁNG (RIM LIGHTING):** Giá đỡ, vành bát, chao đèn nằm ngay dưới nguồn phát sáng tự thân phải có 1 đường viền pixel sáng mang sắc độ của nguồn sáng đó.
3.  **KHOẢNG TỐI TUYỆT ĐỐI:** Khoang rỗng, miệng hang sâu phải có dải màu lùi dần vào màu tối nhất của Palette.
4.  **BÓNG ĐỔ NGHỊCH HƯỚNG 180° (OPPOSING CAST SHADOW):** Khi nguồn sáng di chuyển xung quanh vật cản: Hướng đổ bóng của vật cản trên sàn LUÔN LUÔN ngược chiều 180 độ với vị trí nguồn sáng:
    *   Nguồn sáng ở Trái ($X_{\text{sáng}} < X_{\text{vật}}$) $\rightarrow$ Bóng trên sàn BẮT BUỘC kéo dài sang Phải ($X_{\text{bóng}} > X_{\text{vật}}$).
    *   CẤM vẽ bóng đổ cùng phía với nguồn sáng.
5.  **SPECULAR TĨNH KHI XOAY:** Khi vật thể xoay tròn (bánh xe, bánh răng, kim đồng hồ), điểm phản quang (Specular Highlight 1–2px) BẮT BUỘC giữ nguyên vị trí theo hướng chiếu môi trường (VD: góc Trên-Trái). CẤM xoay vệt sáng theo vật thể.

## 2. Hình học không gian 3D & Phối cảnh lồng ghép
1.  **NAN HÌNH TRỤ & Z-INDEX:** 
    *   Nan ở nửa sau hình trụ dùng màu kim loại tối nhất và bị lõi vật thể bên trong che khuất hoàn toàn. Nan ở nửa trước vẽ đè lên lõi.
    *   Khoảng cách giữa các nan ở giữa lồng rộng nhất, càng ra mép hai bên càng xếp sát nhau để thể hiện độ cong trụ.
2.  **THỦY TINH & CHẤT LỎNG:** Bình thuốc phải có vệt Highlight cong màu trắng sáng nhất vắt ngang qua cả phần không gian rỗng lẫn phần có chất lỏng. Bề mặt chất lỏng trong bình trụ BẮT BUỘC là đường cong ellipse dẹt.
3.  **GỢN SÓNG NƯỚC RỖNG RUỘT (HOLLOW RIPPLES):** Mọi gợn sóng nước, sóng xung kích trên sàn BẮT BUỘC vẽ dưới dạng **đường viền cong rỗng ruột (Hollow Ellipse dày 1px)**, bên trong tâm lộ nền đất/nước. TUYỆT ĐỐI CẤM tô kín ruột thành khối màu đặc hình viên thuốc/thanh kẹo.
4.  **CẤM SÀN TRÀN VIỀN:** Nền tiếp đất của Individual Sprite phải là bục tròn/oval giới hạn, cấm kẻ dải đen thẳng đuột nối liền hai mép canvas.
5.  **ĐỘ NÉN MẶT ĐỨNG GÓC NHÌN 3/4:** Mặt phẳng tròn đặt dựng đứng vuông góc với sàn (mặt đồng hồ, bánh xe) phải nén trục Y lại tỉ lệ 85%–90% để tránh cảm giác bị phẳng góc nhìn 2D chính diện.

## 3. Hoạt họa động lực học chu kỳ N khung hình
1.  **XOAY TỊNH TIẾN ĐƠN ĐIỆU (TRUE ROTATION):** Góc quay $\theta_i$ tại frame thứ $i$ ($i = 1 \dots N$) BẮT BUỘC tịnh tiến theo công thức $\theta_i = (i - 1) \cdot \frac{360^\circ}{N}$. CẤM đảo chiều góc quay giữa chừng gây giật cục.
2.  **SÓNG VẢI TỊNH TIẾN & ĐỘ VÕNG TRỌNG LỰC:**
    *   Gốc tà áo/khăn tiếp giáp với vai/cột BẮT BUỘC rủ võng nhẹ xuống 1–2px trước khi đón gió lượn sóng bay lên.
    *   Đỉnh sóng và rãnh tối BẮT BUỘC trôi dọc trục X từ gốc ra ngọn: $X_{\text{sóng}}(i) < X_{\text{sóng}}(i+1)$.
    *   Tà vải uốn lượn mềm mại, mép đuôi luôn duỗi theo chiều gió. CẤM bẻ góc đột ngột (>45°) biến vải thành ống gấp khúc.
3.  **CAO ĐỘ TRỤC Z & TIẾP ĐẤT HOÃN XUNG:** Khi vật thể nhảy/bay lên cao, bóng tiếp đất (`S`) nằm yên ở sàn và co nhỏ kích thước. Frame ngay sau khi chạm đất (Landing) BẮT BUỘC co nhún dẹp nhẹ (Squash 1–2px) trước khi bung về tư thế đứng (Idle).
4.  **VỆT CHÉM SMEAR FRAME:** Tại pha vung vũ khí đạt vận tốc cực đại ($\frac{1}{4} \rightarrow \frac{1}{3}$ chu kỳ vung), lưỡi kiếm biến dạng thành vệt vòng cung xé gió (Arc Slash). Chuôi vũ khí (Hilt) bắt buộc khóa quanh trục cổ tay.
5.  **PHÂN RÃ HẠT (EMBERS/PARTICLES):** Lửa, khói, bọt ma thuật BẮT BUỘC sinh ra 1–3 pixel hạt nhỏ tách rời khối chính, bay tịnh tiến lên trên rồi tan biến.
6.  **DAO ĐỘNG ĐIỀU HÒA ĐỐI XỨNG QUA TÂM (N FRAMES):** 
    *   Chu kỳ dao động con lắc/chuông reo BẮT BUỘC quét qua cả 2 phía đối diện của trục tâm: Quét sang cực đại Trái $\rightarrow$ Hồi vị qua Giữa $\rightarrow$ Quét sang cực đại Phải $\rightarrow$ Hồi vị qua Giữa khép vòng lặp. CẤM kẹt dao động ở một nửa bán cầu.
    *   Bóng tiếp đất trên sàn BẮT BUỘC trượt ngang đồng bộ với tọa độ X của vật thể treo bên trên: $X_{\text{bóng}}(i) = X_{\text{vật}}(i)$.
7.  **PHẢN CHIẾU MẶT NƯỚC (INVERTED Y REFLECTION):**
    *   Vật thể nổi trên mặt nước TUYỆT ĐỐI KHÔNG vẽ bóng tiếp đất ellipse đen thui (`S`) tách rời đáy canvas.
    *   Ngay dưới mép nước phải vẽ hình ảnh phản chiếu LỘN NGƯỢC ĐẦU (Inverted Y), chiều cao nén dẹt còn 50%–70%, màu sắc hòa với nước và dịch chuyển zigzag $\pm 1\text{px}$ theo sóng nước.

## 4. Vật lý va chạm, cơ khí & phân rã
1.  **LỰC VA CHẠM SÀN (GROUND-UP IMPACT):** Khi vật thể rơi xuống sàn vỡ nát: Tâm vỡ BẮT BUỘC nằm ở điểm đáy tiếp xúc mặt sàn. Đáy vỡ toác dẹt sát sàn, các mảnh thân và miệng phía trên bị phản lực hất văng bổng lên cao theo hình vòng cung parabol. CẤM bung mảnh vỡ đối xứng tỏa tròn như bom nổ giữa tâm.
2.  **KHÓA NEO PHỤ KIỆN BỀ MẶT:** Hoa, quả, đinh tán, đai sắt trên vật thể uốn lượn/văng nổ BẮT BUỘC phải luôn nằm tiếp xúc đè lên bề mặt vật thể chủ. CẤM để phụ kiện trôi lơ lửng ngoài vùng trong suốt (`.`).
3.  **BẢO TỒN RÃNH KHỚP CƠ KHÍ:** Bộ phận cơ khí (cánh tay robot, đuôi kim loại) BẮT BUỘC duy trì đường rãnh khớp nối phân đoạn qua toàn bộ các frame. CẤM làm mịn/hòa tan các đốt thành ống trơn liền mạch hoặc uốn dẻo như cao su trong pha vung đòn.
4.  **BƯỚC CHÂN ĐA CHI PHÂN PHA SO LE:** Bọ máy/sinh vật 4 chân BẮT BUỘC bước so le theo cặp chéo góc (Trước-Trái đi cùng Sau-Phải nhấc bước $\rightarrow$ cặp còn lại cắm sàn làm trụ). CẤM cử động đối xứng hai bên cùng lúc như bơi ếch. Chân cắm sàn phải có đốm bóng tiếp xúc 1px dưới móng.
5.  **BÀO MÒN THEO MẶT ĐÓN GIÓ (WINDWARD EROSION):** Khi vật thể bị gió thổi làm tan rã: Mép trực tiếp đón luồng gió BẮT BUỘC xói mòn và cuốn bay trước tiên. Mép khuất gió chỉ tan biến sau khi luồng gió đã thổi xuyên qua.
