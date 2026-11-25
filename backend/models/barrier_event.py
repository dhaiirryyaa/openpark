from dataclasses import dataclass

@dataclass
class BarrierEvent:
    event_id: str
    barrier_id: str
    event_type: str
    vehicle_plate: str
    timestamp: str
