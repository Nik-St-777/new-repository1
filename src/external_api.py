import requests
import os
from dotenv import load_dotenv
def function(transaction, convert_currency):
    amount = float(transaction['operationAmount']['amount'])
    if transaction['operationAmount']['currency']['code'] in ['USD', 'EUR']:
        converted_amount = convert_currency(amount, transaction['operationAmount']['currency']['code'])
        return converted_amount
    else:
        # Логика для других валют
        return amount  # или другая логика
# функция конвертации валюты
def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
        """
        Отправляет запрос к API, получает курс и возвращает конвертированную сумму.
        """
        load_dotenv()  # Загружаем переменные окружения из .env

        API_KEY = os.getenv("API_KEY")
        BASE_URL = os.getenv("BASE_URL")


        headers = {
            "apikey": API_KEY 
        }

        # Параметры запроса для эндпоинта /convert
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount
        }

        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            response.raise_for_status()  #

            data = response.json()

            # API возвращает результат конвертации в поле 'result'
            if "result" in data:
                return float(data["result"])
            else:
                raise KeyError("Ответ API не содержит поле 'result'")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении HTTP-запроса: {e}")
            raise
