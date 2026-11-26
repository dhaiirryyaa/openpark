def validate_patrol_log(data: dict) -> bool:
    if not isinstance(data, dict): return False
    return bool(data.get('officer_id') and data.get('violations_found', -1) >= 0)
