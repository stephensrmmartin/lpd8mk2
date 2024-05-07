from typing import Iterable
from .any import Any


def flatten(x: Iterable[Iterable[Any]]) -> list[Any]:
    return [i for lst in x for i in lst]
