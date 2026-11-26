"""Parking bay geometric angle entry difficulty score."""

def calculate_bay_angle_difficulty(angle_degrees: float) -> str:
    if angle_degrees <= 45.0:
        return "EASY"
    elif angle_degrees <= 60.0:
        return "MODERATE"
    elif angle_degrees <= 90.0:
        return "STANDARD"
    return "DIFFICULT"
