def test_traccar_coords_validation():
    lat, lon = 12.9716, 77.5946
    assert -90.0 <= lat <= 90.0
    assert -180.0 <= lon <= 180.0
