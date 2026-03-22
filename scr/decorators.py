import datetime


def log(filename=None):
    def decorator_1(func):
        def wrapper(*args, **kwargs):
            try:
                start_time = datetime.datetime.now()
                print(f'Начало работы функции - {start_time}')
                result = f'{func(*args, **kwargs)} '
                end_time = datetime.datetime.now()
                print(f'Конец работы функции - {end_time}')
                log_result = f'{func.__name__} - {result}'
            except Exception as e:
                end_time = datetime.datetime.now()
                print(f'Прекращение работы функции - {end_time}')
                log_result = f'{func.__name__}: - {type(e).__name__} Inputs: {args}, {kwargs}'
            finally:
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_result)
                        return log_result
                else:
                    return log_result
        return wrapper
    return decorator_1


