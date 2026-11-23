from typing import Dict

class TraccarDeviceMock:
    def __init__(self, device_id: str, start_lat: float, start_lon: float):
        self.device_id = device_id
        self.lat = start_lat
        self.lon = start_lon

    def step(self, delta_lat: float = 0.0001, delta_lon: float = 0.0001) -> Dict:
        self.lat += delta_lat
        self.lon += delta_lon
        return {
            "id": self.device_id,
            "lat": round(self.lat, 6),
            "lon": round(self.lon, 6),
            "speed_kmh": 32.5,
            "battery_pct": 88
        }
