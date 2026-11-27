import pytest

from src.processing import filter_by_state, sort_by_date


# 1. Тестирование фильтрации списка словарей по заданному статусу state
@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными"""
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "CANCELED", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 300},
        {"id": 4, "state": "PENDING", "amount": 400},
        {"id": 5, "amount": 500},  # Словарь без ключа state
    ]


def test_filter_by_default_state(sample_data):
    """Проверка фильтрации по умолчанию (EXECUTED)"""
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_custom_state(sample_data):
    """Проверка фильтрации по переданному статусу CANCELED"""
    result = filter_by_state(sample_data, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_empty_list():
    """Проверка работы с пустым списком"""
    assert filter_by_state([], "EXECUTED") == []


def test_filter_no_matching_state(sample_data):
    """Проверка ситуации, когда совпадений нет"""
    result = filter_by_state(sample_data, "NON_EXISTENT")
    assert result == []


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 1),
    ],
)
def test_counts(sample_data, state, expected_count):
    """Параметризованный тест для проверки количества результатов"""
    assert len(filter_by_state(sample_data, state)) == expected_count


# 2. Проверка работы функции при отсутствии словарей с указанным статусом state в списке.


def test_filter_by_state_no_matching_status():
    """Проверка возврата пустого списка, если искомый статус отсутствует"""
    sample_data = [
        {"id": 1, "state": "CANCELED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "amount": 100},  # Ключ state вообще отсутствует
    ]

    result = filter_by_state(sample_data, state="EXECUTED")

    assert result == []
    assert len(result) == 0


# 3. Параметризация тестов для различных возможных значений статуса state.


@pytest.fixture
def sample_data_1():
    """Фикстура с тестовым набором данных"""
    return [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "PENDING"},
        {"id": 5, "state": "FAILED"},
    ]


@pytest.mark.parametrize(
    "search_state, expected_count",
    [
        ("EXECUTED", 2),  # Стандартный статус (повторяется)
        ("CANCELED", 1),  # Стандартный статус (одиночный)
        ("PENDING", 1),  # Другой валидный статус
        ("FAILED", 1),  # Краевой валидный статус
        ("executed", 0),  # Проверка регистрозависимости (строчные буквы)
        ("UNKNOWN", 0),  # Несуществующий статус
        ("", 0),  # Пустая строка вместо статуса
    ],
)
def test_filter_by_state_parameterized(sample_data_1, search_state, expected_count):
    """Параметризованный тест для проверки различных значений state"""
    result = filter_by_state(sample_data_1, state=search_state)
    assert len(result) == expected_count


# Замените your_module на имя вашего файла


def test_sort_by_date_order():
    """1. Тестирование сортировки по датам в порядке убывания и возрастания"""
    data = [
        {"id": 1, "date": "2019-08-26T10:50:58"},
        {"id": 2, "date": "2023-01-15T12:00:00"},
        {"id": 3, "date": "2021-05-10T14:30:15"},
    ]

    descending = sort_by_date(data, reverse=True)
    assert descending[0]["id"] == 2  # 2023
    assert descending[1]["id"] == 3  # 2021
    assert descending[2]["id"] == 1  # 2019

    ascending = sort_by_date(data, reverse=False)
    assert ascending[0]["id"] == 1  # 2019
    assert ascending[1]["id"] == 3  # 2021
    assert ascending[2]["id"] == 2  # 2023


def test_sort_by_date_identical():
    """2. Проверка корректности сортировки при одинаковых датах"""
    data = [
        {"id": 1, "date": "2023-01-15T12:00:00", "label": "first"},
        {"id": 2, "date": "2023-01-15T12:00:00", "label": "second"},
    ]

    result = sort_by_date(data, reverse=True)
    assert result[0]["label"] == "first"
    assert result[1]["label"] == "second"


def test_sort_by_date_invalid_formats():
    """3. Тесты на работу функции с некорректными или нестандартными форматами дат"""
    mixed_data = [
        {"id": 1, "date": "15.01.2023"},
        {"id": 2, "date": "2023-01-15T12:00"},
    ]

    result = sort_by_date(mixed_data, reverse=True)
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1


def test_sort_by_date_missing_key():
    """Дополнительно: проверка падения с ошибкой, если ключа 'date' нет"""
    invalid_data = [{"id": 1, "date": "2023-01-15T12:00:00"}, {"id": 2}]

    with pytest.raises(KeyError):
        sort_by_date(invalid_data)
