import pytest

from scr.decorators import log


def test_successful_execution_with_filename() -> None:

    @log(filename="test_log.txt")
    def test_function(x: int, y: int) -> int:
        return x + y

    result = test_function(5, 3)
    assert result == 8
    with open("test_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert "Начало работы функции test_function" in lines[0]
    assert "Конец работы функции test_function. Результат: 8" in lines[1]


def test_successful_execution_without_filename(capsys: pytest.CaptureFixture) -> None:
    @log()
    def test_function(x: int, y: int) -> int:
        return x * y

    result = test_function(4, 6)
    assert result == 24
    captured = capsys.readouterr()
    output = captured.out
    assert "Начало работы функции test_function" in output
    assert "Конец работы функции test_function. Результат: 24" in output


def test_exception_handling_with_filename() -> None:
    @log(filename="error_log.txt")
    def faulty_function() -> None:
        raise ValueError("Произошла ошибка")

    with pytest.raises(ValueError, match="Произошла ошибка"):
        faulty_function()
    with open("error_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert "Начало работы функции faulty_function" in lines[0]
    assert "Ошибка в функции faulty_function" in lines[1]
    assert "Тип ошибки: ValueError" in lines[1]
    assert "Сообщение: Произошла ошибка" in lines[1]
    assert "Аргументы: args=(), kwargs={}" in lines[1]
