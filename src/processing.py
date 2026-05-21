from datetime import datetime


def filter_by_state(work_list: list, state: str = "EXECUTED") -> list[dict]:
    """Функция для фильтрации списка словарей по ключу"""
    filtered_list = []
    for item in work_list:
        if item.get("state") == state:
            filtered_list.append(item)
    if not filtered_list:
        return filtered_list
    return filtered_list


def sort_by_date(work_list: list, reverse: bool = True) -> list:
    return sorted(
        work_list,
        key=lambda x: datetime.fromisoformat(x["date"].rstrip("Z")),
        reverse=reverse,
    )
