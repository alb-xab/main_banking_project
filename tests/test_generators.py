import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_basic(test_transaction_list: list[dict]) -> None:
    gen = filter_by_currency(test_transaction_list, "USD")
    first = next(gen)
    second = next(gen)
    three = next(gen)

    assert first["operationAmount"]["currency"]["code"] == "USD"
    assert second["operationAmount"]["currency"]["code"] == "USD"
    assert three["operationAmount"]["currency"]["code"] == "USD"
    assert next(gen, None) is None


def test_filter_by_currency_currency_code_branch() -> None:
    transactions = [
        {"currency_code": "USD", "description": "test"},
        {"currency_code": "EUR", "description": "test2"},
    ]

    gen = filter_by_currency(transactions, "USD")
    assert next(gen) == {"currency_code": "USD", "description": "test"}
    assert next(gen, None) is None


def test_filter_by_currency_no_matches(test_transaction_list: list[dict]) -> None:
    assert next(filter_by_currency(test_transaction_list, "EUR"), None) is None


def test_filter_by_currency_empty(test_empty_list: list[dict]) -> None:
    assert next(filter_by_currency(test_empty_list), None) is None


def test_transaction_descriptions_basic(test_transaction_list: list[dict]) -> None:
    gen = transaction_descriptions(test_transaction_list)
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Перевод с карты на карту"
    assert next(gen) == "Перевод организации"


def test_transaction_descriptions_ignores_missing_description() -> None:
    transactions = [
        {"id": 1, "description": "Первое"},
        {"id": 2},
        {"id": 3, "description": "Третье"},
    ]

    gen = transaction_descriptions(transactions)
    assert next(gen) == "Первое"
    assert next(gen) == "Третье"
    assert next(gen, None) is None


def test_transaction_descriptions_empty(test_empty_list: list) -> None:
    assert next(transaction_descriptions(test_empty_list), None) is None


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 1, "0000 0000 0000 0001"),
        (5000000000000000, 5000000000000000, "5000 0000 0000 0000"),
    ],
)
def test_card_number_generator_basic(start: int, stop: int, expected: str) -> None:
    assert card_number_generator(start, stop) == expected


def test_card_number_generator_default_format() -> None:
    result = card_number_generator()
    parts = result.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    assert result.replace(" ", "").isdigit()
