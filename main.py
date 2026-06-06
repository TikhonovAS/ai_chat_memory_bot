import sys
import os

# Добавляем корень проекта в пути импорта, чтобы Python видел папку src/
# Это стандартный паттерн для src-layout проектов
sys.path.insert(0, os.path.dirname(__file__))

from src.utils import load_config, log_action
from src.agent import AI_Agent


def main():
    """Основной цикл работы чат-бота"""
    print("Запуск AI Chat Bot ...\n")

    # 1. Загружаем настройки (или создаем config.json, если его нет)
    cfg = load_config()
    log_action("Бот запущен", log_file=cfg["log_file"])

    # 2. Создаем агента (он автоматически подгрузит старую историю)
    bot = AI_Agent(
        name=cfg.get("bot_name", "AI_Assistant"),
        history_file=cfg.get("history_file", "chat_history.json")
    )

    # 3. Приветственное сообщения из конфига
    print(f"\n{cfg.get('welcome_message', 'Привет! Я готов к работе.')}")
    print("Команды: 'выход' / 'exit' / 'clear' (очистить память)")
    print("=" * 50)

    # 4. БЕСКОНЕЧНЫЙ ЦИКЛ ДИАЛОГА
    try:
        while True:
            user_input = input("\nТы: ").strip()

            # Пропускаем пустые строки
            if not user_input:
                continue

            # Обработка команд выхода
            if user_input.lower() in ["выход", "exit", "quit", "stop"]:
                print("До встречи! История диалога сохранена.")
                log_action("Пользователь завершил диалог", log_file=cfg["log_file"])
                break

            # Команда очистки памяти
            if user_input.lower() == "clear":
                bot.history = []
                bot.save_history()
                print("Память очищена. Начнем с чистого листа!")
                log_action("Память бота очищена пользователем", log_file=cfg["log_file"])
                continue

            # Получаем ответ от агента
            response = bot.get_response(user_input)
            print(f"{bot.name}: {response}")

    except KeyboardInterrupt:
        # Безопасный ответ от агента
        print("\nДиалог прерван (Ctrl+C). История сохранена")
        log_action("Диалог прерван через Ctrl+C", log_file=cfg["log_file"])

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        log_action(f"Критическая ошибка в main: {e}", log_file=cfg["log_file"])


# Эта конструкция гарантирует, что main() запустится только при прямом запуске файле
if __name__ == "__main__":
    main()
