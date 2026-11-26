"""Vehicle tailgating detector for barrier gate entry."""

def is_tailgating_event(time_between_sensors_s: float, min_gap_s: float = 2.0) -> bool:
    return 0.0 < time_between_sensors_s < min_gap_s
