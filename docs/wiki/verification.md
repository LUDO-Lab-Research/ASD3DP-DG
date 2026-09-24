# Verification

Verify each downloaded file against the top-level `SHA256SUMS` in the [Google Drive dataset folder](https://drive.google.com/drive/folders/1dABXcAjs-b6dA5qjiMSdtwvO69cFOt2g) before extraction. The audio files are independent session archives, so you can extract one session at a time.

| Stage | Check |
|---|---|
| Archive | File size and SHA-256 for every part; successful extraction |
| Source audio | Four-channel format, 48 kHz PCM, source manifest hashes |
| Clip plan | Ten-second grid, source-frame boundaries, selection reasons |
| Mono audio | Four channel files per selected clip; 480,000 frames per file |
| Annotations | Clip/session joins, time origin, row grain, and schema membership |
| Public labels | Printer values A/B/C across paths and annotation values |

A checksum verifies file bytes, while annotation review establishes the meaning and admissibility of a label. Both are required for a usable research dataset. See [Time coordinates](timebase.md) before comparing session, WAV, and clip-relative intervals.
