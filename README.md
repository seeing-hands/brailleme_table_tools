# BrailleMe Braille table tools
This repository contains rough scripts attempting to add Braille tables to the BrailleMe display from Innovision which were not originally present in the firmware.
## Warning
These scripts are not supported by Seeing Hands. They are not well-documented, and we make no promises that they will work. This is a small attempt on our part to make something functional, but we will probably not adopt this as a major project.

## Compatibility
These have so far only been tested on a device running version 2.38. It might work on later versions of the firmware for the display, but this is not yet proven. If you have any information about how well these work with other versions, let us know.

## Notes on the device
Most of what we know about how the device works comes from inspecting version 2.38 of the firmware. For a copy of that, see [s.seeinghands.org/brailleme](https://s.seeinghands.org/brailleme).

### Liblouis version
One of the pieces of information we needed to do this was the version of Liblouis installed on the BrailleMe. It wasn't easily found in the firmware, so we isolated it by considering the tables in use. For the tool used to do this, see utils/liblouis_opcode_history.py.

Using this, we determined the following:
* The version is at least 3.14.0 because the opcodes seqbeforechars, seqafterchars, seqafterpattern, attribute, and seqdelimiter were introduced in 3.14.0 and are in use in the UEB grade 2 table. 3.14.0 was released on 2020-06-02.
* The version is at most 3.31.0 because the uplow opcode was removed in 3.32.0.
* It is likely that the version in use is closer to 3.14 than 3.31. While it is possible that 3.15 would be supported, we are targeting 3.14 in these tools for safety.
