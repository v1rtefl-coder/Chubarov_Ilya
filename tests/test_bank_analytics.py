import pytest
import time
from src.bank_analytics import process_bank_operations


def test_basic_functionality():
    """Базовый тест функции подсчета операций."""
    # Исправляем данные - меняем "продуктов" на "продукты"
    bank_transactions = [
        {"id": 1, "description": "Зарплата за январь 2024", "amount": 50000, "date": "2024-01-31"},
        {"id": 2, "description": "Оплата кредита в Сбербанке", "amount": -15000, "date": "2024-01-30"},
        {"id": 3, "description": "Покупка продукты в супермаркете Пятерочка", "amount": -3500, "date": "2024-01-29"},
        # ИЗМЕНИЛ: "продукты"
        {"id": 4, "description": "Перевод другу на карту Тинькофф", "amount": -5000, "date": "2024-01-28"},
        {"id": 5, "description": "Оплата услуг ЖКХ", "amount": -8000, "date": "2024-01-27"},
        {"id": 6, "description": "Транспорт: заправка автомобиля", "amount": -3000, "date": "2024-01-26"},
        # Добавил "Транспорт:"
        {"id": 7, "description": "Премия за успешный проект", "amount": 25000, "date": "2024-01-25"},
        {"id": 8, "description": "Покупка продукты в Магните", "amount": -2800, "date": "2024-01-24"},
        # ИЗМЕНИЛ: "продукты"
        {"id": 9, "description": "Оплата интернета от Ростелеком", "amount": -1000, "date": "2024-01-23"},
        {"id": 10, "description": "Транспорт: такси до работы", "amount": -450, "date": "2024-01-22"},
        # Добавил "Транспорт:"
    ]

    categories = ["зарплата", "кредит", "продукты", "перевод", "жкх", "транспорт", "премия", "интернет"]

    result = process_bank_operations(bank_transactions, categories)

    expected = {
        "зарплата": 1,
        "кредит": 1,
        "продукты": 2,  # Теперь id: 3 и 8 содержат "продукты"
        "перевод": 1,
        "жкх": 1,
        "транспорт": 2,  # id: 6 и 10 содержат "транспорт"
        "премия": 1,
        "интернет": 1
    }

    assert result == expected


def test_case_insensitive_search(bank_transactions):
    """Поиск должен быть нечувствительным к регистру."""
    # Тест с разными регистрами одной категории
    result1 = process_bank_operations(bank_transactions, ["Зарплата"])
    result2 = process_bank_operations(bank_transactions, ["ЗАРПЛАТА"])
    result3 = process_bank_operations(bank_transactions, ["зарплата"])
    result4 = process_bank_operations(bank_transactions, ["ЗаРпЛаТа"])

    # Все должны найти 1 операцию (id: 1 содержит "Зарплата")
    assert result1["Зарплата"] == 1, f"Для 'Зарплата' ожидалось 1, получено {result1['Зарплата']}"
    assert result2["ЗАРПЛАТА"] == 1, f"Для 'ЗАРПЛАТА' ожидалось 1, получено {result2['ЗАРПЛАТА']}"
    assert result3["зарплата"] == 1, f"Для 'зарплата' ожидалось 1, получено {result3['зарплата']}"
    assert result4["ЗаРпЛаТа"] == 1, f"Для 'ЗаРпЛаТа' ожидалось 1, получено {result4['ЗаРпЛаТа']}"


def test_partial_word_matching():
    """Должен находить части слов в описании."""
    transactions = [
        {"description": "Зарплата за январь"},
        {"description": "Продуктовый магазин"},
        {"description": "Транспортные расходы"},
        {"description": "Обед в ресторане"},
    ]

    categories = ["зарплат", "продукт", "транспорт", "ресторан"]
    result = process_bank_operations(transactions, categories)

    assert result == {
        "зарплат": 1,
        "продукт": 1,
        "транспорт": 1,
        "ресторан": 1
    }


def test_multiple_categories_in_one_description():
    """Одна операция может относиться к нескольким категориям."""
    transactions = [
        {"description": "Зарплата и премия за январь"},
        {"description": "Покупка продукты и такси"},
    ]

    categories = ["зарплата", "премия", "продукты", "такси", "январь"]
    result = process_bank_operations(transactions, categories)

    assert result == {
        "зарплата": 1,
        "премия": 1,
        "продукты": 1,
        "такси": 1,
        "январь": 1
    }


def test_empty_categories_list(sample_transactions):
    """При пустом списке категорий должен возвращаться пустой словарь."""
    result = process_bank_operations(sample_transactions, [])
    assert result == {}


