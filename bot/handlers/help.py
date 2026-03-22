def handle() -> str:
    return "Available commands:\n/start - welcome\n/help - this message\n/health - check backend status\n/labs - list available labs"

async def handle_telegram(update, context):
    await update.message.reply_text(handle())
