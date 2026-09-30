from design_robot_punch import frames, check_naked_pixels

naked_f1 = check_naked_pixels(frames[0])
print(f"Total naked in F1: {len(naked_f1)}")
for n in naked_f1[:15]:
    print(" ", n)
