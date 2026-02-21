def filter_by_state(work_list: list, state: str = "EXECUTED") -> list:
    """Функция для фильтрации списка словарей по ключу"""
    filtered_list = []
    for i in work_list:
        if i["state"] == state:
            filtered_list.append(i)
    return filtered_list


def sort_by_date(work_list: list, reverse: bool = True) -> list:
    """Функция для сортировки списка по дате"""
    filtered_list = sorted(work_list, key=lambda x: x["date"], reverse=reverse)
    return filtered_list
