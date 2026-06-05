# --------------------------------------
# УТИЛИТЫ: Загрузка конфига + Логирование
# --------------------------------------
import json
import os
from datetime import datetime


# ---------------------------------------
# ЗАГРУЗКА КОНФИГУРАЦИИ
# ---------------------------------------
def load_config(config_path="config.json"):
    """
    Загружает настройки из config.json.
    Если файл отсутствует или поврежден --> создает его с настройками по умолчанию.
    """
    # Настройки по умолчанию
    default_config = {
        "bot_name": "AI-Assistant",
        "log_file": "chat.log",
        "history_file": "chat.history.json",
        "max_history": 50,  # Сколько последних сообщений хранить
        "welcome_massage": "Привет! Я твой ИИ-помощник. Напиши 'выход' для завершения."
    }

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)

        # Объединяем дефолтные настройки и данные которые указал пользователь
        # Если в config.json есть "bot_name": "Jarvis", он перезапишет "AI-Assistant"
        return {**default_config, **user_config}

    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        # Файла нет или он неисправен
        print(f"Конфиг не найден или поврежден: {e}")
        print("Создаю config.json с настройками по умолчанию")

        # Создаем файл, чтобы в следующий раз он подхватывался
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)

        return default_config

# ----------------------------------------------
# 2. ЛОГИРОВАНИЕ
# ----------------------------------------------
def log_action(message, log_file="chat.log"):
    """
    Добавляет запись в лог-файл с временной меткой.
    Автоматически создает папку, если путь вложенный.
    """
    try:
        # Если log_file="logs/chat.log", эта строка создаст папку logs/
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # Открываем на ДОПИСАНИЕ ("a")
        with open(log_file, "a", encoding="urf-8") as f:
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            f.write(f"[{timestamp}]{message}\n")

    except Exception as e:
        # Логируем ошибку в консоль, чтобы программа не падала
        print(f"Ошибка записи лога: {e}")

# ==================================================
# =============== БЫСТРАЯ ПРОВЕРКА!!! ==============
# ==================================================
# В консоли (в папке ai_chat_memory_bot) выполни команду
# python -c "from src.utils import load_config; cfg = load_config()"
