from dataclasses import dataclass
from typing import Optional

@dataclass
class GeocodingResultModel:
    name: str
    address: str
    lat: float
    lon: float
    category: str
    distance_km: Optional[float] = None
