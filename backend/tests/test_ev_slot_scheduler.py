from backend.algorithms.ev_slot_scheduler import allocate_ev_slot

def test_ev_slot_scheduler():
    res = allocate_ev_slot(60.0, 20.0, 80.0, 22.0)
    assert res['needed_kwh'] == 36.0
    assert res['can_complete'] is True
