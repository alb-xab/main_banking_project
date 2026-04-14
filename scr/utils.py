import json
import os.path
from typing import Any


def read_operations(road_to_file: str) -> None | list[Any] | list:
    """Функция загрузки данных о финансовых операциях с базы данных"""
    if not os.path.exists(road_to_file):
        return []
    try:
        with open(road_to_file, "r", encoding="utf-8") as file:
            database = json.load(file)
        if isinstance(database, list):
            return database
        else:
            return []

    except json.JSONDecodeError:
        print("Invalid JSON data.")


roads_to_file = "../data/operations.json"
result = read_operations(roads_to_file)
print(result)
