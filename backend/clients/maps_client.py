from typing import Dict, List

class UnifiedMapsClient:
    def __init__(self, google_key: str = "", ola_key: str = ""):
        self.google_key = google_key
        self.ola_key = ola_key

    def is_configured(self) -> bool:
        return bool(self.google_key or self.ola_key)
