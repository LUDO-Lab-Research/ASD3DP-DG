# Verification

After extracting the three multipart 7-Zip groups, run `sha256sum -c SHA256SUMS` from the release root. This verifies the reconstructed release files. The audio files are independent session archives, so you can extract one session at a time.

| Stage | Check |
|---|---|
| Distribution | All numbered 7-Zip parts present; successful extraction |
| Release files | SHA-256 checks against the top-level manifest |
| Source audio | Four-channel format, 48 kHz PCM, source manifest hashes |
| Clip plan | Ten-second grid, source-frame boundaries, selection reasons |
| Mono audio | Four channel files per selected clip; 480,000 frames per file |
| Annotations | Clip/session joins, time origin, row grain, and schema membership |
| Public labels | Printer values A/B/C across paths and annotation values |

A checksum verifies file bytes, while annotation review establishes the meaning and admissibility of a label. Both are required for a usable research dataset. See [Time coordinates](timebase.md) before comparing session, WAV, and clip-relative intervals.
