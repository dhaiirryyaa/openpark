"""Peak hour congestion penalty matrix."""

def get_congestion_penalty_factor(level: str) -> float:
    penalties = {
        "LOW": 1.0,
        "MODERATE": 1.35,
        "HEAVY": 1.85,
        "SEVERE": 2.4
    }
    return penalties.get(level.upper(), 1.0)
