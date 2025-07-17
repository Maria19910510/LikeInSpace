from src.processing import filter_by_state, sort_by_date
import pytest


@pytest.fixture
def records():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-10"},
        {"id": 2, "state": "PENDING", "date": "2024-01-09"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-11"},
        {"id": 4, "state": "CANCELLED", "date": "2024-01-08"},
    ]

def test_filter_by_state_default():
    # Проверяем правильность работы фильтрации по состоянию по умолчанию
    result = filter_by_state(records)
    assert len(result) == 2, f"Expected 2 records, got {len(result)}"
    for record in result:
        assert record["state"] == "EXECUTED", f"Record state was {record['state']}, expected 'EXECUTED'"

 def test_sort_by_date_default_reverse(self):
     # Проверка, что список отсортирован по убыванию дат
    result = sort_by_date(self.records)
    dates = [record["date"] for record in result]
    self.assertEqual(dates, sorted(dates, reverse=True))

def test_sort_by_date_ascending(self):
    # Проверка, что список отсортирован по возрастанию дат
    result = sort_by_date(self.records, reverse=False)
    dates = [record["date"] for record in result]
    self.assertEqual(dates, sorted(dates))
