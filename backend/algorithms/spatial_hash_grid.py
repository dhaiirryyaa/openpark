"""Spatial hash grid index for rapid k-nearest neighbor lookups."""
import math

class SpatialHashGrid:
    def __init__(self, cell_size_km: float = 1.0):
        self.cell_size = cell_size_km
        self.grid = {}

    def _cell_key(self, lat: float, lon: float):
        return (int(lat / (self.cell_size / 111.0)), int(lon / (self.cell_size / 111.0)))

    def insert(self, item_id: str, lat: float, lon: float):
        key = self._cell_key(lat, lon)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append((item_id, lat, lon))

    def query_radius(self, lat: float, lon: float, radius_km: float):
        results = []
        c_key = self._cell_key(lat, lon)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                k = (c_key[0] + dx, c_key[1] + dy)
                for item_id, ilat, ilon in self.grid.get(k, []):
                    dist = math.hypot((ilat - lat) * 111.0, (ilon - lon) * 111.0)
                    if dist <= radius_km:
                        results.append((item_id, dist))
        return sorted(results, key=lambda x: x[1])
