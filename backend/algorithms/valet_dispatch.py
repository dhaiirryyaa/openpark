"""Automated valet driver dispatch optimizer."""
import math

def dispatch_closest_valet(drivers: list, pickup_lat: float, pickup_lon: float) -> str:
    available = [d for d in drivers if d.get('status') == 'AVAILABLE']
    if not available:
        return None
    def dist(d):
        return math.hypot(d['lat'] - pickup_lat, d['lon'] - pickup_lon)
    closest = min(available, key=dist)
    return closest['driver_id']
