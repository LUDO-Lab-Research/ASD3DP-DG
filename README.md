# ASD3DP-DG

ASD3DP-DG extends [ASD3DP](https://github.com/LUDO-Lab-Research/ASD3DP) to three printer-build domains, labeled A, B, and C. It provides four-channel 3D-printer audio and session and clip annotations for anomalous sound detection under domain shift. This is a DCASE Task 2-style research dataset, not an official DCASE-organized release.

The collection contains 78 sessions, 40.05 hours of continuous audio, and 11,861 selected 10-second intervals. Four microphone channels provide 47,444 mono clip views. The channels are rear, left, front, and right. Printer A/B/C are build labels; Belt A/B are component names.

The [public dataset guide](docs/wiki/index.md) describes collection, file groups, annotation basics, and download status. The complete A/B/C archive will be linked after integrity checks.

The [three-factor joint-shift protocol](benchmarks/joint_shifts_20260924/README.md)
freezes three combined printer, speed, and microphone assignments with their
exact file selections. Earlier printer-only rotations are retained separately.
