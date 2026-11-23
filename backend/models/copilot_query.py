from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CopilotQueryModel:
    prompt: str
    user_lat: float
    user_lon: float
    detected_intent: str
    target_categories: List[str]
