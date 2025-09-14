import json
from typing import Any, Dict, List

from src.logger_config import setup_module_logger

logger = setup_module_logger(__name__)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список транзакций из JSON-файла.
        Возвращает пустой список, если файл отсутствует, пустой, не список или содержит некорректные данные"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            logger.info(f"Загружено {len(data)} транзакций из {file_path}")
            return data
        else:
            logger.warning(f"Некорректные данные в {file_path}")
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при загрузке файла {file_path}: {e}")
        return []
