def mask_card_number(number: str) -> str:
    """
    Создаём функцию mask_account_card, которая умеет обрабатывать информацию как о картах, так и о счетах.
    """
# Маскирует номер карты: 1234 56** **** 3456


    return f"{number[:4]} {number[4:6]}** **** {number[-4:]}"


def mask_account_number(number: str) -> str:
# Маскирует номер счета: **4305
     return f"**{number[-4:]}"


def mask_account_card(data: str) -> str:
#Маскирует данные карты или счета, разделяя тип и номер
    parts = data.split()

# Номер всегда в конце, но может состоять из одной части.
# Тип может состоять из нескольких слов (например, 'Visa Platinum')
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        return f"{name} {mask_account_number(number)}"
    else:
        return f"{name} {mask_card_number(number)}"


# Примеры работы:
# print(mask_account_card("Visa Platinum 7000792289606361"))
# -> Visa Platinum 7000 79** **** 6361
# print(mask_account_card("Счет 73654108430135874305"))
# -> Счет **4305




def get_date(date_str: str) -> str:
    # Если пришла не строка, принудительно выбрасываем TypeError
    if not isinstance(date_str, str):
        raise TypeError("Входные данные должны быть строкой")

    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"

import pytest

# --- Фикстуры ---

@pytest.fixture
def correct_account_number() -> str:
    """Возвращает стандартный 20-значный номер счета."""
    return "73654108430135874305"


@pytest.fixture
def expected_masked_account() -> str:
    """Возвращает ожидаемый результат маскирования для стандартного счета."""
    return "**4305"


@pytest.fixture
def account_numbers_matrix():
    """Фикстура-матрица для проверки различных номеров счетов (вход, ожидаемый результат)."""
    return [
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("9876", "**9876"),  # Минимально допустимая длина для корректного среза
    ]

# --- Примеры тестов ---
# Имппортируем ОДИН раз вверху файла из правильного модуля (masks или widget)
from src.masks import get_mask_account


# Тест с использованием простых фикстур
def test_get_mask_account(correct_account_number, expected_masked_account):
    # Убрали лишний внутренний импорт template
    assert get_mask_account(correct_account_number) == expected_masked_account


# Тест с использованием матрицы данных
def test_get_mask_account_matrix(account_numbers_matrix):
    # Убрали лишний внутренний импорт template
    for account_number, expected in account_numbers_matrix:
        # Исправили имя функции на правильное get_mask_account
        assert get_mask_account(account_number) == expected



