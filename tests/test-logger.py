import pytest
from logger import log  # Импортируем ваш декоратор

# --- ТЕСТЫ ДЛЯ ВЫВОДА В КОНСОЛЬ (используем capsys) ---


def test_console_logging_success(capsys):
    """Проверяет успешное выполнение функции при выводе в консоль."""

    @log()
    def add(a, b):
        return a + b

    # Проверяем, что функция возвращает правильный результат
    assert add(2, 3) == 5

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в лог ушла правильная строка (учитываем символ переноса строки)
    assert captured.out == "add ok\n"


def test_console_logging_error(capsys):
    """Проверяет логирование ошибки при выводе в консоль."""

    @log()
    def divide(a, b):
        return a / b

    # Убеждаемся, что ошибка пробрасывается дальше наружу
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    # Перехватываем вывод
    captured = capsys.readouterr()

    # Проверяем структуру лога ошибки
    expected_log = "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"
    assert captured.out == expected_log


# --- ТЕСТЫ ДЛЯ ЗАПИСИ В ФАЙЛ (используем tmp_path) ---


def test_file_logging_success(tmp_path):
    """Проверяет успешное выполнение функции при записи в файл."""
    # Создаем путь к временному файлу в изолированной папке
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def greet(name):
        return f"Hello, {name}"

    assert greet("Alice") == "Hello, Alice"

    # Читаем содержимое файла и проверяем лог
    log_content = log_file.read_text(encoding="utf-8")
    assert log_content == "greet ok\n"


def test_file_logging_error(tmp_path):
    """Проверяет логирование ошибки при записи в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def get_element(lst, index):
        return lst[index]

    # Проверяем проброс ошибки (IndexError)
    with pytest.raises(IndexError):
        get_element([1, 2, 3], 5)

    # Проверяем содержимое файла
    log_content = log_file.read_text(encoding="utf-8")
    expected_log = "get_element error: IndexError. Inputs: ([1, 2, 3], 5), {}\n"
    assert log_content == expected_log


def test_file_logging_kwargs_error(tmp_path):
    """Проверяет, что именованные аргументы (kwargs) корректно логируются при ошибке."""
    log_file = tmp_path / "kwargs_error.log"

    @log(filename=str(log_file))
    def calculate(x, *, operation):
        if operation == "unknown":
            raise ValueError("Invalid operation")

    with pytest.raises(ValueError):
        calculate(5, operation="unknown")

    log_content = log_file.read_text(encoding="utf-8")
    # Проверяем наличие именованного аргумента в секции {}
    expected_log = "calculate error: ValueError. Inputs: (5,), {'operation': 'unknown'}\n"
    assert log_content == expected_log
