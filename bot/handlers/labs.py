import httpx
from config import config

def handle() -> str:
    try:
        resp = httpx.get(f"{config.LMS_API_BASE_URL}/items/", 
                         headers={"Authorization": f"Bearer {config.LMS_API_KEY}"},
                         timeout=5)
        if resp.status_code == 200:
            items = resp.json()
            labs = [item["title"] for item in items if item.get("type") == "lab"]
            if labs:
                return "Labs:\n" + "\n".join(labs)
            else:
                return "No labs found."
        else:
            return f"Backend error: {resp.status_code}"
    except Exception as e:
        return f"Backend unreachable: {e}"

async def handle_telegram(update, context):
    await update.message.reply_text(handle())
