"""CO2 emissions savings estimator for direct parking routing."""

def calculate_co2_savings(cruising_distance_km: float, emission_factor_g_per_km: float = 120.0) -> float:
    """Returns grams of CO2 saved by eliminating cruising search time."""
    return round(cruising_distance_km * emission_factor_g_per_km, 1)
