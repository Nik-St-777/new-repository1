def get_mask_account(account: str) -> str:
    if len(account) <= 8:
        return "*" * len(account)
    return account[:4] + "*" * (len(account) - 8) + account[-4:]


def get_mask_card_number(card_number: str) -> str:
    if len(card_number) <= 8:
        return "*" * len(card_number)
    return card_number[:6] + "*" * 6 + card_number[-4:]


def mask_account_card(account: str, card_number: str) -> dict:
    """Возвращает замаскированные account и card_number."""

    def get_mask_account(acc: str) -> str:
        if len(acc) <= 8:
            return "*" * len(acc)
        return acc[:4] + "*" * (len(acc) - 8) + acc[-4:]

    def get_mask_card_number(card: str) -> str:
        if len(card) <= 8:
            return "*" * len(card)
        return card[:6] + "*" * 6 + card[-4:]

    return {
        "account": get_mask_account(account),
        "card_number": get_mask_card_number(card_number),
    }


from datetime import date


def get_date() -> str:
    """Возвращает текущую дату в формате YYYY-MM-DD."""
    return date.today().isoformat()
