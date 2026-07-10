import functools
import sys


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Определяем, куда писать: в файл или в консоль (sys.stdout)
            if filename:
                output = open(filename, "a", encoding="utf-8")
            else:
                output = sys.stdout

            try:
                # Попытка выполнить функцию
                result = func(*args, **kwargs)
                # Успешный лог
                print(f"{func.__name__} ok", file=output)
                return result
            except Exception as e:
                # Лог в случае ошибки
                error_type = type(e).__name__
                print(
                    f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}",
                    file=output,
                )
                raise  # Пробрасываем ошибку дальше, чтобы не ломать логику программы
            finally:
                # Закрываем файл, если он был открыт
                if filename:
                    output.close()

        return wrapper

    return decorator
