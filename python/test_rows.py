# Fix row lengths for rows 34-42

r34 = "....#TU#...##LLMMHHAA#WWWW#AAHHMMLL###TU#......."
r35 = "....#TU#..#LLMMDDHHAA#YYYY#AAHHMMDDLL#TU#......."
r36 = "....#TU#.#CCMDDV#..AAHOOOOHAA..#VDDMMCC#TU#....."
r37 = "....#TU##CCMDDV#....##ROOOR##...#VDDMMCC#TU#...."
r38 = "....#TU##MMDDV#.......#####......#VDDMM#TU#....."
r39 = "...##TUI##DDDV#...###########....#VDDD##TUI##..."
r40 = "..#TTTUII##VV#..##LLMMMMMMLL##....#VV##TTTUII#.."
r41 = ".#TTTUUIII##...#CCMMDDDDDDMMCC#....##TTTUUIII#.."
r42 = "#TTTTUUIIII#...#CCMDDVVVVVDMCC#...#TTTTUUIIII#.."

for idx, r in enumerate([r34, r35, r36, r37, r38, r39, r40, r41, r42], start=34):
    print(f"Row {idx}: len={len(r)}")
