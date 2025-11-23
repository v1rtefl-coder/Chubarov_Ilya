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
```