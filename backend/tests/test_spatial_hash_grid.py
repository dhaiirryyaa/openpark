from backend.algorithms.spatial_hash_grid import SpatialHashGrid

def test_spatial_hash_grid():
    grid = SpatialHashGrid(1.0)
    grid.insert('lot1', 12.9716, 77.5946)
    grid.insert('lot2', 12.9800, 77.6000)
    res = grid.query_radius(12.9716, 77.5946, 2.0)
    assert len(res) >= 1
    assert res[0][0] == 'lot1'
