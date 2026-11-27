"""Automated license plate check-digit validation engine."""

def compute_plate_checksum(plate_str: str) -> int:
    total = 0
    for idx, ch in enumerate(plate_str.upper()):
        val = ord(ch)
        total += val * (idx + 1)
    return total % 97
