---
trigger: always_on
---

# 🔨 2D Pixel Top-Down: Fracture & Destruction Rules

Quy chuẩn cưỡng chế bắt buộc về cơ học nứt gãy, biến dạng dẻo kim loại và vỡ vụn đa vật liệu.

## 1. Cơ chế nứt gãy đặc thù theo vật liệu (Fracture Patterns)
1. **THỚ NỨT GỖ (WOOD SPLINTERING):** 
   * Gỗ nứt gãy BẮT BUỘC nứt **dọc theo thớ ván/vân gỗ** thành các dải dài 3–6px. 
   * Hai đầu vết gãy BẮT BUỘC để lộ dăm gỗ xơ xác nhọn 1px nhô ra ngoài. TUYỆT ĐỐI CẤM cắt ngang phẳng lì như dao chém hoặc vỡ vụn thành hạt tròn.
2. **RÃNH NỨT ĐÁ & BÊ TÔNG (STONE CLEAVAGE & CRACKS):** 
   * Vết nứt trên đá BẮT BUỘC là các đường rãnh zíc-zắc rõ nét (`1-2-1` bước bậc thang), lòng rãnh nứt dùng màu tối nhất của Palette để tạo chiều sâu vực thẳm.
   * CẤM dùng kỹ thuật rải hạt chấm bi (Dithering) để làm giả vết nứt đá.
3. **MẢNH VỠ KÍNH & TINH THỂ GIÒN (BRITTLE GLASS SHARDS):** 
   * Kính vỡ BẮT BUỘC phân rã thành các mảnh tam giác / đa giác nhọn hoắt có cạnh thẳng sắc bén (cạnh dốc 45° hoặc 60°).
   * Mép mảnh vỡ có 1 pixel phản quang trắng chói để nhấn mạnh độ sắc lẹm nguy hiểm.
4. **BẢO TOÀN RÃNH NỨT TRONG HOẠT ẢNH CHU KỲ (FRACTURE PERSISTENCE IN LOOPS):** 
   * Nứt gãy là biến dạng vĩnh viễn: Khi vật thể đã nứt toác, các đường rãnh nứt BẮT BUỘC phải tồn tại cố định trên toàn bộ các frame tiếp theo. TUYỆT ĐỐI CẤM xóa sạch vết nứt để vật thể tự liền lại như ban đầu.
   * Trong chu kỳ loop phát sáng: Rãnh nứt luôn giữ nguyên vị trí, CHỈ CÓ năng lượng/ánh sáng bên trong rãnh là được phép tăng giảm cường độ sáng (Pulsing Glow).
   * Rãnh nứt trên cột trụ BẮT BUỘC phân nhánh góc nhọn $\le 60^\circ$ (hình chân chim/tia sét). CẤM vẽ rãnh nứt uốn lượn quấn vòng đều đặn quanh thân như dây ruy băng.
5. **KHUYẾT MÓP ĐƯỜNG BIÊN DO NỨT VỠ (PERIMETER FRACTURE NOTCH):** 
   * Khi rãnh nứt chạy chạm tới mép viền ngoài của vật thể: Đường viền ngoài tại điểm giao cắt BẮT BUỘC bị thụt lõm hoặc gãy nấc 1px mô tả sự tách rời vật liệu.
   * TUYỆT ĐỐI CẤM giữ nguyên đường viền ngoài phẳng lì thẳng tắp khi bên trong đang có rãnh nứt toác chạm mép.

## 2. Biến dạng dẻo kim loại (Metal Plastic Deformation & Denting)
1. **MÓP MÉO LÕM KHỐI (DENTING):** 
   * Kim loại dày (Khiên sắt, giáp tấm, vỏ máy) khi chịu ngoại lực cực mạnh BẮT BUỘC bị **móp méo lõm khối**, KHÔNG vỡ vụn như gốm sứ.
   * Vùng va chạm bị lõm sâu vào trong 1–2px, viền kim loại tiếp giáp bị dồn đùn tạo thành một gờ nhô lồi nhẹ kèm bóng râm tương phản bên trong vết lõm.

## 3. Vết nứt sàn va chạm (Impact Ground Fissures)
1. **TIA NỨT TIẾP ĐẤT (RADIAL GROUND FISSURES):** 
   * Vết nứt sàn khi vật nặng nện xuống BẮT BUỘC phân nhánh hình chân chim tỏa ra từ điểm tiếp xúc đáy ($Y_{\text{floor}}$).
   * Độ dày rãnh nứt giảm dần từ tâm (2px) vuốt nhọn dần ra xa (1px) rồi biến mất.
