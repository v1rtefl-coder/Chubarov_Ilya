def filter_by_currency(transactions: list, currency: str) -> iter:
    """
    Фильтрует транзакции по валюте операции.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Returns:
        Итератор, который выдает транзакции с указанной валютой
    """
    for transaction in transactions:
        # Получаем код валюты из операции
        operation_amount = transaction.get("operationAmount", {})
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code")

        # Проверяем соответствие валюты
        if currency_code == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> iter:
    """
    Генератор, который возвращает описание каждой транзакции по очереди.
    """
    for transaction in transactions:
        yield transaction.get("description")


def card_number_generator(start: int, end: int) -> iter:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: начальный номер карты (от 1)
        end: конечный номер карты (до 9999999999999999)

    Returns:
        Итератор, который выдает номера карт в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями до 16 цифр
        card_str = str(number).zfill(16)

        # Форматируем в виде XXXX XXXX XXXX XXXX
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card
