from dataclasses import dataclass
from typing import Optional

@dataclass
class DriverProfileModel:
    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    vehicle_type: str = 'car'
    preferred_payment: str = 'upi'
