from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default(records):
    # Проверяем правильность работы фильтрации по состоянию по умолчанию
    result = filter_by_state(records)
    assert len(result) == 2
    for record in result:
        assert record["state"] == "EXECUTED"


def test_sort_by_date_default_reverse(records):
    # Проверка, что список отсортирован по убыванию дат
    result = sort_by_date(records)
    dates = [record["date"] for record in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(records):
    # Проверка, что список отсортирован по возрастанию дат
    result = sort_by_date(records, reverse=False)
    dates = [record["date"] for record in result]
    assert dates == sorted(dates, reverse=False)
