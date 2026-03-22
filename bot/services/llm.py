import httpx
from config import config

class LLMClient:
    def __init__(self):
        self.base_url = config.LLM_API_BASE_URL
        self.headers = {"Authorization": f"Bearer {config.LLM_API_KEY}"}
        self.model = config.LLM_API_MODEL

    def chat(self, prompt: str) -> str:
        # Заглушка для Task 3
        return "LLM not implemented yet."
