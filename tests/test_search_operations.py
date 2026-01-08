import pytest
from src.search_operations import process_bank_search


@pytest.mark.parametrize("search_term,expected_ids", [
    ("payment", [1, 5, 6]),
    ("Payment", [1, 5, 6]),
    ("PAYMENT", [1, 5, 6]),
    ("amazon", [3]),
    ("uber", [2]),
    ("coffee", [4]),
    ("rent", [5]),
    ("nonexistent", []),
])
def test_search_terms(sample_data, search_term, expected_ids):
    """Параметризованный тест различных поисковых запросов."""
    result = process_bank_search(sample_data, search_term)
    result_ids = [op["id"] for op in result]
    assert result_ids == expected_ids


@pytest.mark.parametrize("search_term,expected_ids", [
    (r"payment|purchase", [1, 3, 5, 6]),
    (r"\bpay\b", []),
    (r"\bpayment\b", [1, 5, 6]),
    (r"^Monthly", [5]),
])
def test_regex_search(sample_data, search_term, expected_ids):
    """Тесты с использованием регулярных выражений."""
    result = process_bank_search(sample_data, search_term)
    result_ids = [op["id"] for op in result]
    assert set(result_ids) == set(expected_ids)


def test_empty_search(sample_data):
    """Тест пустого поискового запроса."""
    result = process_bank_search(sample_data, "")
    assert result == []


def test_empty_data():
    """Тест с пустыми данными."""
    result = process_bank_search([], "payment")
    assert result == []


def test_invalid_regex_fallback(sample_data):
    """Тест перехода на обычный поиск при невалидном regex."""
    result = process_bank_search(sample_data, "pay(ment")
    result_ids = [op["id"] for op in result]
    assert set(result_ids) == {1, 5, 6}


def test_operation_without_description():
    """Тест операции без поля description."""
    data = [
        {"id": 1, "description": "Normal"},
        {"id": 2},
        {"id": 3, "description": ""},
    ]

    result = process_bank_search(data, "normal")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_result_structure_integrity(sample_data):
    """Тест на сохранение структуры данных."""
    result = process_bank_search(sample_data, "amazon")

    assert len(result) == 1
    operation = result[0]

    assert operation["id"] == 3
    assert operation["amount"] == 200.00
    assert operation["description"] == "Amazon purchase - electronics"
    assert operation["date"] == "2024-01-17"
