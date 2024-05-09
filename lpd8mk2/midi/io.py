import mido
from ..config.setting import Collection, LPD8MK2HeaderSetting, ReceiveSetting, Setting, ProgramSetting
from ..hex import hex_to_int

class DeviceError(Exception):
    pass

class LPD8Mk2IO(object):
    def __init__(self):
        self.lpd8_name = self._find_lpd8()
        if self.lpd8_name is None:
            raise DeviceError("No LPD8 Mk2 device found.")
        self.in_port = mido.open_input(lpd8_name)
        self.out_port = mido.open_output(lpd8_name)

    def _find_lpd8(self):
        dev_names: list[str] = [dev for dev in mido.get_input_names()]
        for name in dev_names:
            if 'lpd8' in name.lower():
                return name
        return None
    def send(self, msg: mido.Message):
        self.out_port.send(msg)

    def receive(self, program: int):
        receive_program_code = Collection(LPD8MK2HeaderSetting(),
                                          ReceiveSetting(),
                                          Setting(0),
                                          Setting(1),
                                          ProgramSetting(program)
                                          )
        sysex = mido.Message('sysex', [hex_to_int(h) for h in receive_program_code])
        self.send(sysex)
        response = self.in_port.receive()
        return response

