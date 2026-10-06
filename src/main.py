from logging_config import setup_logging
import utils
import masks

if __name__ == "__main__":
    setup_logging()  # здесь создаются file_handler и file_formatter

    utils.do_something(10)
    masks.apply_mask("data123")
