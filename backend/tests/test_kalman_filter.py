from backend.algorithms.kalman_filter import KalmanFilter1D

def test_kalman_filter_smoothing():
    kf = KalmanFilter1D()
    r1 = kf.update(12.9716)
    assert r1 == 12.9716
    r2 = kf.update(12.9720)
    assert 12.9716 <= r2 <= 12.9720
