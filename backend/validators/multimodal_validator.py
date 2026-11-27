def validate_multimodal_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    dist = data.get('walk_distance_m', -1)
    return bool(data.get('parking_lot_id') and data.get('transit_station_id') and 0 <= dist <= 1500)
