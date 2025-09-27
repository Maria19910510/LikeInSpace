import csv
import json
import os

import pytest

from src.main import load_csv, load_json, process_bank_search

TEST_JSON_FILE = "test_transactions.json"
TEST_CSV_FILE = "test_transactions.csv"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Создаем временный JSON-файл
    json_data = [
        {
            "date": "2023-01-01",
            "description": "Test transaction 1",
            "amount": 100,
            "currency": "USD",
            "status": "EXECUTED",
        },
        {
            "date": "2023-01-02",
            "description": "Test transaction 2",
            "amount": 200,
            "currency": "EUR",
            "status": "CANCELED",
        },
    ]
    with open(TEST_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f)
    # Создаем временный CSV-файл
    csv_data = [
        {"date": "2023-02-01", "description": "CSV trans 1", "amount": "150", "currency": "USD", "status": "PENDING"},
        {"date": "2023-02-02", "description": "CSV trans 2", "amount": "250", "currency": "EUR", "status": "EXECUTED"},
    ]
    with open(TEST_CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)
    yield
    # Удаляем файлы после тестов
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)
    if os.path.exists(TEST_CSV_FILE):
        os.remove(TEST_CSV_FILE)


def test_load_json():
    data = load_json(TEST_JSON_FILE)
    assert isinstance(data, list)
    assert data[0]["description"] == "Test transaction 1"


def test_load_csv():
    data = load_csv(TEST_CSV_FILE)
    assert isinstance(data, list)
    assert data[0]["description"] == "CSV trans 1"
    assert data[1]["amount"] == "250"  # проверка строкового значения


def test_process_bank_search():
    transactions = [
        {"description": "Buy groceries"},
        {"description": "Pay rent"},
        {"description": "Grocery shopping"},
    ]

    # Поиск слова "grocery"
    result = process_bank_search(transactions, "grocery")
    assert len(result) == 1

    # Поиск слова "pay"
    result = process_bank_search(transactions, "pay")
    assert len(result) == 1
    assert result[0]["description"] == "Pay rent"

    # Поиск по слову, которого нет
    result = process_bank_search(transactions, "insurance")
    assert len(result) == 0
