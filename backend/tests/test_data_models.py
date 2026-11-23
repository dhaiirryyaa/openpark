from backend.models.driver_profile import DriverProfileModel

def test_driver_profile():
    p = DriverProfileModel(user_id="usr-123", full_name="Dhairya K", email="test@openpark.io")
    assert p.user_id == "usr-123"
    assert p.vehicle_type == "car"
