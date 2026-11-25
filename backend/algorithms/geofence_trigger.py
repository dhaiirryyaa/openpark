"""Circular and polygonal geofence proximity trigger."""
import math

def is_inside_circular_geofence(user_lat: float, user_lon: float, center_lat: float, center_lon: float, radius_m: float) -> bool:
    d_lat = (user_lat - center_lat) * 111320.0
    d_lon = (user_lon - center_lon) * 111320.0 * math.cos(math.radians(center_lat))
    return math.hypot(d_lat, d_lon) <= radius_m
