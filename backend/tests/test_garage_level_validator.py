from backend.validators.garage_level_validator import validate_garage_level

def test_garage_level_validator():
    assert validate_garage_level({'floor_number': 2, 'total_bays': 50}) is True
    assert validate_garage_level({'floor_number': 2, 'total_bays': 0}) is False
    assert validate_garage_level({'floor_number': 50, 'total_bays': 10}) is False
