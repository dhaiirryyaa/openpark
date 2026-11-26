from dataclasses import dataclass

@dataclass
class LoadingPermit:
    permit_id: str
    vehicle_plate: str
    carrier_name: str
    valid_until: str
