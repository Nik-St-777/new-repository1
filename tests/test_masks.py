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



