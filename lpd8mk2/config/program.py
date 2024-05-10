from typing import Union
from .setting import *
from ..constants import *
from ..hex import hex_to_int
import json
import mido
import copy
from .preset import presets

class Program(object):
    """Configure program for the Akai LPD8 Mk2 Midi device.

    Attributes:
    config: dict(
        "global_channel": int [1-16],
        "pressure_message": str ("off", "channel", "polyphonic"),
        "full_level": bool,
        "toggle": bool,
        "pad_note": list[int] : MIDI note value for each of 8 pads,
        "pad_cc": list[int] : MIDI CC value for each of 8 pads,
        "pad_pcn": list[int] : MIDI program change value for each of 8 pads,
        "pad_channel": list[int] : MIDI channel for each of 8 pads [1-17; if 17, set to global channel],
        "pad_off_color": list[list[int]] : List of RGB values for each of 8 pads to display when off.,
        "pad_on_color": list[list[int]] : List of RGB values for each of 8 pads to display when on.,
        "knob_cc": list[int]: MIDI CC value for each of 8 knobs.,
        "knob_channel": list[int]: MIDI channel for each of 8 knobs. [1-17; if 17, set to global channel],
        "knob_min": list[int]: Minimum MIDI value for each of 8 knobs.,
        "knob_max": list[int]: Maximum MIDI value for each of 8 knobs.,
    )

    """
    def __init__(self, config: dict):
        """Configure program for the Akai LPD8 Mk2 Midi device.

        Attributes:
        config: dict(
            "global_channel": int [1-16],
            "pressure_message": str ("off", "channel", "polyphonic"),
            "full_level": bool,
            "toggle": bool,
            "pad_note": list[int] : MIDI note value for each of 8 pads,
            "pad_cc": list[int] : MIDI CC value for each of 8 pads,
            "pad_pcn": list[int] : MIDI program change value for each of 8 pads,
            "pad_channel": list[int] : MIDI channel for each of 8 pads [1-17; if 17, set to global channel],
            "pad_off_color": list[list[int]] : List of RGB values for each of 8 pads to display when off.,
            "pad_on_color": list[list[int]] : List of RGB values for each of 8 pads to display when on.,
            "knob_cc": list[int]: MIDI CC value for each of 8 knobs.,
            "knob_channel": list[int]: MIDI channel for each of 8 knobs. [1-17; if 17, set to global channel],
            "knob_min": list[int]: Minimum MIDI value for each of 8 knobs.,
            "knob_max": list[int]: Maximum MIDI value for each of 8 knobs.,
        )

        It is recommended to use the from_json or from_preset for convenience.
        See readme.md for json format and existing presets.
        """
        self.config = config
        # {
        #     "global_channel": 1,
        #     "pressure_message": "off",
        #     "full_level": false,
        #     "toggle": false,
        #     "pad_note": [36, 37, 38, 39, 40, 41, 42, 43],
        #     "pad_cc": [12, 13, 14, 15, 16, 17, 18, 19],
        #     "pad_pcn": [0, 1, 2, 3, 4, 5, 6, 7],
        #     "pad_channel": [10, 10, 10, 10, 10, 10, 10, 10],
        #     "pad_off_color": [[255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]],
        #     "pad_on_color": [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 255]],
        #     "knob_cc": [70, 71, 72, 73, 74, 75, 76, 77],
        #     "knob_channel": [17, 17, 17, 17, 17, 17, 17, 17],
        #     "knob_min": [0, 0, 0, 0, 0, 0, 0, 0],
        #     "knob_max": [127, 127, 127, 127, 127, 127, 127, 127]
        # }

    @classmethod
    def from_json(cls, path: str):
        with open(path) as json_file:
            config_dict = json.load(json_file)
        return cls(config_dict)

    @classmethod
    def from_preset(cls, preset: int):
        return cls(copy.deepcopy(presets[preset-1]))
        
    def to_json(self, path: str):
        with open(path, 'x') as file:
            json.dump(self.config, file)

    # This should *request* the program, then construct a Program() from it.
    # @classmethod
    # def from_device(cls, program: int):
    #     pass

    def set_pad_colors(self, off: list[int] | Color, on: list[int] | Color, pad_numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8]):
        for p in pad_numbers:
            if off is not None:
                self.config["pad_off_color"][p-1] = off
            if on is not None:
                self.config["pad_on_color"][p-1] = on

    def _build_knobs(self):
        knobs: list = [Knob(*k) for k in zip(*[self.config["knob_" + i] for i in ["cc", "channel", "min", "max"]])]
        return knobs
        # return Collection(knobs)
        # for k in zip(*[self.config["knob_" + i] for i in ["cc", "channel", "min", "max"]]):
        #     knobs.append(Knob(*k))

    def _build_pads(self):
        pads: list = [Pad(*p) for p in zip(*[self.config["pad_" + i] for i in ["note", "cc", "pcn", "channel", "off_color", "on_color"]])]
        return pads
        # return Collection(pads)

    def _compile(self, program: int):
        settings = [LPD8MK2HeaderSetting(),
                    SendSetting(),
                    LPD8MK2SpacerSetting(),
                    ProgramSetting(program),
                    GlobalChannel(self.config["global_channel"]),
                    PressureMessage(self.config["pressure_message"]),
                    FullLevel(self.config["full_level"]),
                    Toggle(self.config["toggle"])]

        knobs = self._build_knobs()
        pads = self._build_pads()

        settings.extend(pads)
        settings.extend(knobs)
        return Collection(settings)

    def __call__(self, program: int):
        settings = self._compile(program)
        return settings()

    def to_sysex(self, program: int) -> mido.Message:
        compiled = [hex_to_int(h) for h in self(program)]
        return mido.Message('sysex', data=compiled)

