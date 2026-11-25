from backend.algorithms.co2_savings import calculate_co2_savings

def test_co2_savings():
    saved = calculate_co2_savings(2.5, 120.0)
    assert saved == 300.0
