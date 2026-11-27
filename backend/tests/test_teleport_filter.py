from backend.algorithms.teleport_filter import detect_gps_teleportation

def test_teleport_filter():
    normal = detect_gps_teleportation(12.9716, 77.5946, 12.9718, 77.5948, 1.0)
    teleport = detect_gps_teleportation(12.9716, 77.5946, 13.5000, 78.5000, 1.0)
    assert normal is False
    assert teleport is True
