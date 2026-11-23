from typing import Dict, Tuple
import re

def validate_reservation_payload(data: Dict) -> Tuple[bool, str]:
    if not data.get("user_id"):
        return False, "Missing user_id"
    plate = data.get("vehicle_plate", "").strip()
    if not plate or len(plate) < 4:
        return False, "Invalid vehicle license plate"
    return True, ""
