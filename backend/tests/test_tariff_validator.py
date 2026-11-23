from backend.validators.tariff_validator import validate_tariff_bounds

def test_tariff_bounds():
    assert validate_tariff_bounds({"base_hourly_car": 40.0})[0] is True
    assert validate_tariff_bounds({"base_hourly_car": 999.0})[0] is False
