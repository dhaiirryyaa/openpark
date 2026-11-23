import time
from backend.models.telemetry_event import TelemetryEventModel
from datetime import datetime

def benchmark_telemetry_creation(count=5000):
    start = time.perf_counter()
    events = [
        TelemetryEventModel(1, f"SN-{i}", "enter", datetime.utcnow(), 50, 50.0)
        for i in range(count)
    ]
    elapsed = time.perf_counter() - start
    print(f"Telemetry creation: {count} events in {elapsed:.4f}s ({count/elapsed:.0f} ops/sec)")

if __name__ == '__main__':
    benchmark_telemetry_creation()
