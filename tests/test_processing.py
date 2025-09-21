import pytest
from src.processing import filter_by_state, sort_by_date


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [1, 3, 5]),
    ("PENDING", [2]),
    ("CANCELED", [4]),
    ("FAILED", [6]),
    ("NONEXISTENT", []),
    ("", []),
])
def test_filter_by_state_various_states(sample_transactions, state, expected_ids):
    """Тестирование фильтрации по различным состояниям"""
    result = filter_by_state(sample_transactions, state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default_parameter(sample_transactions):
    """Тестирование фильтрации со значением по умолчанию"""
    result = filter_by_state(sample_transactions)
    assert all(item["state"] == "EXECUTED" for item in result)
    assert [item["id"] for item in result] == [1, 3, 5]


def test_filter_by_state_missing_key(transactions_with_missing_keys):
    """Тестирование фильтрации при отсутствии ключа state"""
    result = filter_by_state(transactions_with_missing_keys, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_empty_data(empty_data):
    """Тестирование фильтрации пустого списка"""
    result = filter_by_state(empty_data, "EXECUTED")
    assert result == []


def test_filter_by_state_special_values(transactions_with_special_values):
    """Тестирование фильтрации со специальными значениями"""
    result = filter_by_state(transactions_with_special_values, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 3


# Параметризованные тесты для sort_by_date
@pytest.mark.parametrize("reverse, expected_order", [
    (True, [3, 1, 2, 4, 5, 6]),  # По убыванию
    (False, [6, 5, 4, 2, 1, 3]),  # По возрастанию
])
def test_sort_by_date_directions(sample_transactions, reverse, expected_order):
    """Тестирование сортировки в разных направлениях"""
    result = sort_by_date(sample_transactions, reverse=reverse)
    assert [item["id"] for item in result] == expected_order


def test_sort_by_date_default_parameter(sample_transactions):
    """Тестирование сортировки со значением по умолчанию"""
    result = sort_by_date(sample_transactions)
    # Должно быть по убыванию
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_identical_dates(transactions_with_duplicate_dates):
    """Тестирование сортировки с одинаковыми датами"""
    result = sort_by_date(transactions_with_duplicate_dates)
    # Стабильная сортировка - порядок должен сохраниться
    assert [item["id"] for item in result] == [1, 2, 3]


def test_sort_by_date_empty_data(empty_data):
    """Тестирование сортировки пустого списка"""
    result = sort_by_date(empty_data)
    assert result == []


def test_sort_by_date_missing_key(transactions_with_missing_keys):
    """Тестирование сортировки при отсутствии ключа date"""
    with pytest.raises(KeyError):
        sort_by_date(transactions_with_missing_keys)


# Интеграционные тесты
def test_filter_and_sort_integration(sample_transactions):
    """Интеграционный тест: фильтрация + сортировка"""
    filtered = filter_by_state(sample_transactions, "EXECUTED")
    sorted_result = sort_by_date(filtered)

    assert len(sorted_result) == 3
    assert all(item["state"] == "EXECUTED" for item in sorted_result)
    assert [item["id"] for item in sorted_result] == [3, 1, 5]  # По убыванию даты


def test_sort_and_filter_integration(sample_transactions):
    """Интеграционный тест: сортировка + фильтрация"""
    sorted_data = sort_by_date(sample_transactions, reverse=False)
    filtered = filter_by_state(sorted_data, "EXECUTED")

    assert len(filtered) == 3
    assert all(item["state"] == "EXECUTED" for item in filtered)
    assert [item["id"] for item in filtered] == [5, 1, 3]  # По возрастанию даты
