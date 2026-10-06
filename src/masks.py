import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты и возвращает её маску."""
    masked = (
        f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    )
    return masked


def get_mask_account(account_number: str) -> str:
    """Принимает номер счёта и возвращает его маску."""
    return f"**{account_number[-4:]}"

