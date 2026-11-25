"""Turn-by-turn maneuver instruction generator from coordinates."""
import math

def generate_maneuver(heading_in: float, heading_out: float) -> str:
    diff = (heading_out - heading_in + 180.0) % 360.0 - 180.0
    if abs(diff) < 15.0:
        return "Continue straight"
    elif 15.0 <= diff < 45.0:
        return "Bear slight right"
    elif 45.0 <= diff < 135.0:
        return "Turn right"
    elif diff >= 135.0:
        return "Make U-turn"
    elif -45.0 < diff <= -15.0:
        return "Bear slight left"
    elif -135.0 < diff <= -45.0:
        return "Turn left"
    else:
        return "Make sharp left"
