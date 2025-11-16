import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv('.env')

# Ключ API (замените на ваш реальный ключ)
API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """
    Конвертирует сумму из одной валюты в другую используя внешнее API.

    Args:
        amount (float): Сумма для конвертации
        from_currency (str): Исходная валюта (например, "USD", "EUR")
        to_currency (str): Целевая валюта (по умолчанию "RUB")

    Returns:
        float: Сконвертированная сумма в целевой валюте

    Raises:
        Exception: Если произошла ошибка при обращении к API
    """
    headers = {
        "apikey": API_KEY
    }

    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Проверяем статус код

        data = response.json()

        if data.get("success", False):
            return float(data["result"])
        else:
            raise Exception(f"API error: {data.get('error', {}).get('info', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except (KeyError, ValueError) as e:
        raise Exception(f"Invalid response format: {str(e)}")


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях

    Raises:
        ValueError: Если валюта транзакции не поддерживается
        Exception: Если произошла ошибка при конвертации валюты
    """
    # Получаем сумму и валюту из транзакции
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB")

    # Если сумма не число, пытаемся преобразовать
    if not isinstance(amount, (int, float)):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            amount = 0.0

    # Если валюта рубль или не указана, возвращаем как есть
    if currency.upper() in ["RUB", ""]:
        return float(amount)

    # Если валюта USD или EUR, конвертируем
    elif currency.upper() in ["USD", "EUR"]:
        try:
            return convert_currency(amount, currency.upper(), "RUB")
        except Exception as e:
            # В случае ошибки API можно вернуть 0 или пробросить исключение
            # В зависимости от требований бизнес-логики
            raise Exception(f"Failed to convert {amount} {currency} to RUB: {str(e)}")

    else:
        raise ValueError(f"Unsupported currency: {currency}")
