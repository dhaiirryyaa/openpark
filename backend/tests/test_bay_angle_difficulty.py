from backend.algorithms.bay_angle_difficulty import calculate_bay_angle_difficulty

def test_bay_angle_difficulty():
    assert calculate_bay_angle_difficulty(30.0) == 'EASY'
    assert calculate_bay_angle_difficulty(90.0) == 'STANDARD'
