def validate_revenue_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    amount = data.get('amount', -1)
    gst = data.get('gst', -1)
    return amount >= 0 and gst >= 0 and gst <= amount
