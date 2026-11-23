from backend.algorithms.ev_scheduling import schedule_ev_charging_slots

def test_ev_scheduling():
    queue = [
        {"id": "EV-1", "current_soc_pct": 80},
        {"id": "EV-2", "current_soc_pct": 20},
        {"id": "EV-3", "current_soc_pct": 40}
    ]
    scheduled = schedule_ev_charging_slots(queue, total_plugs=2)
    # Lowest battery (EV-2) should get plug 1
    assert scheduled[0]["vehicle_id"] == "EV-2"
    assert scheduled[0]["status"] == "charging"
