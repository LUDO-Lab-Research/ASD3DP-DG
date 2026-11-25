# Annotation layers

The release describes collection conditions at the session level and activity at the clip level. G-code and telemetry provide context for recorded commands and observed printer states. Review decisions inform which evidence is included in the released intervals.

| Layer | Meaning |
|---|---|
| Session context | Printer build, speed program, and planned condition |
| Clip context | Source interval, microphone channel, and selection status |
| Activity ranges | Operation, belt activity, and fault intervals within a clip |
| Timing evidence | Original command observations and their corrected time ranges |

The collection uses normal, soft-anomaly, and hard-anomaly conditions. These categories describe the collection protocol. Fault families cover belt tension, cooling fan, extruder cogging, and toolhead collision. An anomaly session can contain inactive periods or finish printing.

Several ranges can overlap within a clip. To calculate how long one type of activity was present, take the union of its intervals. Preserve unknown values when the evidence is incomplete.

See [Schema and field names](schemas.md) for table interpretation and [Time coordinates](timebase.md) for interval origins.
