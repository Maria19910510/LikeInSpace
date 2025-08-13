import json
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.
    Возвращает пустой список, если файл отсутствует, пустой, не список или содержит некорректные данные"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
