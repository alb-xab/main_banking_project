import json
from unittest.mock import Mock, patch

import pytest

from scr.external_api import conversion_amount


def test_conversion_amount() -> None:
    with pytest.raises(ValueError) as excinfo:
        conversion_amount(0.0, "")
    assert str(excinfo.value) == "Переданные данные пустые"


@patch("requests.request")
def test_conversion_amount_api_success(mock_request: Mock) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"result": 8500.50}'
    mock_request.return_value = mock_response

    result = conversion_amount(100, "USD", "RUB")
    assert result == 8500.50
    mock_request.assert_called_once()


@patch("requests.request")
def test_conversion_amount_api_error_response(mock_request: Mock) -> None:
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = '{"error": "Invalid parameters"}'
    mock_request.return_value = mock_response

    with pytest.raises(Exception):  # или конкретный тип ошибки
        conversion_amount(100, "USD")


@patch("requests.request")
def test_conversion_amount_invalid_json_response(mock_request: Mock) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "invalid json"
    mock_request.return_value = mock_response

    with pytest.raises(json.JSONDecodeError):
        conversion_amount(100, "USD")
