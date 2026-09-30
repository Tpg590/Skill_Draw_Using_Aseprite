import os
from PIL import Image

W, H = 48, 48
FPS = 8

PALETTE = {
    ".": (0, 0, 0, 0),         # Transparent
    "S": (30, 20, 32, 130),    # Soft purple-brown ground shadow (Alpha 130)
    
    # Spit Wood & Stands (Warm Oak Timber)
    "#": (54, 26, 14, 255),    # Soft dark wood outline (#361a0e)
    "T": (195, 135, 75, 255),  # Spit wood light (#c3874b)
    "U": (145, 90, 48, 255),   # Spit wood base (#915a30)
    "I": (95, 52, 28, 255),    # Spit wood shadow (#5f341c)
    
    # Campfire Firewood Logs
    "L": (210, 150, 85, 255),  # Firewood bark light (#d29655)
    "M": (148, 88, 42, 255),   # Firewood bark midtone (#94582a)
    "D": (92, 46, 22, 255),    # Firewood bark dark (#5c2e16)
    "V": (52, 24, 14, 255),    # Firewood deep crevice (#34180e)
    "C": (230, 190, 140, 255), # Log cut-end pale wood (#e6be8c)
    
    # Giant Roast Meat (Succulent Brown-Red Ham with bone & grill crust)
    "Z": (64, 18, 16, 255),    # Charred roast crust / grill marks (#401210)
    "G": (175, 50, 40, 255),   # Roast meat rich red-brown (#af3228)
    "J": (215, 80, 60, 255),   # Roast meat succulent pink-red (#d7503c)
    "K": (245, 140, 110, 255), # Roast meat juicy highlight / fat (#f58c6e)
    "B": (245, 240, 225, 255), # Ham bone ivory-white (#f5f0e1)
    "P": (200, 185, 165, 255), # Ham bone shadow (#c8b9a5)
    
    # Fire & Flames
    "W": (255, 255, 255, 255), # Core white hot heat (#ffffff)
    "Y": (255, 235, 70, 255),  # Blazing bright yellow (#ffeb46)
    "O": (255, 135, 30, 255),  # Radiant flame orange (#ff871e)
    "R": (225, 45, 25, 255),   # Flame crimson red (#e12d19)
    "Q": (125, 20, 15, 255),   # Flame dark red tip (#7d140f)
    
    # OSL Color Bleed
    "H": (255, 205, 80, 255),  # OSL intense yellow-gold glow (#ffcd50)
    "A": (245, 125, 35, 255),  # OSL warm amber-orange glow (#f57d23)
}

