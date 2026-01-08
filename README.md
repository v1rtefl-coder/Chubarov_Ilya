# Домашняя работа
## Описание
Виджет банковских операций клиента. Который показывает несколько последних успешных банковских операций клиента. 
Маскирует номера карт и счета клиента и фильтрации по статусу операций и сортировки по дате. 
## Установка
1.Склонируйте репозиторий или скачайте файлы проекта:

2.Убедитесь, что у вас установлен Python 3.6 или выше
3.Установите зависимости:
```
pip install -r requirements.txt
```
# Использование
Импорт модулей:
```
from src.masks.masks import get_mask_card_number, get_mask_account
```
```
from src.processing.processing import filter_by_state, sort_by_date
```
# Тесты
## Обзор тестирования
Проект включает комплексные тесты, покрывающие все основные модули и функции. 
Тесты написаны с использованием библиотеки `pytest`
## Установка зависимостей для тестирования
### Установка pytest
```
pip install pytest
```
### Или установка всех зависимостей из requirements.txt
```
pip install -r requirements-test.txt
```

# Финансовые операции
Проект для обработки финансовых операций из различных форматов файлов.
Поддержка чтения csv и excel файлов
## Установка и использование
1. Клонирование репозитория
```
git clone <repository-url>
```
2. Установка зависимостей
```
pip install -r requirements.txt
```
3. Использование в коде
```
from src.csv_operations import reading_transactions_csv
from src.excel_operations import reading_transactions_excel

# Чтение из CSV
csv_data = reading_transactions_csv('data/transactions.csv')

# Чтение из Excel
excel_data = reading_transactions_excel('data/transactions.xlsx')

print(f"CSV транзакций: {len(csv_data)}")
print(f"Excel транзакций: {len(excel_data)}")

# Генераторы транзакций
## Описание
Этот проект содержит набор генераторов для работы с банковскими транзакциями и номерами карт.
## Filter_by_currency
Фильтрует транзакции по заданной валюте операции.
### Пример использования
```
from generators import filter_by_currency

transactions = [
    {
        "id": 1,
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    },
    {
        "id": 2,
        "operationAmount": {
            "amount": "200.00",
            "currency": {"code": "EUR"}
        }
    }
]

# Получаем только USD транзакции
usd_transactions = filter_by_currency(transactions, "USD")

# Используем next() для получения по одной транзакции
first_usd = next(usd_transactions)
print(first_usd["id"])  # 1

# Или преобразуем в список
all_usd = list(filter_by_currency(transactions, "USD"))
```
## Transaction_descriptions
Извлекает описания операций из списка транзакций.
### Пример использования
```
from generators import transaction_descriptions

transactions = [
    {
        "id": 1,
        "description": "Перевод организации",
        "operationAmount": {"amount": "100.00"}
    },
    {
        "id": 2,
        "description": "Оплата услуг",
        "operationAmount": {"amount": "200.00"}
    }
]

# Получаем описания
descriptions = transaction_descriptions(transactions)

# Используем next() для получения по одному описанию
first_description = next(descriptions)
print(first_description)  # "Перевод организации"

# Или преобразуем в список
all_descriptions = list(transaction_descriptions(transactions))
# ["Перевод организации", "Оплата услуг"]
```
## Card_number_generator
Генерирует номера банковских карт в заданном диапазоне
### Пример использования
```
from generators import card_number_generator

# Генерируем номера карт от 1 до 5
card_numbers = card_number_generator(1, 5)

# Получаем номера по одному
print(next(card_numbers))  # "0000 0000 0000 0001"
print(next(card_numbers))  # "0000 0000 0000 0002"

# Или преобразуем в список
all_numbers = list(card_number_generator(1, 3))
# ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"] 
```