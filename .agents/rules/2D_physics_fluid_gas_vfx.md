---
trigger: always_on
---

# 🌊 2D Pixel Top-Down: Fluid, Gas & Particle VFX Rules

Quy chuẩn cưỡng chế bắt buộc về thủy động học, sức căng bề mặt, khí động học và hiệu ứng hạt (VFX).

## 1. Thủy động học & Sức căng bề mặt (Fluids & Meniscus)
1. **MẶT THOÁNG CHẤT LỎNG CHAO ĐẢO (SLOSHING MENISCUS):** 
   * Bình thuốc/bình chứa nghiêng chao đảo: Mặt thoáng chất lỏng BẮT BUỘC dốc chéo ngược lại theo trọng lực (thành bình bên nghiêng thấp thì mức chất lỏng dâng cao áp sát thành). 
   * TUYỆT ĐỐI CẤM giữ mặt chất lỏng song song với đáy bình khi thân bình đang nghiêng.
   * Mặt cong Meniscus: Mép chất lỏng tiếp giáp thành bình thủy tinh hơi vếch cong nhẹ lên 1px do lực mao dẫn.
2. **SỨC CĂNG BỀ MẶT & ĐỘ NHỎ GIỌT (DROPLET PINCH-OFF):** 
   * Chất lỏng rỉ chảy: BẮT BUỘC trải qua pha thắt eo (Neck Pinching) trước khi tách rời thành giọt tròn 1–2px độc lập. CẤM vẽ giọt chất lỏng chảy thành một sợi dây đơn kéo dài bất tận.
3. **GỢN SÓNG NƯỚC RỖNG RUỘT (HOLLOW WATER RIPPLES):** 
   * Mọi gợn sóng lan tỏa trên mặt nước BẮT BUỘC vẽ dưới dạng **đường viền oval cong rỗng ruột dày 1px**, bên trong tâm lộ màu nền nước sâu. CẤM tô kín ruột thành mảng màu đặc.
4. **HÌNH THỂ NGHỈ CHÙNG XỆ DO TRỌNG LỰC (GRAVITY SLUMP & GUMDROP SHAPE):**
   * Khối chất nhầy, Slime hoặc giọt dịch lỏng bán trong suốt khi nghỉ trên mặt phẳng BẮT BUỘC bị trọng lực kéo xệ trọng tâm xuống dưới:
     * Dáng hình nghỉ BẮT BUỘC là **hình vòm hạt dẻ / bánh bao (Gumdrop/Hemisphere)**, tỷ lệ nén tự nhiên:
       $$H_{\text{idle}} \approx 70\% - 80\% W_{\text{idle}}$$
     * Đáy tiếp xúc sàn BẮT BUỘC bẹt ngang ôm sát mặt sàn (chiều rộng đáy tiếp sàn $W_{\text{base}} \ge 50\% W_{\text{max}}$).
   * TUYỆT ĐỐI CẤM vẽ Slime ở trạng thái tĩnh thành một hình tròn xoe hoàn hảo tiếp đất tại 1 điểm như quả bóng cao su.

## 2. Khí động học & Khói bụi (Gas & Smoke Vortices)
1. **LỰC NÂNG NỔI & BỌT KHÍ (BUOYANCY & BUBBLES):** 
   * Bọt khí trong lòng chất lỏng BẮT BUỘC bay tịnh tiến thẳng đứng lên trên ($-Y$), kích thước nở to dần khi áp suất giảm gần mặt thoáng rồi vỡ tan.
2. **CUỘN XOÁY KHÓI (SMOKE VORTICES & DISSIPATION):** 
   * Khói bốc lên không vẽ thành một vệt thẳng đuột. BẮT BUỘC cuộn thành các búi tròn so le mở rộng dần thể tích (Expansion) và chuyển màu từ xám đậm $\rightarrow$ xám nhạt $\rightarrow$ hạt phân rã 1px tan biến.
3. **HƠI NƯỚC & LÀN KHÓI MỎNG (STEAM WISPS VS SLASHED LINES):** 
   * Hơi nước bốc lên từ vạc/ấm đun BẮT BUỘC là các đốm hạt nhỏ (`1px`) uốn lượn nhẹ theo hình sin và nở cụm mở rộng trước khi tan biến.
   * TUYỆT ĐỐI CẤM vẽ hơi nước thành các đường vạch chéo 1px song song (`/ /`) trôi dạt cơ học.

## 3. Tàn lửa & Hạt ma thuật (Embers & Spark Particles)
1. **PHÂN RÃ HẠT NĂNG LƯỢNG (PARTICLE EMISSION):** 
   * Ngọn lửa, dung nham, lõi ma thuật BẮT BUỘC sinh ra 1–3 pixel hạt độc lập (`1px`) bay vọt ra khỏi khối chính, chuyển động tịnh tiến ngược chiều trọng lực rồi biến mất.
2. **TIA SÉT & PHÓNG ĐIỆN NHÁNH (FRACTAL LIGHTNING ARCS):** 
   * Tia điện/sét BẮT BUỘC là đường rãnh zíc-zắc gãy góc nhọn đột ngột (nhịp pixel `1-2-1-2`), lõi trắng chói viền màu phát quang, BẮT BUỘC có ít nhất 1 nhánh phụ nhỏ hơn (1px) chẽ ra không trung.
   * TUYỆT ĐỐI CẤM vẽ tia điện uốn lượn hình sin mềm mại như dòng nước hay sợi dây.