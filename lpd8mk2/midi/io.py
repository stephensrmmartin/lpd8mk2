import mido

class MidiIO(object):
    def __init__(self):
        pass

    def _find_lpd8(self):
        dev_names: list[str] = [dev['name'] for dev in mido.backends.rtmidi.get_devices()]
        for name in dev_names:
            if 'lpd8' in name.lower():
                return name
        return None

