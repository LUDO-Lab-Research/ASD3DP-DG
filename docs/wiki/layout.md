# Folders and files

The public dataset is organized into three archive groups, following the distribution pattern of [ASD3DP](https://zenodo.org/records/21313911):

| Group | Contents |
|---|---|
| `all` | Continuous source recordings and session context |
| `annotations` | Session, clip, timing, and interval tables |
| `clipped` | Selected 10-second mono WAVs by channel |

The final archive names, part counts, checksums, and download location will appear on [Downloads](download.md) after packaging and remote verification. A split archive part is only one piece of its group; all parts of a group are needed for extraction.

## File relationships

A recording session provides one four-channel source WAV. A selected temporal clip refers to one source-frame interval and has four corresponding mono WAVs. Use the clip plan and audio manifest to join clip IDs to source intervals, channel paths, and hashes. Use session annotation tables for printer/build and collection condition, and range tables for activity within a clip.

Typical annotation tables include `clip_plan.csv`, `audio_clip_manifest.csv`, `clip_annotations_range.csv`, `clip_timeline.csv`, `clip_gcode.csv`, and `clip_telemetry.csv`. Filenames and column names are part of their respective schemas; printer labels are values of `printer_id`.

The `all` group retains audio before and after selected printing activity. Excluding an interval from `clipped` does not remove it from the continuous recording. A video used for explanatory review is separate from the curated audio dataset.
