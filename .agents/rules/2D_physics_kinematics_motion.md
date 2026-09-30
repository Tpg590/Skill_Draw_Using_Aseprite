---
trigger: always_on
---

# 🏃 2D Pixel Top-Down: Kinematics & Motion Dynamics Rules

Quy chuẩn cưỡng chế bắt buộc về chuyển động học, quán tính, chu kỳ hoạt họa $N$ khung hình và đồng bộ bóng đổ trục Z.

## 1. Trọng lực trục Z & Đổ bóng tiếp đất (Z-Axis & Contact Shadows)
1. **CAO ĐỘ TRỤC Z & KHÓA CHẾT TỌA ĐỘ Y BÓNG TRÊN MẶT ĐỠ (SURFACE SHADOW LOCK):** 
   * Khi vật thể (nhân vật, đồng xu, mảnh vỡ) nhảy hoặc được tung lên cao dọc trục Z rời khỏi mặt đất/mặt bệ đỡ: Tọa độ hàng pixel $Y$ của vệt bóng tiếp đất (`S`) BẮT BUỘC KHÓA CỐ ĐỊNH 100% tại mặt phẳng đỡ (ngay trên đỉnh bục đá/sàn nhà).
   * Trên mọi frame có vật thể trên không, hàng pixel tiếp xúc của mặt bệ BẮT BUỘC phải chứa các ký tự bóng `S` (đốm bóng thu nhỏ tỷ lệ nghịch với cao độ).
   * TUYỆT ĐỐI CẤM xóa sạch bóng trên mặt sàn/mặt bệ khiến vật thể bị trôi lơ lửng mất gốc.
2. **TIẾP ĐẤT HOÃN XUNG (LANDING SQUASH):** 
   * Frame ngay sau khi chạm đất BẮT BUỘC co nhún dẹp nhẹ (Squash 1–2px) trước khi bung về thế đứng chuẩn (Idle).
3. **DAO ĐỘNG BỒNG BỀNH TRỤC Z KHI BAY LƠ LỬNG (HOVER BOBBING DYNAMIC):** 
   * Vật thể bay lơ lửng tại chỗ (con mắt máy, đá ma thuật trôi nổi): Tọa độ Y của khối vật thể BẮT BUỘC nhấp nhô dao động $\pm 1\text{px}$ giữa các frame để mô tả lực nâng không khí/từ trường.
   * CẤM giữ nguyên tọa độ Y đứng im phắc 100% qua toàn bộ các frame khiến vật thể bị cảm giác đóng đinh chết cứng trên màn hình.
4. **SUY GIẢM BIÊN ĐỘ VA CHẠM NẢY SÀN (DECAYING BOUNCE OSCILLATION):** 
   * Khi vật thể nảy sàn suy hao (bóng rơi, giọt nhầy, tạ rơi): Độ cao nảy trục Z và biên độ nén bẹp ($W_{\text{squash}}$) BẮT BUỘC giảm tối thiểu $40\% - 50\%$ sau mỗi lần chạm đất tiếp theo ($Z_{k+1} \le 0.5 \times Z_k$).
   * TUYỆT ĐỐI CẤM vẽ các frame nảy sau có độ cao hoặc độ phình ngang bằng hoặc lớn hơn lần nảy trước.

## 2. Quán tính, Mắt xích & Dây mềm (Inertia & Flexible Links)
1. **ĐỘNG LỰC HỌC MẮT XÍCH RỜI RẠC & TRỄ PHA QUÁN TÍNH (CHAIN LINKS & FOLLOW-THROUGH):** 
   * Dây xích nhiều mắt BẮT BUỘC phải thể hiện từng mắt xích độc lập (hình vòng oval/chữ nhật rỗng 2x3px hoặc 3x2px có khe hở `.` ở tâm). CẤM vẽ thành một sợi dây đơn 1px hoặc thanh kim loại liền khối.
   * Khi vung vũ khí xích (flail, quả cầu gai): Các mắt xích và quả cầu đuôi BẮT BUỘC chuyển động trễ pha quán tính theo dáng uốn cong chữ S so với chuôi cầm.
   * Gai nhọn trên quả cầu chiến BẮT BUỘC phải nhô rõ rệt 1-2px khỏi chu vi quả cầu, không vẽ nhẵn bóng như quả tạ bowling.
