from dataclasses import dataclass

@dataclass
class RefundClaim:
    claim_id: str
    reservation_id: str
    amount_requested: float
    status: str = 'PENDING'
