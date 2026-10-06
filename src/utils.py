import json
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def do_something():
    logger.info("Выполняем полезную функцию в utils")
    # ...


def load_transactions(file_path: str) -> list:
    """Принимает путь к JSON-файлу и возвращает список словарей с транзакциями.

    В случае отсутствия файла, его пустоты или неверного формата возвращает [].
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            else:
                return []

    except json.JSONDecodeError:
        return []
