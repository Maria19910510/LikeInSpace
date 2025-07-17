from src.masks import get_mask_card_number, get_mask_account
import pytest


def test_get_mask_card_number_1():
    card_number = "1234567890123456"
    masked = get_mask_card_number(card_number)
    assert masked == "1234 56** **** 3456"


def test_get_mask_card_number_2():
    # Проверка на менее 10 символов
    with pytest.raises(ValueError):
        get_mask_card_number("123456789")


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
        get_mask_account("123")
