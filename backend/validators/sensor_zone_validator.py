from typing import Dict, Tuple

def validate_sensor_zone(zone: Dict) -> Tuple[bool, str]:
    if not zone.get("id"):
        return False, "Missing zone id"
    if zone.get("floor_level", 0) < -5 or zone.get("floor_level", 0) > 20:
        return False, "Floor level out of range (-5 to 20)"
    return True, ""
