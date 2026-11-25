# Folders and files

The public dataset is organized into three archive groups, following the distribution pattern of [ASD3DP](https://zenodo.org/records/21313911):

| Group | Contents |
|---|---|
| `all` | Continuous source recordings and session context |
| `annotations` | Session, clip, timing, and interval tables |
| `clipped` | Selected 10-second mono WAVs by channel |

The [Downloads](download.md) page links the Zenodo record and describes the session archives. After extracting the distribution groups, check each session archive against `SHA256SUMS` before opening it.

## File relationships

A recording session provides one four-channel source WAV. A selected temporal clip refers to one source-frame interval and has four corresponding mono WAVs. Use the clip plan and audio manifest to join clip IDs to source intervals, channel paths, and hashes. Use session annotation tables for printer/build and collection condition, and range tables for activity within a clip.

For exact column names and file membership, use the headers and manifests in the Zenodo release. See [Reading the released tables](fields.md) for how the tables fit together.

The `all` group retains audio before and after selected printing activity. Excluding an interval from `clipped` does not remove it from the continuous recording. A video used for explanatory review is separate from the curated audio dataset.
