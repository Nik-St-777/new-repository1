from unittest.mock import patch
import pytest

from src.widget import mask_account_card


# 1. Тесты для проверки, что функция корректно распознает и применяет нужный тип маскировки в зависимости от типа входных данных (карта или счет).

# Указываем путь к функциям внутри модуля, где лежит mask_account_card
@patch("src.widget.mask_card_number")
def test_mask_card_calls_card_formatter(mock_mask_card):
    """Проверка, что для карты вызывается функция маскирования карты"""
    # Настраиваем фейковый возврат для функции маскирования карты
    mock_mask_card.return_value = "7000 79** **** 6361"

    result = mask_account_card("Visa Platinum 7000792289606361")

    # Проверяем, что функция маскирования карты была вызвана с верным номером
    mock_mask_card.assert_called_once_with("7000792289606361")
    # Проверяем итоговую строку
    assert result == "Visa Platinum 7000 79** **** 6361"


@patch("src.widget.mask_account_number")
def test_mask_account_calls_account_formatter(mock_mask_account):
    """Проверка, что для счета вызывается функция маскирования счета"""
    # Настраиваем фейковый возврат для функции маскирования счета
    mock_mask_account.return_value = "**4305"

    result = mask_account_card("Счет 73654108430135874305")

    # Проверяем, что функция маскирования счета была вызвана с верным номером
    mock_mask_account.assert_called_once_with("73654108430135874305")
    # Проверяем итоговую строку
    assert result == "Счет **4305"


@patch("src.widget.mask_account_number")
def test_mask_account_case_insensitive(mock_mask_account):
    """Проверка, что слово 'счет' распознается в любом регистре (Счет, СЧЕТ, счет)"""
    mock_mask_account.return_value = "**4305"

    # Передаем "счет" маленькими буквами
    result = mask_account_card("счет 73654108430135874305")

    mock_mask_account.assert_called_once()
    assert result == "счет **4305"


@patch("src.widget.mask_card_number")
def test_mask_card_with_single_word_name(mock_mask_card):
    """Проверка работы с картой, название которой состоит из одного слова"""
    mock_mask_card.return_value = "XXXX XXXX XXXX XXXX"

    result = mask_account_card("Mastercard 1234567812345678")

    mock_mask_card.assert_called_once_with("1234567812345678")
    assert result == "Mastercard XXXX XXXX XXXX XXXX"

# 2. Параметризованные тесты с разными типами карт и счетов для проверки универсальности функции.

@pytest.mark.parametrize(
    "input_data, expected_name, expected_number, mock_return, final_expected",
    [
        # Карты с названиями из одного слова
        ("Visa 4571736541084301", "Visa", "4571736541084301", "4571 73** **** 4301", "Visa 4571 73** **** 4301"),
        ("Mastercard 5412751234123456", "Mastercard", "5412751234123456", "5412 75** **** 3456",
         "Mastercard 5412 75** **** 3456"),
        ("Maestro 6761123456789012", "Maestro", "6761123456789012", "6761 12** **** 9012",
         "Maestro 6761 12** **** 9012"),
        ("МИР 2200123456789012", "МИР", "2200123456789012", "2200 12** **** 9012", "МИР 2200 12** **** 9012"),

        # Карты с названиями из нескольких слов
        ("Visa Platinum 7000792289606361", "Visa Platinum", "7000792289606361", "7000 79** **** 6361",
         "Visa Platinum 7000 79** **** 6361"),
        ("American Express 378282246310005", "American Express", "378282246310005", "3782 82** **** 1005",
         "American Express 3782 82** **** 1005"),
        ("Золотая Корона 9999888877776666", "Золотая Корона", "9999888877776666", "9999 88** **** 6666",
         "Золотая Корона 9999 88** **** 6666"),
    ]
)
@patch("src.widget.mask_card_number")
def test_mask_account_card_various_cards(mock_mask_card, input_data, expected_name, expected_number, mock_return,
                                         final_expected):
    """Проверка работы функции с различными типами и названиями карт"""
    # Настраиваем возвращаемое значение для мока
    mock_mask_card.return_value = mock_return

    result = mask_account_card(input_data)

    # Проверяем, что функция маскирования карты вызвана ровно с номером карты
    mock_mask_card.assert_called_once_with(expected_number)
    # Проверяем склейку названия и маски
    assert result == final_expected


