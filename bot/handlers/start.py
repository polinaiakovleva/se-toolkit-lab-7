def handle() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

async def handle_telegram(update, context):
    await update.message.reply_text(handle())
