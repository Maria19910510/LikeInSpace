from typing import Dict, Iterable, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterable:
    """Возвращает итератор транзакций с указанной валютой"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterable[str]:
    """Генератор, который по очереди возвращает описание каждой транзакции"""
    for transaction in transactions:
        description_type = transaction.get("type")
        if description_type == "transfer_org":
            yield "Перевод организации"
        elif description_type == "transfer_account":
            yield "Перевод со счета на счет"
        elif description_type == "transfer_card":
            yield "Перевод с карты на карту"
        elif description_type == "transfer_person":
            yield "Перевод физическому лицу"
        else:
            yield "Описание операции неизвестно"


def card_number_generator(start: int, end: int) -> Iterable[str]:
    for num in range(start, end + 1):
        # Форматируем число с ведущими нулями до 16 цифр
        card_number = f"{num:016d}"
        # Разбиваем на группы по 4 цифры и соединяем пробелами
        formatted_number = " ".join([card_number[i : i + 4] for i in range(0, 16, 4)])
        yield formatted_number
