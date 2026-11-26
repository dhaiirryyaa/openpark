from dataclasses import dataclass

@dataclass
class GarageLevel:
    level_id: str
    lot_id: str
    floor_number: int
    total_bays: int
    has_ev: bool
