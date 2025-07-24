from typing import List, Dict, Iterable


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterable:
    """Возвращает итератор транзакций с указанной валютой"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction
