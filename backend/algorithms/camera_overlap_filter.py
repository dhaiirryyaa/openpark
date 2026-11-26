"""Multi-camera vision overlap deduplication filter."""

def deduplicate_detections(detections: list, iou_threshold: float = 0.5) -> list:
    # Sort by confidence descending
    sorted_dets = sorted(detections, key=lambda d: d.get('confidence', 0), reverse=True)
    kept = []
    for d in sorted_dets:
        if not any(d.get('bay_id') == k.get('bay_id') for k in kept):
            kept.append(d)
    return kept
