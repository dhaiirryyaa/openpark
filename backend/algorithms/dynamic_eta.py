"""Traffic-weighted dynamic ETA estimator for urban driving corridors."""

def calculate_dynamic_eta(distance_km: float, base_speed_kmh: float = 30.0, congestion_level: float = 1.0) -> float:
    """Returns estimated travel time in minutes."""
    if base_speed_kmh <= 0 or distance_km <= 0:
        return 0.0
    effective_speed = max(5.0, base_speed_kmh / max(0.2, congestion_level))
    return round((distance_km / effective_speed) * 60.0, 1)
