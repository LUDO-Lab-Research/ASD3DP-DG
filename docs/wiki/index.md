# ASD3DP-DG Dataset Guide

ASD3DP-DG extends [ASD3DP](https://github.com/LUDO-Lab-Research/ASD3DP) with recordings from three independently assembled 3D printers, labeled A, B, and C. It supports anomalous sound detection under differences between printer builds. The dataset contains four microphone channels per recording session.

| Collection measure | Count |
|---|---:|
| Printer domains | 3 |
| Recorded sessions | 78 |
| Continuous audio | 40.05 hours |
| Selected 10-second intervals | 11,861 |
| Mono channel views of selected intervals | 47,444 |

These counts describe the selected collection before any benchmark subsampling. The complete public download is being prepared; see [Downloads](download.md) for availability. The underlying files and checksums will be linked only after the final archive has been verified.

## Read the guide

1. [Collection conditions and audio](collection.md)
2. [Folders and files](layout.md)
3. [Time coordinates](timebase.md)
4. [Clip selection](selection.md)
5. [Annotation layers](annotations.md)
6. [Schema and field names](schemas.md)
7. [Complete field dictionary](fields.md)
8. [Verification](verification.md)
9. [Limitations](limits.md)
10. [Three-factor joint-shift benchmark](joint-benchmark.md)

Printer A/B/C are build labels. Belt A/B identify two belts within each printer; they are a separate naming axis. CSV field names and schema keys are preserved.
