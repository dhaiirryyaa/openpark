def validate_refund_claim(data: dict) -> bool:
    if not isinstance(data, dict): return False
    return bool(data.get('reservation_id') and data.get('amount_requested', 0) > 0)
