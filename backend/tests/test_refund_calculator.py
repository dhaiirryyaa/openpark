from backend.algorithms.refund_calculator import calculate_refund_amount

def test_refund_calculator():
    assert calculate_refund_amount(100.0, 25.0) == 95.0
    assert calculate_refund_amount(100.0, 1.0) == 50.0
    assert calculate_refund_amount(100.0, 0.1) == 0.0
