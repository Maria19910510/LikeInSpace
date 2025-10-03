import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Возвращает список операций, у которых в поле 'description' есть строка search.
    Поиск осуществляется с помощью регулярных выражений."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)  # Игнорируем регистр
    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if description is None:
            description = ""
        if pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по категориям, основываясь на поле 'description'.
    Возвращает словарь {категория: число операций}"""
    counts = {category: 0 for category in categories}
    for transaction in data:
        description = transaction.get("description", "")
        if description is None:
            description = ""
        for category in categories:
            pattern = re.compile(r"\b" + re.escape(category) + r"\b", re.IGNORECASE)
            if pattern.search(description):
                counts[category] += 1
                break  # Предположим, одна операция относится к одной категории
    return counts
