from backend.validators.sensor_zone_validator import validate_sensor_zone

def test_sensor_zone():
    assert validate_sensor_zone({"id": "Z1", "floor_level": -1})[0] is True
    assert validate_sensor_zone({"id": "Z1", "floor_level": 99})[0] is False
