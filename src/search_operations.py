import re
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список банковских операций по наличию строки поиска в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операций

    Returns:
        Список отфильтрованных словарей, где в описании найдена строка поиска
    """
    if not search or not data:
        return []

    try:
        # Компилируем регулярное выражение для поиска с игнорированием регистра
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        # Если строка поиска содержит невалидные regex-символы,
        # используем простое текстовое сравнение
        pattern = None

    result = []

    for operation in data:
        # Проверяем наличие поля 'description' в словаре
        description = operation.get('description')
        if not description:
            continue

        # Ищем совпадение с использованием regex или простого поиска
        if pattern:
            if pattern.search(description):
                result.append(operation)
        else:
            if search.lower() in description.lower():
                result.append(operation)

    return result
