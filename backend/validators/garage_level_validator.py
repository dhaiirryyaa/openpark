def validate_garage_level(data: dict) -> bool:
    if not isinstance(data, dict): return False
    floor = data.get('floor_number')
    bays = data.get('total_bays', 0)
    return isinstance(floor, int) and -5 <= floor <= 20 and bays > 0
