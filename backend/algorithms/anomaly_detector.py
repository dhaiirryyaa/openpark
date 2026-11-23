from typing import List

def detect_sensor_reading_anomalies(readings: List[int], max_delta_threshold: int = 50) -> List[int]:
    anomaly_indices = []
    for i in range(1, len(readings)):
        delta = abs(readings[i] - readings[i - 1])
        if delta > max_delta_threshold:
            anomaly_indices.append(i)
    return anomaly_indices
