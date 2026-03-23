from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def handle() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands, or ask me a question in plain text."

async def handle_telegram(update, context):
    keyboard = [
        [InlineKeyboardButton("Available labs", callback_data="labs")],
        [InlineKeyboardButton("Lowest pass rate lab", callback_data="lowest_pass")],
        [InlineKeyboardButton("Top students in lab 4", callback_data="top_lab4")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(handle(), reply_markup=reply_markup)
