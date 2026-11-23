from typing import Dict

class EVChargerKiosk:
    def __init__(self, kiosk_id: str, power_kw: float = 60.0):
        self.kiosk_id = kiosk_id
        self.power_kw = power_kw
        self.current_state = "idle"

    def start_charge_session(self, vehicle_id: str) -> Dict:
        self.current_state = "charging"
        return {
            "kiosk_id": self.kiosk_id,
            "vehicle_id": vehicle_id,
            "power_output_kw": self.power_kw,
            "status": self.current_state
        }
