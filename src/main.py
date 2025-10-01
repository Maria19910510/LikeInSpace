import csv
import json
from typing import Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает транзакции из CSV-файла и возвращает список словарей"""
    transactions: List[Dict[str, str]] = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions


def read_transactions_from_xlsx(file_path: str) -> List[Dict[str, str]]:
    """Читает транзакции из XLSX-файла с помощью pandas и возвращает список словарей"""
    df = pd.read_excel(file_path)
    transactions: List[Dict[str, str]] = df.to_dict(orient="records")
    return transactions


def get_transactions_from_json(file_path: str) -> List[Dict[str, str]]:
    """ Загружает транзакции из JSON-файла"""
    with open(file_path, "r", encoding="utf-8") as f:
        transactions = json.load(f)
    return transactions


def filter_by_status(transactions: List[Dict], status: str) -> List[Dict]:
    """Фильтрует список транзакций по статусу"""
    filtered = [tx for tx in transactions if tx.get("status", "").strip().upper() == status.upper()]
    return filtered


def sort_transactions(transactions: List[Dict], ascending: bool = True) -> List[Dict]:
    """Сортирует транзакции по дате"""
    # Предположим, что у транзакций есть дата в поле 'date'
    # Для надежности преобразуем в дату, если нужно
    from datetime import datetime

    def parse_date(tx: Dict) -> datetime:

        date_str = tx.get("date", "")
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except Exception:
            return datetime.min  # чтобы транзакции с ошибками в дате шли в начало

    return sorted(transactions, key=parse_date, reverse=not ascending)


def filter_by_amount_currency(transactions: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует транзакции по указанной валюте"""
    # Можно фильтровать по 'currency' и, если нужно, по количеству
    def matches(tx: Dict) -> bool:
        sum_str = tx.get("amount", "")
        # допустим, сумма указана так: '40542 руб.' или '130 USD'
        return currency.lower() in sum_str.lower()

    return [tx for tx in transactions if matches(tx)]


def filter_by_keyword(transactions: List[Dict], keyword: str) -> List[Dict]:
    """Фильтрует транзакции по наличию ключевого слова в поле 'description'"""
    keyword_lower = keyword.lower()
    return [tx for tx in transactions if keyword_lower in tx.get("description", "").lower()]


def print_transactions(transactions: List[Dict]) -> None:
    """Выводит список транзакций в удобочитаемом формате"""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for tx in transactions:
        date = tx.get("date", "---")
        description = tx.get("description", "")
        amount = tx.get("amount", "")
        print(f"{date} {description}")
        print(f"Сумма: {amount}\n")


def main() -> None:
    """Основная функция программы, реализующая взаимодействие с пользователем.
    Позволяет выбрать источник данных (JSON, CSV или XLSX файл), загружает транзакции,
    затем предлагает выполнить фильтрацию по статусу, сортировку и дополнительные фильтры,
    после чего отображает итоговый список транзакций"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ").strip()
        transactions: List[Dict] = get_transactions_from_json(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ").strip()
        transactions = read_transactions_from_csv(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ").strip()
        transactions = read_transactions_from_xlsx(file_path)
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    # Получение фильтра по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию."
            "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING"
        ).strip()
        status_upper = status_input.upper()
        if status_upper in valid_statuses:
            print(f'Операции отфильтрованы по статусу "{status_upper}"')
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    filtered_transactions = filter_by_status(transactions, status_upper)

    if not filtered_transactions:
        print("Нет операций, соответствующих выбранному статусу.")
        return

    # Сортировка
    sort_choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice in ["да", "д", "yes", "y", "true"]:
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        ascending = True
        if order in ["по возрастанию", "возрастанию", "по убыванию", "убыванию", "asc", "descending", "desc"]:
            if "убыван" in order:
                ascending = False
            else:
                ascending = True
        filtered_transactions = sort_transactions(filtered_transactions, ascending=ascending)

    # Фильтр по валюте
    currency_filter = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if currency_filter in ["да", "д", "yes", "y", "true"]:
        filtered_transactions = filter_by_amount_currency(filtered_transactions, "руб")

    # Фильтр по слову в описании
    description_filter = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
    )
    if description_filter in ["да", "д", "yes", "y", "true"]:
        keyword = input("Введите слово для поиска в описании: ").strip()
        filtered_transactions = filter_by_keyword(filtered_transactions, keyword)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)
