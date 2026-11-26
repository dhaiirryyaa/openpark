def validate_loading_permit(data: dict) -> bool:
    if not isinstance(data, dict): return False
    return bool(data.get('permit_id') and data.get('vehicle_plate'))
