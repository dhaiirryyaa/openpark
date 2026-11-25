from backend.algorithms.valet_dispatch import dispatch_closest_valet

def test_valet_dispatch():
    drivers = [
        {'driver_id': 'd1', 'status': 'BUSY', 'lat': 12.97, 'lon': 77.59},
        {'driver_id': 'd2', 'status': 'AVAILABLE', 'lat': 12.971, 'lon': 77.591},
        {'driver_id': 'd3', 'status': 'AVAILABLE', 'lat': 12.980, 'lon': 77.600}
    ]
    assigned = dispatch_closest_valet(drivers, 12.971, 77.591)
    assert assigned == 'd2'
