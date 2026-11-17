import json
import pytest
from src.utils import load_transactions
from src.external_api import convert_to_rub
from unittest.mock import mock_open, patch


def test_load_transactions_valid_list():
    """
    Проверяет, что load_transactions корректно загружает и возвращает список транзакций из валидного JSON-файла.
    """
    data = [
        {"amount": 100.0, "currency": "USD"},
        {"amount": 5000.0, "currency": "RUB"},
    ]
    m = mock_open(read_data=json.dumps(data))
    with patch("builtins.open", m):
        result = load_transactions("dummy.json")
    assert result == data


def test_load_transactions_not_a_list():
    """
    Проверяет поведение load_transactions, если файл существует и содержит
    валидный JSON, но данные не являются списком (например, словарь).
    """
    m = mock_open(read_data=json.dumps({"total": 12345}))
    with patch("builtins.open", m):
        result = load_transactions("dummy.json")
    assert result == []


def test_load_transactions_file_not_found():
    """
    Проверяет обработку ситуации, когда запрашиваемый файл не найден.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("missing.json")
    assert result == []


def test_load_transactions_invalid_json():
    """
    Проверяет обработку некорректного (невалидного) JSON‑содержимого файла.
    """
    # Важно: mock_open возвращает объект, который можно читать, но json.load
    # всё равно попытается распарсить содержимое. Чтобы эмулировать JSONDecodeError,
    # нужно замокать именно json.load, а не только open.
    m = mock_open(read_data="{invalid json}")
    with patch("builtins.open", m), patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
        result = load_transactions("bad.json")
    assert result == []
