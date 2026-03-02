from typing import Union

import pytest

from scr.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("test", [1234567898765432, "1234567898765432", "1234 5678 9876 5432"])
def test_mask_card_number_basic_1(test: Union[int, str]) -> None:
    assert get_mask_card_number(test) == "1234 56** **** 5432"


def test_mask_card_number_empty(test_empty_string: str) -> None:
    assert get_mask_card_number(test_empty_string) == "Ошибка ввода номера карты. Повторите попытку"


def test_mask_card_number_input_length() -> None:
    assert get_mask_card_number(12381728719423418239312) == "Ошибка ввода номера карты. Повторите попытку"


def test_mask_card_number_incorrect_input(test_incorrect_input: str) -> None:
    assert get_mask_card_number(test_incorrect_input) == "Ошибка ввода номера карты. Повторите попытку"


@pytest.mark.parametrize("test", [1234567898765432, "1234567898765432", "1234 5678 9876 5432"])
def test_get_mask_account_basic_1(test: Union[int, str]) -> None:
    assert get_mask_account(test) == "**5432"


def test_get_mask_account_empty(test_empty_string: str) -> None:
    assert get_mask_account(test_empty_string) == "Ошибка ввода данных. Повторите попытку снова"


def test_get_mask_account_input_length() -> None:
    assert get_mask_account(123434) == "Ошибка ввода данных. Повторите попытку снова"


def test_get_mask_account_incorrect_input(test_incorrect_input: str) -> None:
    assert get_mask_account(test_incorrect_input) == "Ошибка ввода данных. Повторите попытку снова"
