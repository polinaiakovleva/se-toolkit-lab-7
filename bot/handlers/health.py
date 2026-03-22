import httpx
from config import config

def handle() -> str:
    try:
        resp = httpx.get(f"{config.LMS_API_BASE_URL}/health", timeout=5)
        if resp.status_code == 200:
            return "Backend is healthy."
        else:
            return f"Backend returned status {resp.status_code}"
    except Exception as e:
        return f"Backend unreachable: {e}"

async def handle_telegram(update, context):
    await update.message.reply_text(handle())
