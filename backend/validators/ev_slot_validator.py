def validate_ev_slot_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    if not data.get('user_id') or not data.get('lot_id'): return False
    mins = data.get('duration_minutes', 0)
    return 15 <= mins <= 480
