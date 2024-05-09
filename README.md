
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


