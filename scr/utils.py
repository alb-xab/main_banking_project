import json
import os.path

from scr.external_api import conversion_amount


def load_operations(road_to_file: str) -> list[dict]:
    """Функция загрузки данных о финансовых операциях с базы данных"""
    if not os.path.exists(road_to_file):
        return []
    try:
        with open(road_to_file, "r", encoding="utf-8") as file:
            database = json.load(file)
            if not database:
                return []
            if isinstance(database, list):
                return database
            else:
                return []

    except json.JSONDecodeError:
        return []


def operation_conversion_amount(list_of_operations: list[dict]) -> None | float | str:
    "Функция для получения данных об операциях"

    result = []
    for operation in list_of_operations:
        try:
            if not operation["operationAmount"]:
                return "Ошибка обработки операции. Информация по операции отсутствует"
            if operation["operationAmount"]["currency"]["code"] == "RUB":
                result = operation["operationAmount"]["amount"]

            elif (
                operation["operationAmount"]["currency"]["code"] == "USD"
                or operation["operationAmount"]["currency"]["code"] == "EUR"
            ):
                amount = float(operation["operationAmount"]["amount"])
                currency_from = str(operation["operationAmount"]["currency"]["code"])
                result = conversion_amount(amount, currency_from)

            else:
                result = "Ошибка обработки операции. Неверный формат валюты"
            return result
        except (ValueError, KeyError):
            result = f"Ошибка обработки операции {operation.get('id')}. Информация по операции отсутствует"
    return result
