"""Multi-objective parking lot score ranker balancing distance, price, and availability."""

def score_parking_lot(distance_m: float, free_spots: int, price_hourly: float, has_ev: bool = False, w_dist=0.4, w_spots=0.4, w_price=0.2) -> float:
    norm_dist = max(0.0, 1.0 - (distance_m / 5000.0))
    norm_spots = min(1.0, free_spots / 50.0)
    norm_price = max(0.0, 1.0 - (price_hourly / 100.0))
    ev_bonus = 0.1 if has_ev else 0.0
    return round(w_dist * norm_dist + w_spots * norm_spots + w_price * norm_price + ev_bonus, 3)
