from backend.validators.reservation_validator import validate_reservation_payload

def test_reservation_validator():
    v, _ = validate_reservation_payload({"user_id": "usr-1", "vehicle_plate": "KA01AB1234"})
    assert v is True
    v_bad, _ = validate_reservation_payload({"user_id": "usr-1", "vehicle_plate": ""})
    assert v_bad is False
