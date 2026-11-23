import time
from typing import Dict

class LoRaWANGateway:
    def __init__(self, gateway_eui: str):
        self.gateway_eui = gateway_eui

    def generate_uplink_packet(self, device_id: str, occupied: bool) -> Dict:
        return {
            "gateway_eui": self.gateway_eui,
            "device_id": device_id,
            "payload_hex": "01" if occupied else "00",
            "rssi": -78,
            "snr": 9.5,
            "timestamp": time.time()
        }
