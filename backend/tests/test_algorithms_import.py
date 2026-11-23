def test_algorithms_package_exports():
    import backend.algorithms as algo
    assert hasattr(algo, 'dijkstra_shortest_path')
    assert hasattr(algo, 'haversine_km')
    assert hasattr(algo, 'calculate_spot_decay_probability')
