import time
from functools import wraps
from typing import Any, Callable


def handle_db_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as err:
            print(f"Ошибка: Таблица или столбец {err} не найден.")
        except ValueError as err:
            print(f"Ошибка валидации: {err}")
        except Exception as err:
            print(f"Произошла непредвиденная ошибка: {err}")
        return None

    return wrapper


def confirm_action(action_name: str) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            prompt = (
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            answer = input(prompt).strip().lower()
            if answer != "y":
                print(f'Операция "{action_name}" отменена.')
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        duration = time.monotonic() - start_time
        print(f"Функция {func.__name__} выполнилась за {duration:.4f} секунд.")
        return result

    return wrapper


def create_cacher() -> tuple[
    Callable[[str, Callable[[], Any]], Any], Callable[[], None]
]:
    cache: dict[str, Any] = {}

    def cache_result(key: str, value_func: Callable[[], Any]) -> Any:
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    def clear_cache() -> None:
        cache.clear()

    return cache_result, clear_cache