from typing import Union
from .setting import *
import json

# Create class methods for this. Make an obnoxious init? Ideally could have convenience fns, like set all pads [off] and [on]; set all notes to be [start], or cc to start at.
# Needs config (json?) parser; from json class. Needs
# Should this be a Collection subtype?
# Maybe not... I think this should contain the types of settings; then later create the collection from it, then finally
class Program(object):
    def __init__(self, config: dict):
        self.config = config
        # self.config = dict(program = None, # int
        #                    global_channel = None, # int
        #                    message = None, # int [0, 1, 2]
        #                    full_level = None, # bool
        #                    toggle = None, # bool
        #                    pad_notes = None, # list[int]
        #                    pad_ccs = None, # list[int]
        #                    pad_pcns = None, # list[int]
        #                    pad_channels = None, # list[int]
        #                    pad_colors = None,  # list[list[int]] | list[list[str]]
        #                    knob_ccs = None, # list[int]
        #                    knob_channels = None, # list[int]
        #                    knob_mins = None, # list[int]
        #                    knob_maxs = None # list[int]
        #                    )

    @classmethod
    def from_json(cls, path: str):
        with open(path) as json_file:
            config_dict = json.load(json_file)
        return cls(config)

    def to_json(self, path: str):
        pass

    # This should *request* the program, then construct a Program() from it.
    @classmethod
    def from_device(cls, program: int):
        pass

