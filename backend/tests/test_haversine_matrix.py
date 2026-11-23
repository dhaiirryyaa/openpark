from backend.algorithms.haversine_matrix import haversine_km, distance_matrix

def test_haversine_accuracy():
    # Bangalore MG Road to UB City (~1.4 km)
    dist = haversine_km(12.9754, 77.6066, 12.9716, 77.5946)
    assert 1.0 <= dist <= 2.0

def test_distance_matrix():
    origins = [(12.97, 77.59)]
    destinations = [(12.97, 77.59), (12.98, 77.60)]
    m = distance_matrix(origins, destinations)
    assert len(m) == 1
    assert len(m[0]) == 2
    assert m[0][0] == 0.0
