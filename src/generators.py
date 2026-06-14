# код функции filter_by_currency


def filter_by_currency(transactions, currency):
    """
    Возвращает итератор, который поочередно выдает транзакции,
    где код валюты (currency code) соответствует заданной строке.
    """
    for transaction in transactions:
        # Безопасно извлекаем вложенные словари
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")

        # Если код валюты совпадает с искомым, поочередно возвращаем транзакцию
        if currency_code == currency:
            yield transaction

# код генератора
def transaction_descriptions(transactions):
    """
    Генератор, который поочередно возвращает описание каждой транзакции.
    """
    for transaction in transactions:
        # Безопасно извлекаем описание. Если ключа нет, возвращаем дефолтный текст.
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start, end):
    """
    Генератор номеров карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне.
    """
    for number in range(start, end + 1):
        # Превращаем число в строку из 16 цифр, заполняя пустоты нулями слева
        card_str = f"{number:016d}"

        # Разрезаем 16-значную строку на 4 блока по 4 цифры через пробел
        formatted_card = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card

