from backend.algorithms.level_climb_estimator import estimate_level_climb_seconds

def test_level_climb_estimator():
    assert estimate_level_climb_seconds(3, 12.0) == 75
    assert estimate_level_climb_seconds(0, 12.0) == 0
