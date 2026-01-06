import csv
import pandas as pd
import os
from typing import List, Dict


def reading_transactions_csv(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из CSV-файла.
    Возвращает список словарей с транзакциями.
    """
    try:
        transactions_csv = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_f:
            rd_transactions_csv = csv.DictReader(csv_f, delimiter=';')
            for row in rd_transactions_csv:
                transactions_csv.append(row)
        return transactions_csv
    except FileNotFoundError:
        return []
    except Exception:
        return []


def reading_transactions_excel(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel файла.
    Возвращает список словарей с транзакциями.
    """
    try:
        if not os.path.exists(file_path):
            return []

        df = pd.read_excel(file_path)
        transactions = df.to_dict('records')
        return transactions

    except Exception:
        return []
