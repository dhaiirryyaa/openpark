from typing import Dict

class InductiveLoopCounter:
    def __init__(self, road_segment: str):
        self.road_segment = road_segment
        self.total_vehicles = 0

    def record_passage(self, vehicle_type: str = "car") -> Dict:
        self.total_vehicles += 1
        return {
            "segment": self.road_segment,
            "type": vehicle_type,
            "cumulative_count": self.total_vehicles
        }
