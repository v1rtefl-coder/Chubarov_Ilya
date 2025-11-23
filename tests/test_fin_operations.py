from unittest.mock import mock_open, patch, MagicMock
from src.fin_operations import reading_transactions_csv
from src.fin_operations import reading_transactions_excel


class TestCSVOperations:
    """Тесты для функции чтения CSV файлов"""

    @patch('builtins.open', new_callable=mock_open, read_data="date;amount;description\n2024-01-15;1500;Зарплата")
    @patch('csv.DictReader')
    def test_reading_transactions_csv_success(self, mock_dict_reader, mock_file):
        """Тест успешного чтения CSV файла"""
        # Arrange
        mock_dict_reader.return_value = [
            {'date': '2024-01-15', 'amount': '1500', 'description': 'Зарплата'},
            {'date': '2024-01-16', 'amount': '-250', 'description': 'Продукты'}
        ]

        # Act
        result = reading_transactions_csv('test.csv')

        # Assert
        assert len(result) == 2
        assert result[0]['date'] == '2024-01-15'
        assert result[0]['amount'] == '1500'
        assert result[0]['description'] == 'Зарплата'
        mock_file.assert_called_once_with('test.csv', 'r', newline='', encoding='utf-8')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_reading_transactions_csv_file_not_found(self, mock_file):
        """Тест случая когда файл не найден"""
        # Act
        result = reading_transactions_csv('nonexistent.csv')

        # Assert
        assert result == []

    @patch('builtins.open', side_effect=Exception("Ошибка чтения"))
    def test_reading_transactions_csv_general_exception(self, mock_file):
        """Тест обработки общего исключения"""
        # Act
        result = reading_transactions_csv('corrupted.csv')

        # Assert
        assert result == []

    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('csv.DictReader')
    def test_reading_transactions_csv_empty_file(self, mock_dict_reader, mock_file):
        """Тест чтения пустого CSV файла"""
        # Arrange
        mock_dict_reader.return_value = []

        # Act
        result = reading_transactions_csv('empty.csv')

        # Assert
        assert result == []

    @patch('builtins.open', new_callable=mock_open, read_data="date;amount;description")
    @patch('csv.DictReader')
    def test_reading_transactions_csv_only_headers(self, mock_dict_reader, mock_file):
        """Тест чтения CSV файла только с заголовками"""
        # Arrange
        mock_dict_reader.return_value = []

        # Act
        result = reading_transactions_csv('headers_only.csv')

        # Assert
        assert result == []


class TestExcelOperations:
    """Тесты для функции чтения Excel файлов"""

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_reading_transactions_excel_success(self, mock_read_excel, mock_exists):
        """Тест успешного чтения Excel файла"""
        # Arrange
        mock_exists.return_value = True

        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {'date': '2024-01-15', 'amount': 1500, 'description': 'Зарплата'},
            {'date': '2024-01-16', 'amount': -250, 'description': 'Продукты'}
        ]
        mock_read_excel.return_value = mock_df

        # Act
        result = reading_transactions_excel('test.xlsx')

        # Assert
        assert len(result) == 2
        assert result[0]['date'] == '2024-01-15'
        assert result[0]['amount'] == 1500
        mock_exists.assert_called_once_with('test.xlsx')
        mock_read_excel.assert_called_once_with('test.xlsx')
        mock_df.to_dict.assert_called_once_with('records')

    @patch('os.path.exists')
    def test_reading_transactions_excel_file_not_found(self, mock_exists):
        """Тест случая когда файл не найден"""
        # Arrange
        mock_exists.return_value = False

        # Act
        result = reading_transactions_excel('nonexistent.xlsx')

        # Assert
        assert result == []
        mock_exists.assert_called_once_with('nonexistent.xlsx')

    @patch('os.path.exists')
    @patch('pandas.read_excel', side_effect=Exception("Ошибка Excel"))
    def test_reading_transactions_excel_general_exception(self, mock_read_excel, mock_exists):
        """Тест обработки общего исключения при чтении Excel"""
        # Arrange
        mock_exists.return_value = True

        # Act
        result = reading_transactions_excel('corrupted.xlsx')

        # Assert
        assert result == []

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_reading_transactions_excel_empty_dataframe(self, mock_read_excel, mock_exists):
        """Тест чтения пустого Excel файла"""
        # Arrange
        mock_exists.return_value = True

        mock_df = MagicMock()
        mock_df.to_dict.return_value = []
        mock_read_excel.return_value = mock_df

        # Act
        result = reading_transactions_excel('empty.xlsx')

        # Assert
        assert result == []

    @patch('os.path.exists')
    @patch('pandas.read_excel')
    def test_reading_transactions_excel_single_record(self, mock_read_excel, mock_exists):
        """Тест чтения Excel файла с одной записью"""
        # Arrange
        mock_exists.return_value = True

        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {'date': '2024-01-15', 'amount': 1500, 'description': 'Зарплата'}
        ]
        mock_read_excel.return_value = mock_df

        # Act
        result = reading_transactions_excel('single.xlsx')

        # Assert
        assert len(result) == 1
        assert result[0]['description'] == 'Зарплата'
