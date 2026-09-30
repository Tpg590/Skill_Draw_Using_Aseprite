---
name: color-palette-vault
description: >-
  Thư viện tra cứu bảng màu Pixel Art kinh điển (Sunset, Resurrect-64). Tự động
  cung cấp bảng ánh xạ Palette 1 ký tự duy nhất và dải màu Hue-shifting cho script Lua.
---

# 🎨 Color Palette Vault (Sunset & Resurrect-64)

Tài liệu cung cấp danh mục mã màu chuẩn hóa và bảng ký hiệu đơn (Single-character Key) dùng trực tiếp trong ma trận ký tự của script Aseprite Lua.

---

## 1. Sunset Palette (20 Colors)
Bảng màu hoàng hôn rực rỡ, chuyên dùng cho hiệu ứng OSL ấm áp, bầu trời chiều tà, dung nham ma thuật và năng lượng hư không.

### Bảng ánh xạ ký tự Lua (`Sunset`)
* Ký hiệu `.` mặc định là trong suốt (`nil`), `S` là bóng đất tiếp xúc (`#000000`, Alpha 130).

| Ký tự | Mã HEX | Sắc thái / Nhóm công năng |
| :---: | :---: | :--- |
| `0` | `#000000` | Đen tuyền / Viền tối sâu |
| `1` | `#350769` | Tím đêm cực sẫm |
| `2` | `#3B0769` | Tím thẫm |
| `3` | `#480769` | Tím than |
| `4` | `#540769` | Tím đậm |
| `5` | `#5F0769` | Tím hoa cà sẫm |
| `6` | `#6B115F` | Tím mận |
| `7` | `#99197D` | Tím hồng cánh sen |
| `8` | `#C43F86` | Hồng tím tươi |
| `9` | `#DE458F` | Hồng neon |
| `a` | `#ED6056` | Cam đỏ san hô |
| `b` | `#E87503` | Cam lửa cháy |
| `c` | `#E69005` | Cam hổ phách |
| `d` | `#E6A307` | Vàng cam mật ong |
| `e` | `#E6BD09` | Vàng mù tạt |
| `f` | `#E6D709` | Vàng chanh tươi |
| `g` | `#EDE056` | Vàng bơ nhạt |
| `h` | `#F2E67B` | Vàng kem sáng |
| `i` | `#F7F0BC` | Trắng ngà đón sáng |
| `j` | `#FFFFFF` | Trắng tinh / Highlight tối cao |

---

## 2. Resurrect-64 Palette (64 Colors)
Bảng màu toàn diện 64 sắc độ cân bằng hoàn hảo cho Game RPG/Top-Down (Đất đá, gỗ, kim loại, da thịt hữu cơ, ma thuật).

### Bảng ánh xạ ký tự Lua (`Resurrect-64`)
* Ký hiệu `.` mặc định là trong suốt (`nil`).
* **QUYỀN ĐỘC QUYỀN TOÀN HỆ THỐNG CỦA KÝ TỰ `S`**: Ký tự `S` được **KHÓA CHẾT ĐỘC QUYỀN** cho **Bóng Đổ Tiếp Đất (Ground Contact Shadow, Alpha 130)**. TUYỆT ĐỐI CẤM gán ký tự `S` cho bất kỳ màu vật liệu thông thường nào.
* Ký tự màu phân biệt hoa thường (`a-z`, `A-Z`, `0-9`, các ký tự đặc biệt như `~`, `!`, `@`, `#`, `$`, `^`, `*`, `_`, `-`, `&`, `(`, `)`). Tuyệt đối mỗi màu là 1 ký tự đơn.

#### Nhóm Trung Tính, Đá & Kim Loại Lạnh (Neutral, Stone & Steel)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `k` | `#2E222F` | Đen tím viền | `p` | `#694F62` | Tím xám tối |
| `l` | `#3E3546` | Xám đen đá | `q` | `#7F708A` | Xám chì |
| `m` | `#625565` | Xám đá trung tính | `r` | `#9BABB2` | Bạc sáng |
| `n` | `#966C6C` | Nâu xám nhạt | `s` | `#C7DCD0` | Trắng bạc ánh xanh |
| `o` | `#AB947A` | Cát vàng xỉn | `t` | `#FFFFFF` | Trắng tinh Specular |

#### Nhóm Đỏ, Cam & Lửa (Reds, Oranges & Fire)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `u` | `#6E2727` | Đỏ thẫm bóng | `z` | `#E83B3B` | Đỏ tươi |
| `v` | `#B33831` | Đỏ gạch | `A` | `#FB6B1D` | Cam lửa rực |
| `w` | `#EA4F36` | Đỏ cam | `B` | `#F79617` | Vàng cam đậm |
| `x` | `#F57D4A` | Cam đào sáng | `C` | `#F9C22B` | Vàng kim loại sáng |
| `y` | `#AE2334` | Đỏ mận sẫm | | | |

