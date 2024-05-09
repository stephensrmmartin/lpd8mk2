from ..hex import Hexcode
from ..hex import convert_if_hex
from ..constants import *
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

class PCN(Setting):
    def __init__(self, x: int):
        super().__init__(x)

class Channel(BoundaryMixin,MinusOneMixin,Setting):
    def __init__(self, x: int):
        BoundaryMixin.__init__(self, x, 1, 17).check_bounds(x)
        MinusOneMixin.__init__(self)
        Setting.__init__(self, x)

class GlobalChannel(Channel):
    def __init__(self, x: int):
        super().__init__(x)

class Toggle(Setting):
    def __init__(self, x: bool):
        super().__init__(x)

class FullLevel(Setting):
    def __init__(self, x: bool):
        super().__init__(not x)

class PressureMessage(Setting):
    def __init__(self, x: str):
        message_type = {"off": 0, "channel": 1, "polyphonic": 2}
        super().__init__(message_type[x.lower()])
        

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

class SendSetting(Setting):
    def __init__(self):
        super().__init__(1)

class ProgramSetting(BoundaryMixin, Setting):
    def __init__(self, x: int):
        BoundaryMixin.__init__(self, x, 1, 4).check_bounds(x)
        Setting.__init__(self, x)

class LPD2MK2HeaderSetting(Collection):
    def __init__(self):
        super().__init__([Setting(i) for i in [SYSEX_AKAI, SYSEX_AKAI_2, SYSEX_LPD8_MK2]])

class LPD2MK2SpacerSetting(Collection):
    def __init__(self):
        super().__init__([Setting(i) for i in [SYSEX_LPD8_MK2_SPACER_1, SYSEX_LPD8_MK2_SPACER_2]])

def _class_if_not_class(x, cls):
    if not isinstance(x, cls):
        return cls(x)
    else:
        return x

class Pad(Collection):
    def __init__(self,
                 note: int | Note,
                 cc: int | CC,
                 pcn: int | PCN,
                 channel: int | Channel,
                 on_color : list[int] | Color,
                 off_color: list[int] | Color):
        settings = [_class_if_not_class(x, c) for x, c in zip([note, cc, pcn, channel, on_color, off_color], [Setting, CC, PCN, Channel, Color, Color])]
        super().__init__(settings)

class Knob(Collection):
    def __init__(self,
                 cc: int | Setting,
                 channel: int | Channel,
                 min: int | Setting,
                 max: int | Setting):
        settings = [_class_if_not_class(x, c) for x, c in zip([cc, channel, min, max], [Setting, Channel, Setting, Setting])]

        super().__init__(settings)
