from typing import Dict, Tuple

def validate_telemetry_payload(data: Dict) -> Tuple[bool, str]:
    if not data.get("lot_id"):
        return False, "Missing lot_id"
    if "free_spots" not in data or data["free_spots"] < 0:
        return False, "free_spots must be non-negative integer"
    return True, ""
