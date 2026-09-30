# Helper to adjust strings to exact target width
def fix(s, target_w):
    diff = target_w - len(s)
    if diff == 0:
        return s
    print(f"Diff for '{s[:10]}...': currently {len(s)}, target {target_w} (need {diff})")
    return s
