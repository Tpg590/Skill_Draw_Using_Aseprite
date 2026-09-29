---
trigger: always_on
---

# 🚀 2D Pixel Top-Down Advanced Physics & Dynamic Guide

Tài liệu này bổ trợ cho `pixel_art.md`, tập trung vào các quy chuẩn hình học không gian, vật lý quang học và hoạt họa động lực học phức tạp chuẩn hóa cho chu kỳ hoạt ảnh $N$ khung hình bất kỳ ($N = 4, 6, 8, 12, 16, 24, 32,...$).

## 1. Vật lý Quang học & Ánh sáng Nâng cao
### 1.1. Nguồn Sáng Tự Thân (OSL - Object Source Lighting)
*   **Hắt sáng đổi màu (Color Bleed):** Nếu vật thể có nguồn sáng (Lửa, Dung nham, Pha lê), pixel vật liệu lân cận BẮT BUỘC đổi màu theo dải màu của nguồn sáng (Hue-shifting). Không để viền tiếp giáp mang màu đen/xám lạnh.
*   **Vành đỡ nguồn sáng (Rim Lighting):** Vành bát, giá đỡ, bệ đèn nằm ngay dưới ngọn lửa/lõi năng lượng BẮT BUỘC có 1 đường viền pixel sáng (Highlight) mang sắc độ của ngọn lửa đó.
*   **Khoảng tối tuyệt đối:** Mọi khoang hở (miệng lò, hang sâu) phải có gradient lùi dần vào trong thành màu tối nhất của Palette.

### 1.2. Định Luật Bóng Đổ Nghịch Hướng (Opposing Cast Shadow)
*   **Vector ngược chiều 180°:** Khi nguồn sáng di chuyển xung quanh vật cản (cột trụ, giá treo): Hướng đổ bóng của vật cản trên sàn LUÔN LUÔN ngược chiều 180 độ với vị trí nguồn sáng:
    *   Nguồn sáng ở bên Trái ($X_{\text{sáng}} < X_{\text{cột}}$) $\rightarrow$ Bóng đổ trên sàn BẮT BUỘC ngả dài sang Phải ($X_{\text{bóng}} > X_{\text{cột}}$).
    *   CẤM vẽ bóng đổ cùng phía với nguồn sáng.

### 1.3. Khóa Ánh Sáng Khi Vật Thể Xoay (Stationary Specular Highlight)
*   Khi vật thể xoay tròn (bánh xe, bánh răng, kim đồng hồ), vệt phản quang (Specular Highlight 1-2px) BẮT BUỘC cố định theo hướng chiếu môi trường (VD: góc Trên-Trái). Vật thể xoay qua, nhưng điểm sáng phải ở lại vị trí cũ trên mọi frame.

## 2. Hình Học Không Gian 3D & Phối Cảnh Lồng Ghép
### 2.1. Chiều Sâu Hình Trụ & Lưới Đa Lớp (Z-Index Interlocking)
*   **Phân tách Nan Trước - Sau (Lồng sắt, chấn song):**
    *   Nan ở nửa sau hình trụ BẮT BUỘC dùng màu kim loại tối nhất/viền sẫm và bị lõi/vật thể bên trong che khuất hoàn toàn.
    *   Chỉ nan ở nửa trước mới được vẽ đè lên trên lõi vật thể.
*   **Phân bố Nan Radial:** Khoảng cách giữa các nan ở giữa lồng rộng nhất; càng ra mép hai bên trái/phải, các nan càng phải xếp sát nhau để thể hiện độ cong tròn 3D.

### 2.2. Thủy Tinh Lồi & Khúc Xạ
*   **Thủy tinh lồi (Potion/Bình):** BẮT BUỘC có vệt Highlight cong màu trắng/sáng nhất vắt ngang qua cả phần không gian rỗng lẫn phần có chất lỏng để tạo cảm giác lớp kính bọc ngoài.
*   **Mặt cắt ellipse:** Mặt trên cùng của chất lỏng trong bình trụ/cầu BẮT BUỘC là đường cong ellipse, cấm vẽ đường ngang phẳng lì.

### 2.3. Hình Học Gợn Sóng Nước & Vòng Lan Tỏa (Hollow Concentric Ripples)
*   **Cấu trúc rỗng ruột:** Mọi gợn sóng nước (Water ripple), sóng chấn động, vòng ma thuật trên sàn BẮT BUỘC vẽ dưới dạng **đường viền cong rỗng ruột (Hollow Ellipse dày 1px)**.
*   Tâm vòng sóng phải để lộ nền đất (dùng ký tự `.` hoặc màu sàn). CẤM tô kín ruột thành khối màu đặc (tránh biến gợn sóng thành hình viên thuốc/thanh kẹo).
*   **CẤM sàn kẻ ngang tràn viền:** Nền tiếp đất của Individual Sprite phải là bục tròn/oval giới hạn, cấm kẻ dải đen thẳng đuột nối 2 mép canvas.
*   **Độ nén góc nhìn 3/4 mặt phẳng đứng:** Các vật thể tròn dựng đứng vuông góc với mặt đất (bánh xe, bia ngắm) phải nén trục Y lại tỉ lệ 85%–90% để thể hiện góc nhìn 3/4.

