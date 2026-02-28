from typing import Union


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функция для маркировки номера карты. Сначала она принимает номер в виде строки или набора цифр, затем переводит
    в строку. Отделяет первые шесть и последние четыре числа, остальные маркирует. После с помощью итерации создаёт
    блоки по 4 символа, которые добавляет в список и которые затем преобразуется в строку и выводится наружу"""
    worked_str = str(card_number)
    if " " in worked_str:
        worked_str = worked_str.replace(" ", "")

    if 13 <= len(worked_str) <= 19 and worked_str.isdigit():
        final_mask_card = []

        visible_start = worked_str[:6]
        visible_end = worked_str[-4:]
        mask_numbers = "*" * (len(worked_str) - 10)
        masked_card = visible_start + mask_numbers + visible_end

        for i in range(0, len(masked_card), 4):
            block = masked_card[i : i + 4]
            final_mask_card.append(block)

        result_work = " ".join(final_mask_card)
        return result_work
    return "Ошибка ввода номера карты. Повторите попытку"


def get_mask_account(account_number: Union[int, str]) -> str:
    """функция для маркировки номера счёта, которая выделяет последние четыре цифры и оставляет их видимыми.
    Остальной номер счёта остаётся сокрытым за двумя звёздами"""
    worked_str = str(account_number)
    if " " in worked_str:
        worked_str = worked_str.replace(" ", "")

    if len(worked_str) >= 8 and worked_str.isdigit():
        visible_end = worked_str[-4:]
        masked_account = "**" + visible_end
        return masked_account
    return "Ошибка ввода данных. Повторите попытку снова"
