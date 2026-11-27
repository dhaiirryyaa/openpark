def validate_duration_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    mins = data.get('occupied_minutes', -1)
    return bool(data.get('bay_id') and 0 <= mins <= 43200)
