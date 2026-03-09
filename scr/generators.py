import random


def filter_by_currency(transactions: list, currency: str = "USD"):
    """Функция фильтрации словарей списка и поочередного получения словарей с указанной валютой."""
    if not transactions:
        return []
    for transaction in transactions:
        if (isinstance(transaction, dict) and "operationAmount" in transaction
            and 'currency' in transaction['operationAmount']
            and 'code' in transaction['operationAmount']['currency']
            and transaction['operationAmount']["currency"]["code"] == currency):
            yield transaction


def transaction_descriptions(
    transactions: list,
):
    """Функция генератора, который возвращает описание произведённых операций в списке словарей"""
    for transaction in transactions:
        if transaction is dict and "description" in transaction:
            yield transaction["description"]



def card_number_generator(start: int = 1, stop: int = 9999999999999999):
    """Функция для случайной генерации номера карты в 16-символьном формате
    с заданными начальными и конечными рамками"""
    final_number_card = []
    card_number = random.randint(start, stop)
    card_string = f"{card_number:016d}"

    for i in range(0, len(card_string), 4):
        block = card_string[i : i + 4]
        final_number_card.append(block)

    result = " ".join(final_number_card)
    return result
