from src.generators import filter_by_currency, transaction_descriptions
from src.processing import sort_by_date, filter_by_state
from src.utils import load_operations, process_bank_search
from src.widget import get_date, mask_account_card

def get_valid_choise(text, valid_choices):
    while True:
        choise = input(text).strip().lower()
        if choise in valid_choices:
            return choise
        else:
            print(f"Ошибка: допустимые варианты: {', '.join(valid_choices)}.")

def main():
    """Основная функция приложения"""
    print("""Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")
    user_choice = str(input())
    if user_choice != "1" or user_choice != "2" or user_choice != "3":
        print("Ошибка ввода. Попробуйте снова.")
        main()
    else:
        if user_choice == "1":
            print("Для обработки выбран JSON-файл")
        elif user_choice == "2":
            print("Для обработки выбран CSV-файл")
        elif user_choice == "3":
            print("Для обработки выбран XLSX-файл")

    road_for_file = input("Введите путь до файла:")
    database = load_operations(road_for_file)
    return choise_function(database, user_choice)


def choise_function(data, user_choice):
    print("""Введите статус, по которому необходимо выполнить фильтрацию.
    Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""")
    database = data
    ch_fil = input().upper()
    if ch_fil != "EXECUTED" or ch_fil != "CANCELED" or ch_fil != "PENDING":
        print(f"Статус операции {ch_fil} недоступен.")
        choise_function(data)
    else:
        database = filter_by_state(database, ch_fil)

    need_sort_date = get_valid_choise("Отсортировать операции по дате? Да/Нет", ["да", "нет"])

    sort_for_rub = get_valid_choise("Выводить только рублевые транзакции? Да/Нет", ["да", "нет"])

    filt_for_word = get_valid_choise(
        "Отфильтровать список транзакций по определённому слову в описании? Да/Нет", ["да", "нет"]
    )

    if need_sort_date == "да":
        sort_classic = get_valid_choise(
            "Отсортировать по возрастанию или по убыванию?", ["по возрастанию", "по убыванию"]
        )
        if sort_classic == "по возрастанию":
            database = sort_by_date(database, reverse=False)
        else:
            database = sort_by_date(database)

    if sort_for_rub == "да":
        database = filter_by_currency(database, "RUB")

    if filt_for_word == "да":
        filt_word = str(input("Введите слово для фильтрации: "))
        database = process_bank_search(database, filt_word)

    print("Распечатываю итоговый список транзакций...")

    if user_choice == "1":
        for operation in database:
            date = get_date(operation["date"])
            description = transaction_descriptions(database)
            amount = int(operation["operationAmount"]["amount"])
            if "from" in operation and "to" in operation:
                from_data = mask_account_card(operation["from"])
                to_data = mask_account_card(operation["to"])
                print(f""" {date} {description}
                    {from_data} -> {to_data}
                    Сумма: {amount}
                    """)
            else:
                to_data = mask_account_card(operation["to"])
                print(f""" {date} {description}
                    {to_data}
                    Сумма: {amount}
                    """)
    elif user_choice == "2" or user_choice == "3":
        for operation in database:
            date = get_date(operation["date"])
            description = transaction_descriptions(database)
            amount = int(operation["amount"])
            if "from" in operation and "to" in operation:
                from_data = mask_account_card(operation["from"])
                to_data = mask_account_card(operation["to"])
                print(f""" {date} {description}
                                    {from_data} -> {to_data}
                                    Сумма: {amount}
                                    """)
            else:
                to_data = mask_account_card(operation["to"])
                print(f""" {date} {description}
                                    {to_data}
                                    Сумма: {amount}
                                    """)



