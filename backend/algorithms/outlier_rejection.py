"""GPS sensor jitter outlier rejection filter."""
import math

def is_gps_outlier(prev_fix: dict, cur_fix: dict, max_speed_mps: float = 55.0) -> bool:
    dt = max(0.001, cur_fix.get("timestamp", 0) - prev_fix.get("timestamp", 0))
    d_lat = (cur_fix["lat"] - prev_fix["lat"]) * 111320.0
    d_lon = (cur_fix["lon"] - prev_fix["lon"]) * 111320.0
    distance = math.hypot(d_lat, d_lon)
    implied_speed = distance / dt
    return implied_speed > max_speed_mps
