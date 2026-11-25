def validate_sensor_heartbeat(sensor_id: str, battery_v: float) -> bool:
    return bool(sensor_id and 2.5 <= battery_v <= 4.5)
