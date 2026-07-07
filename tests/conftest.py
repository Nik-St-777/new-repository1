import pytest


@pytest.fixture
def card_number():
    return "7000792289606361"


import pytest


@pytest.fixture
def account_number():
    return "73654108430135874305"


# фикстура на функцию mask_account_card

import pytest


# --- Простые фикстуры ---


@pytest.fixture
def card_input_data():
    """Возвращает строку с данными карты."""
    return "Visa Platinum 7000792289606361"


@pytest.fixture
def account_input_data():
    """Возвращает строку с данными счета."""
    return "Счет 73654108430135874305"


# фикстура на функцию get_date

import pytest


# Простая фикстура, которая возвращает строку с датой в формате ISO
@pytest.fixture
def sample_date():
    return "2024-03-11T02:26:18.671407"


# фикстура на функцию filter_by_state
import pytest


# Простая фикстура, возвращающая список словарей со статусами
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]


# фикстура на функцию sort_by_date
import pytest


# Простая фикстура, возвращающая список словарей со статусами
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
    ]


# фикстура на функцию sort_by_date
import pytest


# Простая фикстура с неотсортированными данными
@pytest.fixture
def unsorted_data():
    return [
        {"id": 1, "date": "2019-08-26T10:50:58.294041"},
        {"id": 2, "date": "2024-03-11T02:26:18.671407"},
        {"id": 3, "date": "2021-01-15T12:00:00.000000"}]


import pytest

@pytest.fixture
def sample_transactions_data():
    return [
        # Здесь должны быть ваши тестовые данные транзакций
    ]
import pytest

@pytest.fixture
def sample_transactions_data():
    return [
        {"id": 1, "operationAmount": {"currency": {"name": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"name": "RUB"}}},
    ]
