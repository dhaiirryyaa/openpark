from backend.algorithms.tailgating_detector import is_tailgating_event

def test_tailgating_detector():
    assert is_tailgating_event(1.2, 2.0) is True
    assert is_tailgating_event(3.5, 2.0) is False
