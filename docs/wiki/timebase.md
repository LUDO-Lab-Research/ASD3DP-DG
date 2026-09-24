# Time coordinates

A shared recorder frame coordinate connects the four channels. Let `F` be the first source frame stored in a WAV, `B` the recording-start boundary frame, and `S` the start frame of a selected clip. At 48,000 frames per second:

```text
WAV frame              = source_frame - F
WAV seconds            = (source_frame - F) / 48000
recording-relative sec = (source_frame - B) / 48000
clip-relative seconds  = (source_frame - S) / 48000
```

Pre-roll can make `F` and `B` different. Convert timestamps to the same origin before deciding that two intervals disagree. An interval end marked `exclusive` is the first frame outside that interval.

## Command observations and corrected time

Recorder cursors around printer-status queries provide observation brackets. They describe when the host observed a command or state, rather than an exact motor or sound-onset time. Source audio and directly observed events retain their original coordinates.

To connect commands to recorded sound, the dataset uses an observed end-of-print reference. Let `[C_L,C_U]` be the ending command bracket and `[O_L,O_U]` the observed ending range; let `O` be the selected observed point. Then:

```text
C   = floor((C_L + C_U) / 2)
D   = O - C
D_L = O_L - C_U
D_U = O_U - C_L
corrected_command_frame = raw_command_frame + D
```

The selected point shifts command annotations for display. Bounds `D_L` and `D_U` support conservative admission of command-derived activity. Source WAV samples, video, telemetry observations, RMS events, and the fixed recording-start clip grid do not move. This session-level correction does not measure the execution time of every command.

The released timeline retains original command observations and corrected ranges. See [Annotation layers](annotations.md) before combining them with audio-derived or telemetry-derived intervals.
