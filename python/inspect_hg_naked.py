from design_hourglass_dissolve import frames, check_naked_pixels

for i in (0, 3):
    naked = check_naked_pixels(frames[i])
    print(f"Frame {i+1} naked:")
    for n in naked:
        print(" ", n)
