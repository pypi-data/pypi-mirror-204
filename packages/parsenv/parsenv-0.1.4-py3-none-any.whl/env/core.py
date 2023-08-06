from os import environ
from typing import TypeVar, Callable

DT = TypeVar("DT")
RT = TypeVar("RT")
Parser = Callable[[str], RT]


class Undefined:
    pass


UNDEFINED = Undefined()


def get_var(
    key: str,
    default: DT = UNDEFINED,
    parser: Parser[RT] = lambda x: x,
) -> DT | RT:
    if key not in environ:
        if isinstance(default, Undefined):
            raise EnvError(key)
        return default

    value = environ[key]

    try:
        return parser(value)
    except ValueError as e:
        raise ParseError(key, e)


class EnvError(KeyError):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"Environment variable `{self.key}` not set"


class ParseError(ValueError):
    def __init__(self, key: str, cause: ValueError):
        self.key = key
        self.cause = cause

    def __str__(self):
        return f"Can't parse environment variable `{self.key}`: {self.cause}"
