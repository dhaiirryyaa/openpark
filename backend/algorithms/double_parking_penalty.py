"""Curbside delivery double-parking penalty estimator."""

def estimate_double_parking_delay(active_double_parkers: int, corridor_capacity_vph: float = 1800.0) -> float:
    """Returns corridor delay multiplier."""
    if active_double_parkers <= 0:
        return 1.0
    capacity_reduction = min(0.60, active_double_parkers * 0.18)
    effective_cap = corridor_capacity_vph * (1.0 - capacity_reduction)
    return round(corridor_capacity_vph / max(100.0, effective_cap), 2)
