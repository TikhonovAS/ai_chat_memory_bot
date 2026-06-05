# -----------------------------------------
# ЯДРО БОТА: Класс AI_Agent
# -----------------------------------------
import json
import random
import os

from src.utils import log_action, load_config

class AI_Agent:
    """
    Класс, представляющий ИИ-агента.
    Управляет памятью, историей диалога и логикой ответов.
    """
    def __init__(self, name, history_file="chat_history.json"):
        """
        Инициализация агента.
        Сразу пытается загрузить старую историю, если есть файл.
        """
        self.name = name
        self.history_file = history_file
        self.history = []

        # Загружаем историю при старте
        self.load_history()

        log_action(f"Агент '{self.name}' запущен. Загружено сообщений: {len(self.history)}")
        print(f"Привет! Я {self.name}. У меня в памяти {len(self.history)} сообщений.")
    def load_history(self):
        """Загружаем историю диалога из JSON-файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
                print(f"История загружена из {self.history_file}")
            except Exception as e:
                print(f"Ошибка чтения истории: {e}")
                self.history = []

            else:
                print("История не найдена, начинаем чистый диалог.")

    def save_history(self):
        """Сохраняет текущую историю в JSON-файл"""
        try:
            # Важно! Мы сохраняем только последние N сообщений,
            # чтобы файл не рос бесконечно (эмуляция окна контекста)
            # Допустим, храним последние 50 сообщений
            max_msgs = 50
            if len(self.history) > max_msgs:
                self.history = self.history[-max_msgs:]

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
                print(f"История сохранена: {len(self.history)} записей")
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def add_message(self, role, text):
        """Добавляет сообщение в историю (и в память, и на диск"""
        msg = {"role": role, "text": text}
        self.history.append(msg)
        self.save_history()      # Сохраняем после каждого сообщения!

    def get_response(self, user_text):
        """
        Обрабатывает сообщения пользователя и возвращает ответ.
        1. Записывает вопрос пользователя в историю
        2. Генерирует ответ.
        3. Записывает ответ в историю.
        """
        # 1. Запоминает, что спросил человек
        self.add_message("user", user_text)

        # 2. Имитация мышления (думания)
        print(f"{self.name} думает...")

        # Простая логика ответов (заглушка)
        if "привет" in user_text.lower():
            answer = f"Привет! Рад видеть тебя снова. Мы обсудили уже {len(self.history)} тем."
        elif "как дела" in user_text.lower():
            answer = f"У меня все отлично, спасибо! Готов помочь с кодом."
        elif "кто ты" in user_text.lower():
            answer = f"Я {self.name}, твой персональный ИИ-ассистент."
        else:
            answers = [
                "Интересный вопрос! Дай мне подумать ..."
                "Я пока учусь, но постараюсь помочь."
                "Это напоминает мне рекурсию - бесконечный поиск ответа!"
                "Запиши это в историю, это важная мысль"
            ]
            answer = random.choice(answers)

        # 3. Запоминает наш ответ
        self.add_message("assistant", answer)

        return answer
