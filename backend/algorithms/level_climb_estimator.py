"""Parking garage level climbing time estimator."""

def estimate_level_climb_seconds(target_level: int, ramp_speed_kmh: float = 12.0) -> int:
    levels_to_climb = abs(target_level)
    seconds_per_level = 25.0 * (12.0 / max(5.0, ramp_speed_kmh))
    return int(round(levels_to_climb * seconds_per_level))
