---
name: marine-aquatic-animator
description: >-
  Chuyên gia thiết kế sinh vật thủy sinh, hải sản (cá, mực, bạch tuộc, tôm, cua,
  sao biển) trong môi trường nước hoặc góc nhìn Top-Down. Kích hoạt khi nhắc tới
  cá, mực, bạch tuộc, tôm, cua, hải sản, sinh vật biển, bơi lội, aquatic, fish.
---

# 🐙 Marine & Aquatic Creature Animator Skill

Kỹ năng chuyên biệt hướng dẫn AI giải phẫu động vật dưới nước, hoạt họa uốn sóng đuôi cá (Fish Wave), cơ chế phản lực phụt nước của loài chân đầu (Cephalopod Jet Propulsion) và búng đuôi lùi của tôm giáp xác (Crustacean Tail-Flip).

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu người dùng khai báo kích thước cụ thể (`16x16`, `24x24`, `32x32`, `48x48`, `64x64`), AI phải tuân thủ kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO:
    * Dùng `32x32` cho cá nhỏ, cua, sao biển, tôm nhỏ.
    * Dùng `48x48` cho mực nang, bạch tuộc xúc tu dài, cá đuối, cá mập.

---

## 2. Động Học Uốn Sóng Bơi Của Loài Cá (Fish Swimming Wave 4 - 6 Frames)
1. **Truyền sóng cơ học từ đầu đến đuôi:**
   * BẮT BUỘC: Đầu cá gần như giữ thăng bằng cố định (chỉ lắc nhẹ $\pm 0.5\text{px}$), sóng uốn lượn hình sin chạy dọc từ vây lưng $\rightarrow$ cuống đuôi $\rightarrow$ vây đuôi quạt mạnh sang hai bên.
   * Vây ngực (Pectoral Fins) phe phẩy ngược pha với nhịp quạt đuôi để giữ thăng bằng thủy động học.
2. **Triệt tiêu bóng sàn đặc đen ([Optics Rule 3.2](../../rules/2D_physics_optics_lighting.md)):**
   * TUYỆT ĐỐI CẤM: Vẽ bóng tiếp đất màu đen thui (`S`) dưới đáy canvas khi cá đang bơi lội trong nước.
   * BẮT BUỘC: Thay thế bằng hình ảnh phản chiếu lộn ngược (Inverted-Y) nén dẹt độ mờ trong làn nước, hoặc vệt khúc xạ ánh sáng mặt nước (Caustics highlight 1px) lung linh trên lưng cá.

---

## 3. Phản Lực Phụt Nước Của Mực & Bạch Tuộc (Cephalopod Jet Propulsion 6 Frames)
Chuyển động của loài chân đầu tuân thủ chu kỳ nén xả thủy động học cực gắt:

```
[ PHA 1: NẠP NƯỚC - INHALE SQUASH ]
Frame 1-2: Khoang áo (Mantle) phình to bè ngang (+W, -H). 
           Chùm xúc tu chùng xệ, xòe lững lờ theo dòng nước.

[ PHA 2: PHỤT PHẢN LỰC - JET STRETCH ]
Frame 3:   Khoang áo co siết cực mạnh, biến dạng thuôn nhọn (-W, +H).
           Thân bắn vọt về phía trước với gia tốc cực lớn.
           Toàn bộ chùm xúc tu duỗi thẳng tắp chụm lại thành mũi tên theo luồng nước rẽ.
           Tại miệng ống phụt (Siphon) BẮT BUỘC sinh ra 2-3 bọt khí 1px trôi ngược chiều di chuyển.

[ PHA 3: HÃM TỐC & BUNG NỞ - GLIDE & FLOWER BLOOM ]
Frame 4-5: Gia tốc giảm dần, thân bắt đầu nở nhẹ trở lại.
           Các xúc tu uốn lượn sóng mềm mại, bung nở xòe rộng sang hai bên như cánh hoa.
Frame 6:   Chuyển tiếp êm ái về trạng thái nạp nước -> Loop Frame 1.
```

* **Ràng buộc cưỡng chế:**
  * BẮT BUỘC: Bảo toàn thể tích khi co giãn ([Impact Rule 1.2](../../rules/2D_physics_impact_mechanics.md)). Khi siết phụt nước, thân phải thon dài; khi nạp nước, thân phải phình bè.
  * TUYỆT ĐỐI CẤM: Để xúc tu cứng đơ như cọng kẽm trong pha bơi lướt.

---

## 4. Động Học Búng Đuôi Lùi Của Tôm Giáp Xác (Crustacean Tail-Flip 4 - 6 Frames)
Đặc thù tự vệ của loài tôm/tôm hùm khi gặp nguy hiểm:
1. **Tư thế thủ (Defensive Idle):** Hai càng giương cao mở rộng đón địch, đuôi xòe quạt nhẹ phía sau.
2. **Cú búng cụp đuôi (Explosive Tail-Flip):**
   * Đuôi tôm (Telson/Uropods) gập cụp một góc $180^\circ$ cực nhanh úp sát vào dưới bụng.
   * Lực đẩy nước hất ngược toàn bộ cơ thể tôm bay lùi về phía sau ($-X$ hoặc $-Y$) với vận tốc âm thanh. Hai càng giương thẳng xuôi theo thân để giảm lực cản.
   * Điểm búng đuôi sinh ra một đám mây hạt nước hoặc bụi cát nhỏ 1px.

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault`:
  * Mực / Bạch tuộc / Da đổi màu: `!` (`#831C5D`), `@` (`#C32454`), `#` (`#F04F78`), `$` (`#A884F3`), `^` (`#EAADED`).
  * Cá biển / Nước sâu: `X` (`#0B5E65`), `Y` (`#0B8A8F`), `Z` (`#0EAF9B`), `0` (`#30E1B9`), `1` (`#8FF8E2`).
  * Vỏ tôm cua / Giáp xác đỏ: `u` (`#6E2727`), `v` (`#B33831`), `w` (`#EA4F36`), `A` (`#FB6B1D`).
  * Bọt khí thủy động học: `t` (`#FFFFFF`) hoặc `s` (`#C7DCD0`).
