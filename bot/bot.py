#!/usr/bin/env python
import sys
import argparse
import os
from config import config
from handlers import start, help, health, labs, scores

def run_test(command: str) -> None:
    cmd = command.strip()
    cmd = os.path.basename(cmd)
    if cmd.startswith('/'):
        cmd = cmd[1:]
    parts = cmd.split()
    base_cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    if base_cmd == "start":
        print(start.handle())
    elif base_cmd == "help":
        print(help.handle())
    elif base_cmd == "health":
        print(health.handle())
    elif base_cmd == "labs":
        print(labs.handle())
    elif base_cmd == "scores":
        if args:
            print(scores.handle(args[0]))
        else:
            print("Please provide a lab name, e.g., /scores lab-04")
    else:
        print("Unknown command. Use /help for available commands.")
    sys.exit(0)

def run_telegram():
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
    app.add_handler(CommandHandler("scores", scores.handle_telegram))
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
