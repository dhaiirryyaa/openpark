import math
from typing import List, Tuple

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)

def distance_matrix(origins: List[Tuple[float, float]], destinations: List[Tuple[float, float]]) -> List[List[float]]:
    matrix = []
    for (o_lat, o_lon) in origins:
        row = [haversine_km(o_lat, o_lon, d_lat, d_lon) for (d_lat, d_lon) in destinations]
        matrix.append(row)
    return matrix
