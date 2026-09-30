---
name: avian-bird-animator
description: >-
  Chuyên gia thiết kế và hoạt ảnh loài chim, sinh vật có cánh (quạ, đại bàng, bồ
  câu, dơi, rồng bay) góc nhìn Top-Down 3/4. Kích hoạt khi nhắc tới chim, bird,
  quạ, sải cánh, đập cánh, bay lượn, cánh dơi, đại bàng, rồng bay.
---

# 🦅 Avian & Winged Creature Animator Skill

Kỹ năng chuyên biệt hướng dẫn AI giải phẫu khớp cánh lông vũ/màng da, hoạt ảnh tư thế đậu (Perched Idle) và động lực học chu kỳ đập cánh (Flap Cycle) cùng bóng đổ trục Z chuẩn xác trong không gian Top-Down 3/4.

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu prompt người dùng có yêu cầu kích thước (`16x16`, `24x24`, `32x32`, `48x48`, `64x64`), AI phải dựng sprite theo kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO:
    * Dùng `32x32` cho chim sẻ, bồ câu, quạ, dơi nhỏ.
    * Dùng `48x48` hoặc `64x64` cho đại bàng, kền kền, sải cánh lớn, rồng bay.

---

## 2. Hoạt Ảnh Tư Thế Đậu Tĩnh (Perched Idle 4 - 6 Frames)
1. **Khóa khớp cánh gấp chữ V (Folded Wing Lock):**
   * BẮT BUỘC: Khi chim đậu trên cành hoặc bệ đá, hai cánh gấp chéo gọn gàng sau lưng tạo thành vòm chữ V dốc xuống.
   * Lông bay chính (Primaries) xếp chồng lên nhau vắt qua gốc đuôi.
   * Đuôi cụp chéo xuống dưới bệ đỡ góc $30^\circ - 45^\circ$.
2. **Nhịp ngó nghiêng giật nấc (Staccato Head Bobbing):**
   * Chuyển động quan sát của loài chim diễn ra theo các xung giật dứt khoát (1 frame giật quay đầu $\rightarrow$ giữ nguyên 2–3 frames đứng yên quan sát $\rightarrow$ giật nhấp nhô đầu 1px).
   * TUYỆT ĐỐI CẤM: Vẽ đầu chim xoay êm đều như người vặn cổ.

---

## 3. Động Lực Học Chu Kỳ Đập Cánh (Flap Cycle 4 - 6 Frames)
Hoạt ảnh đập cánh bay lượn BẮT BUỘC tuân thủ 2 pha khí động học đối lập:

```
[ PHA 1: VỖ XUỐNG - DOWNSTROKE ]  -> Sinh lực nâng (Power Stroke)
Frame 1: Đỉnh đón gió (Apex Up)   -> Hai đầu cánh giương cao trên lưng (W hẹp, H cao)
Frame 2: Quạt chém (Power Snap)  -> Cánh quạt mạnh xuống, sải cánh bung cực đại (+W max)
Frame 3: Ép đáy (Bottom Push)    -> Đầu cánh chúc xuống dưới, thân chim NẨY LÊN (-Y 1-2px)

[ PHA 2: THU CÁNH LƯỚT - UPSTROKE ] -> Giảm lực cản khí (Recovery Stroke)
Frame 4: Gập cổ tay (Wrist Flex) -> Cánh gập co rút sát vào nách, diện tích cản gió thu nhỏ (-W)
Frame 5: Trượt vươn (Gliding Rise)-> Mép cánh sắc lướt ngược lên trên, thân chim chìm nhẹ (+Y 1px)
Frame 6: Trở về đỉnh đón gió   -> Loop về Frame 1
```

* **Ràng buộc cưỡng chế:**
  * BẮT BUỘC: Khi cánh bung quạt cực đại (Frame 2), chiều rộng sải cánh $W$ phải nở rộng tối thiểu $150\% - 200\%$ so với thân chim.
  * BẮT BUỘC: Thân chim phải có độ nảy đồng bộ ngược chiều với cánh: Cánh đập chúc xuống $\rightarrow$ Thân chim bị phản lực đẩy nhô lên trên ($-Y$).
  * TUYỆT ĐỐI CẤM: Giữ nguyên sải cánh phẳng lì rồi chỉ xoay lật góc 2D đơn giản.

---

## 4. Tách Rời Bóng Trục Z Khi Bay Cao ([Kinematics Rule 1.1](../../rules/2D_physics_kinematics_motion.md))
1. **Khóa mặt đất cho vệt bóng đổ `S`:**
   * BẮT BUỘC: Tọa độ Y của vệt bóng đất `S` luôn nằm cố định trên mặt sàn nhà/ngọn cây.
2. **Tương quan cao độ và độ thu nhỏ của bóng:**
   * Khi chim bay lượn ở cao độ cao: Vệt bóng tiếp đất `S` phải **co nhỏ dần** tỷ lệ nghịch với khoảng cách ($W_{\text{bóng}} \approx 30\% - 50\% W_{\text{thân}}$) và có thể dịch chuyển lệch so với thân chim theo hướng chiếu nghiêng của ánh sáng mặt trời.
   * TUYỆT ĐỐI CẤM: Vẽ bóng dính chặt vào móng chân chim khi chim đang ở tư thế sải cánh bay trên không.

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault`:
  * Quạ đen / Cánh sẫm: `k` (`#2E222F`), `l` (`#3E3546`), `m` (`#625565`), `p` (`#694F62`).
  * Đại bàng / Nâu lông vũ: `D` (`#7A3045`), `E` (`#9E4539`), `F` (`#CD683D`), `G` (`#E6904E`), `t` (`#FFFFFF`).
  * Mỏ & Móng vàng kim: `C` (`#F9C22B`), `B` (`#F79617`), `H` (`#FBB954`).
  * Mắt chim: `z` (`#E83B3B`) hoặc `k` (`#2E222F`) viền `t` (`#FFFFFF`).
  * Bóng sàn trục Z: `S` (`#1A1018`, Alpha 130).
