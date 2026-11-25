from backend.algorithms.geofence_trigger import is_inside_circular_geofence

def test_geofence_trigger():
    assert is_inside_circular_geofence(12.971, 77.594, 12.971, 77.594, 50.0) is True
    assert is_inside_circular_geofence(12.971, 77.594, 13.000, 77.594, 50.0) is False
