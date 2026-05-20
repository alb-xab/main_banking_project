import json
import logging
import os.path
import re
from collections import Counter
from typing import Any, Dict, List, Optional

import pandas as pd

from src.external_api import conversion_amount

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_operations(road_to_file: str) -> list[dict]:
    """
    Функция загрузки данных о финансовых операциях из файлов расширений JSON, CSV, XLSX.
    """
    logger.info("Запуск функции загрузки финансовых операций.")
    logger.info("Проверка корректного ввода пути.")

    if not os.path.exists(road_to_file):
        logger.warning("Ошибка. Не найден файл. Проверьте корректность введённого пути.")
        return []

    root, ext = os.path.splitext(road_to_file)
    ext = ext.lower()

    try:
        logger.info(f"Попытка загрузки данных из файла: {road_to_file}")

        if ext == ".json":
            with open(road_to_file, "r", encoding="utf-8") as file:
                database = json.load(file)
                if not database:
                    logger.warning("База данных пуста.")
                    return []
                if isinstance(database, list):
                    logger.info("Загрузка JSON-файла успешна.")
                    return database
                else:
                    logger.warning("Некорректный формат данных в JSON-файле: ожидается список.")
                    return []

        elif ext in (".csv", ".xlsx"):
            if ext == ".csv":
                df = pd.read_csv(road_to_file)
            else:
                df = pd.read_excel(road_to_file, engine="openpyxl")
            if df.empty:
                logger.warning("Файл содержит пустые данные.")
                return []
            return df.to_dict(orient="records")

        else:
            logger.warning(f"Неподдерживаемый формат файла: {ext}. Поддерживаемые форматы: .json, .csv, .xls, .xlsx.")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON-файла {road_to_file}: {e}")
        return []
    except pd.errors.EmptyDataError:
        logger.warning(f"Файл {road_to_file} содержит пустые данные.")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга файла {road_to_file}: {e}")
        return []
    except PermissionError:
        logger.error(f"Нет доступа к файлу {road_to_file}. Проверьте права доступа.")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {road_to_file}: {type(e).__name__}: {e}")
        return []


def operation_conversion_amount(list_of_operations: List[Dict[str, Any]]) -> List[Optional[float]]:
    """
    Функция для получения данных об операциях с конвертацией в RUB.
    """
    results: List[Optional[float]] = []
    logger.info(f"Начало работы функции. Всего операций: {len(list_of_operations)}")

    for i, operation in enumerate(list_of_operations):
        operation_id = operation.get("id", f"index_{i}")
        try:
            operation_amount = operation.get("operationAmount")
            if not operation_amount:
                logger.warning(f"Операция {operation_id}: отсутствует поле 'operationAmount'")
                results.append(None)
                continue

            currency_data = operation_amount.get("currency")
            if not currency_data:
                logger.warning(f"Операция {operation_id}: отсутствует поле 'currency'")
                results.append(None)
                continue

            currency_code = currency_data.get("code")
            if not currency_code:
                logger.warning(f"Операция {operation_id}: отсутствует код валюты")
                results.append(None)
                continue

            amount_str = operation_amount.get("amount")
            if amount_str is None:
                logger.warning(f"Операция {operation_id}: отсутствует сумма операции")
                results.append(None)
                continue

            try:
                amount = float(amount_str)
            except ValueError:
                logger.error(f"Операция {operation_id}: не удалось преобразовать сумму '{amount_str}' в число")
                results.append(None)
                continue

            if currency_code == "RUB":
                logger.debug(f"Операция {operation_id}: валюта RUB, сумма сохраняется без изменений: {amount}")
                results.append(amount)
            elif currency_code in ("USD", "EUR"):
                logger.info(f"Операция {operation_id}: конвертация {amount} {currency_code} в RUB")
                converted_amount = conversion_amount(amount, currency_code)
                results.append(converted_amount)
                logger.debug(f"Операция {operation_id}: конвертация завершена, результат: {converted_amount}")
            else:
                logger.warning(f"Операция {operation_id}: неподдерживаемая валюта {currency_code}")
                results.append(None)
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке операции {operation_id}: {e}")
            results.append(None)

    logger.info(f"Завершение работы функции. Обработано операций: {len(results)}")
    return results


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция для поиска нужных операций по ключу в базе данных и получению нового списка подходящих операций"""
    new_data = []
    pattern_for_search = re.compile(re.escape(search))

    def internal_search(obj: Any) -> Any:
        if obj is None:
            return False
        elif isinstance(obj, str) and pattern_for_search.search(obj):
            return True
        elif isinstance(obj, int | float) and pattern_for_search.search(str(obj)):
            return True
        elif isinstance(obj, list):
            return any(internal_search(item) for item in obj)
        elif isinstance(obj, dict):
            return any(internal_search(item) for item in obj.values())
        else:
            return bool(pattern_for_search.search(str(obj)))

    for operation in data:
        if internal_search(operation):
            new_data.append(operation)
    return new_data


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Функция для каталлогирования операций по переданным категориям"""
    category_counter = Counter()

    for operation in data:
        if "description" not in operation:
            continue

        description = operation["description"]

        for category in categories:
            if category.lower() in description.lower():
                category_counter[category] += 1
                break

    return dict(category_counter)
