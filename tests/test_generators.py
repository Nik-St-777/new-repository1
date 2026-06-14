# тест на функцию filter_by_currency
import pytest
from src.generators import filter_by_currency


def test_filter_by_currency_success():
    """Тест успешной фильтрации транзакций по заданной валюте USD."""
    mock_transactions = [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет"
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод с карты на карту"
        }
    ]

    # Получаем итератор и преобразуем его в список
    result = list(filter_by_currency(mock_transactions, "USD"))

    # Должно найтись ровно 2 транзакции
    assert len(result) == 2
    # Проверяем, что вернулись корректные элементы по их ID
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_no_match():
    """Тест ситуации, когда транзакции с указанной валютой отсутствуют."""
    mock_transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "RUB"}}}
    ]

    result = list(filter_by_currency(mock_transactions, "EUR"))

    # Список должен быть пустым
    assert result == []


def test_filter_by_currency_missing_keys():
    """Тест безопасности функции при работе с поврежденной структурой данных."""
    mock_transactions = [
        {"id": 1},  # Полностью отсутствует operationAmount
        {"id": 2, "operationAmount": {}},  # Отсутствует currency
        {"id": 3, "operationAmount": {"currency": {}}},  # Отсутствует code
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}}  # Корректная запись
    ]

    result = list(filter_by_currency(mock_transactions, "USD"))

    # Функция не должна упасть, а должна вернуть только одну корректную транзакцию
    assert len(result) == 1
    assert result[0]["id"] == 4

import pytest
from src.generators import transaction_descriptions


def test_transaction_descriptions_success():
    """Тест успешного извлечения всех описаний из списка транзакций."""
    mock_transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3},  # Случай без ключа "description" для проверки работы .get()
    ]

    # Превращаем генератор в список для сверки всех значений
    result = list(transaction_descriptions(mock_transactions))

    expected = ["Перевод организации", "Перевод со счета на счет", "Описание отсутствует"]

    assert result == expected


def test_transaction_descriptions_by_step():
    """Тест поочередного извлечения данных через функцию next()."""
    mock_transactions = [
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод организации"},
    ]

    descriptions_gen = transaction_descriptions(mock_transactions)

    # Проверяем строго по одному элементу за раз, как в примере из задания
    assert next(descriptions_gen) == "Перевод с карты на карту"
    assert next(descriptions_gen) == "Перевод организации"


def test_transaction_descriptions_empty():
    """Тест работы генератора с пустым входным списком транзакций."""
    result = list(transaction_descriptions([]))

    assert result == []

import pytest
from src.generators import card_number_generator


def test_card_number_generator_success():
    """Тест генерации номеров карт в заданном диапазоне."""
    # Превращаем генератор в список для проверки всех значений сразу
    result = list(card_number_generator(1, 3))

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]

    assert result == expected


def test_card_number_generator_single():
    """Тест генерации одной карты, когда границы диапазона совпадают."""
    result = list(card_number_generator(9999, 9999))
    assert result == ["0000 0000 0000 9999"]


def test_card_number_generator_by_step():
    """Тест пошагового извлечения номеров карт через функцию next()."""
    cards_gen = card_number_generator(10, 11)

    assert next(cards_gen) == "0000 0000 0000 0010"
    assert next(cards_gen) == "0000 0000 0000 0011"
