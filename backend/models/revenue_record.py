from dataclasses import dataclass

@dataclass
class RevenueRecord:
    record_id: str
    lot_id: str
    amount: float
    gst: float
    is_ev: bool
    timestamp: str
