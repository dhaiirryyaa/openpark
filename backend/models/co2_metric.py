from dataclasses import dataclass

@dataclass
class CO2Metric:
    trip_id: str
    grams_saved: float
    distance_saved_km: float
