from typing import Dict

class WeatherStationSimulator:
    def __init__(self, station_id: str):
        self.station_id = station_id

    def read_environment(self) -> Dict:
        return {
            "station_id": self.station_id,
            "temperature_c": 26.5,
            "humidity_pct": 68,
            "is_raining": False
        }
