import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected, expected_2",
    [
        (
            "USD",
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
        ),
        (
            "RUB",
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160",
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657",
            },
        ),
    ],
)
def test_filter_by_currency_basic(
    test_transaction_list: list, currency: str, expected: dict, expected_2: dict
) -> None:
    test_gen_basic = filter_by_currency(test_transaction_list, currency)
    assert next(test_gen_basic) == expected
    assert next(test_gen_basic) == expected_2


def test_filter_by_currency_basic_3(test_transaction_list: list[dict]) -> None:
    test_gen_basic_3 = filter_by_currency(test_transaction_list, "EUR")
    assert next(test_gen_basic_3, None) is None


def test_filter_by_currency_empty(test_empty_list: list[dict]) -> None:
    assert next(filter_by_currency(test_empty_list), None) is None


@pytest.mark.parametrize(
    "expected_1, expected_2, expected_3",
    [("Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет")],
)
def test_transaction_descriptions_basic(
    test_transaction_list: list[dict], expected_1: str, expected_2: str, expected_3: str
) -> None:
    test_trans_des_basic = transaction_descriptions(test_transaction_list)
    assert next(test_trans_des_basic) == expected_1
    assert next(test_trans_des_basic) == expected_2
    assert next(test_trans_des_basic) == expected_3


def test_transaction_descriptions_empty(test_empty_list: list) -> None:
    test_trans_des_empty = transaction_descriptions(test_empty_list)
    assert next(test_trans_des_empty, None) is None


@pytest.mark.parametrize(
    "start, stop, expected",
    [(1, 1, "0000 0000 0000 0001"), (5000000000000000, 5000000000000000, "5000 0000 0000 0000")],
)
def test_card_number_generator_basic(start: int, stop: int, expected: str) -> None:
    test_card_basic = card_number_generator(start, stop)
    assert test_card_basic == expected
