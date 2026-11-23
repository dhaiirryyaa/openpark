from typing import Tuple

def sanitize_geocoding_query(query: str) -> Tuple[bool, str]:
    cleaned = (query or "").strip()
    if len(cleaned) < 2:
        return False, ""
    # Strip potential SQL or script injection characters
    sanitized = "".join(ch for ch in cleaned if ch.isalnum() or ch in " ,.-_")
    return True, sanitized
