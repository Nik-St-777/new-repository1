import json

def load_transactions(file_path: str):
    """
    Загружает список транзакций из JSON‑файла.

    Параметры:
        file_path (str): Путь к JSON‑файлу с данными транзакций.

    Возвращает:
        list: Список транзакций (словарей), если файл существует и содержит список.
              Если файл не найден, содержит некорректный JSON или данные не являются
              списком — возвращается пустой список

    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Если внутри не список — возвращаем пустой список
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


if __name__ == "main":
    print(load_transactions("transactions.json"))