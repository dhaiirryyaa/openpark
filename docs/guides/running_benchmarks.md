# Running Backend Performance Benchmarks

Execute performance benchmarks:
```bash
python3 backend/benchmarks/bench_spatial_query.py
python3 backend/benchmarks/bench_telemetry_throughput.py
python3 backend/benchmarks/bench_route_calculation.py
```
Results must satisfy latency budgets outlined in `backend/benchmarks/benchmark_results.json`.
