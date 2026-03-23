import httpx
from config import config

class LMSClient:
    def __init__(self):
        self.base_url = config.LMS_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {config.LMS_API_KEY}"}

    def _get(self, endpoint: str):
        with httpx.Client(timeout=10) as client:
            return client.get(f"{self.base_url}/{endpoint}", headers=self.headers)

    def get_items(self):
        return self._get("items/")

    def get_health(self):
        resp = self.get_items()
        if resp.status_code == 200:
            return True, len(resp.json())
        else:
            return False, resp.status_code

    def get_labs(self):
        resp = self.get_items()
        if resp.status_code == 200:
            items = resp.json()
            labs = [item for item in items if item.get("type") == "lab"]
            return labs
        else:
            return None

    def get_pass_rates(self, lab_name: str):
        resp = self._get(f"analytics/pass-rates?lab={lab_name}")
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
