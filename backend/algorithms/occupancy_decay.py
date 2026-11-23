import math

def calculate_spot_decay_probability(free_spots: int, capacity: int, elapsed_minutes: float, turnover_rate_per_hour: float = 2.5) -> float:
    if free_spots <= 0:
        return 0.0
    current_ratio = free_spots / max(1, capacity)
    decay_constant = (turnover_rate_per_hour / 60.0) * (1.0 - current_ratio * 0.5)
    remaining_prob = current_ratio * math.exp(-decay_constant * elapsed_minutes)
    return round(min(100.0, max(0.0, remaining_prob * 100.0)), 1)
