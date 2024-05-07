from ..hex import Hexcode, split_byte_into_two
from ..util import flatten


def color_code_to_hexcodes(x: int) -> list[Hexcode]:
    return split_byte_into_two(x)


def rgb_to_hex_stream(x: list[str] | list[int]) -> list[Hexcode]:
    if isinstance(x, list) and isinstance(x[0], str):
        x = [int(i, 16) for i in x]

    x = [hex(i) for i in x]

    hex_codes: list[list[Hexcode]] = [color_code_to_hexcodes(i) for i in x]

    hex_code_stream: list[Hexcode] = flatten(hex_codes)

    return hex_code_stream
