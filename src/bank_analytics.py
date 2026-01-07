from typing import List, Dict
from collections import Counter


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций определенного типа.

    Args:
        data: Список словарей с транзакциями (банковскими операциями)
        categories: Список категорий операций для подсчёта на основе поля description

    Returns:
        Словарь, в котором ключи — это названия категорий,
        а значения — это количество операций в каждой категории.

    Examples:
        >>> data = [
        ...     {"description": "Payment for groceries"},
        ...     {"description": "Salary January"},
        ...     {"description": "Grocery shopping"}
        ... ]
        >>> categories = ["grocery", "salary", "rent"]
        >>> process_bank_operations(data, categories)
        {"grocery": 2, "salary": 1, "rent": 0}
    """
    # Обработка крайних случаев
    if not categories:
        return {}

    if not data:
        return {category: 0 for category in categories}

    # Инициализируем Counter для подсчета
    counter = Counter()

    # Подготавливаем категории для регистронезависимого поиска
    # Создаем словарь для сопоставления категорий в нижнем регистре с оригинальными
    category_mapping = {}
    for category in categories:
        if category:  # Пропускаем пустые категории
            category_mapping[category.lower()] = category

    # Подсчитываем операции
    for operation in data:
        description = operation.get('description')
        if not description:
            continue

        description_lower = description.lower()

        # Проверяем каждую категорию из mapping
        for category_lower, original_category in category_mapping.items():
            if category_lower in description_lower:
                counter[original_category] += 1

    # Создаем итоговый словарь, сохраняя порядок категорий из входного списка
    # и устанавливая 0 для категорий, не найденных в данных
    result = {}
    for category in categories:
        if category:  # Пропускаем пустые категории
            result[category] = counter.get(category, 0)

    return result
