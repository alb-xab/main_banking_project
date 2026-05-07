import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_get_mask_account_basic_1(test_data: str, expected: str) -> None:
    assert mask_account_card(test_data) == expected


def test_get_mask_account_input_1() -> None:
    assert mask_account_card("") == "Ошибка ввода. Проверьте корректность ввода и повторите попытку"


def test_get_mask_account_input_2() -> None:
    assert (
        mask_account_card("ну и продолжили мы пить чай, а для проверки решили сделать так")
        == "Ошибка ввода. Проверьте корректность ввода и повторите попытку"
    )


@pytest.mark.parametrize(
    "test_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2021-07-11T03:26:18.681407", "11.07.2021"),
        ("2025-12-12T02:26:18.671407", "12.12.2025"),
    ],
)
def test_get_date(test_date: str, expected: str) -> None:
    assert get_date(test_date) == expected


def test_get_date_empty_input(test_empty_string: str) -> None:
    assert get_date(test_empty_string) == "Ошибка ввода формата даты. Повторите попытку позже"


def test_get_date_incorrect_input(test_short_numbers: str) -> None:
    assert get_date(test_short_numbers) == "Ошибка ввода формата даты. Повторите попытку позже"


def test_get_date_incorrect_input_2(test_incorrect_input: str) -> None:
    assert get_date(test_incorrect_input) == "Ошибка ввода формата даты. Повторите попытку позже"
