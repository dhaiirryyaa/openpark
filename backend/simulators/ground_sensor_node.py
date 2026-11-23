import random
from typing import Dict

class UltrasonicGroundSensor:
    def __init__(self, bay_id: str):
        self.bay_id = bay_id
        self.is_occupied = False

    def trigger_reading(self) -> Dict:
        self.is_occupied = random.random() < 0.65
        return {
            "bay_id": self.bay_id,
            "status": "occupied" if self.is_occupied else "vacant",
            "distance_cm": 45 if self.is_occupied else 220,
            "signal_quality_pct": random.randint(92, 100)
        }
