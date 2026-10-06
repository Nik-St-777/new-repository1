from src.masks import get_mask_card_number


def test_mask_card_number_missing_number():
    """Проверка корректности обработки строк без номера карты."""

    # 1. Полностью пустая строка
    assert get_mask_card_number("") == "  ** **** "

    # 2. Строка, содержащая только название платёжной системы
    assert get_mask_card_number("Visa") == "Visa  ** **** Visa"

    # 3. Строка из одних пробелов
    assert get_mask_card_number("   ") == "    ** ****    "
