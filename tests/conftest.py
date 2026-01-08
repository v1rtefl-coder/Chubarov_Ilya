import pytest
from typing import List, Dict, Any


# Фикстуры для модуля masks
@pytest.fixture
def sample_card_numbers():
    return {
        "visa_16": "4111111111111111",
        "mastercard_16": "5500000000000004",
        "amex_15": "378282246310005",
        "short_12": "123456789012",
        "long_19": "1234567890123456789",
        "with_spaces": "1234 5678 9012 3456",
        "with_dashes": "1234-5678-9012-3456"
    }


@pytest.fixture
def sample_account_numbers():
    return {
        "sber_20": "40817810099910004312",
        "tinkoff_20": "40702810500000012345",
        "short_16": "1234567890123456",
        "min_4": "1234",
        "with_spaces": "4081 7810 0999 1000 4312",
        "with_dashes": "4081-7810-0999-1000-4312"
    }


@pytest.fixture
def invalid_data():
    return {
        "empty_string": "",
        "whitespace": "     ",
        "letters": "abcd1234efgh5678",
        "special_chars": "1234!@#$5678%^&*",
        "too_short": "123",
        "none_value": None
    }


# Фикстуры для модуля widget
@pytest.fixture
def sample_dates():
    return {
        "standard": "2023-10-15T12:30:45.123456",
        "without_time": "2023-10-15",
        "with_millis": "2023-10-15T12:30:45.123",
        "edge_january": "2023-01-01T00:00:00.000000",
        "edge_december": "2023-12-31T23:59:59.999999",
        "leap_year": "2020-02-29T12:00:00.000000"
    }


@pytest.fixture
def invalid_dates():
    return {
        "empty_string": "",
        "whitespace": "     ",
        "wrong_format": "2023/10/15",
        "partial_date": "2023-10",
        "invalid_date": "2023-13-45T12:30:45",
        "none_value": None
    }


# Фикстуры для модуля processing
@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-15T12:30:45.123456", "amount": "100.00"},
        {"id": 2, "state": "PENDING", "date": "2023-10-14T10:15:30.654321", "amount": "200.00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-16T08:45:12.987654", "amount": "150.00"},
        {"id": 4, "state": "CANCELED", "date": "2023-10-13T16:20:18.456789", "amount": "300.00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-10-12T09:30:25.321654", "amount": "250.00"},
        {"id": 6, "state": "FAILED", "date": "2023-10-11T14:22:33.789123", "amount": "400.00"}
    ]


@pytest.fixture
def transactions_with_missing_keys():
    return [
        {"id": 1, "date": "2023-10-15T12:30:45.123456", "amount": "100.00"},
        {"id": 2, "state": "EXECUTED", "amount": "200.00"},
        {"id": 3, "state": "PENDING", "date": "2023-10-16T08:45:12.987654", "amount": "150.00"}
    ]


@pytest.fixture
def transactions_with_duplicate_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-15T12:30:45.123456", "amount": "100.00"},
        {"id": 2, "state": "PENDING", "date": "2023-10-15T12:30:45.123456", "amount": "200.00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-15T12:30:45.123456", "amount": "150.00"}
    ]


@pytest.fixture
def empty_data():
    return []


@pytest.fixture
def transactions_with_special_values():
    return [
        {"id": 1, "state": "", "date": "2023-10-15T12:30:45.123456", "amount": "100.00"},
        {"id": 2, "state": None, "date": "2023-10-14T10:15:30.654321", "amount": "200.00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-16T08:45:12.987654", "amount": "150.00"},
        {"id": 4, "state": 123, "date": "2023-10-13T16:20:18.456789", "amount": "300.00"}
    ]



@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "amount": 100.50, "description": "Payment for groceries at Walmart", "date": "2024-01-15"},
        {"id": 2, "amount": 45.00, "description": "Uber ride to airport", "date": "2024-01-16"},
        {"id": 3, "amount": 200.00, "description": "Amazon purchase - electronics", "date": "2024-01-17"},
        {"id": 4, "amount": 75.30, "description": "Starbucks coffee and snacks", "date": "2024-01-18"},
        {"id": 5, "amount": 1200.00, "description": "Monthly rent payment", "date": "2024-01-19"},
        {"id": 6, "amount": 50.00, "description": "Netflix subscription payment", "date": "2024-01-20"},

# Фикстуры для модуля generators
@pytest.fixture
def sample_transactions_list():
    """Фикстура с транзакциями, включая описания."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "amount": "100.00",
            "date": "2023-10-15T12:30:45.123456",
            "description": "Перевод организации"  # ← Добавлено
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "amount": "200.00",
            "date": "2023-10-14T10:20:30.456789",
            "description": "Перевод с карты на карту"  # ← Добавлено
        },
        {
            "id": 3,
            "state": "PENDING",
            "amount": "300.00",
            "date": "2023-10-13T08:15:20.789123",
            "description": "Оплата услуг"  # ← Добавлено
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "amount": "400.00",
            "date": "2023-10-12T16:45:10.123456",
            "description": "Перевод со счета на счет"  # ← Добавлено
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "amount": "500.00",
            "date": "2023-10-11T14:22:33.789123",
            "description": "Пополнение счета"  # ← Добавлено
        },
        {
            "id": 6,
            "state": "FAILED",
            "amount": "600.00",
            "date": "2023-10-10T11:33:44.567890",
            "description": "Снятие наличных"  # ← Добавлено
        }
 ]


@pytest.fixture

def bank_transactions():
    """Фикстура с тестовыми транзакциями для функции process_bank_operations."""
    return [
        {"id": 1, "description": "Зарплата за январь 2024", "amount": 50000, "date": "2024-01-31"},
        {"id": 2, "description": "Оплата кредита в Сбербанке", "amount": -15000, "date": "2024-01-30"},
        {"id": 3, "description": "Покупка в супермаркете Пятерочка", "amount": -3500, "date": "2024-01-29"},
        {"id": 4, "description": "Перевод другу на карту Тинькофф", "amount": -5000, "date": "2024-01-28"},
        {"id": 5, "description": "Оплата услуг ЖКХ", "amount": -8000, "date": "2024-01-27"},
        {"id": 6, "description": "Заправка автомобиля на Лукойл", "amount": -3000, "date": "2024-01-26"},
        {"id": 7, "description": "Премия за успешный проект", "amount": 25000, "date": "2024-01-25"},
        {"id": 8, "description": "Покупка продуктов в Магните", "amount": -2800, "date": "2024-01-24"},
        {"id": 9, "description": "Оплата интернета от Ростелеком", "amount": -1000, "date": "2024-01-23"},
        {"id": 10, "description": "Такси Яндекс.Такси до работы", "amount": -450, "date": "2024-01-22"},

def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_without_currency() -> List[Dict[str, Any]]:
    """Фикстура с транзакциями без информации о валюте."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "operationAmount": {
                "amount": "100.0"
            },
            "description": "Оплата"
        }
 ]
