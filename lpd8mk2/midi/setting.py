from ..hex import Hexcode
from ..hex import convert_if_hex
from ..constants import MIDI_MIN, MIDI_MAX
from ..util import flatten
from ..rgb.rgb import rgb_to_hex_stream
import typing


class Setting(object):
    def __init__(self, x: int | bool | str):
        if isinstance(x, str):
            self.hex_setting = x
            self.input_setting = int(x, 16)
            
        else:
            self.input_setting = x
            self.hex_setting = hex(x)
        self.check_midi_bounds(self.input_setting)

    def check_midi_bounds(self, x: int | bool):
        if x < int(MIDI_MIN, 16) or x > int(MIDI_MAX, 16):
            raise ValueError(f"Setting must be between {MIDI_MIN} and {MIDI_MAX}")
            
    def __call__(self):
        return self.hex_setting

class BoundaryMixin(object):
    def __init__(self, x, lower_bound = MIDI_MIN, upper_bound = MIDI_MAX):
        self.lower_bound = hex(lower_bound)
        self.upper_bound = hex(upper_bound)
        return self

    def check_bounds(self, x, lower_bound = None, upper_bound = None):
        x = convert_if_hex(x)
        if x < int(lower_bound or self.lower_bound, 16) or x > int(upper_bound or self.upper_bound, 16):
            raise ValueError(f"Setting must be between {self.lower_bound} and {self.upper_bound}. Found: {hex(x)}")
        return self
        
class MinusOneMixin(object):
    def __call__(self):
        return hex(int(self.hex_setting, 16) - 1) # TO INT, minus 1, BACK TO HEX

class Note(Setting):
    def __init__(self, x: int):
        super().__init__(x)

class CC(Setting):
    def __init__(self, x: int):
        super().__init__(x)

class Channel(BoundaryMixin,MinusOneMixin,Setting):
    def __init__(self, x: int):
        BoundaryMixin.__init__(self, x, 1, 17).check_bounds(x)
        MinusOneMixin.__init__(self)
        Setting.__init__(self, x)

Collection = typing.NewType("Collection", list)
class Collection(object):
    def __init__(self, settings: list[Setting] | Collection):
        self.settings = settings

    def __call__(self):
        output_stream = flatten([setting() for setting in self.settings])
        return output_stream

class Color(Collection):
    def __init__(self, hexcode: list[str] | list[int]):
        self.hexcode = hexcode
        hexcodes = rgb_to_hex_stream(hexcode)
        super().__init__([Setting(i) for i in hexcodes])

