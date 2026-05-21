from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_date: str) -> str:
    """Функция принимающая название счёта или карты и
    её номер и маркирующая их, чтобы затем вернуть"""
    input_date = str(input_date).strip()

    if len(input_date) >= 8:
        date_base = input_date.split()
        names_date = " ".join(date_base[:-1])
        numbers_date = date_base[-1]
        if numbers_date.isdigit():
            if "счет" in names_date.lower():
                mask_ = get_mask_account(numbers_date)
            else:
                mask_ = get_mask_card_number(numbers_date)
            return names_date + " " + mask_
        return "Ошибка ввода. Проверьте корректность ввода и повторите попытку"
    return "Ошибка ввода. Проверьте корректность ввода и повторите попытку"


def get_date(date: str) -> str:
    """Функция для получения упрощённой даты из более подробного формата
    исключая тем самым точное время операции"""
    test_date = date.rstrip("Z")
    try:
        date_obj = datetime.fromisoformat(test_date)
        clean_date = date_obj.strftime("%d.%m.%Y")
        return clean_date
    except (ValueError, TypeError):
        return "Ошибка ввода формата даты. Повторите попытку позже"
