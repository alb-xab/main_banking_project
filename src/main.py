import logging

import pandas as pd

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_operations, process_bank_search
from src.widget import get_date, mask_account_card

logger = logging.getLogger("mask")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/mask.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_valid_choise(text: str, valid_choices: list) -> str:
    """Функция для работы с допустимыми вариантами для ввода"""
    logger.info("Начало работы функции выборки")
    while True:
        logger.info("Пользователь вводит значение:")
        choise = input(text).strip().lower()
        logger.info("Проверка допустимости значения")
        if choise in valid_choices:
            logger.info("Значение допустимо. Продолжаем")
            return choise
        else:
            logger.warning("Значение недопустимо. Введите значение заново")
            print(f"Ошибка: допустимые варианты: {', '.join(valid_choices)}.")


def main() -> None:
    """Основная функция приложения"""
    logger.info("Начало работы основной функции приложения и приветствие")
    print("""Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")
    logger.info("Предоставление выбора пользователю")
    user_choice = str(input())
    logger.info("Проверка допустимости выбора пользователя")
    if user_choice not in ["1", "2", "3"]:
        logger.info("Недопустимый выбор. Возврат к началу")
        print("Ошибка ввода. Попробуйте снова.")
        return main()
    else:
        if user_choice == "1":
            logger.info("Пользователь для обработки выбрал JSON-файл")
            print("Для обработки выбран JSON-файл")
        elif user_choice == "2":
            logger.info("Пользователь для обработки выбрал CSV-файл")
            print("Для обработки выбран CSV-файл")
        elif user_choice == "3":
            logger.info("Пользователь для обработки выбрал XLSX-файл")
            print("Для обработки выбран XLSX-файл")
    logger.info("Предоставление пользователю возможности указать путь к файлу или выбора значения по умолчанию")
    road_for_file = str(input("""Введите путь к файлу.
Например, "../data/operations.json" или нажмите "Enter" для значения пути по умолчанию. """).strip())
    if not road_for_file and user_choice == "1":
        logger.info("Выбрано значение по умолчанию")
        road_for_file = "../data/operations.json"
    elif not road_for_file and user_choice == "2":
        logger.info("Выбрано значение по умолчанию")
        road_for_file = "../data/transactions.csv"
    elif not road_for_file and user_choice == "3":
        logger.info("Выбрано значение по умолчанию")
        road_for_file = "../data/transactions_excel.xlsx"
    logger.info("Запуска функции загрузки базы данных из выбранного файла на пути")
    database = load_operations(road_for_file)
    return choise_function(database, user_choice)


def choise_function(data: list[dict], user_choice: str) -> None:
    """Функция для получения структурированной информации по операциям, согласно выбранным фильтрам"""
    logger.info("Начало работы функции для получения структурированной информации")
    print("""Введите статус, по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED (по умолчанию), CANCELED, PENDING""")
    logger.info("Загрузка базы данных и получение от пользователя первого фильтра по статусу")
    database = data
    ch_fil = str(input().upper())
    if ch_fil not in ["EXECUTED", "CANCELED", "PENDING", ""]:
        logger.warning("Пользователь ввёл некорректный вариант. Пусть попробует заново.")
        print(f"Статус операции {ch_fil} недоступен.")
        return choise_function(data, user_choice)
    elif not ch_fil:
        logger.info("Выбрано значение по умолчанию - EXECUTED")
        ch_fil = "EXECUTED"
        database = filter_by_state(database, ch_fil)
    else:
        logger.info(f"Выбрано значение - {ch_fil}. Запуск основного фильтра.")
        database = filter_by_state(database, ch_fil)
    logger.info("Предложение использования первого фильтра.")
    need_sort_date = get_valid_choise("Отсортировать операции по дате? Да(по умолчанию)/Нет ", ["да", "", "нет"])
    if need_sort_date == "да" or not need_sort_date:
        logger.info("Пользователь выбрал фильтрацию по дате. Уточнение реверсии.")
        sort_classic = get_valid_choise(
            "Отсортировать по возрастанию(по умолчанию) или по убыванию? ", ["по возрастанию", "", "по убыванию"]
        )
        if sort_classic == "по возрастанию" or not sort_classic:
            logger.info("Выбрана фильтрация по дате по возрастанию")
            database = sort_by_date(database, reverse=False)
        else:
            logger.info("Выбрана фильтрация по дате по убыванию")
            database = sort_by_date(database)
    logger.info("Предложение второй фильтрации на рублевые транзакции у пользователя.")
    sort_for_rub = get_valid_choise("Выводить только рублевые транзакции? Да/Нет(по умолчанию) ", ["да", "", "нет"])
    if sort_for_rub == "да":
        logger.info("Активация второго фильтра на рублевые транзакции")
        database = list(filter_by_currency(database, "RUB"))
    logger.info("Предложение третьей фильтрации по определённому слову в описании.")
    filt_for_word = get_valid_choise(
        "Отфильтровать список транзакций по определённому слову в описании? Да/Нет(по умолчанию) ", ["да", "", "нет"]
    )
    if filt_for_word == "да":
        logger.info("Пользователь выбрал фильтрацию по слову")
        filt_word = str(input("Введите слово для фильтрации: "))
        logger.info(f"Запуск фильтрации по слову {filt_word}")
        database = process_bank_search(database, filt_word)
    logger.info("Завершение всех фильтраций. Выдача списка транзакций")
    print("Распечатываю итоговый список транзакций...")
    if not database:
        logger.info("Нет подходящих транзакций")
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    logger.info("Печать общего количества транзакций")
    print(f"Всего банковский операций в выборке: {len(database)}")
    logger.info("Печать всех транзакций в финальном списке")
    if user_choice == "1":
        for operation in database:
            date = get_date(operation["date"])
            description = operation.get("description", "")
            amount = float(operation["operationAmount"]["amount"])
            amount = int(amount)
            currency = operation["operationAmount"]["currency"]["name"]
            if "from" in operation and "to" in operation:
                from_data = mask_account_card(operation["from"])
                to_data = mask_account_card(operation["to"])

                print(f"""{date} {description}
{from_data} -> {to_data}
Сумма: {amount} {currency}
""")
            else:
                to_data = mask_account_card(operation["to"])
                print(f"""{date} {description}
{to_data}
Сумма: {amount} {currency}
""")
    elif user_choice == "2" or user_choice == "3":
        for operation in database:
            date = get_date(operation["date"])
            description = operation.get("description", "")
            amount = int(operation["amount"])
            currency = operation["currency_name"]
            if "from" in operation and not pd.isna(operation["from"]) and "to" in operation:
                from_data = mask_account_card(operation["from"])
                to_data = mask_account_card(operation["to"])
                print(f"""{date} {description}
{from_data} -> {to_data}
Сумма: {amount} {currency}
""")
            else:
                to_data = mask_account_card(operation["to"])
                print(f"""{date} {description}
{to_data}
Сумма: {amount} {currency}
""")
