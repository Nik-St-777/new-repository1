import logging

logger = logging.getLogger("utils")


def do_something(value):
    logger.debug("Вход в do_something, value=%r", value)
    try:
        result = value * 2
        logger.info("do_something: успех, результат=%r", result)
        return result
    except Exception as e:
        logger.error("do_something: ошибка, value=%r, exception=%s", value, e, exc_info=True)
        raise
