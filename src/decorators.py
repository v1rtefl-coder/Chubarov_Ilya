import functools


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Простое форматирование аргументов
            args_str = str(args)
            kwargs_str = str(kwargs)

            if kwargs:
                inputs_str = f"{args_str}, {kwargs_str}"
            else:
                inputs_str = args_str

            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message, end='')

                return result

            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs_str}\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message, end='')

                raise

        return wrapper

    return decorator
