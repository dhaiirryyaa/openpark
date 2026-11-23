from dataclasses import dataclass
from typing import Optional

@dataclass
class ParkingLotModel:
    id: int
    name: str
    lat: float
    lon: float
    capacity: int
    free_spots: int
    price_car: str
    price_bike: str
    status: str
    address: str
    has_ev: bool = False
    is_covered: bool = False
    updated_mins: int = 1
