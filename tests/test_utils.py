import unittest
from unittest.mock import mock_open, patch
import json
import os
import sys
from utils import load_transactions

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))


class TestLoadTransactions(unittest.TestCase):

    def test_load_transactions_success(self):
        """Тест успешной загрузки транзакций"""
        test_data = [
            {"id": 1, "amount": 100, "currency": "RUB"},
            {"id": 2, "amount": 50, "currency": "USD"}
        ]

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getsize", return_value=100):
                    result = load_transactions("data/operations.json")

        self.assertEqual(result, test_data)

    def test_load_transactions_file_not_found(self):
        """Тест когда файл не найден"""
        with patch("os.path.exists", return_value=False):
            result = load_transactions("data/nonexistent.json")
            self.assertEqual(result, [])

    def test_load_transactions_empty_file(self):
        """Тест когда файл пустой"""
        with patch("os.path.exists", return_value=True):
            with patch("os.path.getsize", return_value=0):
                result = load_transactions("data/empty.json")
                self.assertEqual(result, [])

    def test_load_transactions_invalid_json(self):
        """Тест когда файл содержит невалидный JSON"""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getsize", return_value=100):
                    result = load_transactions("data/invalid.json")
                    self.assertEqual(result, [])

    def test_load_transactions_not_list(self):
        """Тест когда JSON не является списком"""
        test_data = {"transaction": {"id": 1, "amount": 100}}

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getsize", return_value=100):
                    result = load_transactions("data/not_list.json")
                    self.assertEqual(result, [])

    def test_load_transactions_permission_error(self):
        """Тест когда нет прав доступа к файлу"""
        with patch("builtins.open", side_effect=PermissionError("No permission")):
            with patch("os.path.exists", return_value=True):
                with patch("os.path.getsize", return_value=100):
                    result = load_transactions("data/protected.json")
                    self.assertEqual(result, [])
