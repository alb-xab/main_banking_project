import datetime
from unittest.mock import patch

import pytest

from src.decorators import log


def test_log_success_with_filename(tmp_path) -> None:
    log_file = tmp_path / "test_log.txt"
    fixed_dt = datetime.datetime(2024, 1, 2, 3, 4, 5)

    with patch("src.decorators.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_dt

        @log(filename=str(log_file))
        def test_function(x: int, y: int) -> int:
            return x + y

        result = test_function(5, 3)

    assert result == 8
    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert lines[0] == "[2024-01-02 03:04:05] Начало работы функции test_function"
    assert lines[1] == "[2024-01-02 03:04:05] Конец работы функции test_function. Результат: 8"


def test_log_success_without_filename(capsys: pytest.CaptureFixture) -> None:
    fixed_dt = datetime.datetime(2024, 1, 2, 3, 4, 5)

    with patch("src.decorators.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_dt

        @log()
        def test_function(x: int, y: int) -> int:
            return x * y

        result = test_function(4, 6)

    assert result == 24
    output = capsys.readouterr().out
    assert "[2024-01-02 03:04:05] Начало работы функции test_function" in output
    assert "[2024-01-02 03:04:05] Конец работы функции test_function. Результат: 24" in output


def test_log_exception_with_filename(tmp_path) -> None:
    log_file = tmp_path / "error_log.txt"
    fixed_dt = datetime.datetime(2024, 1, 2, 3, 4, 5)

    with patch("src.decorators.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_dt

        @log(filename=str(log_file))
        def faulty_function() -> None:
            raise ValueError("Произошла ошибка")

        with pytest.raises(ValueError, match="Произошла ошибка"):
            faulty_function()

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert lines[0] == "[2024-01-02 03:04:05] Начало работы функции faulty_function"
    assert lines[1] == (
        "[2024-01-02 03:04:05] Ошибка в функции faulty_function. "
        "Тип ошибки: ValueError, Сообщение: Произошла ошибка, Аргументы: args=(), kwargs={}"
    )


def test_log_exception_without_filename(capsys: pytest.CaptureFixture) -> None:
    fixed_dt = datetime.datetime(2024, 1, 2, 3, 4, 5)

    with patch("src.decorators.datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_dt

        @log()
        def faulty_function() -> None:
            raise ValueError("Произошла ошибка")

        with pytest.raises(ValueError, match="Произошла ошибка"):
            faulty_function()

    output = capsys.readouterr().out
    assert "[2024-01-02 03:04:05] Начало работы функции faulty_function" in output
    assert "Ошибка в функции faulty_function" in output
    assert "Тип ошибки: ValueError" in output
    assert "Сообщение: Произошла ошибка" in output
