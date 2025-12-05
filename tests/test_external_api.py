import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Добавляем корневую директорию проекта в PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))  # tests/
project_root = os.path.dirname(current_dir)  # Chubarov_ILya/
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from external_api import get_transaction_amount_in_rub, convert_currency


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))


class TestConvertCurrency(unittest.TestCase):

    @patch('external_api.requests.get')
    def test_convert_currency_success(self, mock_get):
        """Тест успешной конвертации валюты"""
        # Мокаем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": 7500.50
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = convert_currency(100, "USD", "RUB")

        self.assertEqual(result, 7500.50)
        mock_get.assert_called_once()

    @patch('external_api.requests.get')
    def test_convert_currency_api_error(self, mock_get):
        """Тест когда API возвращает ошибку"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            convert_currency(100, "USD", "RUB")

        self.assertIn("API error", str(context.exception))


class TestGetTransactionAmountInRub(unittest.TestCase):

    def test_rub_transaction(self):
        """Тест транзакции в рублях"""
        transaction = {"amount": 1000, "currency": "RUB"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 1000.0)

    def test_rub_transaction_string_amount(self):
        """Тест транзакции в рублях с суммой как строка"""
        transaction = {"amount": "1500.75", "currency": "RUB"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 1500.75)

    @patch('external_api.convert_currency')
    def test_usd_transaction(self, mock_convert):
        """Тест транзакции в USD"""
        # ЗАМОКАНО: Фиксированное значение вместо реального API-вызова
        mock_convert.return_value = 7500.50
        transaction = {"amount": 100, "currency": "USD"}

        result = get_transaction_amount_in_rub(transaction)

        self.assertEqual(result, 7500.50)
        mock_convert.assert_called_once_with(100, "USD", "RUB")

    @patch('external_api.convert_currency')
    def test_eur_transaction(self, mock_convert):
        """Тест транзакции в EUR"""
        # ЗАМОКАНО: Фиксированное значение вместо реального API-вызова
        mock_convert.return_value = 8500.25
        transaction = {"amount": 100, "currency": "EUR"}

        result = get_transaction_amount_in_rub(transaction)

        self.assertEqual(result, 8500.25)
        mock_convert.assert_called_once_with(100, "EUR", "RUB")

    @patch('external_api.convert_currency')
    def test_currency_case_insensitive(self, mock_convert):
        """Тест что валюта обрабатывается case-insensitive"""
        # ЗАМОКАНО: Фиксированное значение вместо реального API-вызова
        mock_convert.return_value = 7500.50
        transaction = {"amount": 100, "currency": "usd"}  # lowercase

        result = get_transaction_amount_in_rub(transaction)

        self.assertEqual(result, 7500.50)
        # Обратите внимание: функция должна конвертировать "usd" в "USD"
        mock_convert.assert_called_once_with(100, "USD", "RUB")

    def test_no_currency_specified(self):
        """Тест когда валюта не указана (по умолчанию RUB)"""
        transaction = {"amount": 1000}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 1000.0)

    def test_empty_currency(self):
        """Тест когда валюта пустая строка"""
        transaction = {"amount": 1000, "currency": ""}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 1000.0)

    def test_invalid_amount_string(self):
        """Тест когда сумма не может быть преобразована в число"""
        transaction = {"amount": "invalid", "currency": "RUB"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 0.0)

    def test_missing_amount(self):
        """Тест когда сумма отсутствует"""
        transaction = {"currency": "RUB"}
        result = get_transaction_amount_in_rub(transaction)
        self.assertEqual(result, 0.0)

    @patch('external_api.convert_currency')
    def test_conversion_error(self, mock_convert):
        """Тест когда конвертация валюты завершается ошибкой"""
        # ЗАМОКАНО: Имитируем исключение от API
        mock_convert.side_effect = Exception("API unavailable")

        transaction = {"amount": 100, "currency": "USD"}

        # Проверяем, что исключение действительно выбрасывается
        with self.assertRaises(Exception) as context:
            get_transaction_amount_in_rub(transaction)

        self.assertIn("API unavailable", str(context.exception))
        # Или, если функция оборачивает исключение:
        # self.assertIn("Failed to convert", str(context.exception))

    def test_unsupported_currency(self):
        """Тест неподдерживаемой валюты"""
        transaction = {"amount": 100, "currency": "GBP"}

        with self.assertRaises(ValueError) as context:
            get_transaction_amount_in_rub(transaction)

        self.assertIn("Unsupported currency", str(context.exception))


if __name__ == '__main__':
    unittest.main()
