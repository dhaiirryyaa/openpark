from backend.algorithms.multimodal_scorer import score_multimodal_park_and_ride

def test_multimodal_scorer():
    res = score_multimodal_park_and_ride(15.0, 20.0, 50.0, 30.0, 45.0)
    assert res['total_time_min'] == 35.0
    assert res['total_cost_inr'] == 80.0
    assert res['time_saved_min'] == 10.0
    assert res['is_recommended'] is True
