from backend.algorithms.dijkstra_router import dijkstra_shortest_path

def test_dijkstra_basic():
    graph = {
        'A': [('B', 1.0), ('C', 4.0)],
        'B': [('C', 2.0), ('D', 5.0)],
        'C': [('D', 1.0)],
        'D': []
    }
    cost, path = dijkstra_shortest_path(graph, 'A', 'D')
    assert cost == 4.0
    assert path == ['A', 'B', 'C', 'D']
