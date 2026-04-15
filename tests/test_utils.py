from scr.utils import load_operations, operation_conversion_amount


def test_load_operations_empty_road() -> None:
    assert load_operations("") == []


def test_load_operations_incorrect_road() -> None:
    assert load_operations("data/not_file.json") == []


# def test_load_operations_correct_state():
#     result = load_operations("../data/test_operations.json")
#     print(result)
#     assert result == [
#         {
#             "id": 939719570,
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод организации",
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702",
#         },
#         {
#             "id": 142264268,
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878",
#             "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 19708645243227258542",
#             "to": "Счет 75651667383060284188",
#         },
#         {
#             "id": 873106923,
#             "state": "EXECUTED",
#             "date": "2019-03-23T01:09:46.296404",
#             "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 44812258784861134719",
#             "to": "Счет 74489636417521191160",
#         },
#         {
#             "id": 895315941,
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод с карты на карту",
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229",
#         },
#         {
#             "id": 594226727,
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод организации",
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657",
#         },
#     ]


def test_operation_conversion_amount_empty_list(test_empty_list: list) -> None:
    assert operation_conversion_amount(test_empty_list) == []


def test_operation_conversion_amount_incorrect_currency(test_transaction_list_incorrect_currency: list) -> None:
    assert (
        operation_conversion_amount(test_transaction_list_incorrect_currency)
        == "Ошибка обработки операции. Неверный формат валюты"
    )


def test_operation_conversion_amount_without_operation(test_transaction_list_without_operation: list) -> None:
    assert (
        operation_conversion_amount(test_transaction_list_without_operation)
        == "Ошибка обработки операции 939719570. Информация по операции отсутствует"
    )
