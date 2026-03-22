import httpx
from config import config

class LMSClient:
    def __init__(self):
        self.base_url = config.LMS_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {config.LMS_API_KEY}"}

    def get(self, endpoint: str):
        with httpx.Client(timeout=10) as client:
            return client.get(f"{self.base_url}/{endpoint}", headers=self.headers)
