from typing import Any, Dict, List, Union


def filter_by_state(records: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Принимает список словарей и опционально значение"""
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: List[Dict[str, Union[str, Any]]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию — убывание)"""
    return sorted(records, key=lambda x: x.get("date", ""), reverse=reverse)
