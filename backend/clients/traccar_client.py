from typing import Dict

class TraccarGatewayClient:
    def __init__(self, host: str = "http://localhost:5055"):
        self.host = host

    def format_position_url(self, device_id: str, lat: float, lon: float) -> str:
        return f"{self.host}/?id={device_id}&lat={lat}&lon={lon}"
