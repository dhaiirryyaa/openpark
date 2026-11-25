import re

def validate_license_plate_format(plate: str) -> bool:
    if not plate or not isinstance(plate, str): return False
    clean = re.sub(r'[^A-Za-z0-9]', '', plate).upper()
    return 6 <= len(clean) <= 10
