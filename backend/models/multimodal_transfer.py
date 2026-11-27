from dataclasses import dataclass

@dataclass
class MultimodalTransfer:
    transfer_id: str
    parking_lot_id: str
    transit_station_id: str
    transit_line: str
    walk_distance_m: float