def test_empty_transactions_data():
    """При пустых данных должен возвращать 0 для всех категорий."""
    categories = ["зарплата", "продукты", "транспорт"]
    result = process_bank_operations([], categories)

    assert result == {"зарплата": 0, "продукты": 0, "транспорт": 0}


def test_categories_not_found(sample_transactions):
    """Для категорий, которых нет в данных, должен возвращаться 0."""
    categories = ["недвижимость", "образование", "отпуск", "медицина"]
    result = process_bank_operations(sample_transactions, categories)

    assert result == {
        "недвижимость": 0,
        "образование": 0,
        "отпуск": 0,
        "медицина": 0
    }


def test_transactions_without_description():
    """Операции без поля description должны игнорироваться."""
    transactions = [
        {"id": 1, "description": "Зарплата"},
        {"id": 2},  # Нет поля description
        {"id": 3, "description": ""},  # Пустое описание
        {"id": 4, "description": None},  # None в description
        {"id": 5, "description": "Продукты"},
    ]

    categories = ["зарплата", "продукты"]
    result = process_bank_operations(transactions, categories)

    # Должны быть учтены только операции 1 и 5
    assert result == {"зарплата": 1, "продукты": 1}


def test_special_characters_and_numbers():
    """Должен корректно обрабатывать специальные символы и числа."""
    transactions = [
        {"description": "Скидка 50% на продукты"},
        {"description": "Оплата счета #12345"},
        {"description": "Бонус 1000 рублей"},
        {"description": "Покупка за 199.99 руб"},
    ]

    categories = ["50%", "#12345", "1000", "199.99", "скидка", "бонус"]
    result = process_bank_operations(transactions, categories)

    assert result == {
        "50%": 1,
        "#12345": 1,
        "1000": 1,
        "199.99": 1,
        "скидка": 1,
        "бонус": 1
    }


def test_duplicate_categories_in_input():
    """При дублировании категорий во входном списке, считает каждую отдельно."""
    transactions = [
        {"description": "Зарплата"},
        {"description": "Продукты"},
    ]

    categories = ["зарплата", "продукты", "зарплата", "продукты"]
    result = process_bank_operations(transactions, categories)

    # Каждая категория учитывается отдельно
    assert result == {
        "зарплата": 1,
        "продукты": 1,
        "зарплата": 1,
        "продукты": 1
    }


def test_large_dataset_performance():
    """Тест производительности на большом наборе данных."""
    # Создаем 10,000 транзакций
    transactions = []
    test_categories = ["зарплата", "продукты", "транспорт", "развлечения", "коммуналка"]

    for i in range(10000):
        category = test_categories[i % len(test_categories)]
        transactions.append({
            "id": i,
            "description": f"Транзакция {i}: оплата {category}",
            "amount": i * 10.0,
            "date": "2024-01-01"
        })

    start_time = time.time()
    result = process_bank_operations(transactions, test_categories)
    execution_time = time.time() - start_time

    # Проверяем корректность подсчета
    for category in test_categories:
        # Каждая категория должна встретиться 2000 раз (10000 / 5)
        assert result[category] == 2000

    # Проверяем производительность (должно быть быстро)
    assert execution_time < 1.0  # Меньше 1 секунды


def test_return_type():
    """Проверка типа возвращаемого значения."""
    transactions = [{"description": "Тест"}]
    categories = ["тест"]

    result = process_bank_operations(transactions, categories)

    # Должен возвращаться словарь
    assert isinstance(result, dict)
    # Ключи должны быть строками
    assert all(isinstance(k, str) for k in result.keys())
    # Значения должны быть целыми числами
    assert all(isinstance(v, int) for v in result.values())


def test_none_values_handling():
    """Обработка None значений."""
    # None в качестве данных
    result1 = process_bank_operations(None, ["категория"])
    assert result1 == {"категория": 0}

    # None в качестве категорий
    result2 = process_bank_operations([{"description": "тест"}], None)
    assert result2 == {}

    # Пустая строка в категориях
    result3 = process_bank_operations([{"description": "тест"}], ["", "тест", ""])
    assert result3 == {"тест": 1}


def test_combined_categories():
    """Тест составных категорий (несколько слов)."""
    transactions = [
        {"description": "Зарплата за январь месяц"},
        {"description": "Оплата мобильной связи"},
        {"description": "Покупка бытовой техники"},
    ]

    categories = ["январь месяц", "мобильной связи", "бытовой техники", "не найдено"]
    result = process_bank_operations(transactions, categories)

    assert result == {
        "январь месяц": 1,
        "мобильной связи": 1,
        "бытовой техники": 1,
        "не найдено": 0
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
