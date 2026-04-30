import json
import logging
import os.path
from typing import Any

from src.external_api import conversion_amount

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_operations(road_to_file: str) -> list[dict]:
    """Функция загрузки данных о финансовых операциях с базы данных"""
    logger.info("Запуск функции загрузки финансовых операций.")
    logger.info("Проверка корректного ввода пути.")
    if not os.path.exists(road_to_file):
        logger.warning("Ошибка. Не найден файл. Проверьте корректность введённого пути")
        return []
    try:
        logger.info("Попытка загрузки данных с базы данных.")
        with open(road_to_file, "r", encoding="utf-8") as file:
            database = json.load(file)
            if not database:
                logger.warning("База данных пуста")
                return []
            if isinstance(database, list):
                logger.info("Загрузка успешна.")
                return database
            else:
                logger.warning("Некорректный формат данных в файле")
                return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка: {e}.")
        return []


def operation_conversion_amount(list_of_operations: list[dict]) -> Any:
    """Функция для получения данных об операциях"""
    result = ""
    logger.info("Начало работы функции для получения данных об операциях")
    logger.info("Начинаем перебор")
    for operation in list_of_operations:
        try:
            if not operation["operationAmount"]:
                logger.warning("Ошибка обработки операции. Информация по операции отсутствует")
                return "Ошибка обработки операции. Информация по операции отсутствует"
            if operation["operationAmount"]["currency"]["code"] == "RUB":
                logger.info("Валюта операции RUB. Пропускаем.")
                result = operation["operationAmount"]["amount"]

            elif (
                operation["operationAmount"]["currency"]["code"] == "USD"
                or operation["operationAmount"]["currency"]["code"] == "EUR"
            ):
                logger.info(
                    f'Операция загружена с валютой {operation["operationAmount"]["currency"]["code"]}. '
                    f"Начинаю конвертацию"
                )
                amount = float(operation["operationAmount"]["amount"])
                currency_from = str(operation["operationAmount"]["currency"]["code"])
                result = conversion_amount(amount, currency_from)
                logger.info("Конвертация завершена")
            else:
                logger.info("Ошибка обработки операции. Неверный формат валюты")
                result = None
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Ошибка обработки операции {operation.get('id')}. Ошибка: {e}")
            result = f"Ошибка обработки операции {operation.get('id')}. Информация по операции отсутствует"
    logger.info("Завершение работы программы")
    return result
