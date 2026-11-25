"""Markov-chain parking occupancy stochastic simulator."""

def simulate_markov_occupancy(current_occupied: int, total_capacity: int, p_enter: float = 0.08, p_exit: float = 0.05) -> int:
    vacant = max(0, total_capacity - current_occupied)
    arrivals = int(round(vacant * p_enter))
    departures = int(round(current_occupied * p_exit))
    next_occ = current_occupied + arrivals - departures
    return max(0, min(total_capacity, next_occ))
