"""Dynamic multi-modal parking-plus-transit routing scorer."""

def score_multimodal_park_and_ride(driving_time_min: float, transit_time_min: float, parking_fee_inr: float, transit_fare_inr: float, direct_drive_min: float) -> dict:
    total_time = driving_time_min + transit_time_min
    total_cost = parking_fee_inr + transit_fare_inr
    time_saved = direct_drive_min - total_time
    is_recommended = total_time <= direct_drive_min * 1.15 and total_cost < 150.0
    return {
        "total_time_min": round(total_time, 1),
        "total_cost_inr": round(total_cost, 2),
        "time_saved_min": round(time_saved, 1),
        "is_recommended": is_recommended
    }
