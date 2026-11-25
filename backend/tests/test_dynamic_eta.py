from backend.algorithms.dynamic_eta import calculate_dynamic_eta

def test_dynamic_eta():
    assert calculate_dynamic_eta(15.0, 30.0, 1.0) == 30.0
    assert calculate_dynamic_eta(15.0, 30.0, 2.0) == 60.0
    assert calculate_dynamic_eta(0, 30.0) == 0.0
