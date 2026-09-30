import math

# Test coordinates
X_pivot = 24.0
Y_pivot = 12.0
L_chain = 7.0
R_bell = 14.0 # distance from pivot to bell center

configs = [
    ("F1 (Sweep Left)",       -12.5,  0.0),
    ("F2 (Extreme Left)",     -25.4,  0.0),
    ("F3 (Return Left, lag)", -12.5,  1.0),
    ("F4 (Center Eq)",          0.0,  0.5),
    ("F5 (Sweep Right)",      +12.5,  0.0),
    ("F6 (Extreme Right)",    +25.4,  0.0),
    ("F7 (Return Right, lag)",+12.5, -1.0),
    ("F8 (Center Eq)",          0.0, -0.5),
]

for name, th_deg, lag_x in configs:
    th = math.radians(th_deg)
    crown_x = X_pivot + L_chain * math.sin(th) + lag_x
    crown_y = Y_pivot + L_chain * math.cos(th)
    
    # Bell center is at local u=0, v=7 (relative to crown)
    # dx = u*cos(th) + v*sin(th) = 7*sin(th)
    # dy = -u*sin(th) + v*cos(th) = 7*cos(th)
    bell_cx = crown_x + 7.0 * math.sin(th)
    bell_cy = crown_y + 7.0 * math.cos(th)
    
    delta_x = bell_cx - 24.0
    print(f"{name:25s}: crown=({crown_x:.1f}, {crown_y:.1f}) bell_center=({bell_cx:.1f}, {bell_cy:.1f}) Delta_X={delta_x:+.1f}px")
