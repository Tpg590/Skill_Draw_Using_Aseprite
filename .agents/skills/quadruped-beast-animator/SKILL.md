---
name: quadruped-beast-animator
description: >-
  Chuyên gia hoạt họa động vật và quái thú 4 chân (chó, sói, ngựa, hươu, gấu,
  thú cưỡi) góc nhìn Top-Down 3/4. Kích hoạt khi nhắc tới động vật 4 chân, thú,
  chó, sói, ngựa, hươu, gấu, quadruped, thú cưỡi, quái thú 4 chân.
---

# 🐺 Quadruped Beast & Creature Animator Skill

Kỹ năng chuyên biệt hướng dẫn AI giải phẫu chi 4 chân, cấu trúc khớp gập ngược (Digitigrade) và hoạt họa dáng đi so le chéo (Trotting) cùng phi nước đại (Galloping) cho động vật và quái thú góc nhìn Top-Down 3/4.

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu người dùng chỉ định kích thước trong prompt (`24x24`, `32x32`, `48x48`, `64x64`), AI phải tuân thủ nghiêm ngặt kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO:
    * Dùng `48x48` cho thú săn mồi cỡ vừa/lớn (sói, ngựa, hươu, gấu, thú cưỡi, quái vật 4 chân).
    * Dùng `32x32` cho thú nhỏ (mèo, thỏ, chuột, chó con).

---

## 2. Giải Phẫu Khớp Chân Thú Săn Mồi (Digitigrade Anatomy)
1. **Khớp chân sau gập chữ Z (Digitigrade Hock Joint):**
   * BẮT BUỘC: Khớp chân sau của thú ăn thịt/móng guốc (sói, báo, ngựa, hươu) chia làm 3 đoạn gập ngược hình zíc-zắc chữ Z:
     * Đoạn đùi trên: Hướng chếch ra trước.
     * Khớp gót chân (Hock): Nhô cao lên không trung gập gập chéo ra sau.
     * Cổ chân & Bàn chân: Dốc thẳng xuống tiếp đất bằng các đầu ngón/móng.
   * TUYỆT ĐỐI CẤM: Vẽ chân sau thẳng tuột như cột đình hoặc gập đầu gối ra phía trước như chân người (Plantigrade).
2. **Khớp chân trước (Foreleg Scapula & Wrist):**
   * Bả vai trước nhô cao ôm lấy ức ngực, khuỷu tay bẻ ra sau và cổ tay gập nhẹ về trước khi nhấc bước.

---

## 3. Hoạt Họa Dáng Bước So Le Chéo (Trotting Gait 6 - 8 Frames)
Theo quy chuẩn động lực học đa chi ([Kinematics Rule 3.3](../../rules/2D_physics_kinematics_motion.md)):

```
Pha 1 (Diagonal Pair A Move):  Chân Trước-Trái (FL) cùng Sau-Phải (HR) nhấc bước vươn tới
Pha 2 (Diagonal Pair B Stand): Chân Trước-Phải (FR) cùng Sau-Trái (HL) cắm chặt sàn làm trụ
Pha 3 (Contact & Down):        Cặp A chạm đất chịu lực, Đầu & Vai hạ 1px (Down)
Pha 4 (Diagonal Pair B Move):  Chân Trước-Phải (FR) cùng Sau-Trái (HL) nhấc bước vươn tới
Pha 5 (Diagonal Pair A Stand): Cặp A cắm chặt sàn làm trụ
Pha 6 (Contact & Down):        Cặp B chạm đất chịu lực, Đầu & Vai hạ 1px -> Loop F1
```

* **Ràng buộc cưỡng chế:**
  * BẮT BUỘC: Cặp chân chéo góc (FL + HR hoặc FR + HL) luôn chuyển động đồng pha với nhau.
  * TUYỆT ĐỐI CẤM: Cho 2 chân cùng một bên (FL + HL) bước cùng lúc (dáng đi xiêu vẹo Pacing), hoặc cử động 2 chân trước đồng thời như bơi ếch.
* **Đốm bóng tiếp xúc mũi chân (Foot Contact Shadow):**
  * BẮT BUỘC: Từng mũi chân khi cắm sàn phải có **1 pixel bóng râm tiếp xúc màu tối (`S`)** ngay dưới móng chân. Khi chân nhấc lên không trung, đốm bóng này bắt buộc biến mất hoặc tách rời thành vệt mờ trên mặt sàn.

---

## 4. Hoạt Họa Phi Nước Đại (Gallop / Sprint Dynamics)
Khi thú chạy nước đại đạt vận tốc cực đại, chuyển động tuân thủ chuỗi biến dạng co giãn thể tích ([Impact Rule 1.2](../../rules/2D_physics_impact_mechanics.md)):

1. **Pha nén cuộn cột sống (Squash & Gather):**
   * Lưng cuộn vòm cong lên trên. Toàn bộ 4 chân co gấp rút chụm sát vào dưới bụng.
   * Chiều dài thân thu ngắn lại ($W$ giảm ~30%), chiều cao lưng nhô cao ($H$ tăng).
2. **Pha bung duỗi trên không (Full Suspension Stretch):**
   * Cột sống duỗi thẳng tắp và hơi võng nhẹ. Hai chân trước phóng hết cỡ về phía trước, hai chân sau đạp duỗi thẳng hết cỡ ra sau.
   * Toàn bộ cơ thể bay bổng lơ lửng trên không trung, bóng tiếp đất `S` trên sàn co nhỏ lại và trôi theo trục X.
3. **Pha tiếp đất lệch pha (Asymmetric Landing):**
   * Chân trước tiếp sàn trước hãm đà $\rightarrow$ Chân sau vọt lên đè vào trong để chuẩn bị cho chu kỳ nhún tiếp theo.

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault`:
  * Lông thú Nâu/Vàng: `D` (`#7A3045`), `E` (`#9E4539`), `F` (`#CD683D`), `G` (`#E6904E`), `H` (`#FBB954`).
  * Lông thú Xám/Sói bạc: `l` (`#3E3546`), `m` (`#625565`), `q` (`#7F708A`), `r` (`#9BABB2`), `s` (`#C7DCD0`).
  * Mắt thú dữ: `z` (`#E83B3B`) hoặc `C` (`#F9C22B`).
  * Móng vuốt: `t` (`#FFFFFF`) hoặc `k` (`#2E222F`).
  * Bóng sàn chân thú: `S` (`#1A1018`, Alpha 130).
