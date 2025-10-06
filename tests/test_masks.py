import pytest
from src.masks import get_mask_card_number, get_mask_account


# Параметризованные тесты для get_mask_card_number
@pytest.mark.parametrize("card_number, expected", [
    ("4111111111111111", "4111 11** **** 1111"),
    ("5500000000000004", "5500 00** **** 0004"),
    ])
def test_get_mask_card_number_various_formats(card_number, expected):
    """Тестирование маскирования """
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("invalid_input", [
    "",
    "123",
    "abcd1234efgh5678",
    "1234!@#$5678%^&*",
])
def test_get_mask_card_number_invalid_input(invalid_input):
    """Тестирование обработки невалидных входных данных для карт"""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_input)


# Параметризованные тесты для get_mask_account
@pytest.mark.parametrize("account_number, expected", [
    ("40817810099910004312", "**4312"),
    ("40702810500000012345", "**2345"),
    ("1234567890123456", "**3456"),
    ("1234567890", "**7890"),
    ("1234", "**1234"),

])
def test_get_mask_account_various_formats(account_number, expected):
    """Тестирование маскирования различных форматов счетов"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("invalid_input", [
    "",
    "     ",
    "123",
    "abcd",
    "123!@#",
])
def test_get_mask_account_invalid_input(invalid_input):
    """Тестирование обработки невалидных входных данных для счетов"""
    with pytest.raises(ValueError):
        get_mask_account(invalid_input)


def test_get_mask_account_minimum_length():
    """Тестирование минимальной длины счета"""
    assert get_mask_account("1234") == "**1234"


def test_get_mask_account_too_short():
    """Тестирование слишком короткого номера счета"""
    with pytest.raises(ValueError):
        get_mask_account("123")
