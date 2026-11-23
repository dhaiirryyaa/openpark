import time
from backend.algorithms.haversine_matrix import haversine_km

def benchmark_spatial_search(iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        haversine_km(12.9716, 77.5946, 12.9815, 77.6045)
    elapsed = time.perf_counter() - start
    print(f"Spatial Haversine: {iterations} iterations in {elapsed:.4f}s ({elapsed/iterations*1e6:.2f}us/op)")

if __name__ == '__main__':
    benchmark_spatial_search()
