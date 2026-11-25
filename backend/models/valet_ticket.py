from dataclasses import dataclass

@dataclass
class ValetTicket:
    ticket_id: str
    vehicle_plate: str
    driver_id: str
    bay_assigned: str
    status: str = 'CHECKED_IN'
