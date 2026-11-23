from typing import Dict, Tuple

def validate_tariff_bounds(tariff: Dict) -> Tuple[bool, str]:
    car_rate = tariff.get("base_hourly_car", 0)
    if car_rate < 0 or car_rate > 500:
        return False, "Car hourly rate outside sensible bounds (0-500 INR)"
    return True, ""