# Master Sculpted Frame 1
f1 = [
    # 0..5: Sky space
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    "................................................",
    # 6..10: Roast meat bulbous top with bone and grill marks
    "..................ZZZZZZZZZZ....................", # y=6: Top rounded roast crust
    "................ZKKKKKKKKKKKKZ..................", # y=7: Fat rind highlight
    "...............ZKKZJJJJZJJJJJJJZ................", # y=8: Seared grill marks (Z)
    "......#..#....ZJJZGGGGZGGGGGGGGZ.......#..#.....", # y=9: Y-fork prong tips at x=6,9 and x=39,42
    "....##BB..#..ZJJZGGGGZGGGGGGGGGGZ.....#..##.....", # y=10: Bone knob at x=4..7
    # 11..14: Spit pole enters and exits meat (Z-Index Layering: Hidden in meat!)
    "...#TTBBP#TT#ZBBGGGGZGGGGGGGGGGGGZ###TTTTTT#....", # y=11: Spit rod through bone into meat, exits at right!
    "..#TTTBBPP###ZBPGGGZGGGGGGGGGGGGGGZ#TTTTTTUU#...", # y=12: Spit cradled in Y-forks!
    "...#TTTII#..#ZBPGGZGGGGGGGGGGGGGGGGZ#TTTTUU#....", # y=13: Meat completely covers spit from x=13 to x=33
    "....#II##...ZBBGZGGGGGGGGGGGGGGGGGZ..#II##......", # y=14: Spit rod bottoms
    # 15..17: Lower meat body & side support poles
    "....#TU#....ZJJZGGGGGGGGGGGGGGGGGZ...#TU#.......", # y=15: Stand poles continue down
    "....#TU#.....ZJJJGGGGGGGGGGGGGGGZ....#TU#.......", # y=16: Juicy lower belly
    "....#TU#......ZZGGGGGGGGGGGGGGZZ.....#TU#.......", # y=17: Meat curves inward
    # 18..20: Bottom of meat with OSL amber/gold glow from fire!
    "....#TU#........ZZAAHHHHHHAAZZ.......#TU#.......", # y=18: OSL gold H & orange A on meat bottom!
    "....#TU#..........ZZAAHHAAZZ...Y.....#TU#.......", # y=19: OSL glow + Ember 1 rising (Y at x=31)
    "....#TU#............ZZZZZZ....OY.....#TU#.......", # y=20: Meat bottom rim + Ember 1 base
    # 21..25: Organic dancing flame tongues
    "....#TU#............RR.....OOYY......#TU#.......", # y=21: Flame tongue left (RR) & right (OOYY)
    "....#TU#...........RYYO...OYYWWY.....#TU#.......", # y=22: Flame core
    "....#TU#..........RYWWYO.OYYWWYYO....#TU#.......", # y=23: White hot cores
    "....#TU#.........OYYWWYYOYYWWYYRO....#TU#.......", # y=24
    "....#TU#.........OYYWWYYYYWWYYRO.....#TU#.......", # y=25
    # 26..30: Main flame body
    "....#TU#........ROYYWWWWWWWWYYRO.....#TU#.......", # y=26: Broad blazing flame
    "....#TU#........ROYYYYWWWWYYYYRO.....#TU#.......", # y=27
    "....#TU#........RROYYYYYYYYYYORR.....#TU#.......", # y=28
    "....#TU#.........RROOOOOOOOOORR......#TU#.......", # y=29
    "....#TU#..........RRRRRRRRRRRR.......#TU#.......", # y=30
    # 31..34: Coals & Firewood with OSL (Gold & Amber on top of logs)
    "....#TU#...........RRRRRRRRRR........#TU#.......", # y=31: Coals
    "....#TU#........####.WYYYYW.####.....#TU#.......", # y=32: Hot coals WYYYYW between logs
    "....#TU#.....###LLHH#WYYYYW#HHLL###..#TU#.......", # y=33: Top of logs lit by OSL H & A!
    "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#.......", # y=34: OSL on logs
    # 35..38: 3 Crisscrossed Firewood Logs (Log 1, Log 2, Log 3)
    "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#.......", # y=35: 3 logs crossing
    "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#.....", # y=36: Cut-ends CC on logs!
    "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#....", # y=37
    "....#TU##MMDDV#.......#####......#VDDMM#TU#.....", # y=38: Logs cross over each other
    # 39..42: Log bottoms & stands
    "...##TUI##DDDV#...###########....#VDDD##TUI##...", # y=39: Stand foot widening
    "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#..", # y=40: Log 3 horizontal front
    ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#..", # y=41: Log 3 cut-ends
    "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#..", # y=42: Stand feet anchored
    # 43..45: Ground Contact Shadow S (Alpha 130)
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", # y=43: Full ground shadow
    ".SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.", # y=44
    "...SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...", # y=45
    # 46..47
    "................................................",
    "................................................",
]

