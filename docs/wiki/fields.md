# Reading the released tables

Use the files shipped with [ASD3DP-DG v1](https://doi.org/10.5281/zenodo.23068430) as the reference for table headers, field names, and allowed values.

| To look up | Start with |
|---|---|
| Printer build, speed program, or collection condition | Session annotations |
| Source interval and selection status | Clip plan |
| File name and microphone channel | Audio manifest |
| Operation, belt activity, or fault timing within a clip | Interval annotations |

To locate the four microphone files for a clip, start with the clip's temporal identifier in the audio manifest and use the channel to select each file. To relate activity to audio, check the interval's time origin and units before aligning it with the source recording.

See [Folders and files](layout.md), [Annotation layers](annotations.md), and [Time coordinates](timebase.md).
