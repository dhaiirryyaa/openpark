import time

def benchmark_lru_cache():
    cache = {f"lot_{i}": {"name": f"Lot {i}", "free": i} for i in range(100)}
    start = time.perf_counter()
    for _ in range(10000):
        _ = cache.get("lot_42")
    elapsed = time.perf_counter() - start
    print(f"L1 Cache get: 10,000 lookups in {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_lru_cache()
