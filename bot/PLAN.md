# Bot Development Plan

## 1. Architecture
- Handlers are separate modules in `handlers/`, each exposing `handle()` (for test mode) and `handle_telegram()` (for Telegram).  
- `bot.py` parses `--test` flag; if present, calls `handle()` and prints result; otherwise starts Telegram polling.

## 2. Backend Integration
- `services/api.py` will contain an `LMSClient` using `httpx` to call backend endpoints with `LMS_API_KEY`.

## 3. Intent Routing (Task 3)
- `services/llm.py` will wrap the Qwen Code API.
- A router will use LLM to classify user message and call appropriate handler.

## 4. Deployment (Task 4)
- Bot will run as a separate container in `docker-compose.yml`.
- Environment variables from `.env.bot.secret` will be used.

This plan ensures the bot is testable, maintainable, and ready for advanced features.
