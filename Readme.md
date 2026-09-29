## Thông số
*   **Grid Size:** `32x32`, `48x48`, `64x64`, hoặc custom (1 cell/frame).
*   **Art Style:** `Terraria`, `Stardew Valley`, `FreeStyle`.
*   **Asset Type:** `Individual Sprite`, `Tilemap`, `Spritesheet`.
*   **Output Type:** `Static`, `Animation`.
*   **Animation FPS:** `4`, `6`, `8`, `12`, `16`, `24` (Mặc định `8`).


## Example format prompt 
## Cấu hình:

Grid Size: 48x48

Art Style: FreeStyle (Hue-shifting, viền sạch).

Asset Type: Individual Sprite

Output Type: Animation (4 frame: Nước trong bình sủi bọt và phát sáng).

## Chi tiết vật thể:
Một bình thủy tinh cổ lọ chứa chất lỏng màu đỏ rực (chất lỏng phát sáng). Bình được đặt trên một bệ đỡ làm từ những cái rễ cây héo úa vặn xoắn vào nhau.

## Yêu cầu khắt khe (Cạm bẫy)( Có thể bỏ qua):

Quy tắc 3.2.2: Bình phải có vệt highlight trắng cong vắt ngang để thể hiện lớp kính trong suốt. Mặt chất lỏng bên trong phải là đường ellipse, không được làm phẳng.

Quy tắc 3.3 (OSL): Chất lỏng màu đỏ phải phát sáng hắt màu (Color Bleed) xuống các rễ cây bên dưới. Các rễ cây gần bình phải ngả sang tone cam/đỏ thay vì màu nâu tối.

Quy tắc 3.4: Rễ cây uốn lượn ôm lấy đáy bình. CẤM vẽ rễ cây bằng các đường chéo 45 độ thẳng tắp. Vân gỗ trên rễ phải uốn theo chiều vặn xoắn.

## muốn chạy tay thì dùng lệnh .\run_draw.bat <lua_file_name>
.\run_draw.bat scripts\cyan_jelly_slime_48.lua