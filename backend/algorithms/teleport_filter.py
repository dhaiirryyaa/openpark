"""Real-time GPS speed anomaly and teleportation filter."""
import math

def detect_gps_teleportation(lat1: float, lon1: float, lat2: float, lon2: float, dt_seconds: float, max_allowed_speed_kmh: float = 160.0) -> bool:
    if dt_seconds <= 0.001:
        return False
    d_lat = (lat2 - lat1) * 111320.0
    d_lon = (lon2 - lon1) * 111320.0 * math.cos(math.radians(lat1))
    dist_m = math.hypot(d_lat, d_lon)
    speed_kmh = (dist_m / dt_seconds) * 3.6
    return speed_kmh > max_allowed_speed_kmh
