import re
from typing import Tuple

def validate_email_format(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email or ""))

def validate_indian_phone(phone: str) -> bool:
    cleaned = re.sub(r'[^0-9]', '', phone or "")
    return len(cleaned) == 10 and cleaned[0] in "6789"
