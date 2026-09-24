# Collection conditions and audio

Source WAVs use 48,000 Hz, signed 16-bit little-endian PCM with four interleaved channels. The channels share source-frame coordinates from one acquisition interface. The four microphones are shown by their display directions:

| Channel | Direction | Physical input |
|---|---|---|
| CH1 | Rear | AMS-44 input 1 |
| CH2 | Left | AMS-44 input 2 |
| CH3 | Front | AMS-44 input 3 |
| CH4 | Right | AMS-44 input 4 |

The directions describe microphone views. They do not define camera placement or measured microphone coordinates. Cameras were attached to a printer in one setup and to microphone robot arms in the others. Video illustrates the equipment and collection setup; it is not a curated dataset input.

The three printer domains are different assembled builds. A and B use Voron 0.2r1 configurations, with B using an LDO V0.1 frame; C is a red-frame Voron 0.2r1 configuration. Domain identity includes component and assembly differences together. It does not isolate the effect of an individual component.

Each printer has 26 sessions. Within each slow and fast program family there are three normal repetitions, three belt interventions (Belt A, Belt B, and both belts), one fan intervention, one extruder intervention, and five collision directions. Slow and Fast denote G-code program families rather than a constant attained toolhead speed. In ordinary runs, the highest explicit commanded feedrates are 12,000 and 30,000 mm/min, respectively; each program uses multiple feedrates and the actual speed can vary by move.

Belt interventions changed rear-tensioner displacement relative to a normal setting. Fan sessions used physical damage to three blades on the right part-cooling fan. Extruder sessions used a loaded-filament cogging intervention. Collision sessions followed five direction-specific contact protocols. Outside the extruder condition, the protocol used no-filament motion. The filament material used for the loaded condition was PLA.

A planned condition does not make every 10-second clip anomalous. Clip admission uses operation boundaries and relevant fault activity as described in [Clip selection](selection.md). The recordings used a small enclosure to reduce external sound; no synthetic background noise was added.
