"""Создаём функцию маскировки банковской карты

"""

def get_mask_card_number(card_number: str) -> str:
    # Превращаем в строку, если пришло число
    card_str = str(card_number)

    # Формируем маску: первые 6 цифр, звезды и последние 4
    # {card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}
    mask = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"

    return mask


# Пример использования:
print(get_mask_card_number("7000792289606361"))
# Вывод: 7000 79** **** 6361

"""Создаём функцию маскировки номера банковского счёта

"""


def get_mask_account(account_number: str) -> str:
    # Преобразуем в строку на случай, если пришло число
    account_str = str(account_number)

    # Берем последние 4 цифры и добавляем две звездочки перед ними
    return f"**{account_str[-4:]}"


# Пример работы:
print(get_mask_account("73654108430135874305"))


