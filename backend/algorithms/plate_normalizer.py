"""Indian license plate regex and checksum normalizer."""
import re

def normalize_indian_plate(plate: str) -> str:
    clean = re.sub(r'[^A-Za-z0-9]', '', plate or '').upper()
    return clean

def is_valid_plate_format(plate: str) -> bool:
    clean = normalize_indian_plate(plate)
    # Example: KA01AB1234 or DL1CA1234
    pattern = r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$'
    return bool(re.match(pattern, clean))
