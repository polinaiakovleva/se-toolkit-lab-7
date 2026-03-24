import json
import httpx
from config import config

class LLMClient:
    def __init__(self):
        self.base_url = config.LLM_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {config.LLM_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model = config.LLM_API_MODEL

    def chat_completion(self, messages, tools=None, tool_choice="auto"):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        with httpx.Client(timeout=30) as client:
            response = client.post(f"{self.base_url}/chat/completions",
                                   headers=self.headers,
                                   json=payload)
            response.raise_for_status()
            return response.json()
