import time
from backend.algorithms.spatial_hash_grid import SpatialHashGrid

def run_benchmark():
    grid = SpatialHashGrid(1.0)
    for i in range(1000):
        grid.insert(f'lot_{i}', 12.9 + (i * 0.0001), 77.5 + (i * 0.0001))
    start = time.perf_counter()
    res = grid.query_radius(12.95, 77.55, 5.0)
    elapsed = (time.perf_counter() - start) * 1000.0
    print(f'1000-point query completed in {elapsed:.3f}ms')

if __name__ == '__main__':
    run_benchmark()
