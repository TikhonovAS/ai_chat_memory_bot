import sys
import os

# Добавляем корень проекта в пути поиска, чтобы Python увидел src/
sys.path.insert(0, os.path.dirname(__file__))

from src.utils import load_config, log_action

cfg = load_config()
print("Конфиг загружен", cfg)
log_action ("Тест из скрипта", cfg["log_file"])
print("Лог записан")