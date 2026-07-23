import functools
import sys


def log(filename=None):
    """Декоратор для логирования результатов работы функции.

    Записывает статус выполнения, тип возникшей ошибки и переданные
    аргументы в файл или в стандартный вывод (консоль).

    Args:
        filename (str, optional): Путь к файлу для записи логов.
            Если не указан, логи выводятся в sys.stdout (консоль).
            По умолчанию None.

    Returns:
        function: Декоратор, принимающий целевую функцию.
    """
    def decorator(func):
        """Принимает декорируемую функцию и оборачивает её.

        Args:
            func (callable): Функция, работу которой необходимо залогировать.

        Returns:
            function: Обернутая функция (wrapper) с сохраненной сигнатурой.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Выполняет целевую функцию и записывает лог её работы.

            Args:
                *args: Позиционные аргументы для целевой функции.
                **kwargs: Именованные аргументы для целевой функции.

            Returns:
                Any: Результат выполнения оригинальной функции.

               Raises:
                Exception: Перенаправляет любое исключение, возникшее
                    внутри декорируемой функции, без изменения логики.
            """
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
