def mask_card_number(number: str) -> str:
    """
    Создаём функцию mask_account_card, которая умеет обрабатывать информацию как о картах, так и о счетах.
    """
    #Маскирует номер карты: 1234 56** **** 3456


    return f"{number[:4]} {number[4:6]}** **** {number[-4:]}"


def mask_account_number(number: str) -> str:
    #Маскирует номер счета: **4305
    #return f"**{number[-4:]}"


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
    """
    Cоздаём функцию get_date, которая принимает на вход строку с датой в формате"2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате"ДД.ММ.ГГГГ("11.03.2024").
    """

    #Преобразует строку с датой в формат ДД.ММ.ГГГГ
    # Извлекаем год, месяц и день по индексам
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]

    return f"{day}.{month}.{year}"


# Пример вызова:
# print(get_date("2024-03-11T02:26:18.671407"))
# -> 11.03.2024
