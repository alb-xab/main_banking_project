import pytest


@pytest.fixture
def test_empty_string() -> str:
    return " "


@pytest.fixture
def test_empty_list() -> list:
    return []


@pytest.fixture
def test_short_numbers() -> str:
    return "1234"


@pytest.fixture
def test_incorrect_input() -> str:
    return "чай попить и кофе"


@pytest.fixture
def test_work_list() -> list:
    return [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
