from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ReservationModel:
    id: str
    user_id: str
    lot_id: int
    vehicle_plate: str
    start_time: datetime
    end_time: datetime
    status: str  # 'active', 'completed', 'cancelled'
    amount_paid: float
