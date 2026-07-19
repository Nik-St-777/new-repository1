import functools
import sys
import pytest


# --- САМ ДЕКОРАТОР (перенесен внутрь, чтобы избежать ошибок импорта) ---
def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if filename:
                output = open(filename, "a", encoding="utf-8")
            else:
                output = sys.stdout
            try:
                result = func(*args, **kwargs)
                print(f"{func.__name__} ok", file=output)
                return result
            except Exception as e:
                error_type = type(e).__name__
                print(
                    f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}",
                    file=output,
                )
                raise
            finally:
                if filename:
                    output.close()

        return wrapper

    return decorator


# --- ТЕСТОВЫЕ ФУНКЦИИ ---
@log()
def success_calc(a, b):
    return a + b


@log()
def fail_calc(a, b):
    return a / b


# --- ТЕСТЫ ДЛЯ ВЫВОДА В КОНСОЛЬ (sys.stdout) ---

def test_log_to_console_success(capsys):
    """Проверяет успешный лог в консоль."""
    result = success_calc(2, 3)

    assert result == 5
    captured = capsys.readouterr()
    assert captured.out == "success_calc ok\n"


def test_log_to_console_error(capsys):
    """Проверяет лог ошибки в консоль и проброс исключения."""
    with pytest.raises(ZeroDivisionError):
        fail_calc(1, 0)

    captured = capsys.readouterr()
    expected_log = "fail_calc error: ZeroDivisionError. Inputs: (1, 0), {}\n"
    assert captured.out == expected_log


# --- ТЕСТЫ ДЛЯ ЗАПИСИ В ФАЙЛ ---

def test_log_to_file_success(tmp_path):
    """Проверяет успешный лог в файл."""
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def custom_success(x):
        return x * 2

    res = custom_success(5)
    assert res == 10
    assert log_file.read_text(encoding="utf-8") == "custom_success ok\n"


def test_log_to_file_error(tmp_path):
    """Проверяет лог ошибки в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def custom_fail():
        raise ValueError("bad value")

    with pytest.raises(ValueError):
        custom_fail()

    expected_log = "custom_fail error: ValueError. Inputs: (), {}\n"
    assert log_file.read_text(encoding="utf-8") == expected_log


def test_log_to_file_append(tmp_path):
    """Проверяет, что логи дописываются в файл (режим 'a'), а не перезаписывают его."""
    log_file = tmp_path / "append.log"

    @log(filename=str(log_file))
    def dummy():
        pass

    dummy()
    dummy()

    content = log_file.read_text(encoding="utf-8")
    assert content == "dummy ok\ndummy ok\n"
