from backend.algorithms.circadian_surge import calculate_circadian_surge

def test_circadian_surge():
    peak_morn = calculate_circadian_surge(9.5)
    midnight = calculate_circadian_surge(2.0)
    assert peak_morn > midnight
    assert midnight >= 1.0
