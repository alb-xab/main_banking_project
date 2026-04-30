import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def conversion_amount(amount: float, currency_from: str, currency_to: str = "RUB") -> float:
    """Функция для конвертации суммы переводов с иностранной валюты на другую.
    Стандартная итоговая валюта установлена рубль"""

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency_to}&from={currency_from}&amount={amount}"

    payload: list = []

    api_key = os.getenv("API_KEY_CONVERSION")
    if not api_key:
        raise ValueError("API key отсутствует.")
    if not amount and not currency_from:
        raise ValueError("Переданные данные пустые")

    headers = {"apikey": api_key}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = json.loads(response.text)
    return float(result["result"])
