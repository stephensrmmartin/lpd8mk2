from typing import Iterable
from .any import Any


def flatten(x: Iterable[Iterable[Any]]) -> list[Any]:
    any_iterables = False
    for i in x:
        if isinstance(i, Iterable):
            any_iterables = True
            break
    if any_iterables:
        output_list = []
        for i in x:
            if isinstance(i, str):
                output_list.append(i)
            elif isinstance(i, Iterable):
                output_list.extend(i)
            else:
                output_list.append(i)
        return output_list
        # return [i for lst in x for i in lst]
    else:
        return x