# Frame 2: Right tongue shoots up, Spark 1 rises to y=13, Spark 2 detaches at y=19
f2 = list(f1)
# Spark 1 at y=13, x=31
f2[13] = "...#TTTII#..#ZBPGGZGGGGGGGGGGGGGGGGZ#TTTTUU#.Y.."
# Spark 2 lifting off at y=19, x=18
f2[19] = "....#TU#..........ZZAAHHAAZZ...Y.....#TU#.......".replace("...Y", "....")
f2[19] = "....#TU#........Y.ZZAAHHAAZZ.........#TU#......."
f2[20] = "....#TU#............ZZZZZZ...........#TU#......."
# Flame changes: Center surges, right leans
f2[21] = "....#TU#...........OOYY......RR......#TU#......."
f2[22] = "....#TU#..........OYYWWY....RYYO.....#TU#......."
f2[23] = "....#TU#.........OYYWWYYO..RYWWYO....#TU#......."
f2[24] = "....#TU#.........ROYYWWYYOYYWWYYO....#TU#......."
f2[25] = "....#TU#.........ROYYWWYYYYWWYYO.....#TU#......."
f2[26] = "....#TU#........ROYYYYWWWWWWYYRO.....#TU#......."
f2[27] = "....#TU#........RROYYYYWWWWYYYYRO....#TU#......."
# Coals flicker
f2[32] = "....#TU#........####.WWYYWW.####.....#TU#......."
f2[33] = "....#TU#.....###LLHH#WWYYWW#HHLL###..#TU#......."

# Frame 3: Spark 1 floats high up to y=7, x=32; Spark 2 floats to y=13, x=17
f3 = list(f1)
# Spark 1 at y=7, x=32
f3[7]  = "................ZKKKKKKKKKKKKZ..Y..............."
# Spark 2 at y=13, x=17
f3[13] = "...#TTTII#..#ZBPGYGGGGGGGGGGGGGGGGGZ#TTTTUU#...."
# Flame changes: Left surges, tongues interweave
f3[20] = "....#TU#............ZZZZZZ...........#TU#......."
f3[21] = "....#TU#..........RYYO.....RYYO......#TU#......."
f3[22] = "....#TU#.........RYWWYO...OYYWWY.....#TU#......."
f3[23] = "....#TU#.........OYYWWYYOOYYWWYYO....#TU#......."
f3[24] = "....#TU#.........OYYWWYYYYWWYYRO.....#TU#......."
f3[25] = "....#TU#........ROYYWWWWWWWWYYRO.....#TU#......."
f3[26] = "....#TU#........ROYYYYWWWWYYYYRO.....#TU#......."
f3[27] = "....#TU#........RROYYYYYYYYYYORR.....#TU#......."
# Coals
f3[32] = "....#TU#........####.YYYYYY.####.....#TU#......."

# Frame 4: Spark 1 vanishes! Spark 2 floats to y=7, x=15
f4 = list(f1)
# Spark 2 at y=7, x=15
f4[7]  = "...............YZKKKKKKKKKKKKZ.................."
# Flame changes: Lower before next cycle
f4[20] = "....#TU#............ZZZZZZ...........#TU#......."
f4[21] = "....#TU#...........RR.......OO.......#TU#......."
f4[22] = "....#TU#..........RYYO.....OYYO......#TU#......."
f4[23] = "....#TU#.........RYWWYO...RYWWYO.....#TU#......."
f4[24] = "....#TU#.........OYYWWYYOYYWWYYO.....#TU#......."
f4[25] = "....#TU#.........OYYWWYYYYWWYYRO.....#TU#......."
f4[26] = "....#TU#........ROYYWWWWWWWWYYRO.....#TU#......."
f4[27] = "....#TU#........ROYYYYWWWWYYYYRO.....#TU#......."

frames = [f1, f2, f3, f4]

# Validate all rows across all 4 frames
for f_idx, fr in enumerate(frames):
    for r_idx, r in enumerate(fr):
        if len(r) != 48:
            raise ValueError(f"Frame {f_idx+1} row {r_idx} has length {len(r)}, expected 48!")

print("All 4 frames validated successfully (48x48)!")

# Render test sheet
sheet_img = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
pil_frames = []

for f_idx, frame_data in enumerate(frames):
    f_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pix = f_img.load()
    for y in range(H):
        row = frame_data[y]
        for x in range(W):
            pix[x, y] = PALETTE.get(row[x], (0, 0, 0, 0))
    sheet_img.paste(f_img, (f_idx * W, 0))
    pil_frames.append(f_img)

os.makedirs("test", exist_ok=True)
sheet_img.save("test/test_campfire_sheet.png")
sheet_img.resize((W * 4 * 4, H * 4), Image.NEAREST).save("test/test_campfire_sheet_4x.png")

print("Generated test/test_campfire_sheet_4x.png successfully!")
