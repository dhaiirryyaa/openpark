import time
from concurrent.futures import ThreadPoolExecutor

def mock_worker(worker_id):
    return worker_id * 2

def benchmark_concurrent_workers(workers=10, tasks=200):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        list(executor.map(mock_worker, range(tasks)))
    elapsed = time.perf_counter() - start
    print(f"ThreadPoolExecutor ({workers} workers, {tasks} tasks): {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_concurrent_workers()
