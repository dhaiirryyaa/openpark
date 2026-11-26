from dataclasses import dataclass

@dataclass
class PatrolLog:
    log_id: str
    officer_id: str
    lot_id: str
    timestamp: str
    violations_found: int
