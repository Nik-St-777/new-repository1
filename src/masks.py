import logging

logger = logging.getLogger("masks")


def apply_mask(data):
    logger.debug("Вход в apply_mask, data=%r", data)
    try:
        if not data:
            raise ValueError("Пустые данные")
        result = f"masked_{data}"
        logger.info("apply_mask: успех, результат=%r", result)
        return result
    except Exception as e:
        logger.error("apply_mask: ошибка, data=%r, exception=%s", data, e, exc_info=True)
        raise
