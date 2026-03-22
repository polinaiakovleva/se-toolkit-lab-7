#!/usr/bin/env python
import sys
import argparse
from config import config
from handlers import start, help, health, labs

def run_test(command: str) -> None:
    cmd = command.strip()
    if cmd.startswith("/start"):
        print(start.handle())
    elif cmd.startswith("/help"):
        print(help.handle())
    elif cmd.startswith("/health"):
        print(health.handle())
    elif cmd.startswith("/labs"):
        print(labs.handle())
    else:
        print("Unknown command")
    sys.exit(0)

def run_telegram():
    """Run bot with Telegram polling."""
    import asyncio
    from telegram.ext import Application, CommandHandler

    if not config.BOT_TOKEN:
        print("Error: BOT_TOKEN not set in .env.bot.secret")
        sys.exit(1)

    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start.handle_telegram))
    app.add_handler(CommandHandler("help", help.handle_telegram))
    app.add_handler(CommandHandler("health", health.handle_telegram))
    app.add_handler(CommandHandler("labs", labs.handle_telegram))
    app.run_polling()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="Run command in test mode", default=None)
    args = parser.parse_args()
    if args.test:
        run_test(args.test)
    else:
        run_telegram()

if __name__ == "__main__":
    main()
