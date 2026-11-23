from typing import Dict, Tuple

def validate_parking_lot_payload(data: Dict) -> Tuple[bool, str]:
    if not data.get("name"):
        return False, "Missing lot name"
    lat, lon = data.get("lat"), data.get("lon")
    if lat is None or not (-90.0 <= lat <= 90.0):
        return False, "Invalid latitude"
    if lon is None or not (-180.0 <= lon <= 180.0):
        return False, "Invalid longitude"
    capacity = data.get("capacity", 0)
    if capacity <= 0:
        return False, "Capacity must be positive integer"
    return True, ""
