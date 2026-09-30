from refine_cape_sprite import frames

for idx, fr in enumerate(frames):
    print(f"--- FRAME {idx+1} CAPE REGION (y=10..25, x=17..45) ---")
    for y in range(10, 26):
        row_str = "".join(f"{fr[y][x]:2s}" for x in range(17, 45))
        # only print if not completely empty
        if any(fr[y][x] != "." for x in range(17, 45)):
            print(f"y={y:2d}: {row_str}")
