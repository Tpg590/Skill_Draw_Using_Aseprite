---
name: humanoid-character-sprite
description: >-
  Chuyên gia thiết kế sprite và hoạt họa nhân vật người (Player, NPC, Hiệp sĩ,
  Pháp sư, Quái hình người) góc nhìn Top-Down 3/4 đa hướng. Kích hoạt khi nhắc
  tới nhân vật, player, npc, human, knight, mage, walk cycle người, idle người.
---

# 🚶 Humanoid Character Sprite & Animation Skill

Kỹ năng chuyên biệt hướng dẫn AI thiết kế cấu trúc giải phẫu pixel, tạo hình đa hướng và chu kỳ hoạt họa bước chân (Walk Cycle) chuẩn xác cho nhân vật hình người góc nhìn Top-Down 3/4.

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu prompt người dùng có định dạng kích thước cụ thể (`16x16`, `24x24`, `32x32`, `48x48`, `64x64`), AI phải dựng sprite và hoạt họa theo đúng kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO:
    * Dùng `32x32` cho nhân vật chuẩn Chibi / RPG cổ điển (2.5–3 đầu).
    * Dùng `48x48` cho nhân vật tỷ lệ chi tiết cao, giáp trụ phức tạp hoặc vũ khí lớn (3.5–4.5 đầu).

---

## 2. Tỷ Lệ Giải Phẫu Pixel & Phân Tầng Z-Index
1. **Tỷ lệ đầu - thân trong Pixel Art:**
   * **Chuẩn Chibi (2.5 đầu - Grid 32x32):**
     * Đầu (bao gồm tóc/mũ): chiếm ~45% chiều cao ($12\text{px} - 14\text{px}$).
     * Thân & Tay: chiếm ~30% chiều cao ($8\text{px} - 9\text{px}$).
     * Chân & Giày: chiếm ~25% chiều cao ($6\text{px} - 7\text{px}$).
   * **Chuẩn Heroic (3.5 - 4 đầu - Grid 48x48):**
     * Đầu: 10px–12px | Thân áo: 14px–16px | Chân: 14px–16px.
2. **Quy tắc phân tầng Z-Index (Che khuất trước sau):**
   * BẮT BUỘC sắp xếp lớp vẽ theo thứ tự từ sau ra trước:
     $$\text{Áo choàng sau} \rightarrow \text{Tay sau/Vũ khí phụ} \rightarrow \text{Chân} \rightarrow \text{Thân áo/Giáp ngực} \rightarrow \text{Đầu/Mặt} \rightarrow \text{Tóc/Mũ phía trước} \rightarrow \text{Tay trước/Vũ khí chính}$$
   * TUYỆT ĐỐI CẤM: Để tay sau hoặc áo choàng sau vẽ đè lên giáp ngực hoặc mặt nhân vật.

---

## 3. Góc Nhìn 4 Hướng Top-Down 3/4 (Cardinal Directions)
Trong góc nhìn Top-Down 3/4, góc camera nghiêng $45^\circ - 60^\circ$ từ trên xuống:

1. **Hướng Xuống / Trực Diện (Down / South - Chiều $+Y$):**
   * BẮT BUỘC: Thấy rõ đỉnh đầu và mái tóc nghiêng về trước, trán, mắt, chóp mũi (1px), cằm, ngực áo, thắt lưng và mũi hai bàn chân chĩa chúc xuống phía trước màn hình.
   * Chân sau bị thân áo che khuất một phần.
2. **Hướng Lên / Sau Lưng (Up / North - Chiều $-Y$):**
   * BẮT BUỘC: Thấy đỉnh đầu, búi tóc/gáy, cổ áo sau, lưng áo/áo choàng, gót chân hướng lên trên.
   * TUYỆT ĐỐI CẤM: Vẽ mắt, mũi hoặc mặt trong hướng nhìn này.
3. **Hướng Ngang (Side / East-West - Chiều $\pm X$):**
   * Thân người xoay nghiêng $3/4$: Một bên vai và cánh tay vươn về phía trước màn hình, cánh tay phía sau thu nhỏ hoặc chỉ lộ một phần viền tối.
   * Mũi giày vươn cong theo hướng di chuyển.

---

## 4. Chu Kỳ Hoạt Họa Bước Chân (Walk Cycle 4 - 6 - 8 Frames)
Chu kỳ bước chân cơ bản gồm 4 pha động lực học chuẩn (chu kỳ lặp 6 hoặc 8 frames cho chuyển động mượt mà):

```
Frame 1: Tiếp đất (Contact L)  -> Chân Trái choãi trước, Chân Phải duỗi sau
Frame 2: Trùng chân (Down)      -> Chân trước gập gối chịu lực, Đầu & Thân TỤT XUỐNG 1px
Frame 3: Vượt chân (Passing)   -> Chân sau nhấc co gối vượt qua chân trụ, Thân về độ cao chuẩn
Frame 4: Nhón chân (Up)         -> Chân trụ nhón gót đẩy đà, Đầu & Thân NHÔ CAO 1px
Frame 5: Tiếp đất (Contact R)  -> Chân Phải choãi trước, Chân Trái duỗi sau
Frame 6: Trùng chân (Down)      -> Chân phải chịu lực, Đầu & Thân TỤT XUỐNG 1px
Frame 7: Vượt chân (Passing)   -> Chân trái nhấc co gối vượt qua chân trụ
Frame 8: Nhón chân (Up)         -> Chân phải đẩy đà, Đầu & Thân NHÔ CAO 1px -> Loop F1
```

* **Quy chuẩn dao động trục Y (Head Bobbing):**
  * BẮT BUỘC: Đầu và thân nhân vật nhấp nhô theo nhịp $\Delta Y = [0, +1, 0, -1, 0, +1, 0, -1]\text{px}$.
  * TUYỆT ĐỐI CẤM: Giữ nguyên tọa độ Y của đầu đứng im phắc suốt chu kỳ bước chân (khiến nhân vật bị cảm giác trôi trượt như đi giày patin).
* **Đánh tay ngược pha (Arm Swing Antiphase):**
  * BẮT BUỘC: Tay Trái đánh về phía trước thì Chân Phải bước tới (nghịch pha $180^\circ$).
* **Bóng tiếp đất trục Z ([Kinematics Rule 1.1](../../rules/2D_physics_kinematics_motion.md)):**
  * BẮT BUỘC: Tọa độ Y của vệt bóng đất `S` khóa chết cố định trên sàn nhà (ngay dưới điểm tiếp xúc thấp nhất). Khi nhân vật nhún chân xuống, bóng nở rộng bè ngang 1px; khi nhón chân lên, bóng co lại 1px.

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault`:
  * Da người: `&` (`#FCA790`), `(` (`#FDCBB0`), `)` (`#CF657F`).
  * Giáp thép / Kim loại: `l` (`#3E3546`), `m` (`#625565`), `r` (`#9BABB2`), `t` (`#FFFFFF`).
  * Vải áo / Tóc: Nhóm Đỏ `u, v, z` hoặc Nâu gỗ `D, E, F` hoặc Xanh navy `2, 3, 4`.
  * Bóng sàn tiếp xúc: `S` (Alpha 130).
