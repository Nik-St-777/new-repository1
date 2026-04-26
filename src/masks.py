def get_mask_card_number(card_number: str) -> str:
    """
    Функция get_mask_card_number принимает на вход номер карты и возвращает ее маску
    """
    #Маскирует номер карты в формате XXXX XX** **** XXXX
    # Маскируем нужную часть: первые 6 цифр, две звезды, четыре звезды и последние 4 цифры
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked

# Пример работы:
print(get_mask_card_number("7000792289606361"))
# Вывод: 7000 79** **** 6361

def get_mask_account(account_number: str) -> str:
    """
    Функция get_mask_account принимает на вход номер счета и возвращает его маску
    """
    #Маскирует номер счета, оставляя только последние 4 цифры.
    return f"**{account_number[-4:]}"

# Пример работы:
print(get_mask_account("73654108430135874305"))
# Вывод: **4305




