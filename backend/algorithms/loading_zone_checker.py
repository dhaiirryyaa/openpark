"""Curb space delivery loading zone permit checker."""

def is_loading_zone_permitted(vehicle_type: str, hour_of_day: float, has_permit: bool = False) -> bool:
    if has_permit: return True
    if vehicle_type.upper() in ('COMMERCIAL', 'DELIVERY', 'VAN'):
        return 6.0 <= hour_of_day <= 11.0
    return False
