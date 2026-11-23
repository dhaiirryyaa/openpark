import time
from typing import Dict

class BoomBarrierGate:
    def __init__(self, gate_id: str):
        self.gate_id = gate_id
        self.barrier_open = False

    def process_vehicle_arrival(self, license_plate: str) -> Dict:
        self.barrier_open = True
        return {
            "gate_id": self.gate_id,
            "license_plate": license_plate.upper(),
            "timestamp": time.time(),
            "action": "barrier_opened",
            "duration_secs": 8.0
        }
