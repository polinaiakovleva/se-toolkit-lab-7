import httpx
from config import config
from services.api import LMSClient

client = LMSClient()

def handle(lab_name: str) -> str:
    lab = lab_name.strip().lower()
    if not lab.startswith("lab-"):
        lab = f"lab-{lab}"
    try:
        data = client.get_pass_rates(lab)
        if data is None:
            return f"Could not fetch pass rates for {lab}. Check that the lab exists."
        if not data:
            return f"No data for {lab}."
        lines = [f"Pass rates for {lab}:"]
        for item in data:
            lines.append(f"- {item['task']}: {item['avg_score']}% ({item['attempts']} attempts)")
        return "\n".join(lines)
    except Exception as e:
        return f"Error fetching scores: {e}"

async def handle_telegram(update, context):
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a lab name, e.g., /scores lab-04")
        return
    lab_name = args[0]
    await update.message.reply_text(handle(lab_name))
