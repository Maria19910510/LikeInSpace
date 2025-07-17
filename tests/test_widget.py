from src.widget import mask_account_card
import pytest


@pytest.fixture(autouse=True)
def patch_get_mask_card_number(monkeypatch):
    monkeypatch.setattr('src.masks.get_mask_card_number', mock_get_mask_card_number)

def test_mask_account_card_with_schet():
    # тест для счета
    result = mask_account_card("Счет 408178105123456789")
    assert result == "Счет **6789"

def test_mask_account_card_with_card():
    # тест для номера карты
    card_info = "Мастеркард Gold 1234 5678 9012 3456"
    result = mask_account_card(card_info)
    # В результате должно быть название + маскированный номер
    assert result.startswith("Мастеркард Gold")
    # проверяем, что последние 4 цифры есть
    assert result.endswith("3456")

def test_mask_account_card_without_spaces():
    # тест для строки без лишних пробелов
    card_info = "Виза  9876 5432 1098 7654"
    result = mask_account_card(card_info)
    assert result.startswith("Виза")
    assert result.endswith("7654")

def test_get_date():
    # тест для преобразования даты
    date_str = "2023-10-05"
    result = get_date(date_str)
    assert result == "05.10.2023"

def test_get_date_with_short_year():
    # тест, когда год трехзначный (например, 2023-10-05)
    date_str = "2023-12-01"
    result = get_date(date_str)
    assert result == "01.12.2023"
