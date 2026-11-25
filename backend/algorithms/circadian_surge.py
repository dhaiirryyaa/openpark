"""Circadian curve surge multiplier calculation for peak urban hours."""
import math

def calculate_circadian_surge(hour_of_day: float, is_weekend: bool = False) -> float:
    if is_weekend:
        peak_offset = math.exp(-0.5 * ((hour_of_day - 19.0) / 2.5) ** 2)
        return round(1.0 + 0.5 * peak_offset, 2)
    morning = math.exp(-0.5 * ((hour_of_day - 9.5) / 1.8) ** 2)
    evening = math.exp(-0.5 * ((hour_of_day - 18.5) / 2.0) ** 2)
    return round(1.0 + 0.65 * morning + 0.85 * evening, 2)