#### Nhóm Nâu Gỗ, Đất & Vàng Đồng (Browns, Wood & Brass)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `D` | `#7A3045` | Nâu đỏ vỏ cây | `I` | `#4C3E24` | Nâu rêu đáy |
| `E` | `#9E4539` | Nâu đất nung | `J` | `#676633` | Vàng rêu úa |
| `F` | `#CD683D` | Nâu gỗ sồi | `K` | `#A2A947` | Xanh cỏ úa |
| `G` | `#E6904E` | Vàng gỗ sáng | `L` | `#D5E04B` | Vàng chanh lá |
| `H` | `#FBB954` | Vàng hổ phách | `M` | `#FBFF86` | Vàng rực đón sáng |

#### Nhóm Xanh Lá Cây & Độc Dược (Greens & Flora)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `N` | `#165A4C` | Lục sẫm rừng già | `~` | `#313638` | Đen xám than |
| `O` | `#239063` | Xanh ngọc đậm | `T` | `#374E4A` | Rêu xám tối |
| `P` | `#1EBC73` | Lục bảo tươi | `U` | `#547E64` | Xanh lính |
| `Q` | `#91DB69` | Lục non | `V` | `#92A984` | Xám rêu nhạt |
| `R` | `#CDDF6C` | Đọt chuối sáng | `W` | `#B2BA90` | Trắng ngà ánh lục |

#### Nhóm Nước Biển & Cyan Ma Thuật (Cyan, Sea & Mana)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `X` | `#0B5E65` | Lam sẫm vực sâu | `2` | `#323353` | Xanh navy đáy biển |
| `Y` | `#0B8A8F` | Xanh mòng két | `3` | `#484A77` | Lam tím đậm |
| `Z` | `#0EAF9B` | Xanh ngọc biển | `4` | `#4D65B4` | Xanh coban |
| `0` | `#30E1B9` | Cyan neon sáng | `5` | `#4D9BE6` | Xanh da trời tươi |
| `1` | `#8FF8E2` | Băng tuyết phát quang | `6` | `#8FD3FF` | Lam nhạt đón sáng |

#### Nhóm Tím Hư Không, Hồng Ma Pháp & Da Hữu Cơ (Purples, Pinks & Skin)
| Key | HEX | Mô tả | Key | HEX | Mô tả |
| :---: | :---: | :--- | :---: | :---: | :--- |
| `7` | `#45293F` | Tím than hư không | `!` | `#831C5D` | Đỏ tía sẫm |
| `8` | `#6B3E75` | Tím ma thuật tối | `@` | `#C32454` | Hồng cánh sen đậm |
| `9` | `#905EA9` | Tím thạch anh | `#` | `#F04F78` | Đỏ hồng tươi |
| `$` | `#A884F3` | Tím dạ quang | `%` | `#F68181` | Hồng san hô nhạt |
| `^` | `#EAADED` | Hồng phấn ma pháp | `&` | `#FCA790` | Màu da người sáng |
| `*` | `#753C54` | Đỏ mận xỉn | `(` | `#FDCBB0` | Da ngà bắt sáng |
| `_` | `#A24B6F` | Hồng tím trung tính | `)` | `#CF657F` | Thịt hồng hữu cơ |
| `-` | `#ED8099` | Hồng tươi da thịt | | | |

---

## 3. Cách Sử Dụng Trong Script Lua
Khi tạo sprite theo phong cách chỉ định, chỉ cần nhặt các cặp Key-HEX cần dùng gán vào bảng `PALETTE` của script:

```lua
-- Ví dụ 1: Trích xuất dải Sunset cho hiệu ứng quả cầu lửa:
local PALETTE = {
    ["."] = nil,       -- Trong suốt
    ["0"] = "#000000", -- Viền ngoài
    ["b"] = "#E87503", -- Vùng tối ngọn lửa
    ["d"] = "#E6A307", -- Màu thân lửa
    ["f"] = "#E6D709", -- Vùng sáng
    ["j"] = "#FFFFFF", -- Lõi sáng chói
    ["S"] = "#000000"  -- Bóng sàn tiếp đất (ĐỘC QUYỀN TOÀN HỆ THỐNG: Alpha 130)
}

-- Ví dụ 2: Trích xuất dải Resurrect-64 cho thực vật / quái rêu đá:
local PALETTE_FLORA = {
    ["."] = nil,       -- Trong suốt
    ["~"] = "#313638", -- Đen xám than / Rêu đá (Alpha 255 đầy đủ, KHÔNG BỊ MỜ)
    ["T"] = "#374E4A", -- Rêu xám tối
    ["N"] = "#165A4C", -- Lục sẫm rừng già
    ["P"] = "#1EBC73", -- Lục bảo tươi
    ["Q"] = "#91DB69", -- Lục non đón sáng
    ["S"] = "#140c1a"  -- Bóng sàn tiếp đất (ĐỘC QUYỀN TOÀN HỆ THỐNG: Alpha 130)
}
```