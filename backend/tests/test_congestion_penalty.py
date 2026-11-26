from backend.algorithms.congestion_penalty import get_congestion_penalty_factor

def test_congestion_penalty():
    assert get_congestion_penalty_factor('LOW') == 1.0
    assert get_congestion_penalty_factor('SEVERE') == 2.4
