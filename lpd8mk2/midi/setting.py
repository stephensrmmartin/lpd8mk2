from ..hex import Hexcode
from ..constants import MIDI_MIN, MIDI_MAX

class Setting(object):
    def __init__(self, x: int | bool):
        self.check_midi_bounds(x)
        self.input_setting = x
        self.hex_setting = hex(x)

    def check_midi_bounds(self, x: int | bool):
        if x < int(MIDI_MIN, 16) or x > int(MIDI_MAX, 16):
            raise ValueError(f"Setting must be between {MIDI_MIN} and {MIDI_MAX}")
            
    def __call__(self):
        return self.hex_setting

class BoundaryMixin(object):
    def __init__(self, x, lower_bound = MIDI_MIN, upper_bound = MIDI_MAX):
        self.lower_bound = hex(lower_bound)
        self.upper_bound = hex(upper_bound)
        self.check_bounds(x)

    def check_bounds(self, x: int | bool):
        if x < int(self.lower_bound, 16) or x > int(self.upper_bound, 16):
            raise ValueError(f"Setting must be between {self.lower_bound} and {self.upper_bound}. Found: {hex(x)}")
        
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
        BoundaryMixin.__init__(self, x, 1, 17)
        MinusOneMixin.__init__(self)
        Setting.__init__(self, x)
