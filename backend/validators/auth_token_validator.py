from typing import Dict, Tuple

def validate_jwt_claims(claims: Dict) -> Tuple[bool, str]:
    if not claims.get("sub"):
        return False, "Missing subject claim"
    if not claims.get("exp"):
        return False, "Missing expiration claim"
    return True, ""
