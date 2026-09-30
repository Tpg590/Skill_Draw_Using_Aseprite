from design_robot_punch import frames, check_naked_pixels

naked_f3 = check_naked_pixels(frames[2])
print(f"Total naked in F3: {len(naked_f3)}")
for n in naked_f3:
    if n[1] != 40: # Ignore plinth at y=40 for now
        print(" ", n)
