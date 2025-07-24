import pytest


@pytest.fixture
def records():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 2, "state": "PENDING", "date": "2024-01-09"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-11"},
        {"id": 4, "state": "CANCELLED", "date": "2024-01-08"},
    ]
