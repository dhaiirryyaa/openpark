from backend.validators.auth_token_validator import validate_jwt_claims

def test_jwt_claims():
    assert validate_jwt_claims({"sub": "driver_1", "exp": 1899999999})[0] is True
    assert validate_jwt_claims({"sub": "driver_1"})[0] is False
