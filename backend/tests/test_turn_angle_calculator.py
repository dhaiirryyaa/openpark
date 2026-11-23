from backend.algorithms.turn_angle_calculator import classify_turn_maneuver

def test_turn_angles():
    assert classify_turn_maneuver(0.0, 5.0) == "straight"
    assert classify_turn_maneuver(0.0, 90.0) == "turn_right"
    assert classify_turn_maneuver(0.0, 270.0) == "turn_left"
