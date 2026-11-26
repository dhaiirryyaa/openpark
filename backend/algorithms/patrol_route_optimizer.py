"""Parking enforcement patrol route optimizer."""

def prioritize_patrol_lots(lots: list) -> list:
    # Sort lots by highest historical violation rate
    return sorted(lots, key=lambda l: l.get('violation_rate', 0.0), reverse=True)
