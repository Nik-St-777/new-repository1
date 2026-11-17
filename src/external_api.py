import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

if not BASE_URL or not API_KEY:
    raise RuntimeError("Не заданы переменные окружения BASE_URL или API_KEY")


def get_rate(currency: str) -> float | None:
    """
    Получить текущий курс указанной валюты к рублю (RUB) через внешний API.

    Параметры:
        currency (str): Код валюты в формате ISO 4217 (например, "USD", "EUR").

    Возвращает:
        float | None: Курс валюты к RUB, если запрос успешен и данные валидны.
                      None — если произошла ошибка запроса, данные отсутствуют
                      или не удалось преобразовать результат в число.

    Пример:
        rate = get_rate("USD")
        if rate is not None:
            print(f"Курс USD к RUB: {rate}")
    """
    url = f"{BASE_URL}/latest"
    params = {"base": currency, "symbols": "RUB"}
    headers = {"apikey": API_KEY}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return float(data["rates"]["RUB"])
    except (requests.RequestException, KeyError, ValueError):
        return None


def convert_to_rub(transaction: dict) -> float:
    """
    Конвертировать сумму транзакции в рубли.

    Функция принимает словарь с данными транзакции и возвращает сумму в рублях.
    Если валюта — RUB, конвертация не требуется. Для USD и EUR выполняется
    запрос к API для получения актуального курса. Для остальных валют возвращается
    исходная сумма (без конвертации).

    Параметры:
        transaction (dict): Словарь транзакции. Ожидаемые ключи:
                            - "amount": числовое значение суммы (int/float).
                            - "currency": код валюты (например, "USD", "eur", "RUB").

    Возвращает:
        float: Сумма транзакции в рублях. Если конвертация невозможна,
               возвращается исходная сумма как float.

    Примеры:
        convert_to_rub({"amount": 100, "currency": "USD"})  # конвертирует по курсу
        convert_to_rub({"amount": 5000, "currency": "RUB"}) # вернёт 5000.0
        convert_to_rub({"amount": 200})                     # валюта по умолчанию RUB
    """
    amount = transaction.get("amount", 0)
    currency = str(transaction.get("currency", "RUB")).upper()

    if currency == "RUB":
        return float(amount)

    if currency in ("USD", "EUR"):
        rate = get_rate(currency)
        if rate is not None and rate > 0:
            return float(amount * rate)

    return float(amount)
