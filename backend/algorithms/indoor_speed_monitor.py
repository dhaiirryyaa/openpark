"""Indoor speed limit excess monitor and alerter."""

def check_indoor_speed(speed_kmh: float, limit_kmh: float = 15.0) -> dict:
    excess = max(0.0, speed_kmh - limit_kmh)
    is_violation = excess > 0.0
    severity = 'high' if excess > 10.0 else ('medium' if excess > 5.0 else ('low' if excess > 0 else 'none'))
    return {
        "speed_kmh": round(speed_kmh, 1),
        "limit_kmh": limit_kmh,
        "is_violation": is_violation,
        "excess_kmh": round(excess, 1),
        "severity": severity
    }
