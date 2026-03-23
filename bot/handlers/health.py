import httpx
from config import config
from services.api import LMSClient

client = LMSClient()

def handle() -> str:
    try:
        ok, info = client.get_health()
        if ok:
            return f"Backend is healthy. {info} items available."
        else:
            return f"Backend error: HTTP {info}. Check that the services are running."
    except httpx.ConnectError:
        return f"Backend error: connection refused ({config.LMS_API_BASE_URL}). Check that the services are running."
    except Exception as e:
        return f"Backend error: {e}"

async def handle_telegram(update, context):
    await update.message.reply_text(handle())
