from backend.validators.loading_permit_validator import validate_loading_permit

def test_loading_permit_validator():
    assert validate_loading_permit({'permit_id': 'P1', 'vehicle_plate': 'KA01AB1234'}) is True
    assert validate_loading_permit({'permit_id': 'P1'}) is False