## 3. Hoạt Họa Động Lực Học (Advanced Animation Physics)
### 3.1. Động Lực Học Sóng Vải & Trọng Lực Chu Kỳ N Frame (Cloth Physics)
*   **Độ võng trọng lực (Gravity Sag):** Gốc tà áo/khăn tiếp giáp với vai/cột BẮT BUỘC rủ võng nhẹ xuống 1–2px trước khi đón gió lượn sóng bay lên.
*   **Pha truyền sóng tịnh tiến liên tục:** Đỉnh sóng và rãnh tối BẮT BUỘC trôi tịnh tiến dọc trục X từ gốc ra ngọn theo hàm pha tuần hoàn:
    $$X_{\text{sóng}}(i) = X_{\text{gốc}} + (i - 1) \cdot \frac{\text{Chiều dài tà áo}}{N}$$
    Đỉnh sóng frame sau luôn dạt xa gốc hơn frame trước ($X_{\text{sóng}}(i) < X_{\text{sóng}}(i+1)$) cho đến khi bung khỏi mép đuôi rồi tạo vòng sóng mới tại gốc.
*   **CẤM nếp gập gãy góc:** Tà vải phải uốn lượn hình sin/Bezier mềm mại, đuôi vải luôn trôi duỗi theo chiều gió. CẤM bẻ góc đột ngột (>45°) làm vải biến thành ống kim loại gấp khúc.

### 3.2. Chuyển Động Z-Axis & Hoạt Họa Rơi Nhảy (N Frames)
*   **Động lực học bóng râm Z-Axis:** Khi vật thể nhảy/bay lên cao, bóng tiếp đất (`S`) BẮT BUỘC nằm yên ở sàn. Kích thước bán kính bóng $R_{\text{bóng}}(i)$ co nhỏ tỷ lệ nghịch với cao độ trục Z của vật thể.
*   **Tiếp đất hoãn xung (Landing Squash):** Dù tổng số frame là bao nhiêu, frame ngay sau thời điểm tiếp đất (Landing) BẮT BUỘC co nhún dẹp nhẹ (Squash 1-2px bề cao, nở bề ngang) trước khi hồi vị về thế đứng chuẩn (Idle).

### 3.3. Xoay Trục & Hành Động Tốc Độ Cao Cho N Khung Hình (General N-Frame Loops)
*   **Xoay tịnh tiến 1 chiều ($N$ frame):** Góc quay $\theta_i$ tại frame thứ $i$ BẮT BUỘC tịnh tiến đơn điệu theo công thức:
    $$\theta_i = (i - 1) \cdot \frac{360^\circ}{N}$$
    CẤM đảo chiều góc quay giữa chừng gây hiện tượng giật lắc (ping-pong).
*   **Khóa tâm xoay (Pivot Point):** Tọa độ gốc xoay $(X_{\text{tâm}}, Y_{\text{tâm}})$ cố định 100% qua toàn bộ $N$ frame.
*   **Khóa tâm xoay vũ khí (Weapon Arc Continuity):** Khi vung vũ khí chém, chuôi kiếm/rìu (Hilt) BẮT BUỘC bám sát quanh tọa độ cổ tay cố định, cấm nhảy cóc sang góc đối diện canvas.
*   **Vệt chém Smear Frame:** Tại giai đoạn vung đạt vận tốc cực đại (khoảng $\frac{1}{4} \rightarrow \frac{1}{3}$ chu kỳ vung), lưỡi vũ khí BẮT BUỘC biến dạng thành vệt vòng cung xé gió (Arc Slash) thay vì vẽ lưỡi thẳng tĩnh.
*   **Phân rã hạt (Particles/Embers):** Lửa, khói, bọt ma thuật BẮT BUỘC sinh ra 1–3 pixel hạt nhỏ tách rời khối chính, bay tịnh tiến theo phương vận tốc và mờ dần/biến mất ở các frame cuối chu kỳ.

## 4. Vật Lý Va Đập & Ràng Buộc Phụ Kiện (Impact & Attached Props)
### 4.1. Động Lực Học Va Chạm Sàn (Ground-Up Impact vs Radial Explosion)
*   **Lực phân rã định hướng:** Khi vật thể rơi xuống sàn rồi vỡ (bình gốm, khối đá, thùng gỗ):
    *   Tâm vỡ BẮT BUỘC nằm ở ĐIỂM TIẾP XÚC ĐÁY VỚI SÀN, không được lấy tâm ở giữa bụng vật thể.
    *   Đáy vật thể vỡ vụn dạt ngang sát sàn, các mảnh phần thân và miệng phía trên bị phản lực hất văng bổng lên cao theo hình vòng cung parabol hướng lên.
    *   TUYỆT ĐỐI CẤM bung mảnh vỡ thành hình tròn/ngũ giác đều đối xứng như bom nổ giữa tâm.

