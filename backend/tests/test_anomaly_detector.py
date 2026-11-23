from backend.algorithms.anomaly_detector import detect_sensor_reading_anomalies

def test_anomaly_detection():
    readings = [100, 98, 97, 10, 96]
    anomalies = detect_sensor_reading_anomalies(readings, max_delta_threshold=50)
    assert 3 in anomalies
