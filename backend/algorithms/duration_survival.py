"""Parking bay occupancy duration survival probability model."""
import math

def estimate_spot_departure_prob(parked_duration_minutes: float, lambda_rate: float = 0.015) -> float:
    """Returns probability that vehicle will vacate in the next 15 minutes given current duration."""
    # Weibull / Exponential hazard function approximation
    prob = 1.0 - math.exp(-lambda_rate * (parked_duration_minutes ** 0.85))
    return round(min(0.95, max(0.05, prob)), 3)
