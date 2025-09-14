import csv
from typing import Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, str]]:
    """ Считывает список финансовых транзакций из CSV-файла. """
    transactions: List[Dict[str, str]] = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions


def read_transactions_from_xlsx(file_path: str) -> List[Dict[str, str]]:
    """ Считывает список финансовых транзакций из файла Excel (.xlsx). """
    df = pd.read_excel(file_path)
    transactions: List[Dict[str, str]] = df.to_dict(orient='records')
    return transactions
