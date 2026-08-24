# тест на правильность работы функции, которая принимает на вход путь до Json-файла и возвращает список словарей с данными о финансовых транзакциях

import json
import pytest
from unittest.mock import mock_open, patch



def test_load_transactions_success():
    """Тест успешной загрузки корректного списка транзакций."""
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    json_data = json.dumps(test_data)

    # Имитируем, что файл существует, и подменяем его содержимое
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=json_data)
    ):
        result = load_transactions("fake_path.json")
        assert result == test_data


def test_load_transactions_file_not_found():
    """Тест ситуации, когда файл не существует."""
    with patch("os.path.exists", return_value=False):
        result = load_transactions("missing_file.json")
        assert result == []


def test_load_transactions_invalid_json():
    """Тест ситуации, когда файл поврежден или содержит некорректный JSON."""
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data="invalid json data")
    ):
        result = load_transactions("corrupted.json")
        assert result == []


def test_load_transactions_not_a_list():
    """Тест ситуации, когда JSON корректен, но внутри словарь вместо списка."""
    dict_data = json.dumps({"status": "error", "message": "not a list"})

    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=dict_data)
    ):
        result = load_transactions("wrong_format.json")
        assert result == []
