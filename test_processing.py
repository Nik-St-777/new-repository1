import pytest
from src.processing import filter_by_state

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

# 2.Проверка работы функции при отсутствии словарей с указанным статусом state в списке.

def test_filter_by_state_no_matching_status():
    """Проверка возврата пустого списка, если искомый статус отсутствует"""
    # Исходные данные содержат только статусы CANCELED и PENDING
    sample_data = [
        {"id": 1, "state": "CANCELED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "amount": 100}  # Ключ state вообще отсутствует
    ]

    # Ищем статус, которого точно нет в списке
    result = filter_by_state(sample_data, state="EXECUTED")

    # Проверяем, что вернулся пустой список
    assert result == []
    assert len(result) == 0

# 3. Параметризация тестов для различных возможных значений статуса state .

@pytest.fixture
def sample_data():
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
        ("EXECUTED", 2),       # Стандартный статус (повторяется)
        ("CANCELED", 1),       # Стандартный статус (одиночный)
        ("PENDING", 1),        # Другой валидный статус
        ("FAILED", 1),         # Краевой валидный статус
        ("executed", 0),       # Проверка регистрозависимости (строчные буквы)
        ("UNKNOWN", 0),        # Несуществующий статус
        ("", 0),               # Пустая строка вместо статуса
    ],
)
def test_filter_by_state_parameterized(sample_data, search_state, expected_count):
    """Параметризованный тест для проверки различных значений state"""
    result = filter_by_state(sample_data, state=search_state)
    assert len(result) == expected_count


import pytest
from src.processing import sort_by_date  # Замените your_module на имя вашего файла


def test_sort_by_date_order():
    """1. Тестирование сортировки по датам в порядке убывания и возрастания"""
    data = [
        {"id": 1, "date": "2019-08-26T10:50:58"},
        {"id": 2, "date": "2023-01-15T12:00:00"},
        {"id": 3, "date": "2021-05-10T14:30:15"},
    ]

    # Проверка убывания (reverse=True) — от свежих к старым
    descending = sort_by_date(data, reverse=True)
    assert descending[0]["id"] == 2  # 2023
    assert descending[1]["id"] == 3  # 2021
    assert descending[2]["id"] == 1  # 2019

    # Проверка возрастания (reverse=False) — от старых к свежим
    ascending = sort_by_date(data, reverse=False)
    assert ascending[0]["id"] == 1  # 2019
    assert ascending[1]["id"] == 3  # 2021
    assert ascending[2]["id"] == 2  # 2023


def test_sort_by_date_identical():
    """2. Проверка корректности сортировки при одинаковых датах"""
    # Python использует стабильную сортировку (Timsort).
    # Элементы с одинаковыми ключами должны сохранить свой исходный порядок.
    data = [
        {"id": 1, "date": "2023-01-15T12:00:00", "label": "first"},
        {"id": 2, "date": "2023-01-15T12:00:00", "label": "second"},
    ]

    result = sort_by_date(data, reverse=True)
    assert result[0]["label"] == "first"
    assert result[1]["label"] == "second"


def test_sort_by_date_invalid_formats():
    """3. Тесты на работу функции с некорректными или нестандартными форматами дат"""
    # Поскольку функция сравнивает даты как обычные строки (лексикографически),
    # смешивание разных форматов приведет к некорректному (по смыслу дат) результату.

    mixed_data = [
        {"id": 1, "date": "15.01.2023"},  # Нестандартный формат для ISO
        {"id": 2, "date": "2023-01-15T12:00"},  # Стандартный ISO
    ]

    # Строка "2023..." начинается с '2', а "15..." начинается с '1'.
    # При сортировке по убыванию '2' идет раньше '1'.
    result = sort_by_date(mixed_data, reverse=True)
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1


def test_sort_by_date_missing_key():
    """Дополнительно: проверка падения с ошибкой, если ключа 'date' нет"""
    invalid_data = [
        {"id": 1, "date": "2023-01-15T12:00:00"},
        {"id": 2}  # Ключ 'date' отсутствует
    ]

    # Функция должна вызвать KeyError, так как обращается к ключу напрямую: x['date']
    with pytest.raises(KeyError):
        sort_by_date(invalid_data)
