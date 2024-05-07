from .hex import Hexcode
from ..constants import MIDI_MAX


def hex_to_int(x: Hexcode) -> int:
    return int(x, 16)


def split_byte_into_two(x: Hexcode) -> list[Hexcode]:
    x_int: int = hex_to_int(x)
    midi_max: int = hex_to_int(MIDI_MAX)

    first: int = x_int // (midi_max + 1)
    remainder: int = x_int % (midi_max + 1)

    return [hex(i) for i in [first, remainder]]
