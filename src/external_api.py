import os
from typing import Union
import requests

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_TOKEN = os.getenv("EXCHANGE_API_KEY")


def get_exchange_rate(currency: str) -> Union[float, None]:
    """Получает текущий курс обмена для указанной валюты по отношению к рублю.
        Возвращает курс или None при ошибке"""
    headers = {
        "apikey": API_TOKEN
    }
    params = {
        "base": currency,
        "symbols": "RUB"
    }
    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data: dict = response.json()
        rate = data['rates'].get("RUB")
        if isinstance(rate, (float, int)):
            return float(rate)
        else:
            return None
    except (requests.RequestException, KeyError):
        return None


def convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму из указанной валюты в рубли.
       Если валюта USD или EUR, обращается к API. Для RUB возвращает исходную сумму"""
    if currency == "RUB":
        return amount
    elif currency in ["USD", "EUR"]:
        rate = get_exchange_rate(currency)
        if rate:
            return amount * rate
        else:
            return amount
    else:
        # Для других валют можно оставить без конвертации или обрабатывать отдельно
        return amount
