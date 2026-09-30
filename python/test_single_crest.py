import math

# Test lambda = 24.0
wavelength = 24.0
shift_per_frame = wavelength / 4.0 # 6.0 px

for f in range(4):
    shift = f * shift_per_frame
    crests = []
    troughs = []
    for x in range(18, 45):
        # We want crest at x=22 for f=0
        # phase = 2*pi*(x - 16 - shift)/24
        # at x=22, f=0: phase = 2*pi*(6)/24 = pi/2 (Crest!)
        phase = 2.0 * math.pi * ((x - 16 - shift) / wavelength)
        sin_val = math.sin(phase)
        
        prev_s = math.sin(2.0 * math.pi * ((x - 1 - 16 - shift) / wavelength))
        next_s = math.sin(2.0 * math.pi * ((x + 1 - 16 - shift) / wavelength))
        if sin_val > prev_s and sin_val >= next_s:
            crests.append(x)
        if sin_val < prev_s and sin_val <= next_s:
            troughs.append(x)
            
    print(f"Frame {f+1}: shift={shift:.1f}, Crests={crests}, Troughs={troughs}")
