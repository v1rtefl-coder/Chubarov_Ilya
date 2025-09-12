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


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        data: Список словарей для сортировки
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список словарей
    """
    return sorted(data, key=lambda x: x['date'], reverse=reverse)
