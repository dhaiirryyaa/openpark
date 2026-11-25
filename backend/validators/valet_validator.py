def validate_valet_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    return bool(data.get('vehicle_plate') and data.get('driver_id'))
