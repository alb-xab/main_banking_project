import datetime
from typing import Any, Callable


def log(filename: str = "") -> Callable:
    """Декоратор логирования"""

    def decorator_1(func: Callable) -> Callable:
        """Декоратор внутренний логирования"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                start_msg = f"[{timestamp}] Начало работы функции {func.__name__}"

                # Перезаписываем файл в начале выполнения функции
                if filename:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(start_msg + "\n")
                else:
                    print(start_msg)

                result = func(*args, **kwargs)
                end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                end_msg = f"[{end_timestamp}] Конец работы функции {func.__name__}. Результат: {result}"

                # Дописываем сообщение о завершении
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:  # теперь дописываем
                        f.write(end_msg + "\n")
                else:
                    print(end_msg)
                return result

            except Exception as e:
                error_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_msg = (
                    f"[{error_timestamp}] Ошибка в функции {func.__name__}. "
                    f"Тип ошибки: {type(e).__name__}, "
                    f"Сообщение: {e}, "
                    f"Аргументы: args={args}, kwargs={kwargs}"
                )

                if filename:
                    try:
                        with open(filename, "a", encoding="utf-8") as f:  # дописываем ошибку
                            f.write(error_msg + "\n")
                    except IOError as file_error:
                        print(f"[{error_timestamp}] Не удалось записать в файл {filename}: {file_error}")
                else:
                    print(error_msg)
                raise

        return wrapper

    return decorator_1
