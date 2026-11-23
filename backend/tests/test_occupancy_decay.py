from backend.algorithms.occupancy_decay import calculate_spot_decay_probability

def test_decay_probability():
    prob_immediate = calculate_spot_decay_probability(free_spots=50, capacity=100, elapsed_minutes=0)
    prob_delayed = calculate_spot_decay_probability(free_spots=50, capacity=100, elapsed_minutes=30)
    assert prob_immediate > prob_delayed
    assert prob_delayed >= 0.0
