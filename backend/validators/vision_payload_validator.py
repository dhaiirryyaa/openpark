from typing import Dict, Tuple

def validate_vision_payload(data: Dict) -> Tuple[bool, str]:
    image_data = data.get("image_base64", "")
    if not image_data or len(image_data) < 100:
        return False, "Image base64 payload too small or empty"
    return True, ""
