
# Summary

Python tool for configuring the Akai LPD8 Mkii (Mk2) Midi controller.
Although many excellent LPD8 configuration tools exist (For example, [lpd8editor](https://github.com/charlesfleche/lpd8editor), [lpd8-web-editor](https://github.com/bennigraf/lpd8-web-editor), [lpd8](https://github.com/boomlinde/lpd8), [LPD8-Editor](https://github.com/navelpluisje/LPD8-Editor)), none could fully configure the Mkii variant.

# Methodology
I used the official Akai LPD8 Mk2 editor in a Windows virtual machine, and used Wireshark to listen to the Sysex messages it sent over USB.
For each possible input, I modified the value in the Windows tool, then examined how the Sysex message changed. 

![Official Akai LPD8 Mk2 tool](./docs/lpd8editor.png)

![Wireshark](./docs/wireshark.png)

This process resulted in a mapping of the Sysex message structure:
![Sysex message for Akai LPD8 mk2](./docs/hex_diagram.svg)

# Usage

```python
import lpd8mk2.config as config
import lpd8mk2.midi.LPD8Mk2IO as io

# Load preset 3

prog = config.Program.from_preset(3)

# View config

print(prog.config)

# Change RGB off color to white, on color to Blue for all pads

prog.set_pad_colors([255, 255, 255], [0, 0, 255])

# Change 8th pad to have an on color of red
prog.set_pad_colors(None, [255, 0, 0], [8])

# Set toggle mode and full level on
prog.config['toggle'] = True
prog.config['full_level'] = True

# Compile out the program to view the Sysex message in hex.
# Compile it to be Program 4 in the device.
print(prog(4))

# Create Sysex message for Sending through Midi (To be assigned to program 4 in the device):
sysex_message = prog.to_sysex(4)

# Send it
io.LPD8Mk2IO().send(sysex_message)

# On the device, change to program 4 if not already. If on program 4, then change to another then back to 4.

```

