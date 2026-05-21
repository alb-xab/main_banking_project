import json
from collections import Counter
from unittest.mock import Mock, mock_open, patch

import pandas as pd
import pytest

from src import utils


def test_load_operations_json_empty_road() -> None:
    assert utils.load_operations("") == []


@patch("builtins.open", new_callable=mock_open, read_data="[]")
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_json_empty_database(mock_exists: Mock, mock_file: Mock) -> None:
    result = utils.load_operations("data.json")
    assert result == []


@patch("src.utils.os.path.exists", return_value=False)
def test_load_operations_file_not_found(mock_exists: Mock) -> None:
    result = utils.load_operations("missing.json")
    assert result == []


@patch("src.utils.json.load", return_value={"id": 1})
@patch("builtins.open", new_callable=mock_open, read_data='{"id": 1}')
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_json_invalid_format(mock_exists: Mock, mock_file: Mock, mock_json_load: Mock) -> None:
    result = utils.load_operations("data.json")
    assert result == []


@patch("src.utils.json.load", return_value=[{"id": 1}])
@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_json_success(mock_exists: Mock, mock_file: Mock, mock_json_load: Mock) -> None:
    result = utils.load_operations("data.json")
    assert result == [{"id": 1}]
    mock_json_load.assert_called_once()


@patch("builtins.open", new_callable=mock_open, read_data="{bad json")
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_json_decode_error(mock_exists: Mock, mock_file: Mock) -> None:
    with patch("src.utils.json.load", side_effect=json.JSONDecodeError("Expecting value", "{bad json", 0)):
        result = utils.load_operations("data.json")
    assert result == []


@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_unsupported_extension(mock_exists: Mock) -> None:
    result = utils.load_operations("data.txt")
    assert result == []


@patch("src.utils.pd.read_csv")
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_csv_success(mock_exists: Mock, mock_read_csv: Mock) -> None:
    df = pd.DataFrame(
        [
            {
                "id": 650703,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            }
        ]
    )
    mock_read_csv.return_value = df

    result = utils.load_operations("data.csv")

    assert result == df.to_dict(orient="records")
    mock_read_csv.assert_called_once_with("data.csv", sep=";")


@patch("src.utils.pd.read_csv", return_value=pd.DataFrame())
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_csv_empty_dataframe(mock_exists: Mock, mock_read_csv: Mock) -> None:
    result = utils.load_operations("empty.csv")
    assert result == []


@patch("src.utils.pd.read_excel")
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_xlsx_success(mock_exists: Mock, mock_read_excel: Mock) -> None:
    df = pd.DataFrame(
        [
            {
                "id": 3598919,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": 29740,
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            }
        ]
    )
    mock_read_excel.return_value = df

    result = utils.load_operations("data.xlsx")

    assert result == df.to_dict(orient="records")
    mock_read_excel.assert_called_once_with("data.xlsx", engine="openpyxl")


@patch("src.utils.pd.read_excel", return_value=pd.DataFrame())
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_xlsx_empty_dataframe(mock_exists: Mock, mock_read_excel: Mock) -> None:
    result = utils.load_operations("empty.xlsx")
    assert result == []


@patch("src.utils.pd.read_excel", side_effect=pd.errors.EmptyDataError)
@patch("src.utils.os.path.exists", return_value=True)
def test_load_operations_xlsx_empty_data_error(mock_exists: Mock, mock_read_excel: Mock) -> None:
    result = utils.load_operations("empty.xlsx")
    assert result == []


def test_process_bank_search_case_insensitive() -> None:
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "перевод с карты на карту"},
    ]

    result = utils.process_bank_search(data, "ПЕРЕВОД")
    assert result == [
        {"description": "Перевод организации"},
        {"description": "перевод с карты на карту"},
    ]


def test_process_bank_search_empty_result() -> None:
    data = [{"description": "Открытие вклада"}]
    assert utils.process_bank_search(data, "Перевод") == []


def test_process_bank_operations_basic() -> None:
    data = [
        {"description": "Перевод организации"},
        {"description": "Оплата услуг"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
        {"id": 1},
    ]
    categories = ["Перевод", "Оплата", "Вклад"]

    result = utils.process_bank_operations(data, categories)

    assert result == {"Перевод": 2, "Оплата": 1, "Вклад": 1}


def test_operation_conversion_amount_rub_returns_same_amount() -> None:
    operations = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"code": "RUB"},
            },
        }
    ]

    result = utils.operation_conversion_amount(operations)
    assert result == [31957.58]


@patch("src.utils.conversion_amount", return_value=725.0)
def test_operation_conversion_amount_usd_calls_converter(mock_conversion: Mock) -> None:
    operations = [
        {
            "id": 2,
            "operationAmount": {
                "amount": "10.0",
                "currency": {"code": "USD"},
            },
        }
    ]

    result = utils.operation_conversion_amount(operations)

    assert result == [725.0]
    mock_conversion.assert_called_once_with(10.0, "USD")


@patch("src.utils.conversion_amount", return_value=1500.0)
def test_operation_conversion_amount_eur_calls_converter(mock_conversion: Mock) -> None:
    operations = [
        {
            "id": 3,
            "operationAmount": {
                "amount": "15.5",
                "currency": {"code": "EUR"},
            },
        }
    ]

    result = utils.operation_conversion_amount(operations)

    assert result == [1500.0]
    mock_conversion.assert_called_once_with(15.5, "EUR")


@patch("src.utils.conversion_amount", return_value=700.0)
def test_operation_conversion_amount_multiple_operations(mock_conversion: Mock) -> None:
    operations = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "RUB"},
            },
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "10",
                "currency": {"code": "USD"},
            },
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "5",
                "currency": {"code": "GBP"},
            },
        },
    ]
    result = utils.operation_conversion_amount(operations)
    assert result == [100.0, 700.0, None]
    mock_conversion.assert_called_once_with(10.0, "USD")


def test_operation_conversion_amount_invalid_amount_string() -> None:
    operations = [
        {
            "id": 10,
            "operationAmount": {
                "amount": "abc",
                "currency": {"code": "RUB"},
            },
        }
    ]
    assert utils.operation_conversion_amount(operations) == [None]


def test_operation_conversion_amount_empty_list(test_empty_list: list) -> None:
    assert utils.operation_conversion_amount(test_empty_list) == []


def test_operation_conversion_amount_incorrect_currency(test_transaction_list_incorrect_currency: list) -> None:
    assert utils.operation_conversion_amount(test_transaction_list_incorrect_currency) == [None]


def test_operation_conversion_amount_without_operation(test_transaction_list_without_operation: list) -> None:
    assert utils.operation_conversion_amount(test_transaction_list_without_operation) == [None]
