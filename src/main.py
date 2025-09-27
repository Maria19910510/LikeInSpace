def main():
    """Основная функция программы для работы с банковскими транзакциями.
    Обеспечивает выбор файла, загрузку данных, фильтрацию по статусу,
    дальнейшую фильтрацию по дате и валюте, а также по слову в описании.
    Затем выводит итоговые транзакции"""
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input()
    print(f"Вы выбрали пункт {choice}")

    # Обработка выбора файла и его загрузки
    if choice == "1":
        filename = input("Введите название JSON-файла: ")
        data = load_json(filename)
    elif choice == "2":
        filename = input("Введите название CSV-файла: ")
        data = load_csv(filename)
    else:
        print("Некорректный выбор.")
        return

    # Фильтрация по статусу
    statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию:\n"
            "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip()
        status_upper = status_input.upper()
        if status_upper in statuses:
            print(f'Операции отфильтрованы по статусу "{status_upper}"')
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    # Фильтрация данных по выбранному статусу
    filtered_data = [t for t in data if t.get("status", "").upper() == status_upper]

    # сортировка по дате
    sort_choice = input("Отсортировать по дате? (да/нет): ").strip().lower()
    if sort_choice == "да":
        # Предполагается, что даты в формате 'YYYY-MM-DD' или подобном
        def parse_date(t):
            from datetime import datetime

            date_str = t.get("date", "")
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return datetime.min  # Если дата отсутствует или неверного формата

        filtered_data.sort(key=parse_date)

    # Фильтрация по валюте
    currency_filter = input("Введите валюту для фильтрации (оставьте пустым, чтобы пропустить): ").strip()
    if currency_filter:
        filtered_data = [t for t in filtered_data if t.get("currency", "").upper() == currency_filter.upper()]

    # Фильтрация по слову в описании
    filter_word = (
        input("Отфильтровать список транзакций по определенному слову в описании? (да/нет): ").strip().lower()
    )
    if filter_word == "да":
        word = input("Введите слово: ").strip()
        filtered_data = process_bank_search(filtered_data, word)

    # Итоговая проверка
    if not filtered_data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Вывод итоговых транзакций
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_data)}")
    for t in filtered_data:
        print(f"{t.get('date', '')} {t.get('description', '')}")
        print(f"Сумма: {t.get('amount', '')} {t.get('currency', '')}\n")


# Объявление вспомогательных функций для загрузки данных
def load_json(filename):
    import json

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(filename):
    import csv

    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def process_bank_search(transactions, keyword):
    """Фильтрует список транзакций по вхождению ключевого слова в описание"""
    keyword_upper = keyword.upper()
    return [t for t in transactions if keyword_upper in t.get("description", "").upper()]
