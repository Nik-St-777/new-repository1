import json
from unittest.mock import patch, mock_open
from src.utils import load_transactions


@patch("os.path.exists", return_value=True)  # 1. Говорим: "Файл существует!"
@patch("builtins.open", new_callable=mock_open,
       read_data='[{"id": 1, "amount": 100}]')  # 2. Говорим: "Вот что внутри файла"
def test_load_transactions_success_mock(mock_open_obj, mock_exists):
    """Тест: файл существует, JSON валидный, внутри список -> возвращаем данные"""
    fake_path = "any_path.json"

    result = load_transactions(fake_path)

    # Проверяем результат
    assert result == [{"id": 1, "amount": 100}]

    # (Опционально) Проверяем, что функции были вызваны
    mock_exists.assert_called_once_with(fake_path)
    mock_open_obj.assert_called_once()


@patch("os.path.exists", return_value=False)  # 1. Говорим: "Файла НЕТ!"
def test_load_transactions_file_not_found_mock(mock_exists):
    """Тест: файла не существует -> сразу возвращаем []"""
    fake_path = "non_existent.json"

    result = load_transactions(fake_path)

    assert result == []
    # Функция даже не должна пытаться открыть файл, если его нет
    mock_exists.assert_called_once_with(fake_path)


@patch("os.path.exists", return_value=True)
@patch("builtins.open", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
def test_load_transactions_invalid_json_mock(mock_open_obj, mock_exists):
    """Тест: файл есть, но внутри мусор (ошибка JSON) -> возвращаем []"""
    fake_path = "bad_format.json"

    result = load_transactions(fake_path)

    assert result == []
    mock_exists.assert_called_once_with(fake_path)
    mock_open_obj.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='{"id": 5}')  # Внутри ОДИН словарь, а не список
def test_load_transactions_not_a_list_mock(mock_open_obj, mock_exists):
    """Тест: файл валидный JSON, но внутри НЕ список (один объект) -> возвращаем []"""
    fake_path = "single_object.json"

    result = load_transactions(fake_path)

    assert result == []
    mock_exists.assert_called_once_with(fake_path)
    mock_open_obj.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("builtins.open", new_callable=mock_open, read_data='[]')  # Пустой список
def test_load_transactions_empty_list_mock(mock_open_obj, mock_exists):
    """Тест: файл содержит пустой список [] -> возвращаем []"""
    fake_path = "empty_list.json"

    result = load_transactions(fake_path)

    assert result == []
    mock_exists.assert_called_once_with(fake_path)


