import os
import pytest
from src.decorators import log


def test_log_to_console_success(capsys):
    """Тестируем вывод в консоль при успешном выполнении функции"""

    @log()  # без filename - вывод в консоль
    def add(a, b):
        return a + b

    # Вызываем функцию
    result = add(2, 3)

    # Проверяем результат функции
    assert result == 5

    # Перехватываем вывод в консоль с помощью capsys
    captured = capsys.readouterr()

    # Проверяем, что в консоль вывелось правильное сообщение
    assert captured.out == "add ok\n"


def test_log_to_console_error(capsys):
    """Тестируем вывод в консоль при ошибке в функции"""

    @log()
    def divide(a, b):
        return a / b

    # Пытаемся выполнить функцию, которая вызовет ошибку
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass  # Ожидаем ошибку, поэтому просто продолжаем

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем сообщение об ошибке
    expected_start = "divide error: ZeroDivisionError. Inputs: (10, 0)"
    assert captured.out.startswith(expected_start)
    assert captured.out.endswith("\n")


def test_log_to_console_with_keyword_arguments(capsys):
    """Тестируем вывод в консоль при использовании именованных аргументов"""

    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    # Вызываем функцию с именованными аргументами
    result = greet("Alice", greeting="Hi")

    # Проверяем результат
    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert captured.out == "greet ok\n"


def test_log_to_console_with_mixed_arguments(capsys):
    """Тестируем вывод в консоль при смешанных аргументах"""

    @log()
    def mixed_function(a, b, c=10, d=20):
        return a + b + c + d

    # Вызываем с позиционными и именованными аргументами
    result = mixed_function(1, 2, c=30, d=40)
    assert result == 73

    captured = capsys.readouterr()
    assert captured.out == "mixed_function ok\n"


def test_log_to_file_success(tmp_path):
    """Тестируем запись в файл при успешном выполнении функции"""

    # Используем временную директорию pytest
    test_filename = tmp_path / "test_success.log"

    @log(filename=str(test_filename))
    def multiply(x, y):
        return x * y

    # Вызываем функцию
    result = multiply(4, 5)

    # Проверяем результат функции
    assert result == 20

    # Проверяем, что файл создался
    assert test_filename.exists()

    # Читаем содержимое файла
    content = test_filename.read_text(encoding='utf-8')

    # Проверяем содержимое файла
    assert content == "multiply ok\n"


def test_log_to_file_error(tmp_path):
    """Тестируем запись в файл при ошибке в функции"""

    test_filename = tmp_path / "test_error.log"

    @log(filename=str(test_filename))
    def failing_function(n):
        raise ValueError("Что-то пошло не так!")

    # Пытаемся выполнить функцию, которая вызовет ошибку
    try:
        failing_function(42)
    except ValueError:
        pass  # Ожидаем ошибку

    # Проверяем, что файл создался
    assert test_filename.exists()

    # Читаем содержимое файла
    content = test_filename.read_text(encoding='utf-8')

    # Проверяем содержимое файла
    assert content == "failing_function error: ValueError. Inputs: (42,)\n"


def test_log_to_file_multiple_calls(tmp_path):
    """Тестируем множественные вызовы с записью в файл"""

    test_filename = tmp_path / "test_multiple.log"

    @log(filename=str(test_filename))
    def counter():
        return "выполнено"

    # Вызываем функцию несколько раз
    result1 = counter()
    result2 = counter()
    result3 = counter()

    # Проверяем результаты
    assert result1 == result2 == result3 == "выполнено"

    # Проверяем содержимое файла
    content = test_filename.read_text(encoding='utf-8')

    # Должно быть 3 записи в лог
    assert content == "counter ok\n" * 3


def test_exception_propagation():
    """Тестируем, что исключение не 'проглатывается', а пробрасывается дальше"""

    @log()
    def raise_custom_error():
        raise RuntimeError("Кастомная ошибка")

    # Проверяем, что исключение действительно возникает
    with pytest.raises(RuntimeError, match="Кастомная ошибка"):
        raise_custom_error()


def test_function_without_arguments(capsys):
    """Тестируем функцию без аргументов"""

    @log()
    def get_pi():
        return 3.14159

    result = get_pi()
    assert result == 3.14159

    captured = capsys.readouterr()
    assert captured.out == "get_pi ok\n"


def test_function_with_only_keyword_arguments(capsys):
    """Тестируем функцию только с именованными аргументами"""

    @log()
    def create_person(name, age=0, city="Unknown"):
        return f"{name}, {age} years, from {city}"

    result = create_person(name="Bob", age=25, city="Moscow")
    assert result == "Bob, 25 years, from Moscow"

    captured = capsys.readouterr()
    assert captured.out == "create_person ok\n"


def test_log_append_to_file(tmp_path):
    """Тестируем, что логи дописываются в файл, а не перезаписываются"""

    test_filename = tmp_path / "test_append.log"

    @log(filename=str(test_filename))
    def simple_func():
        return "result"

    # Первый вызов
    simple_func()

    # Второй вызов
    simple_func()

    # Читаем содержимое файла
    content = test_filename.read_text(encoding='utf-8')

    # Должно быть 2 записи
    lines = content.strip().split('\n')
    assert len(lines) == 2
    assert all(line == "simple_func ok" for line in lines)


def test_different_exception_types(capsys):
    """Тестируем разные типы исключений"""

    @log()
    def key_error_function():
        my_dict = {}
        return my_dict["missing_key"]

    @log()
    def type_error_function():
        return "string" + 42  # Нельзя сложить строку и число

    # Тестируем KeyError
    try:
        key_error_function()
    except KeyError:
        pass

    captured1 = capsys.readouterr()
    assert "key_error_function error: KeyError" in captured1.out

    # Тестируем TypeError
    try:
        type_error_function()
    except TypeError:
        pass

    captured2 = capsys.readouterr()
    assert "type_error_function error: TypeError" in captured2.out


def test_complex_arguments_logging(capsys):
    """Тестируем логирование сложных аргументов"""

    @log()
    def process_data(numbers, name, enabled=True):
        return f"Processed {len(numbers)} numbers for {name}, enabled: {enabled}"

    # Вызываем со списком и именованными аргументами
    result = process_data([1, 2, 3, 4, 5], "test_user", enabled=False)
    assert "Processed 5 numbers for test_user, enabled: False" in result

    captured = capsys.readouterr()
    assert captured.out == "process_data ok\n"


def test_none_filename_uses_console(capsys):
    """Тестируем, что None в filename использует консоль"""

    @log(filename=None)  # Явно указываем None
    def test_func():
        return "test"

    result = test_func()
    assert result == "test"

    captured = capsys.readouterr()
    assert captured.out == "test_func ok\n"


# Дополнительные тесты для проверки граничных случаев
def test_empty_arguments(capsys):
    """Тестируем функцию без аргументов"""

    @log()
    def no_args():
        return "no arguments"

    result = no_args()
    assert result == "no arguments"

    captured = capsys.readouterr()
    assert captured.out == "no_args ok\n"


def test_function_preserves_metadata():
    """Тестируем, что декоратор сохраняет метаданные функции"""

    @log()
    def documented_function(x):
        """Это документированная функция"""
        return x * 2

    # Проверяем, что метаданные сохранились
    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "Это документированная функция"


if __name__ == "__main__":
    # Запуск тестов напрямую через pytest
    pytest.main([__file__, "-v"])