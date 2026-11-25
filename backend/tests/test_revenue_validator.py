from backend.validators.revenue_validator import validate_revenue_payload

def test_revenue_validator():
    assert validate_revenue_payload({'amount': 100, 'gst': 18}) is True
    assert validate_revenue_payload({'amount': 100, 'gst': 150}) is False
    assert validate_revenue_payload({'amount': -10, 'gst': 0}) is False
