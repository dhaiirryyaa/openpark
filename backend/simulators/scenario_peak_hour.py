from typing import Dict, List

def run_peak_hour_scenario(lots: List[Dict]) -> List[Dict]:
    updated_lots = []
    for lot in lots:
        # Simulate sudden 40% occupancy surge
        surge = int(lot.get("capacity", 100) * 0.4)
        current_free = lot.get("free_spots", 50)
        new_free = max(0, current_free - surge)
        updated = dict(lot)
        updated["free_spots"] = new_free
        updated["status"] = "Full" if new_free == 0 else ("Filling up" if new_free < 15 else "Available")
        updated_lots.append(updated)
    return updated_lots
