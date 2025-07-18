from typing import Any, Dict, List

import pytest


@pytest.fixture
def records() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 2, "state": "PENDING", "date": "2024-01-09"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-11"},
        {"id": 4, "state": "CANCELLED", "date": "2024-01-08"},
    ]


@pytest.fixture
def sample_records() -> List[Dict[str, Any]]:
    return [
        {"date": "2023-10-10", "state": "EXECUTED", "amount": 100},
        {"date": "2023-09-09", "state": "PENDING", "amount": 200},
        {"date": "2023-10-05", "state": "EXECUTED", "amount": 300},
        {"date": "2023-08-15", "state": "CANCELLED", "amount": 150},
    ]


@pytest.fixture
def valid_card_info_account() -> str:
    return "Счет 1234567890123456"


@pytest.fixture
def valid_card_info_card() -> str:
    return "Visa Platinum 1234567890123456"


@pytest.fixture
def date_str() -> str:
    return "2023-12-31"
