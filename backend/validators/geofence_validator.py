def validate_geofence_payload(data: dict) -> bool:
    if not isinstance(data, dict): return False
    radius = data.get('radius_m', 0)
    lat = data.get('lat')
    lon = data.get('lon')
    return 10.0 <= radius <= 10000.0 and -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0
