import sys
import os

# Добавляем текущую папку в пути, чтобы импорты сработали
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from handlers.router import handle

# Те самые запросы, на которых падал авточекер
test_queries = [
    "what labs are available",
    "show me scores for lab 4",
    "how many students are enrolled",
    "which group is doing best in lab 3",
    "which lab has the lowest pass rate"
]

print("🚀 Starting local router tests...\n")

for query in test_queries:
    print(f"Пользователь: {query}")
    try:
        response = handle(query)
        print(f"Бот: {response}\n{'-'*40}")
    except Exception as e:
        print(f"🔥 ОШИБКА: {e}\n{'-'*40}")

print("✅ Testing finished!")
