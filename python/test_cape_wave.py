import math

# Test cape centerline and bounds
# x from 18 to 44
# lambda = 20.0, shift per frame = 5.0
wavelength = 20.0
shift_per_frame = wavelength / 4.0 # 5.0 px per frame

for frame_idx in range(4):
    shift = frame_idx * shift_per_frame
    crests = []
    troughs = []
    for x in range(18, 45):
        # Phase at x
        phase = 2 * math.pi * ((x - 18 - shift) / wavelength)
        # Sin value
        s = math.sin(phase)
        # Local extrema detection
        s_prev = math.sin(2 * math.pi * ((x - 1 - 18 - shift) / wavelength))
        s_next = math.sin(2 * math.pi * ((x + 1 - 18 - shift) / wavelength))
        if s > s_prev and s >= s_next:
            crests.append(x)
        if s < s_prev and s <= s_next:
            troughs.append(x)
    print(f"Frame {frame_idx + 1}: shift={shift:.1f}, Crests={crests}, Troughs={troughs}")
