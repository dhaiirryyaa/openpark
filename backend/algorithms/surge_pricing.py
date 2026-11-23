def calculate_dynamic_price(base_price: float, occupancy_pct: float, is_peak_hour: bool = False) -> float:
    multiplier = 1.0
    if occupancy_pct > 90.0:
        multiplier = 1.6
    elif occupancy_pct > 80.0:
        multiplier = 1.35
    elif occupancy_pct > 65.0:
        multiplier = 1.15
    elif occupancy_pct < 25.0:
        multiplier = 0.85
        
    if is_peak_hour:
        multiplier *= 1.25
        
    return round(base_price * multiplier, 2)
