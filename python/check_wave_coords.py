from refine_cape_sprite import frames, H

for idx, fr in enumerate(frames):
    top_ys = {}
    for x in range(18, 45):
        ys = [y for y in range(H) if fr[y][x] not in (".", "S") and fr[y][x] in ("#", "P1", "P2", "P3", "P4", "Y1", "Y2", "Y3")]
        if ys:
            top_ys[x] = min(ys)
    # Find local minima of top_y (which corresponds to highest crest peak)
    peaks = []
    valleys = []
    bot_ys = {}
    for x in range(18, 45):
        ys = [y for y in range(H) if fr[y][x] not in (".", "S") and fr[y][x] in ("#", "P1", "P2", "P3", "P4", "Y1", "Y2", "Y3")]
        if ys:
            bot_ys[x] = max(ys)
            
    for x in range(19, 44):
        if x in top_ys and (x-1) in top_ys and (x+1) in top_ys:
            if top_ys[x] < top_ys[x-1] and top_ys[x] <= top_ys[x+1]:
                peaks.append((x, top_ys[x]))
            elif top_ys[x] <= top_ys[x-1] and top_ys[x] < top_ys[x+1]:
                peaks.append((x, top_ys[x]))
        if x in bot_ys and (x-1) in bot_ys and (x+1) in bot_ys:
            if bot_ys[x] > bot_ys[x-1] and bot_ys[x] >= bot_ys[x+1]:
                valleys.append((x, bot_ys[x]))
            elif bot_ys[x] >= bot_ys[x-1] and bot_ys[x] > bot_ys[x+1]:
                valleys.append((x, bot_ys[x]))
                
    print(f"Frame {idx+1}: Top peaks={peaks}, Bottom valleys={valleys}")
