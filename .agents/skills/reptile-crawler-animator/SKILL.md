---
name: reptile-crawler-animator
description: >-
  Chuyên gia thiết kế bò sát và động vật bò trườn (thằn lằn, cá sấu, rắn, rùa,
  rồng đất) góc nhìn Top-Down 3/4. Kích hoạt khi nhắc tới bò sát, thằn lằn, cá
  sấu, rắn, reptile, rùa, bò trườn, crawler, rồng đất.
---

# 🦎 Reptile & Crawler Animator Skill

Kỹ năng chuyên biệt hướng dẫn AI tạo hình giải phẫu chi choãi ngang (Sprawling Posture), động lực học uốn lượn sóng ngang hình sin (Lateral Undulation) và tả chất liệu vảy sừng thô ráp cho loài bò sát góc nhìn Top-Down 3/4.

---

## 1. Cơ Chế Grid Size Linh Hoạt (Dynamic Grid Size)
* **Quy tắc kiểm tra prompt:**
  * BẮT BUỘC: Nếu người dùng khai báo kích thước cụ thể trong prompt (`16x16`, `24x24`, `32x32`, `48x48`, `64x64`), AI phải dựng sprite theo đúng kích thước đó.
  * MẶC ĐỊNH KHI KHÔNG KHAI BÁO:
    * Dùng `32x32` cho thằn lằn nhỏ, rùa, rắn cuộn.
    * Dùng `48x48` hoặc custom `32x64` cho cá sấu dài, trăn lớn, rồng đất có đuôi quét rộng.

---

## 2. Giải Phẫu Chi Choãi Ngang (Sprawling Posture)
Khác biệt cốt lõi giữa bò sát và động vật có vú:

1. **Khớp chi chìa ngang hông (Lateral Sprawl):**
   * BẮT BUỘC: Khớp khuỷu tay và khớp gối bẻ gập ngang sang hai bên sườn ($90^\circ$ so với trục thân). Xương cánh tay vươn ngang ra ngoài rồi mới dốc cẳng chân xuống cắm móng xuống sàn.
   * TUYỆT ĐỐI CẤM: Cắm chân thẳng đứng song song dưới bụng như chó mèo hoặc ngựa.
2. **Trọng tâm áp sát mặt sàn (Low Center of Mass):**
   * Bụng và ức ngực nằm chỉ cách mặt sàn $1\text{px} - 2\text{px}$, vệt bóng tiếp xúc `S` ôm trọn gần như toàn bộ phần bụng và đuôi dưới đáy.
   * Đuôi dài quét là là mặt đất, uốn theo quán tính của từng bước chân.

---

## 3. Động Lực Học Sóng Ngang Hình Sin (Lateral Undulation 6 - 8 Frames)
Chuyển động bò của thằn lằn, cá sấu và trườn của rắn xuất phát từ sự co rút cơ luân phiên của cột sống:

```
Pha 1: Thân uốn cong chữ C sang TRÁI -> Chân Trước-Trái (FL) cùng Sau-Phải (HR) vươn tới
Pha 2: Đầu chúc nhẹ sang phải        -> Cột sống truyền xung sóng uốn lượn xuống hông
Pha 3: Đỉnh sóng trôi xuống Đuôi    -> Đuôi quất cong sang TRÁI theo quán tính trễ pha
Pha 4: Thân uốn cong chữ C sang PHẢI -> Chân Trước-Phải (FR) cùng Sau-Trái (HL) vươn tới
Pha 5: Đầu chúc nhẹ sang trái        -> Xung sóng truyền xuống hông
Pha 6: Đuôi quất cong sang PHẢI      -> Hoàn tất 1 chu kỳ sóng hình sin -> Loop F1
```

* **Ràng buộc cưỡng chế:**
  * BẮT BUỘC: Khi chân Trước-Trái bước lên, mạng sườn bên trái phải co rút lại làm thân uốn cong lõm về phía bên trái.
  * BẮT BUỘC: Đuôi di chuyển trễ pha $1 - 2$ frames so với thân mình ([Kinematics Rule 2.1](../../rules/2D_physics_kinematics_motion.md)), đỉnh sóng uốn lượn trôi dọc từ gốc đuôi ra chóp đuôi.
  * TUYỆT ĐỐI CẤM: Giữ thân thẳng đơ rồi chỉ di chuyển 4 cái chân như rô-bốt.

---

## 4. Tả Chất Liệu Vảy Sừng Bò Sát ([Material Rule 1.2](../../rules/2D_physics_material_rendering.md))
1. **Bề mặt nhám mờ tán xạ rộng (Matte Rough Surface):**
   * BẮT BUỘC: Tạo độ sần sùi của vảy bằng cách đan xen các pixel tối (`Shadow/Crevice`) so le trên nền màu chính (`Midtone`).
   * Phân bổ các gờ gai sừng (Scutes/Ridges) dọc theo sống lưng thành dải pixel 1px nhấp nhô.
2. **Cấm kỵ về Highlight:**
   * TUYỆT ĐỐI CẤM: Dùng điểm trắng tinh `#FFFFFF` làm vệt highlight lớn trên da cá sấu/thằn lằn (tránh gây cảm giác trơn bóng như kim loại hay nhớt nhát như slime). Highlight của da bò sát chỉ được dùng tone màu sáng nhạt cùng tông (Tint).

---

## 5. Quy Chuẩn Script Lua & Bảng Màu 1 Ký Tự
* **Kế thừa bộ khung:** `aseprite-lua-generator` với hàm `renderGrid(img, gridData, pal)`.
* **Ràng buộc Palette:** Mỗi mã Hex gán vào bảng `PALETTE` BẮT BUỘC là 1 ký tự đơn duy nhất. Tra cứu dải màu tương thích từ `color-palette-vault`:
  * Da cá sấu / Rêu sẫm: `N` (`#165A4C`), `O` (`#239063`), `T` (`#374E4A`), `U` (`#547E64`), `V` (`#92A984`).
  * Da thằn lằn sa mạc / Đất nung: `E` (`#9E4539`), `F` (`#CD683D`), `I` (`#4C3E24`), `J` (`#676633`), `o` (`#AB947A`).
  * Mắt bò sát (Đồng tử dẹp đứng): `C` (`#F9C22B`) hoặc `z` (`#E83B3B`), con ngươi `k` (`#2E222F`).
  * Móng vuốt & Răng nhọn: `s` (`#C7DCD0`) hoặc `W` (`#B2BA90`).
  * Bóng sàn tiếp xúc sát đất: `S` (`#1A1018`, Alpha 130).
