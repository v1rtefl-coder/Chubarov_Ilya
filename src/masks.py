import logging
import os
from datetime import datetime


def setup_logging():
    """Настройка логирования"""
    # Создаем папку logs если она не существует
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Формируем имя файла с текущей датой и временем
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"app_{current_time}.log")

    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, mode='w'),  # 'w' для перезаписи при каждом запуске
            logging.StreamHandler()  # Также выводим в консоль (опционально)
        ]
    )


def get_mask_card_number(card_number: str) -> str:
    """Функция маскирует номер карты в формате XXXX XX** **** XXXX"""
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Начало маскировки номера карты: {card_number}")

        if len(card_number) != 16 or not card_number.isdigit():
            error_msg = "Номеер карты должен состоять из 16 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Номер карты успешно замаскирован: {masked}")
        return masked

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера карты: {str(e)}")
        raise


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета в формате **XXXX"""
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Начало маскировки номера счета: {account_number}")

        if len(account_number) < 4 or not account_number.isdigit():
            error_msg = "Номер счета должен содержать минимум 4 цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        masked_account = f"**{account_number[-4:]}"
        logger.info(f"Номер счета успешно замаскирован: {masked_account}")
        return masked_account

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера счета: {str(e)}")
        raise
