import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture(autouse=True)
def disable_logging(monkeypatch):
    # Заменяем setup_module_logger, чтобы он ничего не делал
    monkeypatch.setattr('src.logger_config.setup_module_logger', lambda module_name: None)


def test_get_mask_card_number_1():
    card_number = "1234567890123456"
    masked = get_mask_card_number(card_number)
    assert masked == "1234 56** **** 3456"


def test_get_mask_card_number_2():
    # Проверка на менее 16 символов, должно подняться исключение
    with pytest.raises(ValueError):
        get_mask_card_number("123456789")  # короче 16 символов


def test_get_mask_card_number_3():
    card_number = "9876543210987654"
    masked = get_mask_card_number(card_number)
    assert masked == "9876 54** **** 7654"


def test_get_mask_account_1():
    account_number = "1234567890"
    masked = get_mask_account(account_number)
    assert masked == "**7890"


def test_get_mask_account_2():
    # Проверка на менее 4 символов
    with pytest.raises(ValueError):
        get_mask_account("123")  # короче 4 символов


@pytest.mark.parametrize(
    "card_number, expected_masked",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210987654", "9876 54** **** 7654"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_param(card_number, expected_masked):
    assert get_mask_card_number(card_number) == expected_masked


@pytest.mark.parametrize(
    "account_number, expected_masked",
    [
        ("1234", "**1234"),
        ("987654321", "**4321"),
        ("00000001", "**0001"),
    ],
)
def test_get_mask_account_param(account_number, expected_masked):
    assert get_mask_account(account_number) == expected_masked
