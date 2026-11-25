from backend.validators.barrier_validator import validate_barrier_payload

def test_barrier_validator():
    assert validate_barrier_payload({'barrier_id': 'B1', 'event_type': 'BARRIER_OPENED'}) is True
    assert validate_barrier_payload({'barrier_id': 'B1', 'event_type': 'UNKNOWN'}) is False
