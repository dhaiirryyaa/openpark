"""Sidewalk accessibility slope and ramp index."""

def evaluate_sidewalk_accessibility(slope_pct: float, has_curb_cut: bool) -> str:
    if not has_curb_cut:
        return "INACCESSIBLE"
    if slope_pct <= 5.0:
        return "FULLY_ACCESSIBLE"
    elif slope_pct <= 8.33:
        return "MODERATELY_ACCESSIBLE"
    return "STEEP"
