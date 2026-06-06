import sys
import os

# Гарантирует, что Python видит папку src/
sys.path.insert(0, os.path.dirname(__file__))

from src.agent import AI_Agent

if __name__ == "__main__":
    # 1. Создаем агента (он сам загрузит историю, если она есть)
    bot = AI_Agent(name="TestBot",history_file="test_bot_memory.json")

    # 2. Отправляем сообщения
    print("\n--- ТЕСТ 1: Приветствие ---")
    reply1 = bot.get_response("Привет, как дела?")
    print(f"Bot: {reply1}")

    print("\n--- ТЕСТ 2: Вопрос ---")
    reply2 = bot.get_response("Кто ты такой?")
    print(f"Bot: {reply2}")

    print("\n--- ТЕСТ 3: Проверка памяти ---")
    print(f"Всего сообщений в истории: {len(bot.history)}")

    # Ожидаемый результат: 4 сообщения (2 от тебя, 2 от бота)
    print("Если файл 'test_bot_memory.json' появился в папке - все работаем!")
