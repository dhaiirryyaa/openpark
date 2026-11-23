from backend.validators.parking_validator import validate_parking_lot_payload

def test_valid_parking_lot():
    valid, err = validate_parking_lot_payload({"name": "Central Garage", "lat": 12.97, "lon": 77.59, "capacity": 100})
    assert valid is True
    assert err == ""

def test_invalid_lat():
    valid, err = validate_parking_lot_payload({"name": "Central Garage", "lat": 120.0, "lon": 77.59, "capacity": 100})
    assert valid is False
    assert "latitude" in err
