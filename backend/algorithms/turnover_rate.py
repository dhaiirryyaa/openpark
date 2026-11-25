"""Parking space turnover rate calculator."""

def calculate_turnover_rate(total_vehicles_parked: int, capacity: int, hours: float) -> float:
    if capacity <= 0 or hours <= 0:
        return 0.0
    return round(total_vehicles_parked / (capacity * hours), 2)
