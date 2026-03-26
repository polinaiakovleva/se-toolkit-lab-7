FROM python:3.12-slim

# Берем быстрый пакетный менеджер uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем весь код бота
COPY . .

# Устанавливаем зависимости
RUN uv sync --no-dev

# Запускаем бота
CMD ["uv", "run", "python", "bot.py"]
