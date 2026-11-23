from dataclasses import dataclass
from datetime import datetime

@dataclass
class TelemetryEventModel:
    lot_id: int
    sensor_id: str
    event_type: str  # 'enter', 'exit', 'heartbeat'
    timestamp: datetime
    free_spots: int
    occupancy_pct: float
