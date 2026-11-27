from backend.validators.multimodal_validator import validate_multimodal_payload
from backend.validators.duration_validator import validate_duration_payload

def test_multimodal_and_duration_validators():
    assert validate_multimodal_payload({'parking_lot_id': 'L1', 'transit_station_id': 'S1', 'walk_distance_m': 350}) is True
    assert validate_multimodal_payload({'parking_lot_id': 'L1'}) is False
    assert validate_duration_payload({'bay_id': 'B1', 'occupied_minutes': 45.0}) is True
    assert validate_duration_payload({'bay_id': 'B1', 'occupied_minutes': -5.0}) is False
