import json
import os
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь до JSON-файла с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Возвращает пустой список, если файл не найден,
                              пустой, или не содержит список.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        # Проверяем, что файл не пустой
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        # Обрабатываем ошибки JSON, отсутствия файла и прав доступа
        return []
