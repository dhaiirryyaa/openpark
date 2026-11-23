from backend.validators.telemetry_validator import validate_telemetry_payload

def test_telemetry_validator():
    v1, _ = validate_telemetry_payload({"lot_id": 1, "free_spots": 20})
    assert v1 is True
    v2, _ = validate_telemetry_payload({"free_spots": 20})
    assert v2 is False
