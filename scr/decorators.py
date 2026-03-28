import datetime
from typing import Callable, Any


def log(filename=None):
    def decorator_1(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = ""

            try:
                start_msg = f"[{timestamp}] Начало работы функции {func.__name__}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(start_msg + "\n")
                else:
                    print(start_msg)

                result = func(*args, **kwargs)
                end_msg = f"[{timestamp}] Конец работы функции {func.__name__}. Результат: {result}"
                log_message = end_msg

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                return result

            except Exception as e:
                error_msg = (
                    f"[{timestamp}] Ошибка в функции {func.__name__}. "
                    f"Тип ошибки: {type(e).__name__}, "
                    f"Сообщение: {e}, "
                    f"Аргументы: args={args}, kwargs={kwargs}"
                )
                log_message = error_msg
                if filename:
                    try:
                        with open(filename, "a", encoding="utf-8") as f:
                            f.write(log_message + "\n")
                    except IOError as file_error:
                        print(f"[{timestamp}] Не удалось записать в файл {filename}: {file_error}")
                else:
                    print(error_msg)
                raise

        return wrapper

    return decorator_1