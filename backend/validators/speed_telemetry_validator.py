def validate_speed_telemetry(speed_kmh: float) -> bool:
    return 0.0 <= speed_kmh <= 250.0
