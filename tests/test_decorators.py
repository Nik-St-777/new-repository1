import functools
import io
import sys
import unittest
from unittest.mock import call, mock_open, patch
from src.decorators import log


class TestLogDecorator(unittest.TestCase):

    def test_console_success(self):
        """Проверка успешного вызова с выводом в консоль."""

        @log()
        def sample_func(x, y):
            return x + y

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = sample_func(2, 3)
            self.assertEqual(result, 5)
            self.assertEqual(mock_stdout.getvalue(), "sample_func ok\n")

    def test_console_error(self):
        """Проверка логирования ошибки при выводе в консоль."""

        @log()
        def division_func(x, y):
            return x / y

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            with self.assertRaises(ZeroDivisionError):
                division_func(1, 0)

            expected_output = (
                "division_func error: ZeroDivisionError. Inputs: (1, 0), {}\n"
            )
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("builtins.open", new_callable=mock_open)
    def test_file_success(self, mock_file):
        """Проверка записи успешного лога в файл."""

        @log(filename="app.log")
        def sample_func(x, y=10):
            return x * y

        result = sample_func(5, y=2)
        self.assertEqual(result, 10)

        mock_file.assert_called_once_with("app.log", "a", encoding="utf-8")

        mock_file().write.assert_has_calls([
            call("sample_func ok"),
            call("\n")
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_file_error(self, mock_file):
        """Проверка записи лога ошибки в файл."""

        @log(filename="errors.log")
        def fail_func(*args, **kwargs):
            raise ValueError("Invalid data")

        with self.assertRaises(ValueError):
            fail_func(1, "test", key="val")

        mock_file.assert_called_once_with("errors.log", "a", encoding="utf-8")

        expected_text = "fail_func error: ValueError. Inputs: (1, 'test'), {'key': 'val'}"
        mock_file().write.assert_has_calls([
            call(expected_text),
            call("\n")
        ])
