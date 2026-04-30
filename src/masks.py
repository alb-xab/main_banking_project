import logging
from typing import Union

logger = logging.getLogger("mask")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/mask.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """Функция для маркировки номера карты. Сначала она принимает номер в виде строки или набора цифр, затем переводит
    в строку. Отделяет первые шесть и последние четыре числа, остальные маркирует. После с помощью итерации создаёт
    блоки по 4 символа, которые добавляет в список и которые затем преобразуется в строку и выводится наружу"""
    logger.info('Начало работы функции для маркировки номера карты.')
    worked_str = str(card_number)
    logger.info("Проверяем корректность введённого номера карты.")
    if " " in worked_str:
        worked_str = worked_str.replace(" ", "")

    if 13 <= len(worked_str) <= 19 and worked_str.isdigit():
        logger.info("Номер введёт корректно. Приступаем к маркировке номера карты.")
        final_mask_card = []

        visible_start = worked_str[:6]
        visible_end = worked_str[-4:]
        mask_numbers = "*" * (len(worked_str) - 10)
        masked_card = visible_start + mask_numbers + visible_end

        for i in range(0, len(masked_card), 4):
            block = masked_card[i : i + 4]
            final_mask_card.append(block)

        result_work = " ".join(final_mask_card)
        logger.info("Маркировка проведена успешно.")
        return result_work
    logger.warning("Ошибка ввода номера карты. Повторите попытку.")
    return ""


def get_mask_account(account_number: Union[int, str]) -> str:
    """функция для маркировки номера счёта, которая выделяет последние четыре цифры и оставляет их видимыми.
    Остальной номер счёта остаётся сокрытым за двумя звёздами"""
    logger.info('Начало работы функции для маркировки номера счёта')
    worked_str = str(account_number)
    logger.info("Проверяем корректность введённого номера счёта")
    if " " in worked_str:
        worked_str = worked_str.replace(" ", "")

    if len(worked_str) >= 8 and worked_str.isdigit():
        logger.info("Номер введёт корректно. Приступаем к маркировке номера счёта")
        visible_end = worked_str[-4:]
        masked_account = "**" + visible_end
        logger.info("Маркировка проведена успешно")
        return masked_account
    logger.info("Ошибка ввода данных. Повторите попытку снова")
    return ""
