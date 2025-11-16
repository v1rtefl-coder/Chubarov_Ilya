import json
import os
import logging
from typing import List, Dict, Any
from datetime import datetime


def setup_logging():
    """Настройка логирования для модуля транзакций"""
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"transactions_{current_time}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),
            logging.StreamHandler()
        ]
    )


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
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Начало загрузки транзакций из файла: {file_path}")

        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Проверяем, что файл не пустой
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        logger.info(f"Размер файла: {file_size} байт")

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            transactions_count = len(data)
            logger.info(f"Успешно загружено {transactions_count} транзакций из файла {file_path}")

            # Логируем информацию о первых нескольких транзакциях для отладки
            if transactions_count > 0:
                sample_transactions = min(3, transactions_count)
                for i in range(sample_transactions):
                    trans = data[i]
                    trans_id = trans.get('id', 'N/A')
                    trans_date = trans.get('date', 'N/A')
                    trans_amount = trans.get('amount', 'N/A')
                    logger.debug(f"Транзакция {i + 1}: ID={trans_id}, Дата={trans_date}, Сумма={trans_amount}")

            return data

        else:
            logger.warning(f"Данные в файле {file_path} не являются списком. Тип данных: {type(data)}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []

    except FileNotFoundError as e:
        logger.error(f"Файл не найден после проверки существования: {file_path}. Ошибка: {str(e)}")
        return []

    except PermissionError as e:
        logger.error(f"Отсутствуют права доступа к файлу {file_path}: {str(e)}")
        return []

    except UnicodeDecodeError as e:
        logger.error(f"Ошибка кодировки файла {file_path}: {str(e)}")
        return []

    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при загрузке транзакций из {file_path}: {str(e)}")
        return []
