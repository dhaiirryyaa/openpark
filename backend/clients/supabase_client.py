import urllib.request
import json
from typing import Dict, Optional

class SupabaseRESTClient:
    def __init__(self, supabase_url: str, api_key: str):
        self.base_url = (supabase_url or "").rstrip('/')
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        return {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
