def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры."""

    card_number = card_number.replace(" ", "").replace("-", "")
    if len(card_number) < 16:
        return card_number  # или можно кинуть ошибку — зависит от требований
    return f"{card_number[:6]}****{card_number[-4:]}"


# Вызов функции
masked = get_mask_card_number("1234 5678 9012 3456")
print(masked)


def get_mask_account(account: str) -> str:
    """Пример маскировки счёта: оставляем последние 4 символа."""

    if len(account) <= 4:
        return "*" * len(account)
    return "*" * (len(account) - 4) + account[-4:]
