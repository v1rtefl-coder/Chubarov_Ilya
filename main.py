import os
from typing import Optional, List
from datetime import datetime

# Импортируем из utils.py
from src.utils import load_transactions

# Импортируем из processing.py
from src.processing import filter_by_state, sort_by_date

# Импортируем из generators.py
from src.generators import filter_by_currency, transaction_descriptions

# Импортируем из masks.py
from src.masks import get_mask_account, get_mask_card_number


def get_user_input(prompt: str, valid_options: Optional[List[str]] = None,
                   case_sensitive: bool = False) -> str:
    """
    Получает ввод от пользователя с валидацией.

    Args:
        prompt: Подсказка для ввода
        valid_options: Список допустимых вариантов (None если любой ввод допустим)
        case_sensitive: Чувствительность к регистру при проверке

    Returns:
        Введенная строка
    """
    while True:
        user_input = input(prompt).strip()

        if not valid_options:
            return user_input

        if not case_sensitive:
            user_input_lower = user_input.lower()
            valid_lower = [opt.lower() for opt in valid_options]
            if user_input_lower in valid_lower:
                # Возвращаем оригинальный вариант из valid_options
                idx = valid_lower.index(user_input_lower)
                return valid_options[idx]
        else:
            if user_input in valid_options:
                return user_input

        print(f"Пожалуйста, введите один из допустимых вариантов: {', '.join(valid_options)}")


def format_date(date_str: str) -> str:
    """
    Форматирует дату из ISO формата в DD.MM.YYYY.

    Args:
        date_str: Дата в строковом формате

    Returns:
        Отформатированная дата
    """
    try:
        # Пытаемся разобрать разные форматы дат
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')
    except (ValueError, AttributeError):
        return date_str


def format_operation_details(operation: dict) -> str:
    """
    Форматирует детали операции для вывода.

    Args:
        operation: Словарь с данными операции

    Returns:
        Отформатированная строка
    """
    date = format_date(operation.get('date', ''))
    description = operation.get('description', 'Без описания')

    from_info = operation.get('from', '')
    to_info = operation.get('to', '')
    amount = operation.get('operationAmount', {}).get('amount', '0')
    currency = operation.get('operationAmount', {}).get('currency', {}).get('name', 'руб.')

    # Маскирование номеров
    if from_info:
        if 'Счет' in from_info:
            from_info = get_mask_account(from_info)
        else:
            from_info = get_mask_card_number(from_info)

    if to_info:
        if 'Счет' in to_info:
            to_info = get_mask_account(to_info)
        else:
            to_info = get_mask_card_number(to_info)

    # Формирование строки
    result = f"{date} {description}\n"

    if from_info:
        result += f"{from_info} -> "
    result += f"{to_info}\n"
    result += f"Сумма: {amount} {currency}\n"

    return result


def get_available_files() -> tuple:
    """
    Проверяет наличие файлов в папке data.

    Returns:
        Кортеж (json_exists, csv_exists, xlsx_exists, json_path, csv_path, xlsx_path)
    """
    data_dir = 'data'

    # Ищем файлы с разными возможными расширениями
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')] if os.path.exists(data_dir) else []
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')] if os.path.exists(data_dir) else []
    xlsx_files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx')] if os.path.exists(data_dir) else []

    # Используем первый найденный файл каждого типа
    json_path = os.path.join(data_dir, json_files[0]) if json_files else None
    csv_path = os.path.join(data_dir, csv_files[0]) if csv_files else None
    xlsx_path = os.path.join(data_dir, xlsx_files[0]) if xlsx_files else None

    return (bool(json_path), bool(csv_path), bool(xlsx_path), json_path, csv_path, xlsx_path)


def load_csv_file(file_path: str):
    """
    Загружает данные из CSV файла.

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список операций
    """
    import csv

    operations = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Преобразуем строку в нужный формат
                operation = {
                    'id': int(row.get('id', 0)),
                    'state': row.get('state', ''),
                    'date': row.get('date', ''),
                    'description': row.get('description', ''),
                    'from': row.get('from', ''),
                    'to': row.get('to', ''),
                    'operationAmount': {
                        'amount': float(row.get('amount', 0)) if row.get('amount') else 0,
                        'currency': {
                            'name': row.get('currency', 'RUB'),
                            'code': row.get('currency_code', 'RUB')
                        }
                    }
                }
                operations.append(operation)
    except Exception as e:
        print(f"Ошибка при загрузке CSV файла: {e}")
        return []

    return operations