@pytest.mark.parametrize(
    "input_data, expected_name, expected_number, mock_return, final_expected",
    [
        # Счета с разным регистром слова "счет"
        ("Счет 73654108430135874305", "Счет", "73654108430135874305", "**4305", "Счет **4305"),
        ("счет 40817810500001234567", "счет", "40817810500001234567", "**4567", "счет **4567"),
        ("СЧЕТ 11112222333344445555", "СЧЕТ", "11112222333344445555", "**5555", "СЧЕТ **5555"),
    ]
)
@patch("src.widget.mask_account_number")
def test_mask_account_card_various_accounts(mock_mask_account, input_data, expected_name, expected_number, mock_return,
                                            final_expected):
    """Проверка работы функции со счетами в разных регистрах"""
    # Настраиваем возвращаемое значение для мока
    mock_mask_account.return_value = mock_return

    result = mask_account_card(input_data)

    # Проверяем, что функция маскирования счета вызвана ровно с номером счета
    mock_mask_account.assert_called_once_with(expected_number)
    # Проверяем склейку слова "Счет" и маски
    assert result == final_expected

# 3. Тестирование функции на обработку некорректных входных данных и проверка ее устойчивости к ошибкам.
# 1. Тесты для проверки, что функция корректно распознает и применяет нужный тип маскировки в зависимости от типа входных данных (карта или счет).

# Указываем путь к функциям внутри модуля, где лежит mask_account_card
@patch("src.widget.mask_card_number")
def test_mask_card_calls_card_formatter(mock_mask_card):
    """Проверка, что для карты вызывается функция маскирования карты"""
    # Настраиваем фейковый возврат для функции маскирования карты
    mock_mask_card.return_value = "7000 79** **** 6361"

    result = mask_account_card("Visa Platinum 7000792289606361")

    # Проверяем, что функция маскирования карты была вызвана с верным номером
    mock_mask_card.assert_called_once_with("7000792289606361")
    # Проверяем итоговую строку
    assert result == "Visa Platinum 7000 79** **** 6361"


@patch("src.widget.mask_account_number")
def test_mask_account_calls_account_formatter(mock_mask_account):
    """Проверка, что для счета вызывается функция маскирования счета"""
    # Настраиваем фейковый возврат для функции маскирования счета
    mock_mask_account.return_value = "**4305"

    result = mask_account_card("Счет 73654108430135874305")

    # Проверяем, что функция маскирования счета была вызвана с верным номером
    mock_mask_account.assert_called_once_with("73654108430135874305")
    # Проверяем итоговую строку
    assert result == "Счет **4305"


@patch("src.widget.mask_account_number")
def test_mask_account_case_insensitive(mock_mask_account):
    """Проверка, что слово 'счет' распознается в любом регистре (Счет, СЧЕТ, счет)"""
    mock_mask_account.return_value = "**4305"

    # Передаем "счет" маленькими буквами
    result = mask_account_card("счет 73654108430135874305")

    mock_mask_account.assert_called_once()
    assert result == "счет **4305"


@patch("src.widget.mask_card_number")
def test_mask_card_with_single_word_name(mock_mask_card):
    """Проверка работы с картой, название которой состоит из одного слова"""
    mock_mask_card.return_value = "XXXX XXXX XXXX XXXX"

    result = mask_account_card("Mastercard 1234567812345678")

    mock_mask_card.assert_called_once_with("1234567812345678")
    assert result == "Mastercard XXXX XXXX XXXX XXXX"

# 1. Тестирование правильности преобразования даты.
import pytest

