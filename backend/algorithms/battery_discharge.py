"""Battery discharge rate estimator for EV routing."""

def estimate_ev_discharge(distance_km: float, avg_consumption_wh_km: float = 150.0) -> float:
    """Returns estimated kWh consumed for the given distance."""
    return round((distance_km * avg_consumption_wh_km) / 1000.0, 2)
