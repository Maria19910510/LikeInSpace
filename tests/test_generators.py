from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_matches():
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "USD"}}}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    for transaction in result:
        assert transaction["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_matches():
    transactions = [
        {"operationAmount": {"currency": {"code": "EUR"}}},
        {"operationAmount": {"currency": {"code": "JPY"}}}
    ]
    assert list(filter_by_currency(transactions, "USD")) == []


def test_transaction_descriptions_known_types():
    transactions = [
        {"type": "transfer_org"},
        {"type": "transfer_account"},
        {"type": "transfer_card"},
        {"type": "transfer_person"},
    ]
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод физическому лицу",
    ]


def test_transaction_descriptions_unknown_type():
    transactions = [{"type": "неизвестный"}]
    result = list(transaction_descriptions(transactions))
    assert result == ["Описание операции неизвестно"]


def test_transaction_descriptions_missing_type():
    transactions = [{}]
    result = list(transaction_descriptions(transactions))
    assert result == ["Описание операции неизвестно"]


def test_card_number_generator_format():
    gen = card_number_generator(0, 2)
    output = list(gen)
    assert output == [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002"
    ]


def test_card_number_generator_range():
    start = 12345
    end = 12350
    gen = card_number_generator(start, end)
    numbers = list(gen)
    for i, num_str in enumerate(numbers, start=start):
        expected_num_str = f"{i:016d}"
        expected_formatted = " ".join([expected_num_str[j:j + 4] for j in range(0, 16, 4)])
        assert num_str == expected_formatted


def test_card_number_generator_empty_range():
    gen = card_number_generator(5, 4)
    assert list(gen) == []
