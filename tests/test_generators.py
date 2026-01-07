import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# Тесты для функции filter_by_currency.
@pytest.mark.parametrize("currency,expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("RUB", [4]),
    ("GBP", [])
])
def test_filter_by_currency(sample_transactions, currency, expected_ids):
    """Тестирование фильтрации транзакций по валюте."""
    # Act
    result = list(filter_by_currency(sample_transactions, currency))

    # Assert
    assert len(result) == len(expected_ids)
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == currency
    assert [t["id"] for t in result] == expected_ids


def test_empty_transactions(empty_transactions):
    """Тестирование с пустым списком транзакций."""
    # Act
    result = list(filter_by_currency(empty_transactions, "USD"))

    # Assert
    assert result == []


def test_transactions_without_currency(transactions_without_currency):
    """Тестирование транзакций без информации о валюте."""
    # Act
    result = list(filter_by_currency(transactions_without_currency, "USD"))

    # Assert
    assert result == []


# Тесты для генератора transaction_descriptions.
def test_descriptions_extraction(sample_transactions):
    """Тестирование извлечения описаний транзакций."""
    # Act
    result = list(transaction_descriptions(sample_transactions))

    # Assert
    # Так как в фикстуре нет полей description, ожидаем список из None
    expected_descriptions = [None, None, None, None, None, None]
    assert result == expected_descriptions


def test_empty_transactions_list(empty_transactions):
    """Тестирование с пустым списком транзакций."""
    # Act
    result = list(transaction_descriptions(empty_transactions))

    # Assert
    assert result == []


def test_transactions_without_descriptions():
    """Тестирование транзакций без описаний."""
    # Arrange
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED", "description": None},
        {"id": 3, "state": "EXECUTED", "description": ""}
    ]

    # Act
    result = list(transaction_descriptions(transactions))

    # Assert - исправляем ожидаемый результат
    assert result == [None, None, ""]


# Тесты для генератора card_number_generator.
@pytest.mark.parametrize("start,end,expected_first,expected_last,expected_count", [
    (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005", 5),
    (9999, 10001, "0000 0000 0000 9999", "0000 0000 0001 0001", 3),
    (9999999999999995, 9999999999999999, "9999 9999 9999 9995", "9999 9999 9999 9999", 5),
    (42, 42, "0000 0000 0000 0042", "0000 0000 0000 0042", 1)
])
def test_card_number_generation(start, end, expected_first, expected_last, expected_count):
    """Тестирование генерации номеров карт в различных диапазонах."""
    # Act
    result = list(card_number_generator(start, end))

    # Assert
    assert len(result) == expected_count
    assert result[0] == expected_first
    assert result[-1] == expected_last

    # Проверяем формат всех номеров
    for card_number in result:
        parts = card_number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 and part.isdigit() for part in parts)


def test_single_number():
    """Тестирование генерации одного номера."""
    # Act
    result = list(card_number_generator(1, 1))

    # Assert
    assert result == ["0000 0000 0000 0001"]


def test_large_range():
    """Тестирование генерации большого диапазона."""
    # Act
    generator = card_number_generator(1, 100)
    first_three = [next(generator) for _ in range(3)]

    # Assert
    assert first_three == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]
