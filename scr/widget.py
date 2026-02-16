from scr.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_date: str) -> str:
    """Функция принимающая название счёта или карты и
    её номер и маркирующая их, чтобы затем вернуть"""

    date_base = input_date.split()
    names_date = " ".join(date_base[:-1])
    numbers_date = date_base[-1]
    if "Счет" in names_date:
        mask_ = get_mask_account(numbers_date)
    else:
        mask_ = get_mask_card_number(numbers_date)
    return names_date + " " + mask_


def get_date(date: str) -> str:
    """Функция для получения упрощённой даты из более подробного формата
    исключая тем самым точное время операции"""

    worker_date = date.split("T")
    year, month, day = worker_date[0].split("-")
    return f"{day}.{month}.{year}"
