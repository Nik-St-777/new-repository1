import json
import os
import logging

# Настройка логера для модуля
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Обработчик для файла
file_handler = logging.FileHandler("utils.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Обработчик для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Единый формат сообщений
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def load_transactions(file_path: str) -> list:
    """Принимает путь к JSON-файлу и возвращает список словарей с транзакциями.

    В случае отсутствия файла, его пустоты или неверного формата возвращает [].
    """
    # 1. Проверяем, существует ли файл вообще
    if not os.path.exists(file_path):
        return []

    try:
        # 2. Открываем и пытаемся прочитать файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # 3. Проверяем, что внутри файла именно список (а не строка или один словарь)
            if isinstance(data, list):
                return data
            else:
                return []

    # Обрабатываем пустой файл или некорректный JSON (ошибки синтаксиса)
    except json.JSONDecodeError:
        return []