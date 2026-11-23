import time
import re

def benchmark_regex_classifier():
    pattern = re.compile(r'hotel|school|hospital|mall|ev|charger|covered', re.I)
    queries = ["cheapest covered ev parking near hotel", "nearest school with parking"] * 500
    
    start = time.perf_counter()
    for q in queries:
        pattern.findall(q)
    elapsed = time.perf_counter() - start
    print(f"Copilot regex classifier: {len(queries)} queries in {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_regex_classifier()
