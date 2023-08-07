from .deps import TypeVar, Callable, Any, environ

T = TypeVar("T")
Caster = Callable[[str], Any]


class Env:
    @staticmethod
    def str(key: str, default: T = ...) -> str | T:
        return get(key, default)

    @staticmethod
    def int(key: str, default: T = ...) -> int | T:
        return get(key, default, int)

    @staticmethod
    def ints(key: str, default: T = ...) -> list[int] | T:
        return get(key, default, parse_ints)


def parse_ints(text: str) -> list[int]:
    return [int(i.strip()) for i in text.strip().split(",")]


def get(key: str, default=..., caster: Caster = None):
    if key not in environ:
        if default is ...:
            raise ValueError(f'Environment variable "{key}" not set')
        return default

    value = environ[key]
    if caster:
        value = caster(value)
    return value


env = Env()
