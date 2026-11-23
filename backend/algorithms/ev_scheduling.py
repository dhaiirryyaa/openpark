from typing import List, Dict

def schedule_ev_charging_slots(queue: List[Dict], total_plugs: int) -> List[Dict]:
    # Sort by battery state of charge (SoC) ascending (lowest first)
    sorted_queue = sorted(queue, key=lambda x: x.get('current_soc_pct', 50))
    scheduled = []
    for idx, vehicle in enumerate(sorted_queue):
        assigned_plug = (idx % total_plugs) + 1 if idx < total_plugs else None
        scheduled.append({
            "vehicle_id": vehicle["id"],
            "assigned_plug": assigned_plug,
            "status": "charging" if assigned_plug else "queued",
            "estimated_wait_mins": 0 if assigned_plug else (idx // total_plugs) * 45
        })
    return scheduled
