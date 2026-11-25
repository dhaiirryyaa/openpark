from backend.algorithms.outlier_rejection import is_gps_outlier

def test_outlier_rejection():
    p1 = {'lat': 12.9716, 'lon': 77.5946, 'timestamp': 1000}
    p2 = {'lat': 12.9718, 'lon': 77.5948, 'timestamp': 1001}
    p_jump = {'lat': 13.5000, 'lon': 78.5000, 'timestamp': 1001}
    assert is_gps_outlier(p1, p2) is False
    assert is_gps_outlier(p1, p_jump) is True
