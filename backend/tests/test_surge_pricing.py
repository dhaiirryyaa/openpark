from backend.algorithms.surge_pricing import calculate_dynamic_price

def test_surge_pricing():
    base = 40.0
    normal = calculate_dynamic_price(base, 50.0, is_peak_hour=False)
    high_surge = calculate_dynamic_price(base, 95.0, is_peak_hour=True)
    assert normal == 40.0
    assert high_surge > normal
