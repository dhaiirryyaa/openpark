from backend.validators.vision_payload_validator import validate_vision_payload

def test_vision_payload():
    assert validate_vision_payload({"image_base64": "A" * 200})[0] is True
    assert validate_vision_payload({"image_base64": ""})[0] is False
