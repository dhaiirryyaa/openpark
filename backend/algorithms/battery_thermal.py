"""EV battery temperature thermal throttling estimator."""

def calculate_thermal_throttle_factor(ambient_temp_c: float, charge_rate_kw: float) -> float:
    if ambient_temp_c > 40.0 and charge_rate_kw > 50.0:
        return 0.75
    elif ambient_temp_c < 5.0:
        return 0.85
    return 1.0
