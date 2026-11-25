from backend.algorithms.indoor_speed_monitor import check_indoor_speed

def test_indoor_speed_monitor():
    res_ok = check_indoor_speed(12.0, 15.0)
    assert res_ok['is_violation'] is False
    res_bad = check_indoor_speed(22.0, 15.0)
    assert res_bad['is_violation'] is True
    assert res_bad['severity'] == 'medium'
