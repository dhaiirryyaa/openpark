from dataclasses import dataclass

@dataclass
class SensorZoneModel:
    id: str
    lot_id: int
    floor_level: int
    total_bays: int
    free_bays: int
    is_ev_zone: bool = False
