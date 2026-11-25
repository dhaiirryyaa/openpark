from dataclasses import dataclass
from typing import Optional

@dataclass
class EVReservation:
    reservation_id: str
    user_id: str
    lot_id: str
    bay_number: str
    charger_type: str
    start_time: str
    duration_minutes: int
    status: str = 'PENDING'
