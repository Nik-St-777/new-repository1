import pytest
from unittest.mock import patch, MagicMock
import os
from external_api import convert_currency


@patch.dict(os.environ, {"API_KEY": "test_key", "BASE_URL": "https://api.example.com"})
@patch("external_api.load_dotenv")
@patch("external_api.requests.get")
def test_convert_currency_success(mock_get, mock_load_dotenv):
    """Тест успешной конвертации."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": 90.5}
    mock_get.return_value = mock_response

    amount = 100.0
    from_currency = "USD"
    to_currency = "RUB"

    result = convert_currency(amount, from_currency, to_currency)

    assert result == 90.5
    mock_get.assert_called_once()

    args, kwargs = mock_get.call_args
    assert kwargs["headers"]["apikey"] == "test_key"
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["params"]["amount"] == 100.0


@patch.dict(os.environ, {"API_KEY": "test_key", "BASE_URL": "https://api.example.com"})
@patch("external_api.load_dotenv")
@patch("external_api.requests.get")
def test_convert_currency_default_to_currency(mock_get, mock_load_dotenv):
    """Тест, когда to_currency не указан (по умолчанию RUB)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": 75.2}
    mock_get.return_value = mock_response

    amount = 50.0
    from_currency = "EUR"

    result = convert_currency(amount, from_currency)

    assert result == 75.2

    args, kwargs = mock_get.call_args
    assert kwargs["params"]["to"] == "RUB"


@patch.dict(os.environ, {"API_KEY": "test_key", "BASE_URL": "https://api.example.com"})
@patch("external_api.load_dotenv")
@patch("external_api.requests.get")
def test_convert_currency_missing_result_field(mock_get, mock_load_dotenv):
    """Тест случая, когда в ответе API нет поля 'result'."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"other_field": 123}
    mock_get.return_value = mock_response

    with pytest.raises(KeyError) as exc_info:
        convert_currency(100.0, "USD", "RUB")

    assert "Ответ API не содержит поле 'result'" in str(exc_info.value)


@patch.dict(os.environ, {"API_KEY": "test_key", "BASE_URL": "https://api.example.com"})
@patch("external_api.load_dotenv")
@patch("external_api.requests.get")
def test_convert_currency_http_error(mock_get, mock_load_dotenv):
    """Тест обработки ошибки HTTP-запроса."""
    from requests.exceptions import HTTPError

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("Bad request")
    mock_get.return_value = mock_response

    with pytest.raises(HTTPError):
        convert_currency(100.0, "USD", "RUB")


@patch.dict(os.environ, {"API_KEY": "test_key", "BASE_URL": "https://api.example.com"})
@patch("external_api.load_dotenv")
@patch("external_api.requests.get", side_effect=Exception("Network error"))
def test_convert_currency_network_error(mock_get, mock_load_dotenv):
    """Тест обработки сетевой ошибки."""
    with pytest.raises(Exception) as exc_info:
        convert_currency(100.0, "USD", "RUB")

    assert str(exc_info.value) == "Network error"
