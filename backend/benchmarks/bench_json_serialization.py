import time
import json

def benchmark_json():
    payload = [{"id": i, "name": f"Parking Lot {i}", "free": 20} for i in range(500)]
    start = time.perf_counter()
    for _ in range(200):
        s = json.dumps(payload)
        json.loads(s)
    elapsed = time.perf_counter() - start
    print(f"JSON 500-item serialize/deserialize: 200 runs in {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_json()
