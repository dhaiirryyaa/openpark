"""Dynamic reservation cancellation refund calculator."""

def calculate_refund_amount(total_paid: float, hours_until_start: float) -> float:
    if hours_until_start >= 24.0:
        return round(total_paid * 0.95, 2)
    elif hours_until_start >= 2.0:
        return round(total_paid * 0.70, 2)
    elif hours_until_start >= 0.5:
        return round(total_paid * 0.50, 2)
    return 0.0
