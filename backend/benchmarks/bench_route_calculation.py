import time
from backend.algorithms.dijkstra_router import dijkstra_shortest_path

def benchmark_dijkstra():
    graph = {f"N{i}": [(f"N{i+1}", 1.0), (f"N{i+2}", 2.5)] for i in range(100)}
    graph["N100"] = []
    graph["N101"] = []
    
    start = time.perf_counter()
    for _ in range(100):
        dijkstra_shortest_path(graph, "N0", "N100")
    elapsed = time.perf_counter() - start
    print(f"Dijkstra 100-node graph: 100 runs in {elapsed:.4f}s")

if __name__ == '__main__':
    benchmark_dijkstra()