def load_xlsx_file(file_path: str):
    """
    Загружает данные из XLSX файла.

    Args:
        file_path: Путь к XLSX файлу

    Returns:
        Список операций
    """
    try:
        import pandas as pd

        df = pd.read_excel(file_path)
        operations = []

        for _, row in df.iterrows():
            operation = {
                'id': int(row.get('id', 0)),
                'state': str(row.get('state', '')),
                'date': str(row.get('date', '')),
                'description': str(row.get('description', '')),
                'from': str(row.get('from', '')),
                'to': str(row.get('to', '')),
                'operationAmount': {
                    'amount': float(row.get('amount', 0)),
                    'currency': {
                        'name': str(row.get('currency', 'RUB')),
                        'code': str(row.get('currency_code', 'RUB'))
                    }
                }
            }
            operations.append(operation)

        return operations
    except ImportError:
        print("Для работы с XLSX файлами установите библиотеку pandas: pip install pandas")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке XLSX файла: {e}")
        return []


def main() -> None:
    """Основная функция программы."""
    print("=" * 60)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("=" * 60)

    # Проверяем наличие папки data
    if not os.path.exists('data'):
        print("Ошибка: Папка 'data' не найдена.")
        print("Пожалуйста, создайте папку 'data' и поместите туда файлы с транзакциями.")
        return

    # Проверяем доступные файлы
    json_exists, csv_exists, xlsx_exists, json_path, csv_path, xlsx_path = get_available_files()

    if not (json_exists or csv_exists or xlsx_exists):
        print("Ошибка: В папке 'data' не найдены файлы с транзакциями.")
        print("Пожалуйста, поместите в папку 'data' файлы в формате JSON, CSV или XLSX.")
        return

    print("\nДоступные файлы для обработки:")
    menu_options = []

    if json_exists:
        print(f"1. {os.path.basename(json_path)} (JSON)")
        menu_options.append('1')
    if csv_exists:
        print(f"2. {os.path.basename(csv_path)} (CSV)")
        menu_options.append('2')
    if xlsx_exists:
        print(f"3. {os.path.basename(xlsx_path)} (XLSX)")
        menu_options.append('3')

    file_type = get_user_input("\nВаш выбор: ", menu_options)

    # Загружаем данные из выбранного файла
    try:
        if file_type == '1' and json_exists:
            print(f"\nДля обработки выбран JSON-файл: {os.path.basename(json_path)}")
            operations = load_transactions(json_path)
        elif file_type == '2' and csv_exists:
            print(f"\nДля обработки выбран CSV-файл: {os.path.basename(csv_path)}")
            operations = load_csv_file(csv_path)
        elif file_type == '3' and xlsx_exists:
            print(f"\nДля обработки выбран XLSX-файл: {os.path.basename(xlsx_path)}")
            operations = load_xlsx_file(xlsx_path)
        else:
            print("Ошибка: Выбран недопустимый вариант.")
            return
    except FileNotFoundError:
        print("Ошибка: Файл не найден.")
        return
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    if not operations:
        print("Нет данных для обработки.")
        return

    # Фильтрация по статусу
    available_states = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print("\n" + "-" * 50)
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтрации статусы: {', '.join(available_states)}")

        user_state = input("Статус: ").strip().upper()

        if user_state in available_states:
            filtered_operations = filter_by_state(operations, user_state)
            print(f"\nОперации отфильтрованы по статусу '{user_state}'")
            break
        else:
            print(f"\nСтатус операции '{user_state}' недоступен.")

    if not filtered_operations:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = get_user_input("\nОтсортировать операции по дате? Да/Нет: ",
                                 ['Да', 'Нет', 'да', 'нет'])

    if sort_choice.lower() in ['да', 'yes']:
        order_choice = get_user_input("\nОтсортировать по возрастанию или по убыванию? "
                                      "(возрастание/убывание): ",
                                      ['возрастание', 'убывание'])

        reverse = (order_choice == 'убывание')
        filtered_operations = sort_by_date(filtered_operations, reverse)
        print("Операции отсортированы.")

    # Фильтрация по валюте
    currency_choice = get_user_input("\nВыводить только рублевые транзакции? Да/Нет: ",
                                     ['Да', 'Нет', 'да', 'нет'])

    if currency_choice.lower() in ['да', 'yes']:
        filtered_operations = filter_by_currency(filtered_operations, 'RUB')
        print("Оставлены только рублевые транзакции.")

    if not filtered_operations:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Фильтрация по ключевому слову
    keyword_choice = get_user_input("\nОтфильтровать список транзакций по определенному "
                                    "слову в описании? Да/Нет: ",
                                    ['Да', 'Нет', 'да', 'нет'])

    if keyword_choice.lower() in ['да', 'yes']:
        keyword = input("Введите слово для поиска в описании: ").strip()
        if keyword:
            filtered_operations = transaction_descriptions(filtered_operations, keyword)
            print(f"Применена фильтрация по слову '{keyword}'.")

    if not filtered_operations:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результатов
    print("\n" + "=" * 60)
    print("Распечатываю итоговый список транзакций...")
    print("=" * 60)
    print(f"\nВсего банковских операций в выборке: {len(filtered_operations)}\n")

    for operation in filtered_operations:
        print(format_operation_details(operation))
        print("-" * 40)


if __name__ == "__main__":
    main()
