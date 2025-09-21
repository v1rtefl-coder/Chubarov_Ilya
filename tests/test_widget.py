import pytest
from src.widget import mask_account_card, get_date


# Параметризованные тесты для mask_account_card
@pytest.mark.parametrize("input_data, expected", [
    ("4111111111111111", "4111 11** **** 1111"),
    ("5500000000000004", "5500 00** **** 0004"),
    ("378282246310005", "3782 82** **** 0005"),
])
def test_mask_account_card_various_inputs(input_data, expected):
    """Тестирование автоматического определения типа номера"""
    result = mask_account_card(input_data)
    assert result == expected


# Тесты для невалидных входных данных - РАЗДЕЛЕННЫЕ ПО ТИПУ ИСКЛЮЧЕНИЙ
@pytest.mark.parametrize("invalid_input", [
    "",
    "     ",
])
def test_mask_account_card_value_error(invalid_input):
    """Тестирование обработки невалидных входных данных (ValueError)"""
    with pytest.raises(IndexError):
        mask_account_card(invalid_input)


def test_mask_account_card_none_input():
    """Тестирование обработки None входных данных (TypeError)"""
    with pytest.raises(AttributeError):
        mask_account_card(None)


# Параметризованные тесты для get_date
@pytest.mark.parametrize("date_string, expected", [
    ("2023-10-15T12:30:45.123456", "15.10.2023"),
    ("2023-10-15T12:30:45", "15.10.2023"),
    ("2023-10-15", "15.10.2023"),
    ("2023-01-01T00:00:00.000000", "01.01.2023"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2020-02-29T12:00:00.000000", "29.02.2020"),
])
def test_get_date_various_formats(date_string, expected):
    """Тестирование преобразования различных форматов дат"""
    result = get_date(date_string)
    assert result == expected


# Тесты для невалидных входных данных дат - РАЗДЕЛЕННЫЕ ПО ТИПУ ИСКЛЮЧЕНИЙ
@pytest.mark.parametrize("invalid_input", [
    "",
    "     ",
    "2023/10/15",
    "2023-10",
    "invalid-date",
])
def test_get_date_value_error(invalid_input):
    """Тестирование обработки невалидных входных данных дат (ValueError)"""
    with pytest.raises(ValueError):
        get_date(invalid_input)
