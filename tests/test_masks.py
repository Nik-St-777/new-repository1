import pytest
from src.masks import get_mask_card_number, get_mask_account


# 1. Тестирование правильности маскирования стандартного 16-значного номера
def test_get_mask_card_number_standard():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

# 2. Проверка работы функции на различных входных форматах номеров карт, включая граничные случаи и нестандартные длины номеров

def test_mask_card_number_short_length():
    """Проверка граничного случая: нестандартная короткая длина (13 знаков)."""
    # Срез [-4:] заберёт "0123", срез [4:6] заберёт "56"
    assert get_mask_card_number("1234567890123") == "1234 56** **** 0123"


def test_mask_card_number_long_length():
    """Проверка граничного случая: нестандартная длинная длина (19 знаков)."""
    # Из-за жёстких срезов [4:6] и [-4:] средняя часть цифр просто проигнорируется
    assert get_mask_card_number("1234567890123456789") == "1234 56** **** 6789"

    import pytest
    from src.masks import get_mask_account

# 1. Тестирование правильности маскирования номера счета.
def test_get_mask_account():
    assert get_mask_account("73654108430135874305")== "**4305"

    # 2.Проверка работы функции с различными форматами и длинами номеров счетов.
    def test_mask_account_standard():
        """Тест стандартного 20-значного номера счета"""
        assert get_mask_account("73654108430135874305") == "**4305"

    def test_mask_account_short():
        """Тест короткого номера счета (ровно 4 цифры)"""
        assert get_mask_account("1234") == "**1234"

    def test_mask_account_very_short():
        """Тест счета, где длина меньше 4 символов"""
        assert get_mask_account("99") == "**99"

    def test_mask_account_empty():
        """Тест пустой строки"""
        assert get_mask_account("") == "**"

    def test_mask_account_with_spaces():
        """Тест номера счета с пробелами"""
        assert get_mask_account("1234 5678 9012") == "**9012"

        # 3.Проверка, что функция корректно обрабатывает входные данные, где номер счета меньше ожидаемой длины.
def test_mask_account_less_than_four_symbols():
    """Номер счета состоит из 3 символов (меньше 4)"""
    assert get_mask_account("123") == "**123"


def test_mask_account_one_symbol():
    """Номер счета состоит всего из 1 символа"""
    assert get_mask_account("7") == "**7"


def test_mask_account_empty_string():
    """В функцию передана пустая строка"""
    assert get_mask_account("") == "**"


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
