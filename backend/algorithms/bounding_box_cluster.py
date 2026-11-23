from typing import List, Dict

def cluster_points(points: List[Dict], grid_size_deg: float = 0.005) -> List[Dict]:
    grid = {}
    for pt in points:
        key = (round(pt['lat'] / grid_size_deg), round(pt['lon'] / grid_size_deg))
        if key not in grid:
            grid[key] = []
        grid[key].append(pt)
        
    clusters = []
    for key, items in grid.items():
        if len(items) == 1:
            clusters.append({"type": "point", "data": items[0]})
        else:
            avg_lat = sum(i['lat'] for i in items) / len(items)
            avg_lon = sum(i['lon'] for i in items) / len(items)
            clusters.append({
                "type": "cluster",
                "count": len(items),
                "lat": round(avg_lat, 5),
                "lon": round(avg_lon, 5),
                "items": items
            })
    return clusters
