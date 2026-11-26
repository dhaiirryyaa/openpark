from backend.algorithms.camera_overlap_filter import deduplicate_detections

def test_camera_overlap_filter():
    dets = [
        {'bay_id': 'bay1', 'confidence': 0.85},
        {'bay_id': 'bay1', 'confidence': 0.92},
        {'bay_id': 'bay2', 'confidence': 0.80}
    ]
    deduped = deduplicate_detections(dets)
    assert len(deduped) == 2
    assert deduped[0]['confidence'] == 0.92
