from backend.algorithms.bounding_box_cluster import cluster_points

def test_clustering():
    points = [
        {"id": 1, "lat": 12.9716, "lon": 77.5946},
        {"id": 2, "lat": 12.9717, "lon": 77.5947},
        {"id": 3, "lat": 13.0400, "lon": 77.6200}
    ]
    clusters = cluster_points(points, grid_size_deg=0.005)
    assert len(clusters) == 2
