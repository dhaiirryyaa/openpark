from backend.algorithms.battery_thermal import calculate_thermal_throttle_factor

def test_battery_thermal():
    assert calculate_thermal_throttle_factor(45.0, 60.0) == 0.75
    assert calculate_thermal_throttle_factor(25.0, 60.0) == 1.0
