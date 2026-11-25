"""Sidewalk walking time estimator from parking bay to destination."""

def estimate_walking_minutes(distance_meters: float, walking_speed_kmh: float = 4.8) -> int:
    speed_mps = (walking_speed_kmh * 1000.0) / 3600.0
    seconds = distance_meters / max(0.5, speed_mps)
    return max(1, int(round(seconds / 60.0)))
