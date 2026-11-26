from backend.algorithms.lane_speed_calibrator import calibrate_lane_speed

def test_lane_speed_calibrator():
    assert calibrate_lane_speed(4, 50.0, True) == 66.0
    assert calibrate_lane_speed(1, 50.0, False) == 49.9
