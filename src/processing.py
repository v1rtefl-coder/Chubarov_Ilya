def filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data: Список словарей для фильтрации
        state: Значение для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список словарей
    """
    return [item for item in data if item.get('state') == state]


