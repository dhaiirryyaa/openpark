import time
from backend.algorithms.haversine_matrix import distance_matrix

def benchmark_matrix():
    origins = [(12.97 + i*0.01, 77.59 + i*0.01) for i in range(10)]
    destinations = [(12.98 + i*0.01, 77.60 + i*0.01) for i in range(50)]
    
    start = time.perf_counter()
    for _ in range(50):
        distance_matrix(origins, destinations)
    elapsed = time.perf_counter() - start
    print(f"10x50 Distance Matrix: 50 runs in {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_matrix()