2. **SÓNG VẢI TỊNH TIẾN & ĐỘ VÕNG TRỌNG LỰC:** 
   * Gốc tà áo/khăn rủ võng nhẹ 1–2px trước khi đón gió lượn sóng bay lên. Đỉnh sóng và rãnh tối BẮT BUỘC trôi dọc trục X từ gốc ra ngọn: $X_{\text{sóng}}(i) < X_{\text{sóng}}(i+1)$.
   * Tà vải uốn lượn hình sin/Bezier mềm mại, mép đuôi luôn duỗi theo chiều gió. CẤM bẻ góc đột ngột (>45°).
3. **ĐỘ TRỄ QUÁN TÍNH CỦA NHÂN CHÌM TRONG CHẤT LỎNG (VISCOUS CORE DRAG):**
   * Vật thể rắn/con mắt chìm bên trong chất nhầy BẮT BUỘC chuyển động trễ pha 1 frame so với biên độ nén giãn của lớp vỏ ngoài:
     * Vỏ ngoài nhún bẹp cực đại (Frame n) $\rightarrow$ Con mắt chìm chạm đáy ở Frame tiếp theo (Frame n+1).
   * CẤM ghim chết con mắt di chuyển đồng bộ cơ học $1:1$ với vỏ ngoài như một miếng dán sticker.

## 3. Chuyển động tuần hoàn & Chu kỳ N Frames (Periodic Cycles)
1. **CHU TRÌNH XOAY ĐỐI XỨNG 360° (FULL YAW ROTATION CONTINUITY):** 
   * Khi vật thể dẹt (khiên, đồng xu) xoay 360° qua $N$ frame: BẮT BUỘC tuân thủ chu trình khép kín: Mặt trước $\rightarrow$ Nghiêng mặt trước $\rightarrow$ Cạnh bên (dày 2-4px) $\rightarrow$ Nghiêng mặt sau $\rightarrow$ Mặt sau chính diện $\rightarrow$ Nghiêng mặt sau phía đối diện $\rightarrow$ Cạnh bên phía đối diện $\rightarrow$ Hồi vị mặt trước.
   * TUYỆT ĐỐI CẤM nhảy cóc từ mặt sau trực tiếp lật về mặt trước mà bỏ qua pha quay của nửa vòng còn lại.
2. **DAO ĐỘNG ĐIỀU HÒA ĐỐI XỨNG QUA TÂM (N FRAMES):** 
   * Chu kỳ dao động con lắc/chuông reo BẮT BUỘC quét qua cả 2 phía đối diện của trục tâm cân bằng. CẤM kẹt dao động ở một nửa bán cầu.
   * Bóng tiếp đất trên sàn BẮT BUỘC trượt ngang đồng bộ với trục X của vật thể treo bên trên: $X_{\text{bóng}}(i) = X_{\text{vật}}(i)$.
3. **BƯỚC CHÂN ĐA CHI PHÂN PHA SO LE & BÓNG MŨI CHÂN TIẾP SÀN:** 
   * Bọ máy/sinh vật 4 chân BẮT BUỘC bước so le theo cặp chéo góc (Trước-Trái đi cùng Sau-Phải nhấc bước $\rightarrow$ cặp còn lại cắm sàn làm trụ). CẤM cử động đối xứng hai bên cùng lúc như bơi ếch.
   * **Bắt buộc đốm bóng tiếp xúc mũi chân:** Từng mũi chân khi cắm sàn BẮT BUỘC phải có 1 pixel bóng râm tiếp xúc màu tối (`S`) ngay dưới đầu móng chân. Khi chân nhấc lên không trung, đốm bóng này phải biến mất hoặc tách rời.
4. **TÍNH LIÊN TỤC CỦA VÒNG LẶP CHU KỲ (LOOP CONTINUITY & PHASING):** 
   * Đối với hoạt ảnh chu kỳ lặp ($N$ frames): Frame cuối cùng ($Frame_N$) BẮT BUỘC phải là pha trung gian chuyển tiếp (Transition/Cooldown phase) có trọng số hình ảnh hòa hợp giữa trạng thái hoạt động và trạng thái tĩnh của $Frame_1$.
   * TUYỆT ĐỐI CẤM cắt cụt hoạt ảnh khiến $Frame_N$ biến thành trạng thái nghỉ cứng nhắc, gây hiện tượng giật cục (stuttering/jump-cut) khi lặp lại vòng GIF.

## 4. Vận tốc cực đại & Vệt mờ (Smear Frames)
1. **VỆT CHÉM CÁNH CUNG (ARC SLASH SMEAR):** 
   * Tại pha vung vũ khí đạt vận tốc cực đại, lưỡi kiếm biến dạng thành vệt dải vòng cung xé gió (Arc Slash) nối dài từ vị trí bắt đầu vung đến điểm kết thúc. Chuôi vũ khí khóa quanh trục cổ tay.