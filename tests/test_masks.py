from src.masks import get_mask_card_number, get_mask_account
import pytest


def test_get_mask_card_number_valid():
    card_number = "1234 5678 9012 3456"
    masked = get_mask_card_number(card_number)
    assert masked == "1234 56** **** 3456"


def test_get_mask_card_number_short():
    with pytest.raises(ValueError):
        get_mask_card_number("123456789")  # менее 10 символов


def test_get_mask_card_number_format():
    card_number = "9876543210987654"
    masked = get_mask_card_number(card_number)
    assert masked == "9876 54** **** 7654"


def test_get_mask_account_valid():
    account_number = "1234567890"
    masked = get_mask_account(account_number)
    assert masked == "**7890"


def test_get_mask_account_short():
    with pytest.raises(ValueError):
        get_mask_account("123")  # менее 4 символов