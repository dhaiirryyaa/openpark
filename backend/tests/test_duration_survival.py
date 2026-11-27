from backend.algorithms.duration_survival import estimate_spot_departure_prob

def test_duration_survival():
    short_prob = estimate_spot_departure_prob(5.0)
    long_prob = estimate_spot_departure_prob(120.0)
    assert long_prob > short_prob
    assert 0.05 <= short_prob <= 0.95
