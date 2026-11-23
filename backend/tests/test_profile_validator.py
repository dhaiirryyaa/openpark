from backend.validators.user_profile_validator import validate_email_format, validate_indian_phone

def test_email_and_phone():
    assert validate_email_format("driver@openpark.in") is True
    assert validate_email_format("invalid-email") is False
    assert validate_indian_phone("9876543210") is True
    assert validate_indian_phone("123") is False
