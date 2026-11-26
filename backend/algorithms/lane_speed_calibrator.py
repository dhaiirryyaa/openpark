"""Multi-lane road segment speed calibrator."""

def calibrate_lane_speed(num_lanes: int, base_speed_kmh: float, is_divided: bool = True) -> float:
    bonus = 0.05 * min(4, num_lanes)
    divided_multiplier = 1.1 if is_divided else 0.95
    return round(base_speed_kmh * (1.0 + bonus) * divided_multiplier, 1)
