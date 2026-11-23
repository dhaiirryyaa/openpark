import heapq
from typing import Dict, List, Tuple

def dijkstra_shortest_path(graph: Dict[str, List[Tuple[str, float]]], start: str, end: str) -> Tuple[float, List[str]]:
    queue = [(0.0, start, [start])]
    visited = set()
    
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        
        if node == end:
            return (cost, path)
            
        for (neighbor, weight) in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))
                
    return (float('inf'), [])
