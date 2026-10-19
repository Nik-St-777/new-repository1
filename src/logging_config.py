import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)


def setup_logging():
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Логгер для utils
    utils_logger = logging.getLogger("utils")
    utils_logger.setLevel(logging.DEBUG)
    if not utils_logger.handlers:  # защита от дублирования при повторном вызове
        utils_handler = RotatingFileHandler(
            "logs/utils.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        utils_handler.setFormatter(formatter)
        utils_logger.addHandler(utils_handler)

    # Логгер для masks
    masks_logger = logging.getLogger("masks")
    masks_logger.setLevel(logging.DEBUG)
    if not masks_logger.handlers:
        masks_handler = RotatingFileHandler(
            "logs/masks.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        masks_handler.setFormatter(formatter)
        masks_logger.addHandler(masks_handler)