from src.widget import get_date  # Замените путь, если функция лежит в другом файле


def test_get_date_standard():
    """Тест стандартной даты из примера"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


@pytest.mark.parametrize(
    "input_date, expected_output",
    [
        # Разные дни и месяцы (однозначные и двузначные)
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
        ("1999-12-31T23:59:59.999999", "31.12.1999"),
        # Конец года и переход месяца
        ("2026-10-25T15:30:00.123456", "25.10.2026"),
        # Тест високосного года (29 февраля)
        ("2024-02-29T12:00:00.000000", "29.02.2024"),
    ],
)
def test_get_date_formats(input_date, expected_output):
    """Параметризованный тест для проверки различных корректных дат"""
    assert get_date(input_date) == expected_output


def test_get_date_short_string():
    """Тест с минимально достаточной строкой (только дата без времени)"""
    assert get_date("2023-05-18") == "18.05.2023"

# 2.Проверка работы функции на различных входных форматах даты, включая граничные случаи и нестандартные строки с датами.

import pytest

from src.widget import get_date  # Замените путь на ваш актуальный


# 1. Тесты на нестандартные форматы, которые функция всё равно обработает успешно из-за совпадения индексов
@pytest.mark.parametrize(
    "input_str, expected",
    [
        # Формат без разделителей (ГГГГММДД...), если индексы сместятся, результат изменится,
        # но для "2024-03-11" дефисы стоят на 4-й и 7-й позициях.
        # Проверим строку, где вместо дефисов другие символы, но позиции сохранены:
        ("2024/03/11T02:26:18", "11.03.2024"),
        ("2024.03.11 12:00:00", "11.03.2024"),
        # Дата с пробелами вместо дефисов
        ("2024 03 11", "11.03.2024"),
    ],
)
def test_get_date_non_standard_delimiters(input_str, expected):
    """Проверка работы с альтернативными разделителями при сохранении позиций"""
    assert get_date(input_str) == expected


# 2. Граничные случаи по длине строки (короткие строки)
def test_get_date_only_date_no_time():
    """Строка содержит только дату ровно до 10 символов"""
    assert get_date("2024-03-11") == "11.03.2024"


@pytest.mark.parametrize(
    "short_str, expected",
    [
        ("2024-03", ".03.2024"),  # Нет дня (срез [8:10] вернет пустую строку)
        ("2024", "..2024"),  # Есть только год (остальные срезы пустые)
        ("", ".."),  # Пустая строка
    ],
)
def test_get_date_short_inputs(short_str, expected):
    """Проверка поведения срезов на слишком коротких строках"""
    assert get_date(short_str) == expected


# 3. Тест на "невозможные" даты (поведение функции при отсутствии валидации)
def test_get_date_invalid_calendar_date():
    """Функция не использует datetime, поэтому пропустит несуществующую дату"""
    # 99 число 99 месяца — функция просто переставит строковые индексы
    assert get_date("9999-99-99T00:00:00") == "99.99.9999"


# 4. Негативные тесты на типы данных
@pytest.mark.parametrize("invalid_type", [1234567890, None, [], {}])
def test_get_date_wrong_types(invalid_type):
    """Передача нестроковых типов должна вызывать ошибку TypeError при попытке взять срез"""
    with pytest.raises(TypeError):
        get_date(invalid_type)

# 3. Проверка, что функция корректно обрабатывает входные строки, где отсутствует дата.
@pytest.mark.parametrize(
    "missing_date_input, expected_output",
    [
        ("", ".."),
        (" ", ".. "),  # Исправили ожидаемый результат (с пробелом на конце)
        ("123", "..123"),
        ("2024", "..2024"),
        ("2024-05", ".05.2024"),
    ],
)
def test_get_date_missing_parts_parametrized(missing_date_input, expected_output):
    """Параметризованный тест для проверки поведения при отсутствии или нехватке частей даты"""
    # Убрали кавычки вокруг переменной expected_output
    assert get_date(missing_date_input) == expected_output
