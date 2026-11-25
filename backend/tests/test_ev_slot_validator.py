from backend.validators.ev_slot_validator import validate_ev_slot_payload

def test_ev_slot_validator():
    assert validate_ev_slot_payload({'user_id': 'u1', 'lot_id': 'l1', 'duration_minutes': 60}) is True
    assert validate_ev_slot_payload({'user_id': 'u1', 'duration_minutes': 60}) is False
    assert validate_ev_slot_payload({'user_id': 'u1', 'lot_id': 'l1', 'duration_minutes': 1000}) is False
