from dataclasses import dataclass

@dataclass
class RateTariffModel:
    lot_id: int
    base_hourly_car: float
    base_hourly_bike: float
    night_rate_multiplier: float = 1.0
    weekend_multiplier: float = 1.2
