import pandas as pd

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_operations, process_bank_search
from src.widget import get_date, mask_account_card


def get_valid_choise(text: str, valid_choices: list) -> str:
    while True:
        choise = input(text).strip().lower()
        if choise in valid_choices:
            return choise
        else:
            print(f"Ошибка: допустимые варианты: {', '.join(valid_choices)}.")


def main() -> None:
    """Основная функция приложения"""
    print("""Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")
    user_choice = str(input())
    if user_choice not in ["1", "2", "3"]:
        print("Ошибка ввода. Попробуйте снова.")
        return main()
    else:
        if user_choice == "1":
            print("Для обработки выбран JSON-файл")
        elif user_choice == "2":
            print("Для обработки выбран CSV-файл")
        elif user_choice == "3":
            print("Для обработки выбран XLSX-файл")

    road_for_file = str(input("""Введите путь к файлу.
Например, "../data/operations.json" или нажмите "Enter" для значения пути по умолчанию. """).strip())
    if not road_for_file and user_choice == "1":
        road_for_file = "../data/operations.json"
    elif not road_for_file and user_choice == "2":
        road_for_file = "../data/transactions.csv"
    elif not road_for_file and user_choice == "3":
        road_for_file = "../data/transactions_excel.xlsx"
    database = load_operations(road_for_file)
    return choise_function(database, user_choice)


def choise_function(data: list[dict], user_choice: str) -> None:
    print("""Введите статус, по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED (по умолчанию), CANCELED, PENDING""")
    database = data
    ch_fil = str(input().upper())
    if ch_fil not in ["EXECUTED", "CANCELED", "PENDING", ""]:
        print(f"Статус операции {ch_fil} недоступен.")
        return choise_function(data, user_choice)
    elif not ch_fil:
        ch_fil = "EXECUTED"
        database = filter_by_state(database, ch_fil)
    else:
        database = filter_by_state(database, ch_fil)

    need_sort_date = get_valid_choise("Отсортировать операции по дате? Да(по умолчанию)/Нет ", ["да", "", "нет"])
    if need_sort_date == "да" or not need_sort_date:
        sort_classic = get_valid_choise(
            "Отсортировать по возрастанию(по умолчанию) или по убыванию? ", ["по возрастанию", "", "по убыванию"]
        )
        if sort_classic == "по возрастанию" or not sort_classic:
            database = sort_by_date(database, reverse=False)
        else:
            database = sort_by_date(database)

    sort_for_rub = get_valid_choise("Выводить только рублевые транзакции? Да/Нет(по умолчанию) ", ["да", "", "нет"])
    if sort_for_rub == "да":
        database = list(filter_by_currency(database, "RUB"))

    filt_for_word = get_valid_choise(
        "Отфильтровать список транзакций по определённому слову в описании? Да/Нет(по умолчанию) ", ["да", "", "нет"]
    )
    if filt_for_word == "да":
        filt_word = str(input("Введите слово для фильтрации: "))
        database = process_bank_search(database, filt_word)

    print("Распечатываю итоговый список транзакций...")
    if not database:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковский операций в выборке: {len(database)}")

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

