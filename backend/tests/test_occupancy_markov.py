from backend.algorithms.occupancy_markov import simulate_markov_occupancy

def test_occupancy_markov():
    occ = simulate_markov_occupancy(50, 100, 0.1, 0.05)
    assert 0 <= occ <= 100