### 4.2. Khóa Neo Phụ Kiện Trên Vật Thể Uốn Lượn (Attached Props Anchoring)
*   **Bảo toàn tiếp xúc bề mặt:** Các chi tiết phụ kiện nhỏ (quả mọng, hoa, đinh tán, cúc áo, mắt) đính trên vật thể đang chuyển động uốn lượn (cây cối, nhân vật, quái vật) BẮT BUỘC phải luôn nằm tiếp xúc đè lên bề mặt của vật thể chủ.
*   CẤM để phụ kiện bị trôi dạt bay lơ lửng vào khoảng không trong suốt (`.`) ngoài rìa vật thể khi chuyển frame.

### 4.3. Bắt Buộc Chiếu Bóng Đổ Lên Nền (Mandatory Cast Shadow Projection)
*   Khi có nguồn sáng di động (đom đóm, ngọn đuốc di chuyển quanh cột trụ): Ngoài việc đổi màu đón sáng trên thân cột (OSL), BẮT BUỘC phải vẽ một vệt bóng đổ mang màu tối (viền sẫm/shadow) quét ngang trên mặt đất/bục cỏ theo định luật nghịch hướng 180°:
    *   Nguồn sáng ở Trái $\rightarrow$ Vệt bóng trên thảm cỏ/sàn kéo dài sang Phải.
    *   Không được bỏ qua việc vẽ bóng đổ trên bề mặt tiếp đất.

### 4.4. Dao Động Đối Xứng Chu Kỳ Chuẩn Hóa N Khung Hình (Symmetrical Oscillation)
1. **Chu kỳ quét 4 pha tỷ lệ:** Với hoạt ảnh dao động con lắc gồm $N$ frame, vị trí ngang $X(i)$ của vật thể tuân theo hàm điều hòa qua tâm cân bằng $X_{\text{tâm}}$:
   * **Pha 1 (Frame $1 \rightarrow \frac{N}{4}$):** Quét từ tâm sang cực đại biên Trái ($X < X_{\text{tâm}} - \Delta X$).
   * **Pha 2 (Frame $\frac{N}{4} \rightarrow \frac{N}{2}$):** Trôi ngược từ biên Trái về vị trí cân bằng ($X \approx X_{\text{tâm}}$), dây xích uốn cong trễ pha (Follow-through).
   * **Pha 3 (Frame $\frac{N}{2} \rightarrow \frac{3N}{4}$):** Quét từ tâm sang cực đại biên Phải ($X > X_{\text{tâm}} + \Delta X$).
   * **Pha 4 (Frame $\frac{3N}{4} \rightarrow N$):** Trôi ngược từ biên Phải về vị trí cân bằng để khép vòng lặp.
   * CẤM dao động lệch hẳn về một phía bán cầu trái hoặc phải.
2. **Đồng bộ bóng đổ trục X:** Tọa độ $X$ của bóng tiếp đất bám sát vật thể qua toàn bộ $N$ frame: $X_{\text{bóng}}(i) = X_{\text{vật}}(i)$.

### 4.5. Phản Chiếu Mặt Nước Chu Kỳ N Khung Hình (Water Surface Reflection)
1. **Cấm bóng râm cạn:** Tuyệt đối không vẽ bóng ellipse màu xám/đen (`S`) tách rời đáy canvas cho vật thể nổi trên mặt nước (tránh biến vật thể thành tàu bay).
2. **Hình học phản chiếu đảo trục Y:**
   * Ngay sát dưới đường mép cắt nước của đáy vật thể, BẮT BUỘC vẽ hình ảnh phản chiếu LỘN NGƯỢC ĐẦU (Inverted Y): Đáy thuyền ở trên, mép trên và phụ kiện (đèn, cờ) chúc ngược xuống dưới. Chiều cao phản chiếu bị nén dẹt còn 50%–70% so với vật thể thực.
   * **Biến dạng gợn sóng tuần hoàn:** Dải màu phản chiếu hòa sắc với nước (giảm độ bão hòa). Các hàng pixel phản chiếu dịch chuyển lệch ngang zigzag $\pm 1\text{px}$ theo hàm sóng hình sin dọc theo $N$ frame để đồng bộ với nhịp dập dềnh của mặt nước.

### 4.6. Động Lực Học Khớp Nối Cơ Khí Phân Đoạn (Articulated Segment Kinematics)
1. **Bảo tồn rãnh khớp (Seams/Joints Integrity):**
   * Đối với cấu trúc cơ khí, giáp trụ, đuôi kim loại gồm nhiều đốt: BẮT BUỘC duy trì các đường rãnh phân tách khớp nối (đường pixel tối hoặc đinh tán đổi màu) giữa từng phân đoạn trên TẤT CẢ các frame.
   * TUYỆT ĐỐI CẤM làm mịn/hòa tan các đốt thành một ống trơn liền mạch hoặc uốn dẻo như dây cao su trong pha vung đòn (Strike/Overshoot).
2. **Bảo toàn chiều dài phân đoạn:** Góc xoay của từng đốt có thể thay đổi để tạo dáng quất roi, nhưng độ dài riêng lẻ của từng đốt kim loại phải được bảo toàn (sai số không quá $\pm 1$ pixel).