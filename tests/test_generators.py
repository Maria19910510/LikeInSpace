import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency_code, expected_ids",
    [
        ("USD", [939719570, 895315941]),
        ("RUB", [873106923]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(sample_transactions_with_type, currency_code, expected_ids):
    filtered = list(filter_by_currency(sample_transactions_with_type, currency_code))
    filtered_ids = [tx["id"] for tx in filtered]
    assert filtered_ids == expected_ids


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "USD")) == []


def test_transaction_descriptions(sample_transactions_with_type):
    descriptions = list(transaction_descriptions(sample_transactions_with_type))
    expected_descriptions = ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]
    assert descriptions == expected_descriptions


def test_card_number_generator_range():
    gen = card_number_generator(6800000000000000, 6800000000000005)
    generated_numbers = list(gen)
    expected_numbers = [
        "6800 0000 0000 0000",
        "6800 0000 0000 0001",
        "6800 0000 0000 0002",
        "6800 0000 0000 0003",
        "6800 0000 0000 0004",
        "6800 0000 0000 0005",
    ]
    assert generated_numbers == expected_numbers


def test_card_number_format():
    gen = card_number_generator(6800000000000000, 6800000000000000)
    number = next(gen)
    assert number == "6800 0000 0000 0000"
    assert len(number) == 19  # 16 цифр + 3 пробела


def test_card_number_generator_end():
    gen = card_number_generator(6800000000000000, 6800000000000002)
    results = [next(gen) for _ in range(3)]
    expected = ["6800 0000 0000 0000", "6800 0000 0000 0001", "6800 0000 0000 0002"]
    assert results == expected
