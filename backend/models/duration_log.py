from dataclasses import dataclass

@dataclass
class DurationLog:
    log_id: str
    bay_id: str
    occupied_minutes: float
    departure_timestamp: str
