# Inspect all raw strings and adjust them so lengths match desired target widths
desired_f1_widths = [
    6, 10, 14, 18, 20, 22, 24, 26, 26, 26, 28, 28, 28, 28, 28, 26, 26, 26, 24, 22, 28, 24, 18
]
desired_f2_widths = [
    12, 20, 26, 30, 34, 36, 36, 36, 36, 34, 34, 32, 30, 38, 32, 22
]
desired_f3_widths = [
    4, 8, 12, 14, 16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 18, 18, 16, 16, 16, 16, 16, 16, 14, 14, 14, 14, 12, 12, 10, 6, 14, 10
]
desired_f4_widths = [
    8, 12, 16, 20, 22, 24, 24, 24, 26, 26, 26, 26, 26, 26, 26, 24, 24, 24, 24, 22, 22, 20, 16, 12, 24, 20, 14
]

print("Lengths needed:")
print("F1:", len(desired_f1_widths), "body/shadow rows")
print("F2:", len(desired_f2_widths), "body/shadow rows")
print("F3:", len(desired_f3_widths), "body/shadow rows")
print("F4:", len(desired_f4_widths), "body/shadow rows")
