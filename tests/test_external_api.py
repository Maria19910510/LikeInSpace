from unittest.mock import Mock, patch
import requests
from src.external_api import convert_to_rub, get_exchange_rate


# Тест для get_exchange_rate
@patch("requests.get")
def test_get_exchange_rate_success(mock_get):
    # Мокаем ответ API
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")
    assert rate == 75.5
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": None},
        params={"base": "USD", "symbols": "RUB"},
        timeout=10,
    )


@patch("requests.get")
def test_get_exchange_rate_failure_response(mock_get):
    # Имитация исключения при запросе
    mock_get.side_effect = requests.RequestException
    rate = get_exchange_rate("USD")
    assert rate is None


@patch("requests.get")
def test_get_exchange_rate_missing_rate(mock_get):
    # Ответ без ключа 'rates' или без 'RUB'
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"rates": {}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")
    assert rate is None


# Тест для convert_to_rub
@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_usd_success(mock_get_rate):
    mock_get_rate.return_value = 70.0
    amount = 10
    currency = "USD"
    result = convert_to_rub(amount, currency)
    assert result == amount * 70.0


@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_usd_fail(mock_get_rate):
    mock_get_rate.return_value = None
    amount = 10
    currency = "USD"
    result = convert_to_rub(amount, currency)
    # При ошибке возвращается исходная сумма
    assert result == amount


def test_convert_to_rub_rub():
    amount = 100
    currency = "RUB"
    result = convert_to_rub(amount, currency)
    assert result == amount


def test_convert_to_rub_other_currency():
    amount = 50
    currency = "GBP"
    result = convert_to_rub(amount, currency)
    # Для других валют просто возвращается сумма
    assert result == amount
