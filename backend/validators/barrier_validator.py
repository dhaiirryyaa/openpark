def validate_barrier_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    valid_types = {'ENTRY_REQUEST', 'BARRIER_OPENED', 'BARRIER_CLOSED', 'OBSTACLE_DETECTED'}
    return bool(data.get('barrier_id') and data.get('event_type') in valid_types)
